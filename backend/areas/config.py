from typing import Dict

from backend.areas.models import Area
from backend.areas.parsers.epodgik import epodgik_parser
from backend.areas.urls import epodgik_url

all_counties: Dict[str, Area] = {
    # 06 – "lubelskie"
    '0619': Area(
        name='włodawski',
        data_parser=epodgik_parser,
        url_builder=epodgik_url,
        url_extras={'area_name': 'wlodawa'},
    ),
    '0662': Area(
        name='miasto Chełm',
        data_parser=epodgik_parser,
        url_builder=epodgik_url,
        url_extras={'area_name': 'mchelm'},
    ),
    # 14 – "mazowieckie"
    '1412': Area(
        name='miński',
        data_parser=epodgik_parser,
        url_builder=epodgik_url,
        url_extras={'area_name': 'minsk'},
    ),
    '1418': Area(
        name='piaseczyński',
        data_parser=epodgik_parser,
        url_builder=epodgik_url,
        url_extras={'area_name': 'piaseczno'},
    ),
    '1421': Area(
        name='pruszkowski',
        data_parser=epodgik_parser,
        url_builder=epodgik_url,
        url_extras={'area_name': 'pruszkow'},
    ),
    '1433': Area(
        name='węgrowski',
        data_parser=epodgik_parser,
        url_builder=epodgik_url,
        url_extras={'area_name': 'wegrow'},
    ),
    '1434': Area(
        name='wołomiński',
        data_parser=epodgik_parser,
        url_builder=epodgik_url,
        url_extras={'area_name': 'wolomin'},
    ),
    '1438': Area(
        name='żyrardowski',
        data_parser=epodgik_parser,
        url_builder=epodgik_url,
        url_extras={'area_name': 'zyrardow'},
    ),
    # 22 – "pomorskie"
    '2215': Area(
        name='wejherowski',
        data_parser=epodgik_parser,
        url_builder=epodgik_url,
        url_extras={'area_name': 'wejherowo'},
    ),
    # 28 – "warmińsko-mazurskie"
    '2806': Area(
        name='giżycki',
        data_parser=epodgik_parser,
        url_builder=epodgik_url,
        url_extras={'area_name': 'gizycko'},
    ),
    '2810': Area(
        name='mrągowski',
        data_parser=epodgik_parser,
        url_builder=epodgik_url,
        url_extras={'area_name': 'mragowo'},
    ),
    '2819': Area(
        name='węgorzewski',
        data_parser=epodgik_parser,
        url_builder=epodgik_url,
        url_extras={'area_name': 'wegorzewo'},
    ),
    # 30 – "wielkopolskie"
    '3014': Area(
        name='międzychodzki',
        data_parser=epodgik_parser,
        url_builder=epodgik_url,
        url_extras={'area_name': 'miedzychod'},
    ),
}
all_areas = all_counties
