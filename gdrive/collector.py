import json
import gspread

from oauth2client.client import SignedJwtAssertionCredentials


json_key = json.load(open('Sirota-lab-f122faf9d28f.json'))
scope = ['https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(
    json_key['client_email'],
    bytes(json_key['private_key'], 'utf-8'),
    scope
)

gc = gspread.authorize(credentials)

f = gc.open("DATA-2015-DEV")

animal_sheet = f.worksheet("Animal")
foo = animal_sheet.get_all_values()  # matrix of values

