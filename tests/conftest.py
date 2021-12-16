import pytest
import os
import tnr.service 

@pytest.fixture
def app():
    os.environ['POLAR_GRB_DATA_CSV'] = 'data/polar/polar_grbs.csv'
    os.environ['TNR_PLUGIN_GWPROXY_ENABLED'] = 'yes'
    app = tnr.service.app
    return app
