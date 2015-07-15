import unittest
import json

from tables.parser import Parser


class TestParser(unittest.TestCase):

    def setUp(self):
        datafile = "tests/data.json"

        with open(datafile, "r") as f:
            self.data = json.load(f)

    def tearDown(self):
        pass

    def test_parse_multiple(self):
        key = "DATA-2015-DEV"

        g = Parser.parse_multiple(key, self.data)

        # TODO add some RDF tests