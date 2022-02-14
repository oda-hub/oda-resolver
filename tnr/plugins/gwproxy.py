import requests
from tnr.resolvers import Resolver
import os
from astropy.time import Time

plugin_enabled = os.environ.get('TNR_PLUGIN_GWPROXY_ENABLED','no') == 'yes'
resolveurl = "https://www.gw-openscience.org/eventapi/json/query/show?name-contains={name}"
used_catalogs = ['GWTC-1-confident', 'GWTC-2', 'GWTC-3-confident']

class GWProxyResolver(Resolver):
        
    def resolve(self, name):
        if not plugin_enabled:
            return {'success': False,
                    'content': "plugin disabled",
                    }
        try:
            
            r=requests.get(resolveurl.format(name=name))

            if r.status_code != 200:
                return {'success': False,
                        'content': str(r.text),
                        }

            d=r.json()
            if d['events'] == {}:
                return {'success': False}
            
            for ev in d['events']:
                if d['events'][ev]['catalog.shortName'] in used_catalogs:
                    event = d['events'][ev]
            
            return {
                'success': True,
                'raw': d,
                'events': d['events'],
                'mjd': Time(event['GPS'], format='gps', scale='utc').mjd,
                'utc': Time(event['GPS'], format='gps', scale='utc').isot,
                'duration': 5 # NOTE hardcoded default duration
            }
        except Exception as e:
            return {'success': False,
                    'exception': repr(e),
                    'raw_response': r.text,
                    }
