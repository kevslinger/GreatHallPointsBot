import os
from utils import constants
import gspread
import json
import pandas as pd
from datetime import datetime


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
    return gspread.service_account('client_secret.json', scopes)


def update_df(df: pd.DataFrame, timestamp: str, idx: str, author_name: str, author_house: str,
              points_post_author: str, points_post_house: str, link: str, mod: bool):
    """Function to add a row of the DataFrame
    :param df: (pd.DataFrame) The current dataframe of suggestions
    :param timestamp: (str) Timestamp for when the reddit comment happened
    :param idx: (str) The ID of the reddit comment
    :param author_name: (str) the suggester of points
    :param author_house: (str) the house (flair) of the suggester
    :param points_post_author: (str) the recipient of the suggestion
    :param points_post_house: (str) the house (flair) of the recipient
    :param link: (str) the link to the comment
    :param mod: (str) whether or not the suggester is a mod"""
    new_row = {constants.TIMESTAMP: [timestamp],
               constants.ID: [idx],
               constants.SUGGESTER: [author_name],
               constants.SUGGESTER_FLAIR: [author_house],
               constants.RECIPIENT: [points_post_author],
               constants.RECIPIENT_FLAIR: [points_post_house],
               constants.LINK: [link],
               constants.AWARDED: ["No"], # This is for house points givers to change after they award
               constants.MAYBE_IS_MOD: [str(mod)]}
    tmp_df = pd.DataFrame.from_dict(new_row)
    return pd.concat([df, tmp_df], ignore_index=True)


def get_current_tab_name():
    """Our tab name will be <Month> <Year> e.g. March 2022"""
    return datetime.strftime(datetime.now(), '%B %Y')


def get_specific_tab_url(sheet: gspread.Spreadsheet, tab_name: str):
    """The url for a specific tab is the url of the sheet concatenated with /edit#gid=<tab_id>"""
    return sheet.url + '/edit#gid=' + str(sheet.worksheet(tab_name).id)
