import pytest
import os

import tnr.service

__this_dir__ = os.path.join(os.path.abspath(os.path.dirname(__file__)))


@pytest.fixture
def app():
    os.environ['POLAR_GRB_DATA_CSV'] = 'data/polar/polar_grbs.csv'
    os.environ['TNR_PLUGIN_GWPROXY_ENABLED'] = 'yes'
    os.environ['IVOA_RDF_DATA'] = 'data/ivoa_rdf_data/object-type.ttl'
    app = tnr.service.app
    return app
