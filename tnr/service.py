from flask import Flask, jsonify

def create_app():
    return Flask(__name__)

app = create_app()



import json
import requests
from astropy.time import Time
import numpy as np

from tnr.resolvers import RootResolver


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()

        try:
            return json.JSONEncoder.default(self, obj)
        except:
            print("problem serilizing",obj)
            raise

app.json_encoder = NumpyEncoder

@app.route('/')
def root():
    return jsonify(service='Transient Name Resolver',version=os.environ.get('CONTAINER_VERSION','unknown'))

@app.route('/api/v1.0/byname/<string:name>')
def resolve(name):
    root_resolver=RootResolver()

    return jsonify(root_resolver.resolve(name))

@app.route('/api/v1.1/byname/<string:name>')
def timespan_byname_v11(name):
    root_resolver=RootResolver()

    utcs={}
    mjds={}
    durations={}

    data=root_resolver.resolve(name)

    for resolver,event in data.items():
        utcs[resolver]=event.get('utc')
        mjds[resolver]=event.get('mjd')
        durations[resolver]=event.get('duration','100')

    
    if data.get('polargrbs.PolarResolver').get('exception',None) is None:
        utc=data.get('polargrbs.PolarResolver').get('utc')
        mjd=data.get('polargrbs.PolarResolver').get('mjd')
        duration=data.get('polargrbs.PolarResolver').get('duration')
        print("managed to polar",utc,mjd,duration)
    else:
        utc=data.get('gcproxy.GCProxyResolver').get('utc',None)
        mjd=data.get('gcproxy.GCProxyResolver').get('mjd',None)
        duration=data.get('gcproxy.GCProxyResolver').get('duration',None)
        print("resorted to gc",utc,mjd,duration)

    ra=None
    dec=None
    have_coordinates=False
    for resolver_name in 'sesameproxy.SesameProxyResolver', 'gcproxy.GCProxyResolver':
        resolver_data = data.get(resolver_name)
        if 'ra_deg' in resolver_data and 'dec_deg' in resolver_data:
            ra = resolver_data['ra_deg']
            dec = resolver_data['dec_deg']
            have_coordinates = True
            break
        

    if mjd is None or duration is None:
        return jsonify(
                    success=False,
                    comment='all resolvers failed',
                )
    else:
        viewing_range=dict(
            t1=dict(mjd=mjd-max(duration,1)/24./3600.),
            t2=dict(mjd=mjd+(duration+max(duration,1))/24./3600.),
        )

        viewing_range['t1']['utc'] = Time(viewing_range['t1']['mjd'], format='mjd', scale='utc').isot
        viewing_range['t2']['utc'] = Time(viewing_range['t2']['mjd'], format='mjd', scale='utc').isot

        return jsonify(dict(
                    success=True,
                    utcs=utcs,
                    mjds=mjds,
                    durations=durations,
                    utc=utc,
                    mjd=mjd,
                    duration=duration,
                    view=viewing_range,
                    ra=ra,
                    dec=dec,
                    have_coordinates=have_coordinates,
                ))


@app.route('/api/v1.0/timespan/byname/<string:name>')
def timespan_byname(name):
    root_resolver=RootResolver()

    utcs={}
    mjds={}
    durations={}

    data=root_resolver.resolve(name)

    for resolver,event in data.items():
        utcs[resolver]=event.get('utc')
        mjds[resolver]=event.get('mjd')
        durations[resolver]=event.get('duration','100')

    
    if data.get('polargrbs.PolarResolver').get('exception',None) is None:
        utc=data.get('polargrbs.PolarResolver').get('utc')
        mjd=data.get('polargrbs.PolarResolver').get('mjd')
        duration=data.get('polargrbs.PolarResolver').get('duration')
        print("managed to polar",utc,mjd,duration)
    else:
        utc=data.get('gcproxy.GCProxyResolver').get('utc',None)
        mjd=data.get('gcproxy.GCProxyResolver').get('mjd',None)
        duration=data.get('gcproxy.GCProxyResolver').get('duration',None)
        print("resorted to gc",utc,mjd,duration)

    ra=None
    dec=None
    have_coordinates=False
    for resolver_name in 'sesameproxy.SesameProxyResolver', 'gcproxy.GCProxyResolver':
        resolver_data = data.get(resolver_name)
        if 'ra_deg' in resolver_data and 'dec_deg' in resolver_data:
            ra = resolver_data['ra_deg']
            dec = resolver_data['dec_deg']
            have_coordinates = True
            break
        

    if mjd is None or duration is None:
        return jsonify(
                    success=False,
                    comment='all resolvers failed',
                )
    else:
        viewing_range=dict(
            t1=dict(mjd=mjd-max(duration,1)/24./3600.),
            t2=dict(mjd=mjd+(duration+max(duration,1))/24./3600.),
        )

        viewing_range['t1']['utc'] = Time(viewing_range['t1']['mjd'], format='mjd', scale='utc').isot
        viewing_range['t2']['utc'] = Time(viewing_range['t2']['mjd'], format='mjd', scale='utc').isot

        return jsonify(dict(
                    success=True,
                    utcs=utcs,
                    mjds=mjds,
                    durations=durations,
                    utc=utc,
                    mjd=mjd,
                    duration=duration,
                    view=viewing_range,
                    ra=ra,
                    dec=dec,
                    have_coordinates=have_coordinates,
                ))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
