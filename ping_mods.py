from utils import reddit_utils, google_utils, constants
from datetime import datetime
import os
from dotenv import load_dotenv
from pytz import timezone



def main():
    reddit_client = reddit_utils.create_reddit_client()
    gspread_client = google_utils.create_gspread_client()
    spreadsheet = gspread_client.open_by_key(os.getenv('SHEET_KEY').replace('\'', ''))
    ping_mods(spreadsheet, reddit_client)


def ping_mods(sheet, reddit):
    """Send a message to the ping list with sheet link"""
    ping_list = sheet.worksheet(constants.PINGLIST_SHEET)
    for record in ping_list.get_all_records():
        reddit.redditor(record[constants.USERNAME]).message(
            f'GreatHallPointsBot Weekly Update for {datetime.now().strftime("%B %d, %Y")}',
            google_utils.get_specific_tab_url(sheet, google_utils.get_current_tab_name())
        )
    print(f"[ {google_utils.get_formatted_time()} ] Pung the mods.")


if __name__ == '__main__':

    current_day = datetime.now(timezone('US/Eastern')).strftime('%A')
    if current_day != constants.PING_MODS_DAY:
        print(f"Today is {current_day} but I only want to run on {constants.PING_MODS_DAY}")
        exit(0)

        
    load_dotenv(override=True)
    main()
