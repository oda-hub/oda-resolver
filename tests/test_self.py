import pytest
from flask import url_for

def test_unknown(client):

    r=client.get(url_for('resolve',name='xx'))

    assert r.status_code == 200
    print(r.json)

    assert r.json['polargrbs.PolarResolver']['success'] == False
    assert r.json['gcproxy.GCProxyResolver']['success'] == False

def test_known(client):

    r=client.get(url_for('resolve',name='GRB170114B'))

    assert r.status_code == 200
    print(r.json)

    assert r.json['polargrbs.PolarResolver']['success'] == True
    assert r.json['gcproxy.GCProxyResolver']['success'] == True

def test_known(client):

    r=client.get(url_for('resolve',name='GRB170114B'))

    assert r.status_code == 200
    print(r.json)

    assert r.json['polargrbs.PolarResolver']['success'] == True
    assert r.json['gcproxy.GCProxyResolver']['success'] == True

def test_known_timespan(client):

    r=client.get(url_for('timespan_byname',name='GRB170114B'))

    assert r.status_code == 200
    print(r.json)

    assert r.json['success'] == True

def test_unknown_timespan(client):

    r=client.get(url_for('timespan_byname',name='GRB170114X'))

    assert r.status_code == 200
    print(r.json)

    assert r.json['success'] == False

def test_sesame(client):

    r=client.get(url_for('resolve',name='Crab'))

    print(r)

    assert r.status_code == 200
    print(r.json)

    assert r.json['success'] == True
