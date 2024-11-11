# TODO Healthcheck feature is to rewrite or remove
import json
from datetime import datetime
from dataclasses import asdict, dataclass
from os import getenv
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import httpx

from backend.core.config import settings


@dataclass
class HealthCheckTestAreaData:
    teryt: str
    name: str
    lat: float
    lon: float
    expected_tags: Dict[str, Any]


@dataclass(frozen=True)
class HealthCheckAreaReport:
    test_area_data: HealthCheckTestAreaData
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


def report_all_areas(server_uri: str) -> HealthCheckReport:
    """
    It sends requests to all defined servers to check:
     - connection
     - response status
     - response data withh comparing expected building tags

    It works similar to e2e tests.

    :param server_uri: main server root endpoint (without / at the end)
    """
    from backend.areas.data.healthcheck_all_areas_buildings import all_areas_data

    endpoint = urljoin(server_uri, 'api/v1/buildings/')
    start_report_dt = datetime.utcnow().isoformat()
    areas_reports_counties: Dict[str, HealthCheckAreaReport] = {}
    areas_reports_communes: Dict[str, HealthCheckAreaReport] = {}

    for area in all_areas_data:
        building_data = False
        expected_building_data = False
        building_tags = None

        with httpx.Client() as client:
            response = client.get(
                endpoint, params={'lat': area.lat, 'lon': area.lon, 'live': True}, timeout=30
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
                logging.debug(f'Expected: {area.expected_tags}, got: {building_tags}')

        area_report = HealthCheckAreaReport(
            test_area_data=area,
            status_code=status_code,
            has_building_data=building_data,
            has_expected_building_data=expected_building_data,
            result_tags=building_tags,
        )

        if len(area.teryt) == 4:
            areas_reports_counties[area.teryt] = area_report
        else:
            areas_reports_communes[area.teryt] = area_report

    end_report_dt = datetime.utcnow().isoformat()
    return HealthCheckReport(
        start_dt=start_report_dt,
        end_dt=end_report_dt,
        counties=areas_reports_counties,
        communes=areas_reports_communes,
    )


if __name__ == '__main__':
    import logging

    logging.basicConfig(level=logging.INFO)

    report = report_all_areas(getenv('server_uri', 'http://0.0.0.0:8000'))
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
