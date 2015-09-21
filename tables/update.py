#!/usr/bin/python

from rdflib import Graph
from parser import Parser
from gdrive import GDrive
from fuse import Fuser

import os, sys


if __name__ == "__main__":
    """
    Usage:
    python tables/update.py tests/credentials.json /tmp/data.ttl

    Input args:

    1) credentials file path
    2) RDF file path with existing data
    """
    credentials = sys.argv[1]
    rdf_store = sys.argv[2]
    rdf_format = 'turtle'

    # existing
    graph1 = Graph()
    if not os.path.exists(rdf_store):
        os.mknod(rdf_store)

    graph1.parse(rdf_store, format=rdf_format)

    # fetched
    key = "DATA-2015-DEV"
    gd = GDrive(credentials)
    data = gd.fetch(key)

    graph2 = Parser.parse_multiple(key, data)
   
    merged = Fuser.fuse(graph1, graph2)
    merged.serialize(rdf_store, format=rdf_format)


