from backend.areas.models import HealtCheckTestAreaData


counties = [
    # 06 – "lubelskie"
    HealtCheckTestAreaData(
        name='włodawski',
        teryt='0619',
        lat=51.54789,
        lon=23.55561,
        expected_tags={'building': 'office'},
    ),
    HealtCheckTestAreaData(
        name='miasto Chełm',
        teryt='0662',
        lat=51.13321,
        lon=23.49482,
        expected_tags={'building': 'yes', 'building:levels': '4'},
    ),
    # 14 – "mazowieckie"
    HealtCheckTestAreaData(
        name='miński',
        teryt='1412',
        lat=52.18138,
        lon=21.55919,
        expected_tags={'building': 'office', 'building:levels': '3'},
    ),
    HealtCheckTestAreaData(
        name='piaseczyński',
        teryt='1418',
        lat=52.07573,
        lon=21.03090,
        expected_tags={'building': 'office', 'building:levels': '3'},
    ),
    HealtCheckTestAreaData(
        name='pruszkowski',
        teryt='1421',
        lat=52.16323,
        lon=20.80185,
        expected_tags={'building': 'office', 'building:levels': '5'},
    ),
    HealtCheckTestAreaData(
        name='węgrowski',
        teryt='1433',
        lat=52.39642,
        lon=22.01390,
        expected_tags={'building': 'office', 'building:levels': '4'},
    ),
    HealtCheckTestAreaData(
        name='wołomiński',
        teryt='1434',
        lat=52.34413,
        lon=21.23856,
        expected_tags={'building': 'office', 'building:levels': '3'},
    ),
    HealtCheckTestAreaData(
        name='żyrardowski',
        teryt='1438',
        lat=52.05622,
        lon=20.43519,
        expected_tags={'building': 'office', 'building:levels': '4'},
    ),
    # 22 – "pomorskie"
    HealtCheckTestAreaData(
        name='wejherowski',
        teryt='2215',
        lat=54.60103,
        lon=18.23298,
        expected_tags={'building': 'office', 'building:levels': '3'},
    ),
    # 24 - "śląskie"
    HealtCheckTestAreaData(
        name='cieszyński',
        teryt='2403',
        lat=49.73631,
        lon=18.73886,
        expected_tags={'building': 'office'},
    ),
    # 28 – "warmińsko-mazurskie"
    HealtCheckTestAreaData(
        name='giżycki',
        teryt='2806',
        lat=54.03585,
        lon=21.76786,
        expected_tags={'building': 'office', 'building:levels': '5'},
    ),
    HealtCheckTestAreaData(
        name='mrągowski',
        teryt='2810',
        lat=53.87659,
        lon=21.30455,
        expected_tags={'building': 'office', 'building:levels': '2'},
    ),
    HealtCheckTestAreaData(
        name='węgorzewski',
        teryt='2819',
        lat=54.20739,
        lon=21.73810,
        expected_tags={'building': 'office', 'building:levels': '2'},
    ),
    # 30 – "wielkopolskie"
    HealtCheckTestAreaData(
        name='międzychodzki',
        teryt='3014',
        lat=52.60663,
        lon=15.90180,
        expected_tags={'building': 'office', 'building:levels': '3'},
    ),
]

# Few exception which counties are already defined but these communes has own service for the data
communes = [
    HealtCheckTestAreaData(
        name='międzychodzki',
        teryt='2403011',
        lat=49.75167,
        lon=18.63988,
        expected_tags={'building': 'office'},
    ),
]

all_areas_data = counties + communes
