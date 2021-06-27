import requests, socket, json

import config

def plexStatus():
    health_url = config.Plex.URL + "/media/providers"
    headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-Plex-Token": config.Plex.Token
    }
    response = ""
    try:
        response = requests.request("GET", health_url, headers=headers, verify=False, timeout=10)
    except:
        print("Timeout while reaching Plex.")
        return False

    if response.status_code != 200:
        return False
    
    return True



def teamspeakStatus():
    teamspeak_host = config.Teamspeak.Host
    teamspeak_port = 10011
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try: 
        result = s.connect_ex((teamspeak_host, teamspeak_port))
        if result != 0:
            s.close()
            return False
        s.close()
        return True
    except:
        return False

