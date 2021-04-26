from dotenv import load_dotenv
from utils import constants, reddit_utils, google_utils
from gspread.exceptions import WorksheetNotFound
import os
import pandas as pd
import praw
from datetime import datetime

# Features:
# [X] Log into r/HP
# [X] Connect to a google sheet
# [X] Track comments in r/HP
# [X] Parse comments for select phrase (e.g. !HousePoints)
# [X] If the user's flair is not set to a house, let them know they can't get house points without setting it.
#       TODO: Should we still add these posts to the sheet?
# [X] OP cannot use !HousePoints on their own submission
#       - Unless it's a mod of the sub
# [X] If everything is clean (OP not awarding to themselves, user has house flair set), then grab the URL and put it
#       On a google sheet.
# [X] Keep a dataframe of all the new records (posts) and then at the end of each day, append to the sheet
# [X] Make sure duplicates are not added.
# [ ] Create a new sheet every month.
#       Issue is that schedule has no "every month" feature. And you can't do every 30 days for obvious reasons
#       One thing to do is make it every day, check if we're the first of the month, and then make the sheet if it is.
#       Else, make it a labor (we can create basically years worth of months now, make it not an issue)
# [ ] Swap to new sheet at start of month
#       With this in mind, seems like we'll just have
# [X] Periodically (weekly?) Ping the mods with the link to the google sheet.
# [X] The sheet should have a row to let other mods know it's already been given points.
# TODO: Instead of sending a message to modmail, maybe get the list of head humans?
# TODO: highlight suggestions from reddit mod team https://pypi.org/project/gspread-formatting/?


class Bot:
    def __init__(self):
        # We keep a dataFrame of all the new comments which should be considered for house points.
        self.df = pd.DataFrame(columns=constants.COLUMNS)

        cur_time = datetime.now()
        self.month = cur_time.month
        self.year = cur_time.year
        # Testing year change
        # self.year = '2000'

        # Create the gsheets client, open the worksheet.
        gsheets = google_utils.create_gspread_client()
        sheet_key = os.getenv('SHEET_KEY').replace('\'', '')
        # TODO: Stay consistent with current month/year
        self.sheet = gsheets.open_by_key(sheet_key)
        try:
            # Current tab is month year (e.g. January 2022)
            self.current_tab = self.sheet.worksheet(google_utils.get_current_tab_name())
        except WorksheetNotFound:
            # If the tab doesn't exist, create it.
            # args are the name of the tab, the number of rows/columns, and position in spreadsheet
            # TODO: is it right to always make it the tab after the ping list tab?
            self.current_tab = self.sheet.add_worksheet(google_utils.get_current_tab_name(), 0, len(constants.COLUMNS), 1)

        self.submission_ids = pd.DataFrame(self.current_tab.get_all_records(), columns=constants.COLUMNS)[constants.ID]
        print(self.submission_ids)

        self.reddit = reddit_utils.create_reddit_client()
        # TODO: for testing
        #self.subreddit = self.reddit.subreddit(constants.SUBREDDIT_NAME)
        self.subreddit = self.reddit.subreddit('kevsTestSubreddit4')
        print(f"[ {google_utils.get_formatted_time()} ] Have connected to {self.subreddit.display_name}")


    def append_rows_to_sheet(self):
        """Move the current suggestions and append them to the google sheet"""
        if len(self.df) > 0:
            # If the sheet is brand new (new month), add columns
            if len(self.current_tab.get_all_values()) < 1:
                self.current_tab.append_rows([self.df.columns.tolist()])
            self.current_tab.append_rows(self.df.values.tolist())
            print(f"[ {google_utils.get_formatted_time()} ] Appended {len(self.df)} rows to sheet.")
            self.df = pd.DataFrame(columns=constants.COLUMNS)
        else:
            print(f"[ {google_utils.get_formatted_time()} ] No new suggestions - did not append to sheet.")

    def scrape_comments(self):
        for comment in self.reddit.inbox.unread(mark_read=True):
            if not isinstance(comment, praw.models.Comment):
                print("Skipping as this is not a comment")

            comment.mark_read()
            # Keeps a stream of comments, starting from when the bot is started up
            # If the commenter used "!housepoints", then we need to find the comment/submission above that.
            # TODO: /u/ or just u/?
            if reddit_utils.triggered_bot(comment):
                parent_id = comment.parent_id
                # Submissions (posts) ID are t3_{id}, comments ID are t1_{id}
                points_post = reddit_utils.get_points_post(self.reddit, parent_id)
                # Hedge against a weird reddit thing that isn't a comment (t1) or post (t3)
                if points_post is None:
                    continue
                # Could be either comment or submission
                points_post_author = points_post.author.name
                # Allow mods to self-suggest, otherwise don't allow it.
                if points_post_author == comment.author.name and points_post_author not in self.subreddit.moderator():
                    comment.reply(
                        f"Hey u/{comment.author.name}, you cannot suggest your own post for house points, sorry!"
                        f"{constants.BOT_ENDING}"
                    )
                    continue
                print(f"parent_id is {parent_id}")
                print(f"submission_ids is {self.submission_ids.values.tolist()}")
                # Don't allow duplicate posts.
                if parent_id in self.submission_ids.values.tolist():
                    comment.reply(
                        f"Hey u/{comment.author.name}, thanks for suggesting this post for house points! We've already "
                        f"recorded it, and will let the mod team know. Thanks! {constants.BOT_ENDING}"
                    )
                    continue

                points_post_author_flair_class = points_post.author_flair_css_class
                points_post_author_flair_text = points_post.author_flair_text
                points_post_house = reddit_utils.convert_flair_to_house(points_post_author_flair_class,
                                                                        points_post_author_flair_text)
                # TODO: Should we still add them to the sheet?
                if points_post_house is None:
                    comment.reply(f"Hey u/{points_post_author}, u/{comment.author.name} thinks your post is deserving "
                                  f"of house points! "
                                  f"What is your Hogwarts house? Please set your house flair with a crest in order to "
                                  f"be considered. Click "
                                  f"[here](https://www.reddit.com/r/harrypotter/wiki/oursub#wiki_add_house_flair) "
                                  f"for instructions on how to do that. {constants.BOT_ENDING}")
                    print("User has not selected a house flair.")
                    # do something
                else:
                    comment.reply(
                        f"Hey u/{points_post_author}, u/{comment.author.name} thinks your post is deserving of house points, congrats! "
                        f"We'll pass this along to our mod team. "
                        f"{constants.BOT_ENDING}")
                comment = comment.submission
                # Add the new row to the dataframe.
                # TODO: if this is slow, we can batch it by just doing this once at the very end.
                self.df = google_utils.update_df(self.df, google_utils.convert_reddit_timestamp(comment.created_utc),
                                                 parent_id, comment.author.name,
                                                 reddit_utils.convert_flair_to_house(comment.author_flair_css_class,
                                                                                     comment.author_flair_text),
                                                 points_post_author, points_post_house,
                                                 reddit_utils.convert_link(points_post.permalink),
                                                 points_post_author in self.subreddit.moderator())
                self.submission_ids = self.submission_ids.append(pd.Series(parent_id), ignore_index=True)
        self.append_rows_to_sheet()


if __name__ == '__main__':
    load_dotenv(override=True)
    bot = Bot()
    bot.scrape_comments()
