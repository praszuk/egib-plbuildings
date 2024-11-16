import argparse
import datetime
import json
import logging

from dataclasses import asdict, dataclass
from os import getenv
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import httpx

from backend.core.config import settings
from backend.areas.data.expected_building import all_areas_data, AreaExpectedBuildingData


ENDPOINT = urljoin(getenv('server_uri', 'http://0.0.0.0:8000'), 'api/v1/buildings/')


@dataclass(frozen=True)
class HealthCheckAreaReport:
    test_area_data: AreaExpectedBuildingData
    status_code: int
    has_building_data: bool = False
    has_expected_building_data: bool = False
    result_tags: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class HealthCheckReport:
    start_dt: str
    end_dt: str
    counties: Dict[str, HealthCheckAreaReport]
    communes: Dict[str, HealthCheckAreaReport]


def report_area(area, use_db_data) -> HealthCheckAreaReport:
    building_data = False
    expected_building_data = False
    building_tags = None

    with httpx.Client() as client:
        response = client.get(
            ENDPOINT, params={'lat': area.lat, 'lon': area.lon, 'live': not use_db_data}, timeout=30
        )
        status_code = response.status_code
        response_data = response.json()

    if status_code == 200 and response_data['features']:
        building_data = True
        building_feature = response_data['features'][0]
        building_tags = building_feature['properties']

        if area.expected_tags == building_tags:
            expected_building_data = True
        else:
            expected_building_data = False

    return HealthCheckAreaReport(
        test_area_data=area,
        status_code=status_code,
        has_building_data=building_data,
        has_expected_building_data=expected_building_data,
        result_tags=building_tags,
    )


def report_areas(teryt_ids: list[str] | None = None, use_db_data=False) -> HealthCheckReport:
    """
    It sends requests to all defined servers to check:
     - connection
     - response status
     - response data withh comparing expected building tags

    It works similar to e2e tests.
    """
    start_report_dt = datetime.datetime.now(datetime.UTC).isoformat()
    areas_reports_counties: Dict[str, HealthCheckAreaReport] = {}
    areas_reports_communes: Dict[str, HealthCheckAreaReport] = {}
    areas = all_areas_data
    if teryt_ids is not None:
        areas = [area for area in all_areas_data if area.teryt in teryt_ids]

    for area in areas:
        area_report = report_area(area, use_db_data)
        logging.debug(area_report)
        if len(area.teryt) == 4:
            areas_reports_counties[area.teryt] = area_report
        else:
            areas_reports_communes[area.teryt] = area_report

    return HealthCheckReport(
        start_dt=start_report_dt,
        end_dt=datetime.datetime.now(datetime.UTC).isoformat(),
        counties=areas_reports_counties,
        communes=areas_reports_communes,
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('--offline', action='store_true')
    parser.add_argument(
        '-t',
        '--teryt_ids',
        type=lambda s: s.replace(' ', '').split(','),
        help='Comma-separated list of area teryt IDs',
    )
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    logging.getLogger('httpx').setLevel(level=logging.WARNING)
    logging.getLogger('httpcore').setLevel(level=logging.WARNING)

    report = report_areas(args.teryt_ids, use_db_data=args.offline)

    with open(settings.AREAS_HEALTHCHECK_CACHE_FILENAME, 'w') as f:
        json.dump(asdict(report), f)

    all_reports = list(report.counties.values()) + list(report.communes.values())
    success_reports_num = sum(1 for report in all_reports if report.has_expected_building_data)
    logging.info(f'Success: {success_reports_num}/{len(all_reports)}')
    if len(all_reports) != success_reports_num:
        failed_teryt = ', '.join(
            [
                report.test_area_data.teryt
                for report in all_reports
                if not report.has_expected_building_data
            ]
        )

        logging.error(f'Failed teryt: {failed_teryt}')
        exit(1)

    exit(0)
