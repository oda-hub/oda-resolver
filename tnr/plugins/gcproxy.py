from tnr.resolvers import Resolver

import requests
from requests.auth import HTTPBasicAuth

class GCProxyResolver(Resolver):
    def resolve(self,name):
        return requests.get("http://134.158.75.161/cat/grbcatalog/api/v1.1/"+name,auth=HTTPBasicAuth("integral",open("secret").read().strip())).json()

