import os
from utils import constants
import gspread
import json
import pandas as pd
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials


def get_formatted_time():
    """Get time and format it to be human readable"""
    return datetime.strftime(datetime.now(), '%B %d, %Y %H:%M:%S')


def convert_reddit_timestamp(time):
    """Convert from unix time to human-readable"""
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


def update_df(df: pd.DataFrame, timestamp: str, idx: str, author_name: str, author_house: str,
              points_post_author: str, points_post_house: str, link: str, mod: bool):
    """Function to add a row of the DataFrame
    :param df: (pd.DataFrame)"""
    new_row = {constants.TIMESTAMP: [timestamp],
               constants.ID: [idx],
               constants.SUGGESTED_BY: [author_name],
               constants.SUGGESTED_BY_FLAIR: [author_house],
               constants.RECIPIENT: [points_post_author],
               constants.RECIPIENT_FLAIR: [points_post_house],
               constants.LINK: [link],
               constants.AWARDED: ["No"], # This is for house points givers to change after they award
               constants.MAYBE_IS_MOD: [str(mod)]}
    tmp_df = pd.DataFrame.from_dict(new_row)
    return pd.concat([df, tmp_df], ignore_index=True)


def get_sheet_name():
    return datetime.strftime(datetime.now(), '%B %Y')
