from tnr.resolvers import Resolver

import os
import requests
from requests.auth import HTTPBasicAuth

class GCProxyResolver(Resolver):

    @property
    def secret(self):
        return open(os.environ.get("GCPROXY_SECRET_LOCATION","secret")).read().strip()

    def resolve(self,name):
        return requests.get("http://134.158.75.161/cat/grbcatalog/api/v1.1/"+name,
                            auth=HTTPBasicAuth("integral", self.secret),
                        ).json()

