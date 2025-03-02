from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
]

SERVICE_ACCOUNT_FILE = 'keys/receiptautomationaettua-2e51520e8323.json'
SPREADSHEET_ID = "18iAm74cWxhvfPZSxaP9a0UTD8_5v5kV-wXnEwqPaVTw"

class Sheets:

    def __init__(self):
        #Client Auth
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        self.service = build('sheets', 'v4', credentials=creds)
        self.sheet_metadata = self.service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
        
        self.lastRow: int = None

    def addEntry(self, data: dict):

        request = {
            "requests": [
                {
                    "updateCells": {
                        "range": {
                            "sheetId": 0,
                            "startRowIndex": self.getLastRow(),
                            "endRowIndex": self.getLastRow() + 1,
                            "startColumnIndex": 0,
                            "endColumnIndex": len(data.values())
                        },
                        "rows": [
                            {
                                "values": fullEntry(data)
                            }
                        ],
                        "fields": "userEnteredValue"
                    }
                }
            ]
        }

        self.batch(request, SPREADSHEET_ID)

    def batch(self, request: dict, spreadID: int = 0):
        response = self.service.spreadsheets().batchUpdate(
                spreadsheetId=spreadID,
                body=request
                ).execute()
        
        print(response)
    
    def getLastRow(self):
        if not self.lastRow:
            result = self.service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range="Folha1").execute()
            self.lastRow = len(result.get('values', []))

        return self.lastRow

def fullEntry(data: dict) -> list:
    return [{"userEnteredValue": {"stringValue": str(v)}} for v in data.values()]