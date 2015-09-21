from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef


class Fuser(object):
    
    @staticmethod
    def fuse(graph1, graph2):
        return graph1 + graph2

