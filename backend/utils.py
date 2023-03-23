from lxml import etree
from osgeo import ogr  # noqa

import json

from typing import Any, Dict


def gml_to_geojson(gml_content: str) -> Dict[Any, Any]:
    result = {
        'type': 'FeatureCollection',
        'features': []
    }
    root = etree.fromstring(bytes(gml_content, encoding='utf-8'))
    for wfs_member in root.findall('.//wfs:member', namespaces=root.nsmap):
        polygons = wfs_member.findall('.//gml:Polygon', namespaces=root.nsmap)

        if len(polygons) == 0:  # not sure
            continue

        gml_polygon = etree.tostring(polygons[0]).decode('utf-8')
        geometry: ogr.Geometry = ogr.CreateGeometryFromGML(gml_polygon)
        geojson_str_geometry: str = geometry.ExportToJson()
        feature = {
            'type': 'Feature',
            'geometry': json.loads(geojson_str_geometry)
        }
        result['features'].append(feature)

    return result
