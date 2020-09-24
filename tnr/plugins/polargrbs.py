
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

    def read_grbs(self):
        self.polar_grbs=dict([
                            (k,dict([
                                        [c,r.values[0]]
                                        for c,r in v.iteritems()
                                    ]))
                            for k,v in pd.read_csv(os.environ.get("POLAR_GRB_DATA_CSV"), engine='python').groupby("name")
                        ])


    def resolve(self,name):
        if name in self.polar_grbs:
            grb_data=self.polar_grbs.get(name)
            
            grb_data['mjd']=Time(grb_data['utc'],format="isot").mjd

            grb_data['success']=True
            return grb_data
        else:
            return dict(
                    success=False,
                    exception="name %s unknown"%name,
                )
    

