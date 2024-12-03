from IPython import get_ipython  # noqa

ipython = get_ipython()
ipython.run_line_magic('load_ext', 'autoreload')
ipython.run_line_magic('autoreload', '2')

# Predefined imports
from backend.models.building import Building  # noqa
