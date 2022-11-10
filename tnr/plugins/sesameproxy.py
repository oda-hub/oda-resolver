import os
import rdflib

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
            source_coord = SkyCoord(result_table['RA'],result_table['DEC'],unit=("hourangle","deg"))
            object_type = str(result_table[0]['OTYPE']).strip()
            main_id = str(result_table[0]['MAIN_ID']).strip()
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
                        [('main_id', main_id)]+
                        [('oids', source_ids_list)]+
                        [('otype_links', links)]+
                        [('otype_description', ivoa_object_description)]
                    )
        except Exception as e:
            return dict(
                    success=False,
                    exception=repr(e),
                )
    

