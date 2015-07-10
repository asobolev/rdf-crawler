import json
import gspread

from oauth2client.client import SignedJwtAssertionCredentials
from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import DC, FOAF


class Parser(object):
    """
    Class that downloads data from a remote Google Table file and parses it
    to RDF.
    """
    base_ont = "../base.owl"
    custom_ont = "../custom.owl"

    owl_cls = 'http://www.w3.org/2002/07/owl#Class'

    scope = ['https://spreadsheets.google.com/feeds']

    def __init__(self, path_to_credentials, filename):
        self.credentials = path_to_credentials
        self.filename = filename
        self.f = None

    def connect(self):
        json_key = json.load(open(self.credentials))

        credentials = SignedJwtAssertionCredentials(
            json_key['client_email'],
            bytes(json_key['private_key'], 'utf-8'),
            Parser.scope
        )

        gc = gspread.authorize(credentials)
        self.f = gc.open("DATA-2015-DEV")

    def parse(self):

        # parse base ontology
        g = Graph()
        g.parse(Parser.base_ont, format="application/rdf+xml")

        cls_triples = g.triples((None, RDF.type, URIRef(Parser.owl_cls)))
        cls_list = [s for s, p, o in cls_triples if not type(s) == BNode]
        cls_names = [x.split("#")[1] for x in cls_list]

        for sheet in self.f.worksheets():
            if sheet.title in cls_names:
                # class is found in ontology
                pass

            else:
                # should be saved in custom ontology
                pass

            # data = sheet.get_all_values()  # matrix of values


class Fuser(object):
    pass