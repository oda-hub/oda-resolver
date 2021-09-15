
import os
import requests
import pandas as pd
from requests.auth import HTTPBasicAuth
from astropy.time import Time

from tnr.resolvers import Resolver


class MAGICResolver(Resolver):

    def __init__(self):
        pass


    def resolve(self,name):
        if False:
            raise NotImplementedError
        else:
            return dict(
                    success=False,
                    exception="name %s unknown"%name,
                )
    

