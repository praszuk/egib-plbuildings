# flake8: noqa
from typing import Dict, TypeVar

from backend.areas.parsers import (
    BaseAreaParser,
    EpodgikAreaParser,
    GeoportalAreaParser,
    Geoportal2AreaParser,
    GIPortalAreaParser,
    LublinAreaParser,
    WarszawaAreaParser,
    WebEwidAreaParser,
    WroclawAreaParser,
)

AreaParser = TypeVar('AreaParser', bound=BaseAreaParser)
all_counties: Dict[str, AreaParser] = {
    # 02 – "dolnośląskie"
    '0201': GeoportalAreaParser(name='bolesławiecki', url_code='0201'),
    '0202': GeoportalAreaParser(
        name='dzierżoniowski',
        base_url='https://geoportal.pow.dzierzoniow.pl/ggp',
        url_typenames='budynki',
        gml_prefix='WMS',
        gml_geometry_key='MSGEOMETRY',
        custom_crs=2177,
    ),
    '0203': Geoportal2AreaParser(name='głogowski', url_code='glogow'),
    '0204': Geoportal2AreaParser(name='górowski', url_code='gora'),
    '0205': Geoportal2AreaParser(name='jaworski', url_code='jawor'),
    '0206': GIPortalAreaParser(
        name='karkonoski', base_url='https://wms.podgik.jgora.pl/jeleniagora-egib'
    ),
    '0207': GIPortalAreaParser(
        name='kamiennogórski', base_url='https://wms.kamienna-gora.pl/kamiennagora-egib'
    ),
    '0208': GeoportalAreaParser(
        name='kłodzki',
        base_url='https://geoportal.powiat.klodzko.pl/ggp',
        url_typenames='budynki',
        gml_prefix='WMS',
        gml_geometry_key='MSGEOMETRY',
        custom_crs=2177,
    ),
    '0209': WebEwidAreaParser(name='legnicki', url_code='legnicki-wms'),
    '0210': GIPortalAreaParser(name='lubański', base_url='https://iegib.powiatluban.pl/luban-egib'),
    '0211': WebEwidAreaParser(name='lubiński', url_code='lubinski-wms'),
    '0212': GIPortalAreaParser(
        name='lwówecki', base_url='https://ikerg.powiatlwowecki.pl/lwowekslaski-egib'
    ),
    '0213': WebEwidAreaParser(name='milicki', url_code='milicki-wms'),
    '0214': WebEwidAreaParser(name='oleśnicki', url_code='olesnicki', port=4444),
    '0215': WebEwidAreaParser(
        name='oławski', base_url='https://ewid.starostwo.olawa.pl:4444/iip/ows'
    ),
    '0216': WebEwidAreaParser(name='polkowicki', url_code='polkowicki-wms'),
    '0217': WebEwidAreaParser(name='strzeliński', url_code='strzelinski-wms'),
    '0218': GeoportalAreaParser(name='średzki', url_code='0218'),
    '0219': WebEwidAreaParser(name='świdnicki', url_code='swidnicki-wms'),
    '0220': WebEwidAreaParser(name='trzebnicki', url_code='trzebnicki-wms'),
    '0221': WebEwidAreaParser(name='wałbrzyski', url_code='walbrzyski-wms'),
    '0222': WebEwidAreaParser(
        name='wołowski', url_code='wolowski-wms', gml_geometry_key='msGeometry'
    ),
    '0223': WebEwidAreaParser(name='wrocławski', base_url='https://wms.wrosip.pl/iip/ows'),
    '0224': WebEwidAreaParser(name='ząbkowicki', url_code='zabkowicki', port=444),
    '0225': GIPortalAreaParser(
        name='zgorzelecki', base_url='https://iegib.powiat.zgorzelec.pl/zgorzelec-egib'
    ),
    '0226': GIPortalAreaParser(
        name='złotoryjski', base_url='https://wms.powiat-zlotoryja.pl/zlotoryja-egib'
    ),
    '0261': GeoportalAreaParser(
        name='miasto Jelenia Góra',
        base_url='https://geoportal.jeleniagora.pl/ggp',
        url_typenames='budynki',
        gml_prefix='WMS',
        gml_geometry_key='MSGEOMETRY',
        custom_crs=2176,
    ),
    '0262': WebEwidAreaParser(name='miasto Legnica', base_url='https://wms.legnica.eu/iip/ows'),
    '0264': WroclawAreaParser(name='miasto Wrocław', url_code=''),
    '0265': WebEwidAreaParser(name='miasto Wałbrzych', url_code='walbrzych-wms'),
    # 04 – "kujawsko-pomorskie"
    '0401': Geoportal2AreaParser(
        name='aleksandrowski', base_url='https://mapa.aleksandrow.pl/map/geoportal/wfs.php'
    ),
    '0402': Geoportal2AreaParser(
        name='brodnicki', base_url='https://mapa.brodnica.com.pl/map/geoportal/wfs.php'
    ),
    '0403': GeoportalAreaParser(name='bydgoski', url_code='0403'),
    '0404': WebEwidAreaParser(name='chełmiński', url_code='chelminski', port=44316),
    '0405': WebEwidAreaParser(name='golubsko-dobrzyński', url_code='golubsko-dobrzynski-wms'),
    '0406': GeoportalAreaParser(name='grudziądzki', url_code='0406'),
    '0407': WebEwidAreaParser(name='inowrocławski', url_code='inowroclawski-wms'),
    '0408': Geoportal2AreaParser(name='lipnowski', url_code='lipno'),
    '0409': WebEwidAreaParser(name='mogileński', url_code='mogilenski', port=4444),
    '0410': WebEwidAreaParser(name='nakielski', url_code='nakielski', port=62627),
    '0411': Geoportal2AreaParser(name='radziejowski', url_code='radziejow'),
    '0412': Geoportal2AreaParser(name='rypiński', url_code='rypin'),
    '0413': GeoportalAreaParser(name='sępoleński', url_code='0413'),
    '0414': WebEwidAreaParser(name='świecki', base_url='https://wms.csw.pl/iip/ows'),
    '0415': WebEwidAreaParser(name='toruński', url_code='torunski-wms'),
    '0416': WebEwidAreaParser(name='tucholski', url_code='tucholski-wms'),
    '0417': Geoportal2AreaParser(name='wąbrzeski', url_code='wabrzezno'),
    '0418': Geoportal2AreaParser(name='włocławski', url_code='wloclawek'),
    '0419': WebEwidAreaParser(name='żniński', url_code='zninski-wms'),
    '0461': GeoportalAreaParser(name='miasto Bydgoszcz', url_code='0461'),
    '0462': GeoportalAreaParser(
        name='miasto Grudziądz',
        base_url='https://geoportal.grudziadz.pl/ggp',
        url_typenames='budynki',
        gml_prefix='WMS',
        gml_geometry_key='MSGEOMETRY',
    ),
    '0463': WebEwidAreaParser(name='miasto Toruń', url_code='mtorun-wms'),
    '0464': Geoportal2AreaParser(
        name='miasto Włocławek', base_url='https://geoportal.wloclawek.eu/map/geoportal/wfs.php'
    ),
    # 06 – "lubelskie"
    '0601': Geoportal2AreaParser(name='bialski', url_code='powiatbialski'),
    '0602': Geoportal2AreaParser(name='biłgorajski', url_code='bilgorajski'),
    '0603': WebEwidAreaParser(name='chełmski', url_code='chelmski-wms'),
    '0604': Geoportal2AreaParser(name='hrubieszowski', url_code='hrubieszow'),
    '0605': Geoportal2AreaParser(name='janowski', url_code='janow'),
    '0606': Geoportal2AreaParser(name='krasnostawski', url_code='powiatkrasnostawski'),
    '0607': WebEwidAreaParser(name='kraśnicki', url_code='krasnicki-wms'),
    '0608': Geoportal2AreaParser(name='lubartowski', url_code='powiatlubartowski'),
    '0609': Geoportal2AreaParser(name='lubelski', url_code='powiatlubelski'),
    '0610': Geoportal2AreaParser(name='łęczyński', url_code='leczna'),
    '0611': Geoportal2AreaParser(name='łukowski', url_code='powiatlukowski'),
    '0612': Geoportal2AreaParser(name='opolski', url_code='opolelubelskie'),
    '0613': Geoportal2AreaParser(name='parczewski', url_code='parczew'),
    '0614': Geoportal2AreaParser(name='puławski', url_code='pulawy'),
    '0615': Geoportal2AreaParser(name='radzyński', url_code='powiatradzynski'),
    '0616': Geoportal2AreaParser(name='rycki', url_code='ryki'),
    '0617': Geoportal2AreaParser(name='świdnicki', url_code='powiatswidnik'),
    '0618': Geoportal2AreaParser(name='tomaszowski', url_code='tomaszowlubelski'),
    '0619': EpodgikAreaParser(name='włodawski', url_code='wlodawa'),
    '0620': Geoportal2AreaParser(name='zamojski', url_code='powiatzamojski'),
    '0661': Geoportal2AreaParser(name='miasto Biała Podlaska', url_code='bialapodlaska'),
    '0662': EpodgikAreaParser(name='miasto Chełm', url_code='mchelm'),
    '0663': LublinAreaParser(name='miasto Lublin', custom_crs=2179),
    '0664': Geoportal2AreaParser(name='miasto Zamość', url_code='zamosc'),
    # 08 – "lubuskie"
    '0801': Geoportal2AreaParser(name='gorzowski', url_code='powiatgorzowski'),
    '0802': GIPortalAreaParser(
        name='krośnieński', base_url='https://wms.powiatkrosnienski.pl/krosno-egib'
    ),
    '0803': Geoportal2AreaParser(name='międzyrzecki', url_code='powiat-miedzyrzecki'),
    '0804': GIPortalAreaParser(
        name='nowosolski', base_url='https://wms.powiat-nowosolski.pl/nowasol-egib'
    ),
    '0805': Geoportal2AreaParser(name='słubicki', url_code='slubice'),
    '0806': Geoportal2AreaParser(name='strzelecko-drezdenecki', url_code='fsd'),
    '0807': Geoportal2AreaParser(name='sulęciński', url_code='sulecin'),
    '0808': GIPortalAreaParser(
        name='świebodziński', base_url='https://giportal2.powiat.swiebodzin.pl/swiebodzin-egib'
    ),
    '0809': GIPortalAreaParser(
        name='zielonogórski', base_url='https://giportal.powiat-zielonogorski.pl/zielonagora-egib'
    ),
    '0810': WebEwidAreaParser(name='żagański', url_code='zaganski-wms'),
    '0811': Geoportal2AreaParser(name='żarski', url_code='zary'),
    '0812': Geoportal2AreaParser(name='wschowski', url_code='wschowa'),
    '0861': Geoportal2AreaParser(
        name='miasto Gorzów Wielkopolski',
        base_url='https://geoportal.wms.um.gorzow.pl/map/geoportal/wfs.php',
    ),
    # 10 – "łódzkie"
    '1001': Geoportal2AreaParser(name='bełchatowski', url_code='belchatow'),
    '1002': Geoportal2AreaParser(name='kutnowski', url_code='powiatkutno'),
    '1003': Geoportal2AreaParser(name='łaski', url_code='lask'),
    '1004': Geoportal2AreaParser(name='łęczycki', url_code='leczycki'),
    '1005': Geoportal2AreaParser(name='łowicki', url_code='lowicz'),
    '1006': Geoportal2AreaParser(name='łódzki wschodni', url_code='lodzkiwschodni'),
    '1007': Geoportal2AreaParser(name='opoczyński', url_code='opoczno'),
    '1008': Geoportal2AreaParser(name='pabianicki', url_code='pabianice'),
    '1009': Geoportal2AreaParser(name='pajęczański', url_code='pajeczno'),
    '1010': Geoportal2AreaParser(name='piotrkowski', url_code='piotrkow'),
    '1011': Geoportal2AreaParser(name='poddębicki', url_code='poddebice'),
    '1012': Geoportal2AreaParser(name='radomszczański', url_code='radomszczanski'),
    '1013': WebEwidAreaParser(name='rawski', base_url='https://wms.powiatrawski.pl/iip/ows'),
    '1014': Geoportal2AreaParser(name='sieradzki', url_code='sieradz'),
    '1015': Geoportal2AreaParser(name='skierniewicki', url_code='powiat-skierniewice'),
    '1016': Geoportal2AreaParser(name='tomaszowski', url_code='powiat-tomaszowski'),
    '1017': Geoportal2AreaParser(name='wieluński', url_code='wielun'),
    '1018': Geoportal2AreaParser(name='wieruszowski', url_code='wieruszow'),
    '1019': GeoportalAreaParser(name='zduńskowolski', url_code='1019'),
    '1020': GeoportalAreaParser(name='zgierski', url_code='1020'),
    '1021': Geoportal2AreaParser(name='brzeziński', url_code='brzeziny'),
    '1062': GIPortalAreaParser(
        name='miasto Piotrków Trybunalski', base_url='https://ikerg.piotrkow.pl/piotrkow-egib'
    ),
    '1063': Geoportal2AreaParser(name='miasto Skierniewice', url_code='skierniewice'),
    # 12 – "małopolskie"
    '1201': WebEwidAreaParser(
        name='bocheński', url_code='bochenski-wms', gml_geometry_key='msGeometry'
    ),
    '1202': Geoportal2AreaParser(name='brzeski', url_code='brzesko'),
    '1203': WebEwidAreaParser(name='chrzanowski', url_code='chrzanowski', port=22443),
    '1204': WebEwidAreaParser(name='dąbrowski', url_code='dabrowski-wms'),
    '1205': GeoportalAreaParser(name='gorlicki', url_code='1205'),
    '1206': WebEwidAreaParser(
        name='krakowski', base_url='https://wms.powiat.krakow.pl:1518/iip/ows'
    ),
    '1207': WebEwidAreaParser(name='limanowski', url_code='limanowski-wms'),
    '1208': Geoportal2AreaParser(name='miechowski', url_code='miechow'),
    '1209': GeoportalAreaParser(name='myślenicki', url_code='1209'),
    # 1210: same server as for 1262 – same data
    '1210': WebEwidAreaParser(name='nowosądecki', base_url='https://wms.nowosadecki.pl/iip/ows'),
    '1211': Geoportal2AreaParser(name='nowotarski', url_code='nowotarski'),
    '1212': WebEwidAreaParser(name='olkuski', url_code='olkuski', port=4434),
    '1213': WebEwidAreaParser(name='oświęcimski', url_code='oswiecimski', port=4422),
    '1214': GeoportalAreaParser(name='proszowicki', url_code='1214'),
    '1215': Geoportal2AreaParser(name='suski', url_code='powiatsuski'),
    '1216': WebEwidAreaParser(
        name='tarnowski', base_url='https://webewid.powiat.tarnow.pl:20443/iip/ows'
    ),
    '1217': WebEwidAreaParser(name='tatrzański', url_code='tatrzanski-wms'),
    '1218': WebEwidAreaParser(name='wadowicki', url_code='wadowicki', port=20443),
    '1219': WebEwidAreaParser(name='wielicki', url_code='wielicki-wms'),
    '1261': GIPortalAreaParser(
        name='miasto Kraków', base_url='https://geodezja.eco.um.krakow.pl/krakow-egib'
    ),
    '1262': WebEwidAreaParser(
        name='miasto Nowy Sącz', base_url='https://wms.nowosadecki.pl/iip/ows'
    ),
    '1263': WebEwidAreaParser(name='miasto Tarnów', base_url='https://wms.umt.tarnow.pl/iip/ows'),
    # 14 – "mazowieckie"
    '1401': Geoportal2AreaParser(name='białobrzeski', url_code='bialobrzegi'),
    '1402': Geoportal2AreaParser(name='ciechanowski', url_code='ciechanow'),
    '1403': Geoportal2AreaParser(name='garwoliński', url_code='garwolinski', port=8443),
    '1404': Geoportal2AreaParser(name='gostyniński', url_code='gostynin'),
    '1405': Geoportal2AreaParser(name='grodziski', url_code='grodzisk'),
    '1406': Geoportal2AreaParser(name='grójecki', url_code='grojec'),
    '1407': Geoportal2AreaParser(name='kozienicki', url_code='kozienicepowiat'),
    '1408': Geoportal2AreaParser(name='legionowski', url_code='powiat-legionowski'),
    '1409': Geoportal2AreaParser(name='lipski', url_code='powiatlipsko'),
    '1410': Geoportal2AreaParser(name='łosicki', url_code='losice'),
    '1411': Geoportal2AreaParser(name='makowski', url_code='makow'),
    '1412': EpodgikAreaParser(name='miński', url_code='minsk'),
    '1413': Geoportal2AreaParser(name='mławski', url_code='powiatmlawski'),
    '1414': Geoportal2AreaParser(name='nowodworski', url_code='nowodworski'),
    '1415': Geoportal2AreaParser(name='ostrołęcki', url_code='powiatostrolecki'),
    '1416': Geoportal2AreaParser(name='ostrowski', url_code='ostrowmaz'),
    '1417': Geoportal2AreaParser(name='otwocki', url_code='powiat-otwocki'),
    '1418': EpodgikAreaParser(name='piaseczyński', url_code='piaseczno'),
    '1419': Geoportal2AreaParser(name='płocki', url_code='powiat-plock'),
    '1420': Geoportal2AreaParser(name='płoński', url_code='plonski'),
    '1421': EpodgikAreaParser(name='pruszkowski', url_code='pruszkow'),
    '1422': Geoportal2AreaParser(name='przasnyski', url_code='przasnysz'),
    '1423': Geoportal2AreaParser(name='przysuski', url_code='przysucha'),
    '1424': Geoportal2AreaParser(name='pułtuski', url_code='powiatpultuski'),
    '1425': Geoportal2AreaParser(name='radomski', url_code='radom'),
    '1426': Geoportal2AreaParser(name='siedlecki', url_code='powiatsiedlecki'),
    '1427': Geoportal2AreaParser(name='sierpecki', url_code='sierpc'),
    '1428': Geoportal2AreaParser(name='sochaczewski', url_code='sochaczew'),
    '1429': Geoportal2AreaParser(name='sokołowski', url_code='powiat-sokolowski'),
    '1430': Geoportal2AreaParser(name='szydłowiecki', url_code='szydlowiecpowiat'),
    '1432': WebEwidAreaParser(name='warszawski zachodni', base_url='https://wms.pwz.pl/iip/ows'),
    '1433': EpodgikAreaParser(name='węgrowski', url_code='wegrow'),
    '1434': EpodgikAreaParser(name='wołomiński', url_code='wolomin'),
    '1435': Geoportal2AreaParser(name='wyszkowski', url_code='powiat-wyszkowski'),
    '1436': Geoportal2AreaParser(name='zwoleński', url_code='zwolenpowiat'),
    '1437': Geoportal2AreaParser(name='żuromiński', url_code='zuromin-powiat'),
    '1438': EpodgikAreaParser(name='żyrardowski', url_code='zyrardow'),
    '1461': Geoportal2AreaParser(name='miasto Ostrołęka', url_code='ostroleka'),
    '1462': WebEwidAreaParser(
        name='miasto Płock', base_url='https://wms-ggk.plock.eu:4443/iip/ows'
    ),
    '1463': GIPortalAreaParser(
        name='miasto Radom', base_url='https://ikerg.modgik.radom.pl/radom-egib'
    ),
    '1464': Geoportal2AreaParser(name='miasto Siedlce', url_code='siedlce'),
    '1465': WarszawaAreaParser(name='miasto Warszawa', url_code=''),
    # 16 – "opolskie"
    '1601': GIPortalAreaParser(name='brzeski', base_url='https://imapa.brzeg-powiat.pl/brzeg-egib'),
    '1602': GIPortalAreaParser(
        name='głubczycki', base_url='https://ikerg.powiatglubczycki.pl/glubczyce-egib'
    ),
    '1603': GeoportalAreaParser(name='kędzierzyńsko-kozielski', url_code='1603'),
    '1604': GIPortalAreaParser(name='kluczborski', base_url='http://185.108.68.134/kluczbork-egib'),
    '1605': GIPortalAreaParser(
        name='krapkowicki', base_url='https://ikerg.powiatkrapkowicki.pl/krapkowice-egib'
    ),
    '1606': GIPortalAreaParser(
        name='namysłowski', base_url='https://iegib.namyslow.pl/cgi-bin/namyslow-egib'
    ),
    '1607': GIPortalAreaParser(name='nyski', base_url='https://wms-egib.powiat.nysa.pl/nysa-egib'),
    '1608': GIPortalAreaParser(name='oleski', base_url='https://iegib.powiatoleski.pl/olesno-egib'),
    '1610': GIPortalAreaParser(
        name='prudnicki', base_url='https://ikerg2.powiatprudnicki.pl/prudnik-egib'
    ),
    '1611': GeoportalAreaParser(
        name='strzelecki',
        base_url='https://mapy.powiatstrzelecki.pl/ggp',
        url_typenames='budynki',
        gml_prefix='WMS',
        gml_geometry_key='MSGEOMETRY',
        custom_crs=2177,
    ),
    '1661': GIPortalAreaParser(name='miasto Opole', base_url='https://wms.um.opole.pl/opole-egib'),
    # 18 – "podkarpackie"
    '1801': WebEwidAreaParser(name='bieszczadzki', url_code='bieszczadzki-wms', port=4434),
    '1802': WebEwidAreaParser(name='brzozowski', url_code='brzozowski', port=4443),
    '1803': Geoportal2AreaParser(name='dębicki', url_code='debica'),
    '1804': WebEwidAreaParser(name='jarosławski', url_code='jaroslawski-wms'),
    '1805': WebEwidAreaParser(name='jasielski', url_code='jasielski-wms'),
    '1806': Geoportal2AreaParser(name='kolbuszowski', url_code='kolbuszowa'),
    '1807': WebEwidAreaParser(name='krośnieński', url_code='krosnienski-wms'),
    '1808': Geoportal2AreaParser(name='leżajski', url_code='lezajsk'),
    '1809': Geoportal2AreaParser(name='lubaczowski', url_code='lubaczow'),
    '1810': Geoportal2AreaParser(name='łańcucki', url_code='lancut'),
    '1811': Geoportal2AreaParser(name='mielecki', url_code='mielec'),
    '1812': Geoportal2AreaParser(name='niżański', url_code='powiat-nisko'),
    '1813': Geoportal2AreaParser(name='przemyski', url_code='powiat-przemysl'),
    '1814': WebEwidAreaParser(
        name='przeworski', base_url='https://sip.powiatprzeworsk.pl:4443/iip/ows'
    ),
    '1815': Geoportal2AreaParser(name='ropczycko-sędziszowski', url_code='spropczyce'),
    '1816': Geoportal2AreaParser(name='rzeszowski', url_code='powiatrzeszowski'),
    '1817': WebEwidAreaParser(name='sanocki', url_code='sanocki', port=8443),
    '1818': Geoportal2AreaParser(name='stalowowolski', url_code='stalowawola'),
    '1819': Geoportal2AreaParser(name='strzyżowski', url_code='strzyzowski'),
    '1820': Geoportal2AreaParser(name='tarnobrzeski', url_code='tarnobrzeski'),
    '1821': Geoportal2AreaParser(name='leski', url_code='lesko'),
    '1861': WebEwidAreaParser(name='miasto Krosno', url_code='krosno-wms'),
    '1862': Geoportal2AreaParser(name='miasto Przemyśl', url_code='przemysl'),
    '1863': Geoportal2AreaParser(
        name='miasto Rzeszów', base_url='https://osrodek.erzeszow.pl/map/geoportal/wfs.php'
    ),
    '1864': Geoportal2AreaParser(name='miasto Tarnobrzeg', url_code='tarnobrzeg'),
    # 20 – "podlaskie"
    '2001': Geoportal2AreaParser(name='augustowski', url_code='augustowski'),
    '2002': Geoportal2AreaParser(name='białostocki', url_code='bialystok'),
    '2003': Geoportal2AreaParser(name='bielski', url_code='powiatbielski'),
    '2004': Geoportal2AreaParser(name='grajewski', url_code='starostwograjewo'),
    '2005': Geoportal2AreaParser(name='hajnowski', url_code='hajnowka'),
    '2006': WebEwidAreaParser(name='kolneński', url_code='kolnenski-wms'),
    '2008': Geoportal2AreaParser(name='moniecki', url_code='monki'),
    '2009': Geoportal2AreaParser(name='sejneński', url_code='sejny'),
    '2010': GIPortalAreaParser(
        name='siemiatycki', base_url='https://geoportal.siemiatycze.pl/siemiatycze-egib'
    ),
    '2011': Geoportal2AreaParser(name='sokólski', url_code='powiatsokolski'),
    '2012': GeoportalAreaParser(name='suwalski', url_code='2012'),
    '2013': Geoportal2AreaParser(name='wysokomazowiecki', url_code='wysokomazowiecki'),
    '2014': Geoportal2AreaParser(name='zambrowski', url_code='powiatzambrowski'),
    '2061': WebEwidAreaParser(
        name='miasto Białystok', base_url='https://webewid-wms.um.bialystok.pl/iip/ows'
    ),
    '2063': GeoportalAreaParser(
        name='miasto Suwałki',
        base_url='https://geoportal.um.suwalki.pl/ggp',
        url_typenames='budynki',
        gml_prefix='WMS',
        gml_geometry_key='MSGEOMETRY',
        custom_crs=2179,
    ),
    # 22 – "pomorskie"
    '2201': WebEwidAreaParser(name='bytowski', url_code='bytowski', port=4433),
    '2202': WebEwidAreaParser(name='chojnicki', url_code='chojnicki-wms'),
    '2204': WebEwidAreaParser(name='gdański', url_code='gdanski-wms'),
    '2205': WebEwidAreaParser(name='kartuski', url_code='kartuski-wms'),
    '2206': WebEwidAreaParser(name='kościerski', url_code='koscierski-wms'),
    '2207': WebEwidAreaParser(name='kwidzyński', url_code='kwidzynski-wms'),
    '2208': WebEwidAreaParser(name='lęborski', url_code='leborski', port=44443),
    '2209': WebEwidAreaParser(name='malborski', url_code='malborski-wms'),
    '2210': GeoportalAreaParser(name='nowodworski', url_code='2210'),
    '2211': WebEwidAreaParser(name='pucki', base_url='https://pdp.puck.pl/iip/ows'),
    '2212': WebEwidAreaParser(name='słupski', base_url='https://wms.powiat.slupsk.pl/iip/ows'),
    '2213': WebEwidAreaParser(
        name='starogardzki', base_url='https://wms.powiatstarogard.pl/iip/ows'
    ),
    '2214': WebEwidAreaParser(name='tczewski', base_url='https://wms.powiat.tczew.pl/iip/ows'),
    '2215': EpodgikAreaParser(name='wejherowski', url_code='wejherowo'),
    '2216': GeoportalAreaParser(name='sztumski', url_code='2216'),
    '2261': WebEwidAreaParser(
        name='miasto Gdańsk', base_url='https://ewid-wms.gdansk.gda.pl/iip/ows'
    ),
    '2262': WebEwidAreaParser(
        name='miasto Gdynia', base_url='https://pc73.miasto.gdynia.pl/iip/ows'
    ),
    '2263': WebEwidAreaParser(name='miasto Słupsk', base_url='https://wms.slupsk.eu/iip/ows'),
    '2264': WebEwidAreaParser(name='miasto Sopot', base_url='https://wms.um.sopot.pl/iip/ows'),
    # 24 – "śląskie"
    '2401': GIPortalAreaParser(
        name='będziński', base_url='https://ikerg.powiat.bedzin.pl/bedzin-egib'
    ),
    '2402': WebEwidAreaParser(name='bielski', url_code='bielski-ows'),
    '2403': Geoportal2AreaParser(name='cieszyński', url_code='cieszyn'),
    '2404': Geoportal2AreaParser(name='częstochowski', url_code='czestochowa'),
    '2405': WebEwidAreaParser(name='gliwicki', url_code='gliwicki', port=4443),
    '2406': GeoportalAreaParser(
        name='kłobucki',
        base_url='https://mapy.powiatklobucki.pl/ggp',
        url_typenames='budynki',
        gml_prefix='WMS',
        gml_geometry_key='MSGEOMETRY',
        custom_crs=2177,
    ),
    '2407': GIPortalAreaParser(name='lubliniecki', base_url='http://83.17.150.14/lubliniec-egib'),
    '2408': Geoportal2AreaParser(
        name='mikołowski', base_url='https://mapa.mikolowski.pl/map/geoportal/wfs.php'
    ),
    '2409': GIPortalAreaParser(
        name='myszkowski', base_url='https://imapa.powiatmyszkowski.pl/myszkow-egib'
    ),
    '2410': WebEwidAreaParser(name='pszczyński', url_code='pszczynski-wms'),
    '2411': Geoportal2AreaParser(name='raciborski', url_code='raciborz'),
    '2412': Geoportal2AreaParser(name='rybnicki', url_code='rybnik'),
    '2413': WebEwidAreaParser(
        name='tarnogórski', base_url='https://geodane.tarnogorski.pl/iip/ows'
    ),
    '2414': WebEwidAreaParser(name='bieruńsko-lędziński', url_code='sbl', port=8443),
    '2416': GIPortalAreaParser(
        name='zawierciański', base_url='https://ikerg.zawiercie.powiat.pl/powiatzawiercianski-egib'
    ),
    '2417': WebEwidAreaParser(name='żywiecki', url_code='zywiecki-wms'),
    '2461': GIPortalAreaParser(
        name='miasto Bielsko-Biała', base_url='https://ikerg.bielsko-biala.pl/bielsko-egib'
    ),
    '2462': GIPortalAreaParser(name='miasto Bytom', base_url='https://iwms.um.bytom.pl/bytom-egib'),
    '2465': WebEwidAreaParser(
        name='miasto Dąbrowa Górnicza', base_url='https://geoportal-wms.dg.pl/iip/ows'
    ),
    '2466': WebEwidAreaParser(
        name='miasto Gliwice', base_url='https://wmswfs-geodezja.gliwice.eu/iip/ows'
    ),
    '2467': Geoportal2AreaParser(name='miasto Jastrzębie-Zdrój', url_code='jastrzebie'),
    '2468': WebEwidAreaParser(name='miasto Jaworzno', url_code='jaworzno-wms'),
    '2470': GIPortalAreaParser(
        name='miasto Mysłowice', base_url='https://wms.myslowice.pl/myslowice-egib'
    ),
    '2471': GIPortalAreaParser(
        name='miasto Piekary Śląskie', base_url='https://wms.sip.piekary.pl/piekary-egib'
    ),
    '2472': Geoportal2AreaParser(name='miasto Ruda Śląska', url_code='rudaslaska'),
    '2473': GIPortalAreaParser(
        name='miasto Rybnik', base_url='https://geodeta.gpue.rybnik.eu/rybnik-egib'
    ),
    '2474': Geoportal2AreaParser(name='miasto Siemianowice Śląskie', url_code='siemianowice'),
    '2475': GeoportalAreaParser(name='miasto Sosnowiec', url_code='2475'),
    '2476': Geoportal2AreaParser(name='miasto Świętochłowice', url_code='swietochlowice'),
    '2477': WebEwidAreaParser(name='miasto Tychy', base_url='https://geowms.umtychy.pl/iip/ows'),
    '2478': WebEwidAreaParser(name='miasto Zabrze', base_url='https://wms.miastozabrze.pl/iip/ows'),
    # 26 – "świętokrzyskie"
    '2601': Geoportal2AreaParser(
        name='buski', base_url='https://geodezja.powiat.busko.pl/map/geoportal/wfs.php'
    ),
    '2602': Geoportal2AreaParser(name='jędrzejowski', url_code='jedrzejow'),
    '2603': Geoportal2AreaParser(name='kazimierski', url_code='kazimierzaw'),
    '2604': Geoportal2AreaParser(
        name='kielecki', base_url='https://geoportal.powiat.kielce.pl/map/geoportal/wfs.php'
    ),
    '2605': Geoportal2AreaParser(name='konecki', url_code='konskie'),
    '2606': Geoportal2AreaParser(name='opatowski', url_code='opatow'),
    '2607': Geoportal2AreaParser(name='ostrowiecki', url_code='ostrowiec'),
    '2608': Geoportal2AreaParser(name='pińczowski', url_code='pinczow'),
    '2609': Geoportal2AreaParser(name='sandomierski', url_code='sandomierz'),
    '2610': Geoportal2AreaParser(name='skarżyski', url_code='skarzysko'),
    '2611': Geoportal2AreaParser(name='starachowicki', url_code='starachowice'),
    '2612': Geoportal2AreaParser(name='staszowski', url_code='staszow'),
    '2613': Geoportal2AreaParser(name='włoszczowski', url_code='wloszczowa'),
    '2661': GIPortalAreaParser(name='miasto Kielce', base_url='https://wms.kielce.eu/kielce-egib'),
    # 28 – "warmińsko-mazurskie"
    '2801': Geoportal2AreaParser(name='bartoszycki', url_code='powiatbartoszyce'),
    '2802': Geoportal2AreaParser(name='braniewski', url_code='powiat-braniewo'),
    '2803': Geoportal2AreaParser(name='działdowski', url_code='powiatdzialdowski'),
    '2804': GIPortalAreaParser(
        name='elbląski', base_url='https://ikerg.powiat.elblag.pl/elblaski-egib'
    ),
    '2805': Geoportal2AreaParser(name='ełcki', url_code='powiatelk'),
    '2806': EpodgikAreaParser(name='giżycki', url_code='gizycko'),
    '2807': Geoportal2AreaParser(name='iławski', url_code='ilawa'),
    '2808': Geoportal2AreaParser(name='kętrzyński', url_code='powiatketrzynski'),
    '2809': Geoportal2AreaParser(name='lidzbarski', url_code='powiatlidzbarski'),
    '2810': EpodgikAreaParser(name='mrągowski', url_code='mragowo'),
    '2811': Geoportal2AreaParser(name='nidzicki', url_code='powiatnidzicki'),
    '2812': Geoportal2AreaParser(name='nowomiejski', url_code='powiat-nowomiejski'),
    '2813': Geoportal2AreaParser(name='olecki', url_code='olecko'),
    '2814': Geoportal2AreaParser(name='olsztyński', url_code='powiatolsztynski'),
    '2815': Geoportal2AreaParser(name='ostródzki', url_code='ostroda'),
    '2816': Geoportal2AreaParser(name='piski', url_code='powiatpiski'),
    '2817': Geoportal2AreaParser(name='szczycieński', url_code='szczytno'),
    '2818': Geoportal2AreaParser(name='gołdapski', url_code='powiatgoldap'),
    '2819': EpodgikAreaParser(name='węgorzewski', url_code='wegorzewo'),
    '2861': GIPortalAreaParser(
        name='miasto Elbląg', base_url='https://wms.geodezja.elblag.eu/elblag-wms'
    ),
    '2862': WebEwidAreaParser(
        name='miasto Olsztyn', base_url='https://webewidwms.olsztyn.eu/iip/ows'
    ),
    # 30 – "wielkopolskie"
    '3001': GeoportalAreaParser(name='chodzieski', url_code='3001'),
    '3003': GIPortalAreaParser(
        name='gnieźnieński', base_url='https://wms.geodezjagniezno.pl/gniezno-egib'
    ),
    '3004': GIPortalAreaParser(
        name='gostyński', base_url='https://imapa.powiat.gostyn.pl/gostyn-egib'
    ),
    '3005': GIPortalAreaParser(name='grodziski', base_url='https://ikerg.pgw.pl/grodziskwlkp-egib'),
    '3006': GIPortalAreaParser(
        name='jarociński', base_url='https://ikerg.powiat-jarocinski.pl/jarocin-egib'
    ),
    '3007': Geoportal2AreaParser(name='kaliski', url_code='kalisz'),
    '3008': GIPortalAreaParser(name='kępiński', base_url='https://ikerg.powiatkepno.pl/kepno-egib'),
    '3009': GIPortalAreaParser(
        name='kolski', base_url='https://ikerg.starostwokolskie.pl/powiatkolski-egib'
    ),
    '3010': Geoportal2AreaParser(name='koniński', url_code='konin'),
    '3012': GeoportalAreaParser(name='krotoszyński', url_code='3012'),
    '3013': WebEwidAreaParser(name='leszczyński', url_code='leszczynski', port=543),
    '3014': EpodgikAreaParser(name='międzychodzki', url_code='miedzychod'),
    '3015': GIPortalAreaParser(
        name='nowotomyski', base_url='https://wms.powiatnowotomyski.pl/nowytomysl-egib'
    ),
    '3016': GeoportalAreaParser(name='obornicki', url_code='3016'),
    '3017': GIPortalAreaParser(
        name='ostrowski', base_url='https://ikerg.powiat-ostrowski.pl/ostrow-egib'
    ),
    '3019': GeoportalAreaParser(name='pilski', url_code='3019'),
    '3020': GIPortalAreaParser(name='pleszewski', base_url='https://wms.geo.net.pl/pleszew-egib'),
    '3021': GIPortalAreaParser(
        name='poznański', base_url='https://ikerg.podgik.poznan.pl/wms-poznanski'
    ),
    '3022': GeoportalAreaParser(name='rawicki', url_code='3022'),
    '3023': GeoportalAreaParser(name='słupecki', url_code='3023'),
    '3024': GIPortalAreaParser(
        name='szamotulski', base_url='https://wms.szamotuly.com.pl/szamotuly-egib'
    ),
    '3026': GIPortalAreaParser(name='śremski', base_url='https://wms.powiat-srem.pl/srem-egib'),
    '3028': GIPortalAreaParser(
        name='wągrowiecki', base_url='https://ikerg.wagrowiec.pl/wagrowiec-egib'
    ),
    '3029': GIPortalAreaParser(
        name='wolsztyński', base_url='https://ikerg.powiatwolsztyn.pl/wolsztyn-egib'
    ),
    '3030': GIPortalAreaParser(
        name='wrzesiński', base_url='https://wms.wrzesnia.powiat.pl/wrzesnia-egib'
    ),
    '3031': GIPortalAreaParser(
        name='złotowski', base_url='https://ikerg.zlotow-powiat.pl/zlotow-egib'
    ),
    '3061': GIPortalAreaParser(
        name='miasto Kalisz', base_url='https://ikerg.um.kalisz.pl/kalisz-egib'
    ),
    '3062': GIPortalAreaParser(
        name='miasto Konin', base_url='https://ikerg.kosit.konin.eu/konin-egib'
    ),
    '3063': GeoportalAreaParser(name='miasto Leszno', url_code='3063'),
    # 32 – "zachodniopomorskie"
    '3201': WebEwidAreaParser(name='białogardzki', url_code='bialogardzki-wms'),
    '3202': GIPortalAreaParser(
        name='choszczeński', base_url='https://ikerg.geopowiatchoszczno.pl/choszczno-egib'
    ),
    '3203': WebEwidAreaParser(name='drawski', url_code='drawski-wms'),
    '3204': WebEwidAreaParser(name='goleniowski', url_code='goleniowski', port=6443),
    '3205': GIPortalAreaParser(
        name='gryficki', base_url='https://ikerg.podgikgryfice.pl/gryfice-egib'
    ),
    '3206': WebEwidAreaParser(name='gryfiński', url_code='gryfinski', port=4439),
    '3207': GIPortalAreaParser(
        name='kamieński', base_url='https://ikerg.powiatkamienski.pl/kamien'
    ),
    '3208': WebEwidAreaParser(name='kołobrzeski', url_code='kolobrzeski-wms'),
    '3209': WebEwidAreaParser(name='koszaliński', url_code='koszalinski-wms'),
    '3210': GIPortalAreaParser(
        name='myśliborski', base_url='https://wms.powiatmysliborski.com.pl/mysliborz-egib'
    ),
    '3211': GIPortalAreaParser(name='policki', base_url='https://wgkik.policki.pl/police-egib'),
    '3212': GIPortalAreaParser(name='pyrzycki', base_url='https://ikerg.pyrzyce.pl/pyrzyce-egib'),
    '3213': WebEwidAreaParser(name='sławieński', url_code='slawienski', port=4443),
    '3214': GIPortalAreaParser(
        name='stargardzki', base_url='https://ikerg2.powiatstargardzki.eu/stargard-egib'
    ),
    '3215': WebEwidAreaParser(name='szczecinecki', url_code='szczecinecki-wms'),
    '3216': GeoportalAreaParser(name='świdwiński', url_code='3216'),
    '3217': WebEwidAreaParser(name='wałecki', url_code='walecki', port=4434),
    '3218': GIPortalAreaParser(name='łobeski', base_url='https://wms.powiatlobeski.pl/lobez-egib'),
    '3261': GeoportalAreaParser(name='miasto Koszalin', url_code='3261'),
    '3262': GIPortalAreaParser(
        name='miasto Szczecin', base_url='https://wms.e-osrodek.szczecin.pl/szczecin-egib'
    ),
    '3263': GIPortalAreaParser(
        name='miasto Świnoujście', base_url='https://geo-wms.um.swinoujscie.pl/swinoujscie'
    ),
}
# Few exception which counties are already defined but these communes has own servive for the data
communes = {
    '2403011': Geoportal2AreaParser(name='miasto Cieszyn', url_code='miastocieszyn'),
}
all_areas = all_counties | communes
