from backend.powiats.models import Powiat

_SRSNAME = 'EPSG:4326'


def epodgik_url(
    powiat: Powiat, lat: float, lon: float, srsname: str = _SRSNAME
) -> str:
    if not (area_name := powiat.url_extras.get('area_name', None)):
        raise ValueError('Missing area_name for epodgik url builder!')

    bbox = ','.join(map(str, [lat, lon, lat, lon]))
    return (
        f'https://wms.epodgik.pl/cgi-bin/{area_name}/wfs'
        '?service=wfs'
        '&version=2.0.0'
        '&request=GetFeature'
        '&typeNames=ms:budynki'
        f'&SRSNAME={srsname}'
        f'&bbox={bbox},{srsname}'
    )
