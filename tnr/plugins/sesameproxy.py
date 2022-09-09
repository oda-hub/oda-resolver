import requests

from tnr.resolvers import Resolver

import os
import rdflib

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
            Simbad.add_votable_fields("otype")
            result_table = Simbad.query_object(name)
        except Exception as e:
            return dict(
                        success=False,
                        content="exception accessing Simbad: "+repr(e),
                    )

        if result_table is None or len(result_table) == 0:
            return dict(
                        success=False,
                        content="simbad found no sources",
                    )
        
        if len(result_table) > 1: 
            return dict(
                        success=False,
                        content="simbad found multiple (%i) sources"%len(result_table),
                    )

        try:
            source_coord = SkyCoord(result_table['RA'],result_table['DEC'],unit=("hourangle","deg"))
            object_type = str(result_table[0]['OTYPE']).strip()
            # query rdf ivoa data
            ivoa_ttl_path = os.environ.get("IVOA_RDF_DATA", None)
            object_links = None
            if ivoa_ttl_path is not None:
                links = None
                G = rdflib.Graph()
                G.parse(ivoa_ttl_path, format="ttl")
                label_matches_list = list(G[:rdflib.URIRef('http://www.w3.org/2000/01/rdf-schema#label'):rdflib.Literal(object_type)])
                if len(label_matches_list) == 1:
                    exact_matches_links = list(G[label_matches_list[0]:rdflib.URIRef('http://www.w3.org/2000/01/rdf-schema#exactMatch')])
                    for link in exact_matches_links:
                        if links is None:
                            links = []
                        links.append(str(link))
                if links is not None:
                    object_links = ",".join(links)

        except ValueError:
            return dict(
                        success=False,
                        content="simbad found but no coordinates "+repr(result_table),
                    )
        try:
            object_ids_table = Simbad.query_objectids(name)
            source_ids_list = object_ids_table['ID'].tolist()
        except ValueError:
            source_ids_list = []

        try:
            return dict(
                        [('success',True)]+
                        [('ra_deg',source_coord.ra.deg[0])]+
                        [('dec_deg',source_coord.dec.deg[0])]+
                        [('origin',result_table['COO_BIBCODE'][0])]+
                        [('otype', object_type)]+
                        [('oids', source_ids_list)]+
                        [('otype_links', object_links)]
                    )
        except Exception as e:
            return dict(
                    success=False,
                    exception=repr(e),
                )
    

