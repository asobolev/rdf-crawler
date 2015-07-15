import unittest
from tables.gdrive import GDrive


class TestGDrive(unittest.TestCase):

    def setUp(self):
        credentials = "tests/credentials.json"

        self.gd = GDrive(credentials)

    def tearDown(self):
        pass

    def test_auth(self):
        client = self.gd.authenticate()

        assert client.auth.access_token is not None

    def test_fetch(self):
        filename = "DATA-2015-DEV"

        data = self.gd.fetch(filename)

        for name in ('Animal', 'Experiment', 'Electrode'):
            assert name in data.keys()
            assert type(data[name]) == list
            assert len(data[name]) > 0
            assert type(data[name][0]) == list