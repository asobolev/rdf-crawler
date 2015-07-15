import unittest
from tables.gdrive import GDrive


class TestGDrive(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_auth(self):
        credentials = "credentials.json"