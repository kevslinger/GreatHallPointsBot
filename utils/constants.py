
#########################
# Google Sheets Columns #
#########################
PINGLIST_SHEET = "Mod List"
USERNAME = "Username"

TIMESTAMP = "Timestamp"
ID = "ID"
SUGGESTER = "Suggester"
SUGGESTER_FLAIR = "Suggester Flair"
RECIPIENT = "Recipient"
RECIPIENT_FLAIR = "Recipient Flair"
LINK = "Link"
AWARDED = "Points Awarded?"
MAYBE_IS_MOD = "Mod Suggested"
COLUMNS = [TIMESTAMP, ID, SUGGESTER, SUGGESTER_FLAIR, RECIPIENT, RECIPIENT_FLAIR, LINK, AWARDED, MAYBE_IS_MOD]

###################
# Hogwarts Houses #
# and r/HP flairs #
###################

GRYFFINDOR = "Gryffindor"
GRYFF = "Gryff"
GRYFF_CSS_CLASS = "GR"
HUFFLEPUFF = "Hufflepuff"
PUFF = "Puff"
PUFF_CSS_CLASS = "HF"
RAVENCLAW = "Ravenclaw"
CLAW = "Claw"
CLAW_CSS_CLASS = "RV"
SLYTHERIN = "Slytherin"
SLYTH = "Slyth"
SLYTH_CSS_CLASS = "SL"

####################
# PRAW Reddit text #
####################

SUBMISSION_ID_PREFIX = "t3_"
COMMENT_ID_PREFIX = "t1_"
SUBREDDIT_NAME = "harrypotter"

#################
# Misc Bot Text #
#################

POINTS_PHRASE = "+"
KEV = "u/kevslinger"
PM_KEV = f"[PM u\/kevslinger](https://www.reddit.com/message/compose/?to=kevslinger)"
BOT_ENDING = f"\n\n****\n\n*I'm a bot. Do not reply to this message. Questions? [About me](https://www.github.com/kevslinger/GreatHallPointsBot) More Questions? {PM_KEV}*"

################
# Gspread ENV  #
################

JSON_PARAMS = ["type", "project_id", "private_key_id", "private_key", "client_email", "client_id", "auth_uri",
               "token_uri", "auth_provider_x509_cert_url", "client_x509_cert_url"]

#######################
## Heroku Scheduling ##
#######################

PING_MODS_DAY = 'Sunday'