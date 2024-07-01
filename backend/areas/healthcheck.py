import json
from datetime import datetime
from dataclasses import asdict
from os import getenv
from typing import Dict
from urllib.parse import urljoin

import httpx

from backend.core.config import settings
from backend.core.logger import logger
from backend.areas.models import HealthCheckAreaReport, HealthCheckReport
from backend.areas.data.healtcheck_all_areas_buildings import all_areas_data


def report_all_areas(server_uri: str) -> HealthCheckReport:
    """
    It sends requests to all defined servers to check:
     - connection
     - response status
     - response data withh comparing expected building tags

    It works similar to e2e tests.

    :param server_uri: main server root endpoint (without / at the end)
    """

    endpoint = urljoin(server_uri, 'api/v1/buildings/')
    start_report_dt = datetime.utcnow().isoformat()
    areas_reports_counties: Dict[str, HealthCheckAreaReport] = {}
    areas_reports_communes: Dict[str, HealthCheckAreaReport] = {}

    for area in all_areas_data:
        status_code = -1
        building_data = False
        expected_building_data = False
        building_tags = None

        response_data = None
        try:
            with httpx.Client() as client:
                response = client.get(endpoint, params={'lat': area.lat, 'lon': area.lon})
                status_code = response.status_code
                response_data = response.json()
        except (IOError, httpx.ReadTimeout):
            logger.warning('Error at connecting for reporting areas')
            status_code = 500
        except (TypeError, json.JSONDecodeError):
            logger.warning('Incorrect data returned from server')
            logger.debug(response.content)

        if response_data and response_data['features']:
            building_data = True
            building_feature = response_data['features'][0]
            building_tags = building_feature['properties']

            if area.expected_tags == building_tags:
                expected_building_data = True
            else:
                expected_building_data = False
                logger.debug(f'Expected: {area.expected_tags}, got: {building_tags}')

        area_report = HealthCheckAreaReport(
            test_area_data=area,
            status_code=status_code,
            is_building_data=building_data,
            is_expected_building_data=expected_building_data,
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
    logger = logging  # type:ignore

    report = report_all_areas(getenv('server_uri', 'http://0.0.0.0:8000'))
    with open(settings.AREAS_HEALTHCHECK_CACHE_FILENAME, 'w') as f:
        json.dump(asdict(report), f)

    logger.info(report)
    all_reports = list(report.counties.values()) + list(report.communes.values())
    success = all(p_report.is_expected_building_data for p_report in all_reports)
    exit(0 if success else 1)
