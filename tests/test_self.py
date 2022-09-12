import pytest
import requests
import logging
import os
import json

from flask import url_for

logger = logging.getLogger(__name__)

def test_unknown(client):

    r=client.get(url_for('resolve',name='xx'))

    assert r.status_code == 200
    print(r.json)

    assert r.json['polargrbs.PolarResolver']['success'] == False
    #assert r.json['gcproxy.GCProxyResolver']['success'] == False

def test_known(client):

    r=client.get(url_for('resolve',name='GRB170114B'))

    assert r.status_code == 200
    print(r.json)

    assert r.json['polargrbs.PolarResolver']['success'] == True
    #assert r.json['gcproxy.GCProxyResolver']['success'] == True

def test_known(client):

    r=client.get(url_for('resolve',name='GRB170114B'))

    assert r.status_code == 200
    print(r.json)

    assert r.json['polargrbs.PolarResolver']['success'] == True
    #assert r.json['gcproxy.GCProxyResolver']['success'] == True

def test_known_timespan(client):

    r=client.get(url_for('timespan_byname_v11',name='GRB170114B'))

    assert r.status_code == 200
    print(r.json)

    assert r.json['success'] == True

def test_known_timespan_coord(client):

    r=client.get(url_for('timespan_byname_v11',name='GRB120711A'))

    assert r.status_code == 200
    print(r.json)

    assert r.json['success'] == True

    assert r.json['have_coordinates'] == True
    assert 'ra' in r.json
    assert 'dec' in r.json

def test_unknown_timespan(client):

    r=client.get(url_for('timespan_byname_v11',name='GRB170114X'))

    assert r.status_code == 200
    print(r.json)

    assert r.json['success'] == False

def test_sesame(client):

    r=client.get(url_for('resolve',name='Crab'))

    print(r)

    assert r.status_code == 200
    print(r.json)

    assert r.json['sesameproxy.SesameProxyResolver']['success'] == True


def test_bytime(client):
    r=client.get(url_for('bytime',t0='2019-06-10T11:27:45',span=100))

    print(r)

    assert r.status_code == 200
    print(r.json)

    import time

    t0=time.time()
    print("repeating request")
    r=client.get(url_for('bytime',t0='2019-06-10T11:27:45',span=100))

    print(r)

    assert r.status_code == 200
    print(r.json)

    assert (time.time() - t0)<1
    
def test_gw(client):
    r=client.get(url_for('timespan_byname_v11',name='GW190412'))

    assert r.status_code == 200
    print(r.json)

    assert r.json['mjds']['gwproxy.GWProxyResolver'] is not None
    assert r.json['success'] == True
    assert r.json['success_time'] == True


@pytest.mark.parametrize('source_name', ['Crab', 'Mrk 421', 'aaaaaa'])
def test_byname_11(resolver_live_fixture, source_name):
    server = resolver_live_fixture

    c = requests.get(os.path.join(server, f"api/v1.1/byname/{source_name}"))

    jdata = c.json()

    logger.info('Json output content')
    logger.info(json.dumps(jdata, indent=4))

    if source_name != 'aaaaaa':
        assert jdata['success'] is True
        assert 'object_type' in jdata
        assert 'object_links' in jdata
    else:
        assert jdata['success'] is False
