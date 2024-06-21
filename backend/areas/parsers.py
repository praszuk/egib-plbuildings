from __future__ import annotations

import json
from typing import Any, List, Dict

from lxml import etree
from osgeo import ogr, osr  # noqa

from backend.exceptions import InvalidKeyParserError
from backend.areas.models import AreaParser

from typing import Final

DEFAULT_BUILDING: Final = 'yes'

# EGiB KST classification "EGB_RodzajWgKSTType"
# XSD: http://www.gugik.gov.pl/bip/prawo/schematy-aplikacyjne
BUILDING_KST_CODE_TYPE: Final = {
    'm': 'residential',  # "mieszkalny"
    'g': DEFAULT_BUILDING,  # "produkcyjnoUslugowyIGospodarczy"
    't': DEFAULT_BUILDING,  # "transportuILacznosci"
    'k': DEFAULT_BUILDING,  # "oswiatyNaukiIKulturyOrazSportu"
    'z': DEFAULT_BUILDING,  # "szpitalaIInneBudynkiOpiekiZdrowotnej"
    'b': 'office',  # "biurowy"
    'h': 'retail',  # "handlowoUslugowy"
    'p': 'industrial',  # "przemyslowy"
    's': DEFAULT_BUILDING,  # "zbiornikSilosIBudynekMagazynowy"
    'i': DEFAULT_BUILDING,  # "budynekNiemieszkalny"
}


class EpodgikAreaParser(AreaParser):
    def build_url(self, lat: float, lon: float) -> str:
        bbox = ','.join(map(str, [lat, lon, lat, lon]))
        return (
            f'https://wms.epodgik.pl/cgi-bin/{self.url_code}/wfs'
            '?service=wfs'
            '&version=2.0.0'
            '&request=GetFeature'
            '&typeNames=ms:budynki'
            f'&SRSNAME={self.SRS_NAME}'
            f'&bbox={bbox},{self.SRS_NAME}'
        )

    def parse_gml_to_geojson(self, gml_content: str) -> dict[str, Any]:
        features: List[Dict[str, Any]] = []

        root = etree.fromstring(bytes(gml_content, encoding='utf-8'))
        wfs_members = root.findall('.//wfs:member', namespaces=root.nsmap)  # type: ignore[arg-type]

        for wfs_member in wfs_members:
            # get ms:budynki member
            bud_member = wfs_member.getchildren()[0]  # type: ignore[attr-defined]
            feature: Dict[str, Any] = {
                'type': 'Feature',
                'geometry': {},
                'properties': {},
            }
            for child in bud_member.getchildren():
                # Geometry and GUGIK attributes start with "ms"
                if not child.tag.startswith('{' + str(root.nsmap.get('ms'))):
                    continue

                clean_tag = child.tag.replace(root.nsmap.get('ms'), '')[2:]
                if clean_tag == 'msGeometry':
                    polygons = bud_member.findall('.//gml:Polygon', namespaces=root.nsmap)
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

            features.append(feature)

        return {'type': 'FeatureCollection', 'features': features}

    def parse_feature_properties_to_osm_tags(self, properties: Dict[str, Any]) -> Dict[str, Any]:
        tags: Dict[str, Any] = {}
        try:
            tags['building'] = BUILDING_KST_CODE_TYPE.get(properties['FUNKCJA'], DEFAULT_BUILDING)
            if 'KONDYGNACJE_NADZIEMNE' in properties:
                tags['building:levels'] = properties.get('KONDYGNACJE_NADZIEMNE')

            if 'KONDYGNACJE_PODZIEMNE' in properties:
                tags['building:levels:underground'] = properties.get('KONDYGNACJE_PODZIEMNE')

            # RODZAJ and ID_BUDYNKU skipped

        except KeyError as e:
            raise InvalidKeyParserError(e)

        return tags
