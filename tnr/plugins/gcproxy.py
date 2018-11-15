from tnr.resolvers import Resolver

import os
import requests
from requests.auth import HTTPBasicAuth

class GCProxyResolver(Resolver):

    @property
    def secret(self):
        return open(os.environ.get("GCPROXY_SECRET_LOCATION","/secret")).read().strip()

    def resolve(self,name):
        r=requests.get("http://134.158.75.161/cat/grbcatalog/api/v1.1/"+name,
                            auth=HTTPBasicAuth("integral", self.secret),
                        )

        if r.status_code != 200:
            return dict(
                        success=True,
                        content=r.content,
                    )

        try:
            d=r.json()
            return dict(
                        [('success',True)]+
                        [('raw',d)]+
                        d['events'][0].items()+
                        [('mjd',d['events'][0]['ijd']+51544.0)]
                    )
        except Exception as e:
            return dict(
                    success=False,
                    exception=repr(e),
                    raw_response=r.content,
                )
    

