# google_sheets.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class GoogleSheetsStorage:
    def __init__(self, creds_json_path, sheet_name):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_json_path, scope)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open(sheet_name).sheet1

    def save_trade(self, trade):
        # trade should be a dict like: {'timestamp': ..., 'strategy': ..., 'profit': ..., 'details': ...}
        row = [trade.get('timestamp', ''),
               trade.get('strategy', ''),
               str(trade.get('profit', '')),
               trade.get('details', '')]
        self.sheet.append_row(row)

    def get_trade_history(self):
        return self.sheet.get_all_records()
