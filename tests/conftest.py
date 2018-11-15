import pytest

import tnr.service 

@pytest.fixture
def app():
    app = tnr.service.app
    return app
