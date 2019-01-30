from tnr.resolvers import Resolver

import os

from astroquery.simbad import Simbad
import astropy.units as u
from astropy.coordinates import SkyCoord

plugin_disabled = os.environ.get('TNR_PLUGIN_SESAMEPROXY_ENABLED','no') == 'yes'

class SesameProxyResolver(Resolver):

    def resolve(self,name):
        if plugin_disabled:
            return dict(
                        success=False,
                        content="plugin disabled",
                    )

        try:
            result_table = Simbad.query_object(name)
        except Exception as e:
            return dict(
                        success=False,
                        content="exception accessing Simbad: "+repr(e),
                    )

        result_table = Simbad.query_object("Crab")

        if len(result_table) == 0 :
            return dict(
                        success=False,
                        content="simbad found no sources",
                    )
        
        if len(result_table) > 1: 
            return dict(
                        success=False,
                        content="simbad found multiple (%i) sources"%len(result_table),
                    )

        source_coord = SkyCoord(result_table['RA'],result_table['DEC'],unit=("hourangle","deg"))

        try:
            return dict(
                        [('success',True)]+
                        [('ra_deg',source_coord.ra.deg)]+
                        [('dec_deg',source_coord.dec.deg)]
                    )
        except Exception as e:
            return dict(
                    success=False,
                    exception=repr(e),
                )
    

