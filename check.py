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
    synclounge_url = config.SyncLounge.URL
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

def requestStatus():
    requests_url = config.Requests.URL
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    try:
        response = requests.request("GET", requests_url, headers=headers, verify=False, timeout=10)
        if response.status_code != 200:
            print("Non 200 HTTP response from Request system. It was: %d", response.status_code)
            return False
        return True
    except Exception as err:
        print("Issue while reaching Requests. Err:")
        print(err)
        return False


def fileUploadStatus():
    file_upload_api = config.FileUpload.Upload_API
    test_image_url = config.FileUpload.RemoteFile
    file_content = ""

    # Let's download an image and then try re-uploading it. This should test the full lifecycle.
    try:
        response = requests.get(test_image_url, timeout=10)
        if response.status_code != 200:
            print("Non 200 HTTP response from Pomf on file get. It was: %d", response.status_code)
            return False
        file_content = response.content
    except Exception as err:
        print("Issue while trying to download pomf file. Err:")
        print(err)
        return False
    
    # Viewing an image worked (cool), now let's try uploading it back.
    # I should expect the API to return the same URL as `test_image_url` since it runs de-dupe.

    try:
        response = requests.post(file_upload_api, files={'files[]': file_content}, timeout=10)
        if response.status_code != 200:
            print("Non 200 HTTP response from Pomf API while trying to uplaod file system. It was: %d", response.status_code)
            return False

        response_json = json.loads(response.text)
        resulting_file_url = response_json["files"][0]["url"]

        if resulting_file_url != test_image_url:
            print("Didn't get back same URL from Pomf API while trying to upload an existing file. We got: %s instead.", resulting_file_url)
            return False
        
        return True
    except Exception as err:
        print("Issue while reaching Requests. Err:")
        print(err)
        return False