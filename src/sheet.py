import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

SCOPE = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
    ]

CLIENT_KEY = 'verySecureKeys/receiptautomationaettua-c23fe4274e0f.json'

class Sheets:
    def __init__(self):
        #Client Auth
        creds = ServiceAccountCredentials.from_json_keyfile_name(CLIENT_KEY, SCOPE)
        self.client = gspread.authorize(creds)

    # Create entry

    # Add header

    #

