from typing import Dict

from backend.powiats.models import Powiat
from backend.powiats.parsers.epodgik import epodgik_parser
from backend.powiats.urls import epodgik_url

all_powiats: Dict[str, Powiat] = {
    '1418': Powiat(
        name='piaseczynski',
        data_parser=epodgik_parser,
        url_builder=epodgik_url,
        url_extras={'area_name': 'piaseczno'},
    ),
    '1421': Powiat(
        name='pruszkowski',
        data_parser=epodgik_parser,
        url_builder=epodgik_url,
        url_extras={'area_name': 'pruszkow'},
    ),
}
