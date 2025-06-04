import os
import rdflib
import numpy as np

from tnr.resolvers import Resolver
from astroquery.simbad import Simbad
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
            ra = result_table['ra'] if 'ra' in result_table.keys() else result_table['RA']
            dec = result_table['dec'] if 'dec' in result_table.keys() else result_table['DEC']
            source_coord = SkyCoord(ra, dec, unit=("hourangle","deg"))
            otype = result_table[0]['otype'] if 'otype' in result_table[0].keys() else result_table[0]['OTYPE']
            object_type = str(otype).strip()
            mid = result_table[0]['main_id'] if 'main_id' in result_table[0].keys() else result_table[0]['MAIN_ID']
            main_id = str(mid).strip()
            # query rdf ivoa data
            ivoa_ttl_path = os.environ.get("IVOA_RDF_DATA", None)
            links = []
            ivoa_object_description = []
            if ivoa_ttl_path is not None:
                G = rdflib.Graph()
                G.parse(ivoa_ttl_path, format="ttl")

                for label_match in G[:rdflib.URIRef('http://www.w3.org/2000/01/rdf-schema#label'):rdflib.Literal(object_type)]:
                    ivoa_object_description.extend([str(link) for link in G[label_match:rdflib.URIRef(
                        'http://www.w3.org/2000/01/rdf-schema#comment')]])
                    links.extend([str(link) for link in G[label_match:rdflib.URIRef(
                        'http://www.w3.org/2004/02/skos/core#exactMatch')]])

        except ValueError:
            return dict(
                        success=False,
                        content="simbad found but no coordinates " + repr(result_table)
                    )
        try:
            object_ids_table = Simbad.query_objectids(name)
            oidt = object_ids_table['id'] if 'id' in object_ids_table.keys() else object_ids_table['ID']
            source_ids_list = oidt.tolist()
        except ValueError:
            source_ids_list = []

        try:
            coo = result_table['COO_BIBCODE'][0] if 'COO_BIBCODE' in result_table.keys() else result_table['coo_bibcode'][0]
            rsp = {'success':True,
                   'origin':coo,
                   'otype': object_type,
                   'main_id': main_id,
                   'oids': source_ids_list,
                   'otype_links': links,
                   'otype_description': ivoa_object_description}
            if ~np.isnan(source_coord.ra.deg[0]):
                rsp['ra_deg'] = source_coord.ra.deg[0]
            if ~np.isnan(source_coord.dec.deg[0]):
                rsp['dec_deg'] = source_coord.dec.deg[0]
            return rsp
                    
        except Exception as e:
            return dict(
                    success=False,
                    exception=repr(e),
                )
    

