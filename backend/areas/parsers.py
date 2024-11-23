from __future__ import annotations

import json
from typing import Any, List, Dict, Tuple
from urllib.parse import urlparse, parse_qs, urlencode

from lxml import etree
from lxml.etree import XMLSyntaxError
from osgeo import ogr, osr  # noqa
from osgeo.ogr import Geometry

from backend.exceptions import InvalidKeyParserError, ParserError
from abc import abstractmethod

from typing import Final

DEFAULT_BUILDING: Final = 'yes'

# EGiB KST classification "EGB_RodzajWgKSTType"
# XSD: http://www.gugik.gov.pl/bip/prawo/schematy-aplikacyjne
BUILDING_KST_CODE_TYPE: Final = {
    'm': 'residential',
    'g': DEFAULT_BUILDING,
    't': DEFAULT_BUILDING,
    'k': DEFAULT_BUILDING,
    'z': DEFAULT_BUILDING,
    'b': 'office',
    'h': 'retail',
    'p': 'industrial',
    's': DEFAULT_BUILDING,
    'i': DEFAULT_BUILDING,
}
KST_NAME_CODE: Final = {
    'mieszkalny': 'm',
    'produkcyjnoUslugowyIGospodarczy': 'g',
    'transportuILacznosci': 't',
    'oswiatyNaukiIKulturyOrazSportu': 'k',
    'szpitalaIInneBudynkiOpiekiZdrowotnej': 'z',
    'biurowy': 'b',
    'handlowoUslugowy': 'h',
    'przemyslowy': 'p',
    'zbiornikSilosIBudynekMagazynowy': 's',
    'budynekNiemieszkalny': 'i',
}


def merge_url_query_params(url: str, additional_params: dict) -> str:
    """
    https://stackoverflow.com/a/52373377
    """
    url_components = urlparse(url)
    original_params = parse_qs(url_components.query)
    merged_params = {**original_params, **additional_params}
    updated_query = urlencode(merged_params, doseq=True)
    return url_components._replace(query=updated_query).geturl()


class BaseAreaParser:
    DEFAULT_SRS_NAME: str = 'EPSG:4326'
    DEFAULT_FULL_SRS_NAME: str = 'urn:ogc:def:crs:EPSG:4326'

    def __init__(
        self,
        name: str,
        url_code: str = None,
        base_url: str = None,
        port: int | None = None,
        custom_crs: int = None,
        gml_prefix: str = 'ms',
        gml_geometry_key: str = 'msGeometry',
    ):
        self.name = name
        self.url_code = url_code
        self.base_url = base_url
        self.port = port
        self.custom_crs = custom_crs
        self.gml_prefix = gml_prefix
        self.gml_geometry_key = gml_geometry_key

    @abstractmethod
    def build_buildings_url(self) -> str:
        pass

    @abstractmethod
    def build_buildings_bbox_url(self, lat: float, lon: float) -> str:
        pass

    @abstractmethod
    def parse_properties_to_osm_tags(self, properties: Dict[str, Any]) -> Dict[str, Any]:
        pass

    def parse_gml_to_geojson(self, gml_content: str) -> dict[str, Any]:
        features: List[Dict[str, Any]] = []

        geoms_and_props = self.parse_gml_to_geometries_and_properties(gml_content)
        for geometry, properties in geoms_and_props:
            geojson_str_geometry: str = geometry.ExportToJson()
            features.append(
                {
                    'type': 'Feature',
                    'geometry': json.loads(geojson_str_geometry),
                    'properties': properties,
                }
            )

        return {'type': 'FeatureCollection', 'features': features}

    def parse_gml_to_geometries_and_properties(
        self, gml_content: str
    ) -> List[Tuple[Geometry, Dict[str, Any]]]:
        geometries_and_properties: List[Tuple[Geometry, Dict[str, Any]]] = []

        try:
            parser = etree.XMLParser(recover=True)
            root = etree.fromstring(bytes(gml_content, encoding='utf-8'), parser)
        except XMLSyntaxError:
            raise ParserError('Cannot parse root of GML content')

        if root is None:
            raise ParserError('GML root not found')

        try:
            wfs_members = root.findall('.//wfs:member', namespaces=root.nsmap)
        except (KeyError, SyntaxError):
            raise ParserError('Cannot parse wfs members')

        for wfs_member in wfs_members:
            building_member = wfs_member.getchildren()[0]  # get <prefix> member

            geometries = []
            properties = {}
            for child in building_member.getchildren():
                if not child.tag.startswith('{' + str(root.nsmap.get(self.gml_prefix))):
                    continue

                clean_tag = child.tag.replace(root.nsmap.get(self.gml_prefix), '')[2:]
                if clean_tag == self.gml_geometry_key:
                    # 1 building member object (multisurface), can contain multiple polygons
                    polygons = building_member.findall('.//gml:Polygon', namespaces=root.nsmap)

                    for polygon in polygons:
                        gml_geom = etree.tostring(polygon).decode('utf-8')
                        geometry: ogr.Geometry = ogr.CreateGeometryFromGML(gml_geom)

                        # Reproject to 4326
                        if self.custom_crs and self.custom_crs != 4326:
                            source = osr.SpatialReference()
                            source.ImportFromEPSG(self.custom_crs)
                            target = osr.SpatialReference()
                            target.SetWellKnownGeogCS('WGS84')
                            transform = osr.CoordinateTransformation(source, target)
                            geometry.Transform(transform)

                        # fix incorrect lat lon order
                        point = geometry.GetGeometryRef(0).GetPoint(0)
                        if point[0] > point[1]:
                            self.swap_geometry_coordinates(geometry)

                        geometries.append(geometry)

                else:
                    properties[clean_tag] = child.text

            for geometry in geometries:
                # ignoring duplicated building_id etc.
                geometries_and_properties.append((geometry, properties))

        return geometries_and_properties

    def replace_properties_with_osm_tags(self, geojson: Dict[str, Any]) -> None:
        for index, feature in enumerate(geojson['features']):
            properties = feature['properties']
            tags = self.parse_properties_to_osm_tags(properties)
            geojson['features'][index]['properties'] = self.clean_tags(tags)

    @staticmethod
    def clean_tags(osm_tags: Dict[str, Any]) -> Dict[str, Any]:
        """
        Skip empty tags.
        Parse building levels as numbers and reject errors.
        """
        tags = {}
        for k, v in osm_tags.items():
            if not k or not v:
                continue

            if k in ('building:levels', 'building:levels:underground'):
                try:
                    v = int(v)
                except ValueError:
                    continue

                if v <= 0:
                    continue

            tags[k] = v

        return tags

    @staticmethod
    def reproject_coordinates(lat: float, lon: float, dest_epsg: int) -> (float, float):
        """
        :param lat: in EPSG:4326
        :param lon: in EPSG:4326
        :param dest_epsg: destination projection from EPSG code e.g. 2180
        :return: x, y
        """

        source = osr.SpatialReference()
        source.ImportFromEPSG(4326)

        target = osr.SpatialReference()
        target.ImportFromEPSG(dest_epsg)

        # Create a coordinate transformation
        transform = osr.CoordinateTransformation(source, target)

        # Transform the point
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(lat, lon)

        point.Transform(transform)

        return point.GetX(), point.GetY()

    @staticmethod
    def swap_geometry_coordinates(geometry: Geometry) -> None:
        source = osr.SpatialReference()
        source.ImportFromEPSG(4326)
        target = osr.SpatialReference()
        target.ImportFromEPSG(4326)
        target.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
        transform = osr.CoordinateTransformation(source, target)
        geometry.Transform(transform)


