from typing import Dict

from backend.counties.models import County
from backend.counties.parsers.epodgik import epodgik_parser
from backend.counties.urls import epodgik_url

all_counties: Dict[str, County] = {
    # 06 – "lubelskie"
    '0619': County(
        name='włodawski',
        data_parser=epodgik_parser,
        url_builder=epodgik_url,
        url_extras={'area_name': 'wlodawa'},
    ),
    '0662': County(
        name='miasto Chełm',
        data_parser=epodgik_parser,
        url_builder=epodgik_url,
        url_extras={'area_name': 'mchelm'},
    ),
    # 14 – "mazowieckie"
    '1412': County(
        name='miński',
        data_parser=epodgik_parser,
        url_builder=epodgik_url,
        url_extras={'area_name': 'minsk'},
    ),
    '1418': County(
        name='piaseczyński',
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
    '1433': County(
        name='węgrowski',
        data_parser=epodgik_parser,
        url_builder=epodgik_url,
        url_extras={'area_name': 'wegrow'},
    ),
    '1434': County(
        name='wołomiński',
        data_parser=epodgik_parser,
        url_builder=epodgik_url,
        url_extras={'area_name': 'wolomin'},
    ),
    '1438': County(
        name='żyrardowski',
        data_parser=epodgik_parser,
        url_builder=epodgik_url,
        url_extras={'area_name': 'zyrardow'},
    ),
    # 22 – "pomorskie"
    '2215': County(
        name='wejherowski',
        data_parser=epodgik_parser,
        url_builder=epodgik_url,
        url_extras={'area_name': 'wejherowo'},
    ),
    # 28 – "warmińsko-mazurskie"
    '2806': County(
        name='giżycki',
        data_parser=epodgik_parser,
        url_builder=epodgik_url,
        url_extras={'area_name': 'gizycko'},
    ),
    '2810': County(
        name='mrągowski',
        data_parser=epodgik_parser,
        url_builder=epodgik_url,
        url_extras={'area_name': 'mragowo'},
    ),
    '2819': County(
        name='węgorzewski',
        data_parser=epodgik_parser,
        url_builder=epodgik_url,
        url_extras={'area_name': 'wegorzewo'},
    ),
    # 30 – "wielkopolskie"
    '3014': County(
        name='międzychodzki',
        data_parser=epodgik_parser,
        url_builder=epodgik_url,
        url_extras={'area_name': 'miedzychod'},
    ),
}
