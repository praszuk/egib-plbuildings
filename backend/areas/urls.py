from backend.areas.models import Area

_SRSNAME = 'EPSG:4326'


def epodgik_url(area: Area, lat: float, lon: float, srsname: str = _SRSNAME) -> str:
    if not (area_name := area.url_extras.get('area_name', None)):
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


def geoportal2_url(area: Area, lat: float, lon: float, srsname: str = _SRSNAME) -> str:
    if not (area_name := area.url_extras.get('area_name', None)):
        raise ValueError('Missing area_name for geoportal2 url builder!')

    offset = 0.00001
    # geoportal2 ewmapa services return 400 if lat1 == lat2 or lon1 == lon2
    bbox = ','.join(map(str, [lat, lon, lat + offset, lon + offset]))
    return (
        f'https://{area_name}.geoportal2.pl/map/geoportal/wfs.php'
        f'?service=WFS'
        f'&REQUEST=GetFeature'
        f'&TYPENAMES=ewns:budynki'
        f'&SRSNAME={_SRSNAME}'
        f'&bbox={bbox},{srsname}'
    )
