import requests
from tnr.resolvers import Resolver
import os
from astropy.time import Time

plugin_enabled = os.environ.get('TNR_PLUGIN_GWPROXY_ENABLED','no') == 'yes'
resolveurl = "https://www.gw-openscience.org/eventapi/json/query/show?name-contains={name}"

class GWProxyResolver(Resolver):
        
    def resolve(self, name):
        if not plugin_enabled:
            return {'success': False,
                    'content': "plugin disabled",
                    }
            
        r=requests.get(resolveurl.format(name=name))

        if r.status_code != 200:
            return {'success': False,
                    'content': str(r.text),
                    }

        try:
            d=r.json()
            if d['events'] == {}:
                return {'success': False}
            
            for ev in d['events']:
                if d['events'][ev]['catalog.shortName'] in ['GWTC-1-confident', 'GWTC-2']:
                    event = d['events'][ev]
            
            return {
                'success': True,
                'raw': d,
                'events': d['events'],
                'mjd': Time(event['GPS'], format='gps').mjd,
                'utc': Time(event['GPS'], format='gps').isot,
                'duration': 5 # NOTE hardcoded default duration
            }
        except Exception as e:
            return {'success': False,
                    'exception': repr(e),
                    'raw_response': r.text,
                    }