class EpodgikAreaParser(BaseAreaParser):
    def build_buildings_url(self) -> str:
        return (
            f'https://wms.epodgik.pl/cgi-bin/{self.url_code}/wfs'
            '?service=wfs'
            '&version=2.0.0'
            '&request=GetFeature'
            '&typeNames=ms:budynki'
            f'&SRSNAME={self.DEFAULT_SRS_NAME}'
        )

    def build_buildings_bbox_url(self, lat: float, lon: float) -> str:
        bbox = ','.join(map(str, [lat, lon, lat, lon]))
        return merge_url_query_params(
            self.build_buildings_url(), {'bbox': f'{bbox},{self.DEFAULT_SRS_NAME}'}
        )

    def parse_properties_to_osm_tags(self, properties: Dict[str, Any]) -> Dict[str, Any]:
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


class GeoportalAreaParser(BaseAreaParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, custom_crs=2180)

    def build_buildings_url(self) -> str:
        return (
            f'https://mapy.geoportal.gov.pl/wss/ext/PowiatoweBazyEwidencjiGruntow/{self.url_code}'
            f'?service=WFS'
            f'&version=2.0.0'
            f'&REQUEST=GetFeature'
            f'&TYPENAMES=ms:budynki'
        )

    def build_buildings_bbox_url(self, lat: float, lon: float) -> str:
        x, y = self.reproject_coordinates(lat, lon, self.custom_crs)
        bbox = ','.join(map(str, [x, y, x, y]))
        return merge_url_query_params(self.build_buildings_url(), {'bbox': bbox})

    def parse_properties_to_osm_tags(self, properties: Dict[str, Any]) -> Dict[str, Any]:
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


class Geoportal2AreaParser(BaseAreaParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, gml_prefix='ewns', gml_geometry_key='geometria')

    def build_buildings_url(self) -> str:
        port_frag = f':{self.port}' if self.port else ''
        return (
            f'https://{self.url_code}.geoportal2.pl{port_frag}/map/geoportal/wfs.php'
            f'?service=WFS'
            f'&REQUEST=GetFeature'
            f'&TYPENAMES=ewns:budynki'
            f'&SRSNAME={self.DEFAULT_SRS_NAME}'
        )

    def build_buildings_bbox_url(self, lat: float, lon: float) -> str:
        offset = 0.00001
        # geoportal2 ewmapa services return 400 if lat1 == lat2 or lon1 == lon2
        bbox = ','.join(map(str, [lat, lon, lat + offset, lon + offset]))
        return merge_url_query_params(
            self.build_buildings_url(), {'bbox': f'{bbox},{self.DEFAULT_SRS_NAME}'}
        )

    def parse_properties_to_osm_tags(self, properties: Dict[str, Any]) -> Dict[str, Any]:
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


