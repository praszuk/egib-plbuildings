import json
from datetime import datetime
from os import getenv, path
from typing import Dict
from urllib.parse import urljoin

import httpx

from backend.core.config import settings
from backend.core.logger import logger
from backend.powiats.models import HealthCheckPowiatReport, HealthCheckReport

ALL_POWIATS_DATA_FILENAME = path.join(
    settings.DATA_DIR, 'healtcheck_all_powiats_buildings.json'
)


def report_all_powiats(
    server_uri: str,
    filename: str = ALL_POWIATS_DATA_FILENAME,
) -> HealthCheckReport:
    """
    It sends requests to all defined servers to check:
     - connection
     - response status
     - response data withh comparing expected building tags

    It works similar to e2e tests.

    :param server_uri: main server root endpoint (without / at the end)
    :param filename: path to filename with teryt, lat, lon and expected tags
    """

    with open(filename, 'r') as f:
        powiats_coordinates_buildings = json.load(f)

    endpoint = urljoin(server_uri, 'api/v1/buildings/')
    start_report_dt = datetime.utcnow().isoformat()
    powiats_reports: Dict[str, HealthCheckPowiatReport] = {}

    for powiat in powiats_coordinates_buildings:
        teryt = powiat['teryt']

        status_code = -1
        building_data = False
        expected_building_data = False

        response_data = None
        try:
            with httpx.Client() as client:
                response = client.get(
                    endpoint,
                    params={'lat': powiat['lat'], 'lon': powiat['lon']},
                )
                status_code = response.status_code
                response_data = response.json()
        except IOError:
            logger.exception('Error at connecting for reporting powiats')
        except (TypeError, json.JSONDecodeError):
            logger.exception('Incorrect data returned from server')
            logger.debug(response.content)

        if response_data and response_data['features']:
            building_data = True
            building_feature = response_data['features'][0]
            building_tags = building_feature['properties']

            if (expected_tags := powiat.get('tags', {})) == building_tags:
                expected_building_data = True
            else:
                expected_building_data = False
                logger.debug(
                    f'Expected: {expected_tags}, got: {building_tags}'
                )

        powiats_reports[teryt] = HealthCheckPowiatReport(
            status_code=status_code,
            is_building_data=building_data,
            is_expected_building_data=expected_building_data,
        )

    end_report_dt = datetime.utcnow().isoformat()
    return HealthCheckReport(
        start_dt=start_report_dt, end_dt=end_report_dt, powiats=powiats_reports
    )


if __name__ == '__main__':
    import logging

    logging.basicConfig(level=logging.INFO)
    logger = logging  # type:ignore

    report = report_all_powiats(getenv('server_uri', 'http://0.0.0.0:8000'))

    logger.info(report)
    success = all(
        p_report.is_expected_building_data
        for p_report in report.powiats.values()
    )
    exit(0 if success else 1)
