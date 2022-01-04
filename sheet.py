import os.path
from typing import ValuesView
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
spreadsheet_id = 'your sheet id'

def getCreds():
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # if os.path.exists('token.json'):
    #     creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # # If there are no (valid) credentials available, let the user log in.
    # if not creds or not creds.valid:
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         flow = InstalledAppFlow.from_client_secrets_file(
    #             'credentials.json', SCOPES)
    #         creds = flow.run_local_server(port=0)
    #     # Save the credentials for the next run
    #     with open('token.json', 'w') as token:
    #         token.write(creds.to_json())
    return creds

def getUserSheet():
    creds = getCreds()
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range='User!A2:E').execute()
    values = result.get('values', [])
    return values

def getTransactionSheet():
    creds = getCreds()
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range='Transaction!A2:G').execute()
    values = result.get('values', [])
    return values

def addUserSheet(id,password,money,type,lineID):
    creds = getCreds()
    service = build('sheets', 'v4', credentials=creds)
    range_ = 'User!A2:E'
    value_input_option = 'RAW'
    insert_data_option = 'INSERT_ROWS'
    data = [[id,password,money,type,lineID]]
    request = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=range_, 
        valueInputOption=value_input_option, 
        insertDataOption=insert_data_option, body={"values":data})
    response = request.execute()
    return response

def addTransactionSheet(id,in_,out_,cretification,recode,money,date):
    creds = getCreds()
    service = build('sheets', 'v4', credentials=creds)
    range_ = 'Transaction!A2:G'
    value_input_option = 'RAW'
    insert_data_option = 'INSERT_ROWS'
    data = [[id,in_,out_,cretification,recode,money,date]]
    request = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=range_, 
        valueInputOption=value_input_option, 
        insertDataOption=insert_data_option, body={"values":data})
    response = request.execute()
    return response


def updateSheetValue(sheetName,column,number,newValue):
    creds = getCreds()
    service = build('sheets', 'v4', credentials=creds)
    range_ = sheetName+'!'+str(column)+str(number)
    value_input_option = 'USER_ENTERED'
    body = [[newValue]]
    request = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, 
        range=range_,valueInputOption=value_input_option,
        body={"values":body}).execute()
    return request