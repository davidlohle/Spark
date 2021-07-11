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

    # Create keys if they don't exist (poor-mans schema migration)
    services = ["plex", "teamspeak", "synclounge", "requests", "ipv7", "minecraft"]
    for service in services:
        if service not in status_db:
            status_db[service] = 0


def commit():
    global status_db
    with open(config.DB.FilePath, 'w+') as file:
        json.dump(status_db, file, indent=4, sort_keys=True)