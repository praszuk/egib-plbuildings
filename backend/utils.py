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

                gml_poly = etree.tostring(polygons[0]).decode('utf-8')
                geometry: ogr.Geometry = ogr.CreateGeometryFromGML(gml_poly)
                geojson_str_geometry: str = geometry.ExportToJson()
                feature['geometry'] = json.loads(geojson_str_geometry)
            else:
                feature['properties'][clean_tag] = child.text

        result['features'].append(feature)

    return result
