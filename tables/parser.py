from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import XSD, OWL, DC


class Parser(object):
    """
    Class that parses 2D sheet data to RDF.
    """

    # ontology statics
    base_ont = "../base.owl"
    custom_ont = "../custom.owl"
    owl_cls = 'http://www.w3.org/2002/07/owl#Class'

    # spreadsheet parsing attrs
    exclude = ('HOWTO',)

    ignore = 'ignore'
    prefix = 'prefix'
    reverse = 'hasReverse'
    relation = 'relation'
    alias = 'alias'
    header = 'header'

    @staticmethod
    def parse_single(key, title, data):

        def parse_indexes():
            idx_dict = {}
            tech_col = [x[0] for x in data]
            for name in (P.ignore, P.prefix, P.reverse, P.relation, P.alias, P.header):
                try:
                    idx_dict[name] = tech_col.index(name)
                except ValueError:
                    raise ValueError("Sheet %s does not have a proper %s record" % (title, name))

            idx_dict['id'] = data[idx_dict[P.header]].index('id')
            return idx_dict

        def build_obj_id(prefix, uid):
            # like "DATA-2015:http://foo.com/bar#Animal:12"
            return ":".join([key, prefix, uid])

        def parse_row(row):
            obj_id = build_obj_id(rdf_type, row[idx['id']])

            g.add((URIRef(obj_id), RDF.type, URIRef(rdf_type)))

            for j, value in enumerate(row):
                try:
                    if j <= idx['id'] or bool(int(data[idx[P.ignore]][j])):
                        continue  # ignore technical info
                except ValueError:
                    raise ValueError("Sheet %s does not have a proper 'ignore' at %s position" % (title, str(j + 1)))

                if len(value) == 0:
                    continue  # empty value

                predicate = "".join([data[idx[P.prefix]][j], data[idx[P.header]][j]])

                if len(data[idx[P.relation]][j]) > 0:
                    local_id = value.split('(')[1].split(')')[0]
                    rel_id = build_obj_id(data[idx[P.relation]][j], local_id)
                    g.add((URIRef(obj_id), URIRef(predicate), URIRef(rel_id)))

                else:
                    g.add((URIRef(obj_id), URIRef(predicate), Literal(value)))

        g = Graph()

        P = Parser
        idx = parse_indexes()

        # this is like http://foo.com/bar#Animal
        rdf_type = data[idx[P.prefix]][idx['id']]

        for row in data[idx[P.header] + 1:]:
            if len(row[idx['id']]) > 0 and any(row[idx['id'] + 1:]):
                parse_row(row)

        return g

    @staticmethod
    def parse_multiple(key, sheets_list, verbose=False):
        """
        Parses a remote file with a given filename. Returns parsed graph.

        # ontology-related stuff, to be used later
        g.parse(Parser.base_ont, format="application/rdf+xml")

        cls_triples = g.triples((None, RDF.type, URIRef(Parser.owl_cls)))
        cls_list = [s for s, p, o in cls_triples if not type(s) == BNode]
        cls_names = [x.split("#")[1] for x in cls_list]
        """
        g = Graph()

        for title, sheet in sheets_list.items():
            if title not in Parser.exclude:
                g += Parser.parse_single(key, title, sheet)

                if verbose:
                    print("Sheet %s parsed" % title)

        return g