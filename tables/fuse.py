from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef


class Fuser(object):
    
    @staticmethod
    def fuse(graph1, graph2):
        g = Graph()

        existing = [x[0] for x in g.namespaces()]

        namespaces = list(graph1.namespaces()) + list(graph2.namespaces())
        for namespace, prefix in namespaces:
            if namespace not in existing:
                g.namespace_manager.bind(namespace, prefix)

        g += graph1 + graph2

        return g

