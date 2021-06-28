import requests, socket, json

import config

def plexStatus():
    health_url = config.Plex.URL + "/media/providers"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Plex-Token": config.Plex.Token
    }
    try:
        response = requests.request("GET", health_url, headers=headers, verify=False, timeout=10)
        if response.status_code != 200:
            print("Non 200 HTTP response from Plex. It was: %d", response.status_code)
            return False
        return True
    except Exception as err:
        print("Issue while reaching Plex. Err:")
        print(err)
        return False

def teamspeakStatus():
    teamspeak_host = config.Teamspeak.Host
    teamspeak_port = 10011
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try: 
        result = s.connect_ex((teamspeak_host, teamspeak_port))
        if result != 0:
            s.close()
            print("Non 0 ex_connect to Teamspeak RCON.")
            return False
        s.close()
        return True
    except Exception as err:
        print("Unknown issue connecting to TeamSpeak RCON. Err:")
        print(err)
        return False

def syncLoungeStatus():
    synclounge_url: config.SyncLounge.URL
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    try:
        response = requests.request("GET", synclounge_url, headers=headers, verify=False, timeout=10)
        if response.status_code != 200:
            print("Non 200 HTTP response from SyncLounge. It was: %d", response.status_code)
            return False
        return True
    except Exception as err:
        print("Issue while reaching SyncLounge. Err:")
        print(err)
        return False