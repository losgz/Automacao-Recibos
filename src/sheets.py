from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
]

SERVICE_ACCOUNT_FILE = 'keys/receiptautomationaettua-2e51520e8323.json'
SPREADSHEET_ID = "1yT758a92j-Bge0dNhVGqP-Y0KgIcoupMPDI5TOHgZZg"

class Sheets:

    def __init__(self):
        #Client Auth
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        self.service = build('sheets', 'v4', credentials=creds)
        self.lastRow: int = None

    def addEntry(self, data: dict):

        if not data:
            print("Null data")
            return
        
        if len(data.keys()) != 12:
            print("Bad data")
            return

        request = {
            "requests": [
                { #Add content
                    "updateCells": {
                        "start": {
                            "sheetId": 0,
                            "rowIndex": self.getLastRow(),
                            "columnIndex": 0,
                        },
                        "rows": [
                            {
                                "values": fullEntry(data)
                            }
                        ],
                        "fields": "userEnteredValue, hyperlink"
                    }
                },
                { #Add checkboxes in the last 2 fields
                    'repeatCell': { 
                        'cell': {
                            'dataValidation': {
                                'condition': {
                                    'type': 'BOOLEAN'
                                }
                            }
                        },
                        "range": {
                            "sheetId": 0,
                            "startRowIndex": self.getLastRow(),
                            "endRowIndex": self.getLastRow() + 1,
                            "startColumnIndex": 10,
                            "endColumnIndex": 12
                        },
                        'fields': 'dataValidation'
                    }
                },
            ]
        }

        self.batch(request)
        self.lastRow += 1

    def batch(self, request: dict):
        response = self.service.spreadsheets().batchUpdate(
                spreadsheetId=SPREADSHEET_ID,
                body=request
                ).execute()
        
        print(response)
    
    def getLastRow(self):
        if not self.lastRow:
            result = self.service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range="Folha1").execute()
            self.lastRow = len(result.get('values', []))

        return self.lastRow

def fullEntry(data: dict) -> list:
    cellData = []
    for k, v in data.items():
        cell = None

        match k:
            case "link":
                cell = hyperlinkCell(str(v))
            case "paj" | "rac":
                cell = booleanCell(v)
            case _:
                cell = textCell(str(v))

        cellData.append(cell)

    return cellData

def textCell(text: str) -> dict:
    cell = userEnteredDataCell()
    cell["userEnteredValue"].setdefault("stringValue", text)
    return cell

def booleanCell(initialValue: bool) -> dict:
    cell = userEnteredDataCell()
    cell["userEnteredValue"].setdefault("boolValue", initialValue)
    return cell

def userEnteredDataCell() -> dict:
    return {
        "userEnteredValue": {
        }
    }

def hyperlinkCell(link: str) -> dict:
    return {    "hyperlink": link, 
                "userEnteredValue": {
                    "stringValue": link
                }
            }