
import os
import requests
import pandas as pd
from requests.auth import HTTPBasicAuth
from astropy.time import Time

from tnr.resolvers import Resolver


class PolarResolver(Resolver):

    def __init__(self):
        try:
            self.read_grbs()
        except Exception as e:
            print("failed to read polar GRBs:", e)
            self.polar_grbs=dict()


    def resolve(self,name):
        if True:
            raise NotImplementedError
        else:
            return dict(
                    success=False,
                    exception="name %s unknown"%name,
                )
    

