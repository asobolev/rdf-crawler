import json
import gspread

from oauth2client.client import SignedJwtAssertionCredentials


class GDrive(object):
    """
    This class is used to fetch data from Google Drive spreadsheets.
    """
    scope = ['https://spreadsheets.google.com/feeds']

    def __init__(self, path_to_credentials, verbose=False):
        self.credentials = path_to_credentials
        self.verbose = verbose

    def authenticate(self):
        json_key = json.load(open(self.credentials))

        import ipdb
        ipdb.set_trace()

        credentials = SignedJwtAssertionCredentials(
            json_key['client_email'],
            #bytes(json_key['private_key'], 'utf-8'),
            bytes(json_key['private_key']),
            GDrive.scope
        )

        return gspread.authorize(credentials)

    def fetch(self, filename):
        """
        Downloads all sheets from a file with a given filename.
         Returns a dict of 2D lists with sheet names as keys.
        """
        sheets_list = {}

        f = self.authenticate().open(filename)
        for sheet in f.worksheets():
            sheets_list[sheet.title] = sheet.get_all_values()

            if self.verbose:
                print("Sheet %s downloaded." % sheet.title)

        return sheets_list