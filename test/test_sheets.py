from src.sheets import Sheets

def test():
    print("Running test")

    sheet = Sheets()

    data = {i:i for i in range(12)}
    del data[0]

    data["link"] = "https://docs.google.com/spreadsheets/d/1j0ZOvi0m_EJNV5O7guHRjCb8o_x-YUirAtEIAGh1DT8/edit?gid=0#gid=0"

    sheet.addEntry(data)

    print("Test complete...")

if __name__ == "__main__":
    test()