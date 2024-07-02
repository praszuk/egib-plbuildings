from backend.areas.models import HealtCheckTestAreaData


counties = [
    # 02 – "dolnośląskie"
    HealtCheckTestAreaData(
        name='głogowski',
        teryt='0203',
        lat=51.66531,
        lon=16.07441,
        expected_tags={'building': 'office'},
    ),
    HealtCheckTestAreaData(
        name='górowski',
        teryt='0204',
        lat=51.66517,
        lon=16.54239,
        expected_tags={'building': 'office'},
    ),
    HealtCheckTestAreaData(
        name='jaworski',
        teryt='0205',
        lat=51.05149,
        lon=16.20572,
        expected_tags={'building': 'office'},
    ),
    # 04 – "kujawsko-pomorskie"
    HealtCheckTestAreaData(
        name='lipnowski',
        teryt='0408',
        lat=52.84022,
        lon=19.17100,
        expected_tags={'building': 'office'},
    ),
    HealtCheckTestAreaData(
        name='radziejowski',
        teryt='0411',
        lat=52.62279,
        lon=18.52755,
        expected_tags={'building': 'office'},
    ),
    HealtCheckTestAreaData(
        name='rypiński',
        teryt='0412',
        lat=53.06290,
        lon=19.41146,
        expected_tags={'building': 'office'},
    ),
    HealtCheckTestAreaData(
        name='wąbrzeski',
        teryt='0417',
        lat=53.27565,
        lon=18.94620,
        expected_tags={'building': 'office'},
    ),
    HealtCheckTestAreaData(  # gmina Kowal
        name='włocławski',
        teryt='0418',
        lat=52.53273,
        lon=19.15530,
        expected_tags={'building': 'office'},
    ),
    # 06 – "lubelskie"
    HealtCheckTestAreaData(  # gmina Konstantynów
        name='bialski',
        teryt='0601',
        lat=52.20697,
        lon=23.08980,
        expected_tags={'building': 'yes'},  # empty
    ),
    HealtCheckTestAreaData(  # gmina Tarnogród
        name='biłgorajski',
        teryt='0602',
        lat=50.35931,
        lon=22.74292,
        expected_tags={'building': 'yes'},  # empty
    ),
    HealtCheckTestAreaData(
        name='hrubieszowski',
        teryt='0604',
        lat=50.80644,
        lon=23.88755,
        expected_tags={'building': 'office'},
    ),
    HealtCheckTestAreaData(
        name='janowski',
        teryt='0605',
        lat=50.70261,
        lon=22.41879,
        expected_tags={'building': 'office'},
    ),
    HealtCheckTestAreaData(
        name='krasnostawski',
        teryt='0606',
        lat=50.98220,
        lon=23.16148,
        expected_tags={'building': 'office'},
    ),
    HealtCheckTestAreaData(
        name='lubartowski',
        teryt='0608',
        lat=51.46557,
        lon=22.60975,
        expected_tags={'building': 'office'},
    ),
    HealtCheckTestAreaData(
        name='lubelski',
        teryt='0609',
        lat=50.44727,
        lon=23.41521,
        expected_tags={'building': 'office'},
    ),
    HealtCheckTestAreaData(
        name='łęczyński',
        teryt='0610',
        lat=51.29881,
        lon=22.88610,
        expected_tags={'building': 'office'},
    ),
    HealtCheckTestAreaData(
        name='łukowski',
        teryt='0611',
        lat=51.93003,
        lon=22.37824,
        expected_tags={'building': 'office'},
    ),
    HealtCheckTestAreaData(
        name='opolski',
        teryt='0612',
        lat=51.14870,
        lon=21.97042,
        expected_tags={'building': 'office'},
    ),
    HealtCheckTestAreaData(
        name='parczewski',
        teryt='0613',
        lat=51.63985,
        lon=22.89702,
        expected_tags={'building': 'office'},
    ),
    HealtCheckTestAreaData(
        name='puławski',
        teryt='0614',
        lat=51.41358,
        lon=21.96274,
        expected_tags={'building': 'office'},
    ),
    HealtCheckTestAreaData(
        name='radzyński',
        teryt='0615',
        lat=51.78286,
        lon=22.61551,
        expected_tags={'building': 'office'},
    ),
    HealtCheckTestAreaData(
        name='rycki',
        teryt='0616',
        lat=51.62444,
        lon=21.92719,
        expected_tags={'building': 'office'},
    ),
    HealtCheckTestAreaData(
        name='świdnicki',
        teryt='0617',
        lat=51.21957,
        lon=22.69944,
        expected_tags={'building': 'office'},
    ),
    HealtCheckTestAreaData(
        name='tomaszowski',
        teryt='0618',
        lat=50.44727,
        lon=23.41522,
        expected_tags={'building': 'office'},
    ),
    HealtCheckTestAreaData(
        name='włodawski',
        teryt='0619',
        lat=51.54789,
        lon=23.55561,
        expected_tags={'building': 'office'},
    ),
    HealtCheckTestAreaData(
        name='miasto Biała Podlaska',
        teryt='0661',
        lat=52.03496,
        lon=23.12653,
        expected_tags={'building': 'yes'},  # empty,
    ),
    HealtCheckTestAreaData(
        name='miasto Chełm',
        teryt='0662',
        lat=51.13321,
        lon=23.49482,
        expected_tags={'building': 'yes', 'building:levels': '4'},
    ),
    HealtCheckTestAreaData(
        name='miasto Zamość',
        teryt='0664',
        lat=50.72284,
        lon=23.26218,
        expected_tags={'building': 'office'},
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
