from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import random

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
COHORT_SPREADSHEET_IDs = ['1jHFtzPV8dUBlOpoXgBwnoLqb1d27KHyUZKDTqBNpe_8', '19bQjw_RzInIgFoMdHylQqXi05bp5p59TEIvwPxzXf1o', '1y85fw3YI9JIzoQDya0WewAWyMqhRAKy_ARgMeIhLQAc', '1or4TT9jHSMbT7Ey6ve1Jeb_bVhj-GxxelGjK0lYZlAk']
RANGE_NAME = "'March'"
WEEK = 4

updates = []

def get_updates():
    """
    Save name and update of every person in a specific sheet
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Go through each cohort
    for cohort in range(len(COHORT_SPREADSHEET_IDs)):
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=COHORT_SPREADSHEET_IDs[cohort],
                                    range=RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            for row in values:
                try:
                    # Cohort 1 has extra column for "ambition"
                    if cohort == 0:
                        # Top row has headers for each column, including "name"
                        if row[0] != '' and row[WEEK+3] != '' and row[0] != 'Name':
                            updates.append([row[0], row[WEEK+3]])
                    elif row[0] != '' and row[WEEK+2] != '' and row[0] != 'Name':
                            updates.append([row[0], row[WEEK+2]])
                # Ignore cell if empty
                except:
                    pass

    return updates
