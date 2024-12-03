import asyncio
import datetime

from dataclasses import dataclass

from httpx import AsyncClient, HTTPError, Timeout
from sqlalchemy import insert, bindparam

from backend.areas.data.expected_building import all_areas_data
from backend.areas.config import all_areas
from backend.areas.finder import area_finder
from backend.areas.parsers import BaseAreaParser
from backend.core.logger import default_logger
from backend.models.building import Building
from backend.models.area_import import AreaImport, ResultStatus
from backend.database.session import SessionLocal
from backend.exceptions import ParserError
from backend.services.buildings import query_building_from_db_at


@dataclass
class ImportResult:
    teryt: str
    status: ResultStatus
    building_count: int = 0
    has_building_type: bool = False
    has_building_levels: bool = False
    has_building_levels_undg: bool = False
    hc_lat: float | None = None
    hc_lon: float | None = None
    hc_expected_tags: dict | None = None
    hc_result_tags: dict | None = None


async def area_import_attempt(area_parser: BaseAreaParser, teryt: str) -> ImportResult | None:
    url = area_parser.build_buildings_url()

    default_logger.debug(f'[IMPORT] [{teryt}] Downloading data from {url}')
    try:
        async with AsyncClient(verify=False, timeout=Timeout(300, connect=30)) as client:
            response = await client.get(url)
            gml_raw = response.text
            if response.status_code != 200:
                raise HTTPError(f'Invalid status code: {response.status_code}')

    except HTTPError as err_msg:
        default_logger.debug(f'[IMPORT] [{teryt}] Error at downloading data: {err_msg}')
        return ImportResult(teryt=teryt, status=ResultStatus.DOWNLOADING_ERROR)

    default_logger.debug(f'[IMPORT] [{teryt}] Parsing data')
    try:
        data = area_parser.parse_gml_to_geometries_and_properties(gml_raw)
    except ParserError as err_msg:
        default_logger.debug(f'[IMPORT] [{teryt}] Parsing error: {err_msg}')
        return ImportResult(teryt=teryt, status=ResultStatus.PARSING_ERROR)

    if not data:
        default_logger.debug(f'[IMPORT] [{teryt}] No data found after parsing')
        return ImportResult(teryt=teryt, status=ResultStatus.EMPTY_DATA_ERROR)

    # Check for unexpected projection change from server
    if not any(area_finder.geometry_in_area(building_geom, teryt) for building_geom, _ in data):
        default_logger.debug(f'[IMPORT] [{teryt}] Parsing error: Building data not in area.')
        return ImportResult(teryt=teryt, status=ResultStatus.PARSING_ERROR)

    buildings_data = []
    for geometry, raw_properties in data:
        tags = area_parser.clean_tags(area_parser.parse_properties_to_osm_tags(raw_properties))
        buildings_data.append({'wkt': geometry.ExportToWkt(), 'tags': tags, 'teryt': teryt})
    default_logger.debug(f'[IMPORT] [{teryt}] Parsed {len(buildings_data)} buildings.')

    with SessionLocal() as session:
        session.query(Building).filter(Building.teryt == teryt).delete()
        session.execute(insert(Building).values(geometry=bindparam('wkt')), buildings_data)
        session.commit()

        # Healthcheck section
        expected = all_areas_data[teryt]
        hc_lat = expected.lat
        hc_lon = expected.lon
        hc_expected_tags = expected.expected_tags

        geojson = await query_building_from_db_at(session, expected.lat, expected.lon)
        if geojson['features']:
            hc_result_tags = geojson['features'][0]['properties']
        else:
            hc_result_tags = None

    return ImportResult(
        teryt=teryt,
        status=ResultStatus.SUCCESS,
        building_count=len(buildings_data),
        has_building_type=any(d['tags'].get('building', 'yes') != 'yes' for d in buildings_data),
        has_building_levels=any(
            d['tags'].get('building:levels') is not None for d in buildings_data
        ),
        has_building_levels_undg=any(
            d['tags'].get('building:levels:underground') is not None for d in buildings_data
        ),
        hc_lat=hc_lat,
        hc_lon=hc_lon,
        hc_expected_tags=hc_expected_tags,
        hc_result_tags=hc_result_tags,
    )


async def area_import_in_parallel(
    teryt_ids: list[str],
    max_workers: int = 3,
    max_attempts_per_area: int = 3,
    delay_between_attempts: float = 10,
):
    default_logger.info(
        f'[IMPORT] Area import data started. Updating data from {len(teryt_ids)} areas.'
    )

    semaphore = asyncio.Semaphore(max_workers)

    async def import_with_attempts_task(teryt: str) -> ImportResult:
        attempts = 0
        while attempts < max_attempts_per_area:
            async with semaphore:
                if attempts == 0:
                    start_at = datetime.datetime.now(datetime.UTC)

                import_result = await area_import_attempt(all_areas[teryt], teryt)
                if import_result.status == ResultStatus.SUCCESS:
                    break

            attempts += 1
            if attempts < max_attempts_per_area:
                default_logger.debug(
                    f'[IMPORT] [{teryt}] Import failed.'
                    f' Waiting {delay_between_attempts} seconds before next attempt'
                )
                await asyncio.sleep(delay_between_attempts)
            else:
                break

        area_import = AreaImport(
            teryt=teryt,
            result_status=import_result.status,
            start_at=start_at,
            building_count=import_result.building_count,
            has_building_type=import_result.has_building_type,
            has_building_levels=import_result.has_building_levels,
            has_building_levels_undg=import_result.has_building_levels_undg,
            hc_lat=import_result.hc_lat,
            hc_lon=import_result.hc_lon,
            hc_expected_tags=import_result.hc_expected_tags,
            hc_result_tags=import_result.hc_result_tags,
        )
        with SessionLocal() as session:
            session.add(area_import)
            session.commit()

        return import_result

    area_results = await asyncio.gather(*[import_with_attempts_task(teryt) for teryt in teryt_ids])
    success_areas = 0
    failed_teryt_areas = []
    total_building_count = 0

    for area_import_result in area_results:
        if area_import_result.status == ResultStatus.SUCCESS:
            success_areas += 1
            total_building_count += area_import_result.building_count
        else:
            failed_teryt_areas.append(area_import_result.teryt)

    failed_areas_msg = ''
    if failed_teryt_areas:
        failed_areas_msg = f' Failed areas: {",".join(failed_teryt_areas)}'

    default_logger.info(
        '[IMPORT] Area import data finished. Successfuly imported data from '
        f'{success_areas}/{len(area_results)} ({success_areas * 100 / len(area_results):.2f}%)'
        f' areas. In total: {total_building_count} buildings.{failed_areas_msg}'
    )


if __name__ == '__main__':
    import argparse
    import yaml

    from logging import config, DEBUG

    area_finder.load_data()

    with open('backend/core/log_config.yaml') as file:
        loaded_config = yaml.safe_load(file)
        config.dictConfig(loaded_config)

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument(
        '-t',
        '--teryt_ids',
        type=lambda s: s.replace(' ', '').split(','),
        help='Comma-separated list of area teryt IDs',
    )
    args = parser.parse_args()

    if args.debug:
        default_logger.setLevel(DEBUG)

    if not (area_teryt_ids := args.teryt_ids):
        area_teryt_ids = all_areas.keys()

    asyncio.run(area_import_in_parallel(area_teryt_ids))
