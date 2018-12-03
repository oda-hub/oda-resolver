from tnr.resolvers import Resolver

import os
import requests
from requests.auth import HTTPBasicAuth

plugin_disabled = os.environ.get('TNR_PLUGIN_GCPROXY_ENABLED','yes') == 'yes'

class GCProxyResolver(Resolver):

    @property
    def secret(self):
        return open(os.environ.get("GCPROXY_SECRET_LOCATION","/secret")).read().strip()

    def resolve(self,name):
        if plugin_disabled:
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
                        content=r.content,
                    )

        try:
            d=r.json()
            return dict(
                        [('success',True)]+
                        [('raw',d)]+
                        d['events'][0].items()+
                        [('mjd',d['events'][0]['ijd']+51544.0)]+
                        [('duration',d['duration'])]
                    )
        except Exception as e:
            return dict(
                    success=False,
                    exception=repr(e),
                    raw_response=r.content,
                )
    

