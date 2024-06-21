from typing import Dict, TypeVar

from backend.areas.models import AreaParser
from backend.areas.parsers import EpodgikAreaParser

BaseAreaParser = TypeVar('BaseAreaParser', bound=AreaParser)
all_counties: Dict[str, BaseAreaParser] = {
    # 06 – "lubelskie"
    '0619': EpodgikAreaParser(name='włodawski', url_code='wlodawa'),
    '0662': EpodgikAreaParser(name='miasto Chełm', url_code='mchelm'),
    # 14 – "mazowieckie"
    '1412': EpodgikAreaParser(name='miński', url_code='minsk'),
    '1418': EpodgikAreaParser(name='piaseczyński', url_code='piaseczno'),
    '1421': EpodgikAreaParser(name='pruszkowski', url_code='pruszkow'),
    '1433': EpodgikAreaParser(name='węgrowski', url_code='wegrow'),
    '1434': EpodgikAreaParser(name='wołomiński', url_code='wolomin'),
    '1438': EpodgikAreaParser(name='żyrardowski', url_code='zyrardow'),
    # 22 – "pomorskie"
    '2215': EpodgikAreaParser(name='wejherowski', url_code='wejherowo'),
    # 28 – "warmińsko-mazurskie"
    '2806': EpodgikAreaParser(name='giżycki', url_code='gizycko'),
    '2810': EpodgikAreaParser(name='mrągowski', url_code='mragowo'),
    '2819': EpodgikAreaParser(name='węgorzewski', url_code='wegorzewo'),
    # 30 – "wielkopolskie"
    '3014': EpodgikAreaParser(name='międzychodzki', url_code='miedzychod'),
}
all_areas = all_counties
