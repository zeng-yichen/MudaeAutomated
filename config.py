"""
USER_TOKEN

a unique token corresponding to your unique Discord account
This is needed in order to link the automation script to your account
Instructions for obtaining this token can be found here: https://discordpy-self.readthedocs.io/en/latest/authenticating.html

PLEASE WRAP THE TOKEN WITH QUOTES! The USER_TOKEN must be a Python string.
"""

USER_TOKEN = ""

"""
EMOJI

the emoji with which the script will use to claim characters
"""

EMOJI = "❤️"

"""
MUDAE_CHANNELS

a python list of Discord channel IDs in which the script will roll, claim, etc.
The script will only perform Mudae-related tasks in the MUDAE_CHANNELS specified here
PLEASE MAKE SURE THAT MUDAE_CHANNELS IS A PYTHON LIST

May 11th 2025: CURRENTLY, ONLY ONE CHANNEL ID IS SUPPORTED FOR MUDAE_CHANNELS
"""

MUDAE_CHANNELS = []

"""
ALL_CHANNELS

a python list of Discord channel IDs in which the script will NOT perform Mudae-realted activities but WILL LISTEN to commands

LIST OF SUPPORTED COMMANDS:
@{you} list delay: lists all internal delays
"""

ALL_CHANNELS = []

"""
VALID_USERS

a python list of Discord user IDs
Only these users have access to the supported commands listed above
"""

VALID_USERS = []

"""
MIN_KAKERA

the minimum kakera that a character must possess in order to be claimed
It is suggested that MIN_KAKERA be larger than MIN_KAKERA_LAST_HOUR
"""

MIN_KAKERA = 500

"""
MIN_KAKERA_LAST_HOUR

the minimum kakera that a character must possess in order to be claimed IN THE LAST HOUR, IMMEDIATELY AFTER YOUR ROLLS IN THE LAST HOUR
It is suggested that MIN_KAKERA be larger than MIN_KAKERA_LAST_HOUR
"""

MIN_KAKERA_LAST_HOUR = 25

"""
SNIPE_TYPE

whether or not you wish to snipe other users' WISHED characters
Remember, the script will attempt to snipe ALL NON-WISHED characters

SNIPE_TYPE = 0: the script will NOT attempt to snipe other users' WISHED characters
SNIPE_TYPE = 1: the script WILL attempt to snipe other users' WISHED characters
"""

SNIPE_TYPE = 1 # Please enter either 0 or 1