from lxml import etree
from osgeo import ogr, osr  # noqa

import json

from typing import Any, Dict


def get_powiat_teryt_at(lat: float, lon: float) -> str:
    """
    :return: 4 characters number of powiat
    :raises ValueError: if location is incorrect
    """
    return '1421'  # TODO hardcoded 1 powiat for testing


def gml_to_geojson(gml_content: str) -> Dict[Any, Any]:
    result = {
        'type': 'FeatureCollection',
        'features': []
    }
    root = etree.fromstring(bytes(gml_content, encoding='utf-8'))
    for wfs_member in root.findall('.//wfs:member', namespaces=root.nsmap):
        bud_member = wfs_member.getchildren()[0]  # ms:budynki
        feature = {
            'type': 'Feature',
            'geometry': {},
            'properties': {}
        }
        for child in bud_member.getchildren():
            # Geometry and GUGIK attributes start with "ms"
            if not child.tag.startswith('{' + root.nsmap.get('ms')):
                continue

            clean_tag = child.tag.replace(root.nsmap.get('ms'), '')[2:]
            if clean_tag == 'msGeometry':
                polygons = bud_member.findall(
                    './/gml:Polygon',
                    namespaces=root.nsmap
                )
                if len(polygons) == 0:  # not sure
                    continue

                gml_geom = etree.tostring(polygons[0]).decode('utf-8')
                geometry: ogr.Geometry = ogr.CreateGeometryFromGML(gml_geom)

                # fix incorrect lat lon order
                point = geometry.GetGeometryRef(0).GetPoint(0)
                if point[0] > point[1]:
                    source = osr.SpatialReference()
                    source.ImportFromEPSG(4326)
                    target = osr.SpatialReference()
                    target.SetWellKnownGeogCS('WGS84')
                    transform = osr.CoordinateTransformation(source, target)
                    geometry.Transform(transform)

                geojson_str_geometry: str = geometry.ExportToJson()

                feature['geometry'] = json.loads(geojson_str_geometry)
            else:
                feature['properties'][clean_tag] = child.text

        result['features'].append(feature)

    return result