class GIPortalAreaParser(BaseAreaParser):
    def build_buildings_url(self) -> str:
        return (
            f'{self.base_url}'
            f'?service=WFS'
            f'&version=2.0.0'
            f'&REQUEST=GetFeature'
            f'&TYPENAMES=ms:budynki'
            f'&SRSNAME={self.DEFAULT_SRS_NAME}'
        )

    def build_buildings_bbox_url(self, lat: float, lon: float) -> str:
        bbox = ','.join(map(str, [lat, lon, lat, lon]))
        return merge_url_query_params(
            self.build_buildings_url(), {'bbox': f'{bbox},{self.DEFAULT_SRS_NAME}'}
        )

    def parse_properties_to_osm_tags(self, properties: Dict[str, Any]) -> Dict[str, Any]:
        tags: Dict[str, Any] = {}
        try:
            tags['building'] = BUILDING_KST_CODE_TYPE.get(
                KST_NAME_CODE.get(properties.get('RODZAJ'), None), DEFAULT_BUILDING
            )
            if 'KONDYGNACJE_NADZIEMNE' in properties:
                tags['building:levels'] = properties.get('KONDYGNACJE_NADZIEMNE')

            if 'KONDYGNACJE_PODZIEMNE' in properties:
                tags['building:levels:underground'] = properties.get('KONDYGNACJE_PODZIEMNE')

        except KeyError as e:
            raise InvalidKeyParserError(e)

        return tags


class WarszawaAreaParser(BaseAreaParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, gml_prefix='Q1', gml_geometry_key='GEOMETRY')

    def build_buildings_url(self) -> str:
        return (
            f'https://wms2.um.warszawa.pl/geoserver/wfs/wfs'
            '?service=wfs'
            '&version=2.0.0'
            '&request=GetFeature'
            '&typeNames=wfs:budynki'
            f'&SRSNAME={self.DEFAULT_SRS_NAME}'
        )

    def build_buildings_bbox_url(self, lat: float, lon: float) -> str:
        bbox = ','.join(map(str, [lat, lon, lat, lon]))
        return merge_url_query_params(
            self.build_buildings_url(), {'bbox': f'{bbox},{self.DEFAULT_FULL_SRS_NAME}'}
        )

    def parse_properties_to_osm_tags(self, properties: Dict[str, Any]) -> Dict[str, Any]:
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


class WebEwidAreaParser(BaseAreaParser):
    def __init__(self, *args, **kwargs):
        if 'gml_geometry_key' not in kwargs:
            kwargs['gml_geometry_key'] = 'geometry'

        super().__init__(*args, **kwargs)

    def buildings_url(self) -> str:
        if self.base_url:
            endpoint = self.base_url
        else:
            port_frag = f':{self.port}' if self.port else ''
            endpoint = f'https://{self.url_code}.webewid.pl{port_frag}/iip/ows'
        return f'{endpoint}?service=wfs&version=2.0.0&request=GetFeature&typeNames=ms:budynki'

    def build_buildings_url(self) -> str:
        return merge_url_query_params(self.buildings_url(), {'SRSNAME': self.DEFAULT_SRS_NAME})

    def build_buildings_bbox_url(self, lat: float, lon: float) -> str:
        """
        Note: At 2024 BBOX filtering still not work, or work completely randomly.
        This function exists only for healthcheck.
        """
        buildings_url = self.buildings_url()

        if self.custom_crs and self.custom_crs != 4326:
            x, y = self.reproject_coordinates(lat, lon, self.custom_crs)
            url = merge_url_query_params(buildings_url, {'BBOX': ','.join(map(str, [x, y, x, y]))})
        else:
            url = merge_url_query_params(
                buildings_url,
                {
                    'SRSNAME': self.DEFAULT_SRS_NAME,
                    'BBOX': ','.join(map(str, [lat, lon, lat, lon])) + f',{self.DEFAULT_SRS_NAME}',
                },
            )

        return url

    def parse_properties_to_osm_tags(self, properties: Dict[str, Any]) -> Dict[str, Any]:
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


class WroclawAreaParser(BaseAreaParser):
    def build_buildings_url(self) -> str:
        return (
            f'https://iwms.zgkikm.wroc.pl/wroclaw-egib'
            '?service=wfs'
            '&version=2.0.0'
            '&request=GetFeature'
            '&typeNames=ms:budynki'
            f'&SRSNAME={self.DEFAULT_SRS_NAME}'
        )

    def build_buildings_bbox_url(self, lat: float, lon: float) -> str:
        bbox = ','.join(map(str, [lat, lon, lat, lon]))
        return merge_url_query_params(
            self.build_buildings_url(), {'bbox': f'{bbox},{self.DEFAULT_SRS_NAME}'}
        )

    def parse_properties_to_osm_tags(self, properties: Dict[str, Any]) -> Dict[str, Any]:
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
