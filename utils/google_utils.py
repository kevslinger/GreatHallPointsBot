import os
from utils import constants
import gspread
import json
import pandas as pd
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials


def convert_time(time):
    """Convert string in year/month/day hour:minute:second format to datetime object"""
    return datetime.utcfromtimestamp(int(time)).strftime('%Y-%m-%d %H:%M:%S')


def create_gspread_client():
    """Create the client to access Google Sheets"""
    # Scope of what we can do in google drive
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    # Write the credentials file if we don't have it
    if not os.path.exists('client_secret.json'):
        json_creds = dict()
        for param in constants.JSON_PARAMS:
            json_creds[param] = os.getenv(param).replace('\"', '').replace('\\n', '\n')
        with open('client_secret.json', 'w') as f:
            json.dump(json_creds, f)
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scopes)
    return gspread.authorize(creds)


def update_df(df, timestamp, idx, author_name, author_house,
              points_post_author, points_post_house, link):
    """Function to add a row of the DataFrame"""
    new_row = {constants.TIMESTAMP: [timestamp],
               constants.ID: [idx],
               constants.AWARDER: [author_name],
               constants.AWARDER_HOUSE: [author_house],
               constants.AWARDEE: [points_post_author],
               constants.AWARDEE_HOUSE: [points_post_house],
               constants.LINK: [link],
               constants.AWARDED: ["No"]}
    tmp_df = pd.DataFrame.from_dict(new_row)
    return pd.concat([df, tmp_df], ignore_index=True)

