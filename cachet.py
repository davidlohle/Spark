import requests, json

import config

class Components:
    Plex = 7
    Teamspeak = 4
    SyncLounge = 9
    Requests = 13
    FileUpload = 5

class ComponentStatus:
    Operational = 1
    MajorOutage = 4

class IncidentStatus:
    Investigating = 1
    Fixed = 4

def createIncident(payload):
    headers = {
        "Accept": "application/json",
        "X-Cachet-Application": "SeventhProtocol StatusBot",
        "Content-Type": "application/json",
        "X-Cachet-Token": config.Cachet.Token
    }
    response = requests.request("POST", config.Cachet.URL + "/api/v1/incidents", json=payload, headers=headers)

    responseJson = json.loads(response.text)

    return responseJson["data"]["id"]

def closeIncident(component_code, incident_code, message):
    headers = {
        "Accept": "application/json",
        "X-Cachet-Application": "SeventhProtocol StatusBot",
        "Content-Type": "application/json",
        "X-Cachet-Token": config.Cachet.Token
    }
    close_payload = {
    "id": incident_code,
    "status": IncidentStatus.Fixed, 
    "component_id": component_code, 
    "component_status": ComponentStatus.Operational,
    "message": message
    }
    response = requests.request("PUT", config.Cachet.URL + "/api/v1/incidents/" + str(incident_code), json=close_payload, headers=headers)

