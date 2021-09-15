from tnr.resolvers import Resolver

import os
import requests
from requests.auth import HTTPBasicAuth

plugin_enabled = os.environ.get('TNR_PLUGIN_GCPROXY_ENABLED','no') == 'yes'

class GCProxyResolver(Resolver):

    @property
    def secret(self):
        return open(os.environ.get("GCPROXY_SECRET_LOCATION","/secret")).read().strip()

    def resolve(self,name):
        if not plugin_enabled:
            return dict(
                        success=False,
                        content="plugin disabled",
                    )

        r=requests.get("http://134.158.75.161/cat/grbcatalog/api/v1.1/"+name,
                            auth=HTTPBasicAuth("integral", self.secret),
                        )

        if r.status_code != 200:
            return dict(
                        success=False,
                        content=str(r.content),
                    )

        try:
            d=r.json()
            if str(d['ijd']) == "nan":
                return dict(
                        success=False,
                        raw_response=r.content,
                    )
            return dict(
                        [('success',True)]+
                        [('raw',d)]+
                        [('events',d['events'])]+
                        [('mjd',d['ijd']+51544.0)]+
                        [('duration',d['duration'])]
                    )
        except Exception as e:
            return dict(
                    success=False,
                    exception=repr(e),
                    raw_response=r.content,
                )
    

