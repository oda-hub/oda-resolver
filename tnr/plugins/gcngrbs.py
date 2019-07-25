
import os
import time
import requests
import pandas as pd
from requests.auth import HTTPBasicAuth
from astropy.time import Time

from tnr.resolvers import Resolver


def get_gcn_grbs(prefix="swift"):
    page = requests.get("https://gcn.gsfc.nasa.gov/"+prefix+"_grbs.html")

    d=pd.read_html(page.content)[0]

    return d.drop([1,d.index.max()])

    
    
def extract_time(d):
    date=None
    for g, date_field in ('GRB/TRIGGER', 'Date yy/mm/dd'), ('TRIGGER', 'Date'):
        try:
            date = d[g][date_field]
        except Exception as e:
            print("failed to get date as", date_field)

    if date is None:
        raise Exception("failed to extract date field, available", d.columns)
        
    
    for g, time_field in ('GRB/TRIGGER', 'Time UT'), ('TRIGGER', 'Time UT'):
        try:
            time_ut = d[g][time_field]
        except Exception as e:
            print("failed to get date as", time_field)
    
    d['isotime'] = "20"+date.str.replace("/","-")+"T"+ time_ut   
    
    d=d[time_ut.notnull()]
    d=d[~d['isotime'].str.contains('SWIFT')]
        
    t=Time(list(d['isotime']), format="isot", scale="utc")
    d['mjd']=t.mjd
    return d


cache=dict()

class GCNGRBResolver(Resolver):

    @property
    def d(self):
        return cache

    def resolve(self,name):
        return dict(
                success=False,
                exception="name %s unknown"%name,
            )

    def load(self):
        for prefix in "swift", "fermi":
            if prefix in self.d:
                age = time.time() - self.d[prefix]['updated_at']
                if age < 60*5:
                    print("ready recent record for", prefix, "age", age)
                    continue
                else:
                    print("old record for", prefix, "age", age)
            else:
                print("no record yet for", prefix)

            d = get_gcn_grbs(prefix)
            d = extract_time(d)

            self.d[prefix] = dict(
                        updated_at = time.time(),
                        data = d,
                    )
    

    def bytime(self,t0,span_s):
        self.load()

        t0_mjd = Time(t0).mjd

        r = []
        
        for k,v in self.d.items():
            m = (v['data'].mjd - t0_mjd).abs() < span_s/24./3600.

            print("found in",k,len(m))
            
            for i,dr in v['data'][m].iterrows():
                r.append({ ("/".join([i for i in k if i!=""])): v 
                        for k,v in dict(dr).items()
                    })
        
                print
            
    
        return r
    

