import gspread
from oauth2client.service_account import ServiceAccountCredentials

def auth_gss_client(path, scopes):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(path,
                                                                   scopes)
    return gspread.authorize(credentials)
