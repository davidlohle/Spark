import json

import config

def initialize():
    global status_db
    print(config.DB.FilePath)
    try:
        with open(config.DB.FilePath, 'r+') as file:
            status_db = json.load(file)
    except:
        status_db = {}
        print("Error loading status DB, starting with empty file.")
    try:
        plex_status = status_db["plex"]
    except:
        status_db["plex"] = True
    try:
        teamspeak_status = status_db["teamspeak"]
    except:
        status_db["teamspeak"] = True


def commit():
    global status_db
    with open(config.DB.FilePath, 'w+') as file:
        json.dump(status_db, file, indent=4, sort_keys=True)