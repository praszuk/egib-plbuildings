from __future__ import annotations

import json
from typing import Any, List, Dict

from lxml import etree
from osgeo import ogr, osr  # noqa

from backend.exceptions import InvalidKeyParserError
from backend.areas.models import Area
from abc import abstractmethod

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


class BaseAreaParser(Area):
    SRS_NAME: str = 'EPSG:4326'
    FULL_SRS_NAME: str = 'urn:ogc:def:crs:EPSG:4326'

    @abstractmethod
    def build_url(self, lat: float, lon: float) -> str:
        pass

    @abstractmethod
    def parse_gml_to_geojson(self, gml_content: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def parse_feature_properties_to_osm_tags(self, properties: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @staticmethod
    def _gml_to_geojson(gml_content: str, prefix: str, geometry_tag: str) -> dict[str, Any]:
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
                if not child.tag.startswith('{' + str(root.nsmap.get(prefix))):
                    continue

                clean_tag = child.tag.replace(root.nsmap.get(prefix), '')[2:]
                if clean_tag == geometry_tag:
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

    def replace_properties_with_osm_tags(self, geojson: Dict[str, Any]) -> None:
        for index, feature in enumerate(geojson['features']):
            properties = feature['properties']
            tags = self.parse_feature_properties_to_osm_tags(properties)
            geojson['features'][index]['properties'] = self.clean_empty_tags(tags)

    @staticmethod
    def clean_empty_tags(osm_tags: Dict[str, Any]) -> Dict[str, Any]:
        """
        Removes tags without values
        """
        return {k: v for k, v in osm_tags.items() if v is not None}


class EpodgikAreaParser(BaseAreaParser):
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
        return self._gml_to_geojson(gml_content, prefix='ms', geometry_tag='msGeometry')

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


class Geoportal2AreaParser(BaseAreaParser):
    def build_url(self, lat: float, lon: float) -> str:
        offset = 0.00001
        # geoportal2 ewmapa services return 400 if lat1 == lat2 or lon1 == lon2
        bbox = ','.join(map(str, [lat, lon, lat + offset, lon + offset]))
        return (
            f'https://{self.url_code}.geoportal2.pl/map/geoportal/wfs.php'
            f'?service=WFS'
            f'&REQUEST=GetFeature'
            f'&TYPENAMES=ewns:budynki'
            f'&SRSNAME={self.SRS_NAME}'
            f'&bbox={bbox},{self.SRS_NAME}'
        )

    def parse_gml_to_geojson(self, gml_content: str) -> dict[str, Any]:
        return self._gml_to_geojson(gml_content, prefix='ewns', geometry_tag='geometria')

    def parse_feature_properties_to_osm_tags(self, properties: Dict[str, Any]) -> Dict[str, Any]:
        tags: Dict[str, Any] = {}
        try:
            tags['building'] = BUILDING_KST_CODE_TYPE.get(
                properties.get('RODZAJ'), DEFAULT_BUILDING
            )
            # ID_BUDYNKU skipped
            # Levels and underground levels are visible in WMS but not in WFS yet

        except KeyError as e:
            raise InvalidKeyParserError(e)

        return tags


class WarszawaAreaParser(BaseAreaParser):
    def build_url(self, lat: float, lon: float) -> str:
        bbox = ','.join(map(str, [lat, lon, lat, lon]))
        return (
            f'https://wms2.um.warszawa.pl/geoserver/wfs/wfs'
            '?service=wfs'
            '&version=2.0.0'
            '&request=GetFeature'
            '&typeNames=wfs:budynki'
            f'&SRSNAME={self.SRS_NAME}'
            f'&bbox={bbox},{self.FULL_SRS_NAME}'
        )

    def parse_gml_to_geojson(self, gml_content: str) -> dict[str, Any]:
        return self._gml_to_geojson(gml_content, prefix='Q1', geometry_tag='GEOMETRY')

    def parse_feature_properties_to_osm_tags(self, properties: Dict[str, Any]) -> Dict[str, Any]:
        tags: Dict[str, Any] = {}
        try:
            tags['building'] = BUILDING_KST_CODE_TYPE.get(
                properties.get('RODZAJ'), DEFAULT_BUILDING
            )
            if 'KONDYGNACJE_NADZIEMNE' in properties:
                tags['building:levels'] = properties.get('KONDYGNACJE_NADZIEMNE')

            if 'KONDYGNACJE_PODZIEMNE' in properties:
                tags['building:levels:underground'] = properties.get('KONDYGNACJE_PODZIEMNE')

        except KeyError as e:
            raise InvalidKeyParserError(e)

        return tags
