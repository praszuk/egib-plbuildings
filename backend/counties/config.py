from typing import Dict

from backend.counties.models import County
from backend.counties.parsers.epodgik import epodgik_parser
from backend.counties.urls import epodgik_url

all_counties: Dict[str, County] = {
    '1418': County(
        name='piaseczynski',
        data_parser=epodgik_parser,
        url_builder=epodgik_url,
        url_extras={'area_name': 'piaseczno'},
    ),
    '1421': County(
        name='pruszkowski',
        data_parser=epodgik_parser,
        url_builder=epodgik_url,
        url_extras={'area_name': 'pruszkow'},
    ),
    '1438': County(
        name='żyrardowski',
        data_parser=epodgik_parser,
        url_builder=epodgik_url,
        url_extras={'area_name': 'zyrardow'},
    ),
}
