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

# Default parser should be using EGiB 1.6 XSD names
