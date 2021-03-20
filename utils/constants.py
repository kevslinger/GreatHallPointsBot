
#########################
# Google Sheets Columns #
#########################

# TODO: Better names? Awarder, Awardee, Awarded only 1 letter off. Very confusing
TIMESTAMP = 'Timestamp'
ID = 'ID'
AWARDER = 'Awarder'
AWARDER_HOUSE = 'Awarder House'
AWARDEE = 'Awardee'
AWARDEE_HOUSE = 'Awardee House'
LINK = 'Link'
AWARDED = 'Points Awarded?'
COLUMNS = [TIMESTAMP, ID, AWARDER, AWARDER_HOUSE, AWARDEE, AWARDEE_HOUSE, LINK, AWARDED]

###################
# Hogwarts Houses #
# and r/HP flairs #
###################

GRYFFINDOR = 'Gryffindor'
GRYFF = 'Gryff'
GRYFF_CSS_CLASS = 'GR'
HUFFLEPUFF = 'Hufflepuff'
PUFF = 'Puff'
PUFF_CSS_CLASS = 'HF'
RAVENCLAW = 'Ravenclaw'
CLAW = 'Claw'
CLAW_CSS_CLASS = 'RV'
SLYTHERIN = 'Slytherin'
SLYTH = 'Slyth'
SLYTH_CSS_CLASS = 'SL'

####################
# PRAW Reddit text #
####################

SUBMISSION_ID_PREFIX = 't3_'
COMMENT_ID_PREFIX = 't1_'
SUBREDDIT_NAME = 'harrypotter'

#################
# Misc Bot Text #
#################

POINTS_PHRASE = '!housepoints'
KEV = "u/kevslinger"
BOT_ENDING = f"\n\n****\n\n*I am a bot. Beep boop. Have questions? Ask {KEV}*"

################
# Gspread text #
################

JSON_PARAMS = ["type", "project_id", "private_key_id", "private_key", "client_email", "client_id", "auth_uri",
               "token_uri", "auth_provider_x509_cert_url", "client_x509_cert_url"]

###################
# Month Constants #
###################

NUM_TO_MONTH = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec"
}