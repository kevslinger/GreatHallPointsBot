import praw
import os
from utils import constants


def create_reddit_client():
    """Return a PRAW Reddit Client based on ENV variables"""
    ME = os.getenv('REDDIT_USERNAME')
    PASSWORD = os.getenv('REDDIT_PASSWORD')
    CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
    CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')

    return praw.Reddit(client_id=CLIENT_ID,
                       client_secret=CLIENT_SECRET,
                       user_agent=f'{ME} is a bot by u/kevslinger',
                       username=ME,
                       password=PASSWORD)


def convert_flair_to_house(flair_css_class: str, flair_text: str):
    """Take the User's flair and return the house.
    Note: this won't pick up *all* flairs. But it will get all the ones
    with the crest (:Gryff:, :Puff:, :Claw:, :Slyth:)"""
    if flair_css_class is None:
        return None
    if constants.GRYFF_CSS_CLASS in flair_css_class:
        return constants.GRYFFINDOR
    elif constants.PUFF_CSS_CLASS in flair_css_class:
        return constants.HUFFLEPUFF
    elif constants.CLAW_CSS_CLASS in flair_css_class:
        return constants.RAVENCLAW
    elif constants.SLYTH_CSS_CLASS in flair_css_class:
        return constants.SLYTHERIN
    else:
        return flair_text
    # Remove case sensitivity
    #flair_lower = flair_css_class.lower()
    # TODO: Could just be a for loop
    #if constants.GRYFF.lower() in flair_lower:
    #    return constants.GRYFFINDOR
    #elif constants.PUFF.lower() in flair_lower:
    #    return constants.HUFFLEPUFF
    #elif constants.CLAW.lower() in flair_lower:
    #    return constants.RAVENCLAW
    #elif constants.SLYTH.lower() in flair_lower:
    #    return constants.SLYTHERIN
    #else:
    #    return None  # flair_css_class


def get_points_post(reddit, parent_id):
    """Get the parent of the comment which suggests points"""
    if parent_id.startswith(constants.SUBMISSION_ID_PREFIX):
        points_post = reddit.submission(id=parent_id.replace(constants.SUBMISSION_ID_PREFIX, ""))
    elif parent_id.startswith(constants.COMMENT_ID_PREFIX):
        points_post = reddit.comment(id=parent_id.replace(constants.COMMENT_ID_PREFIX, ""))
    else:
        print("Uhhhh I've never seen this type of response before.")
        points_post = None
    return points_post


def convert_link(link):
    """Prepend reddit.com to link ID"""
    return 'https://reddit.com' + link


def triggered_bot(comment):
    return (f"{constants.POINTS_PHRASE}/u/{os.getenv('REDDIT_USERNAME')}".lower() in comment.body.lower() or
            f"{constants.POINTS_PHRASE}u/{os.getenv('REDDIT_USERNAME')}".lower() in comment.body.lower())