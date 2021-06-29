import requests, urllib3, datetime

import db, cachet, check, config

def main():
    global status_db
    print(datetime.datetime.now().strftime("%D at %T"))
    checkService(check.plexStatus(), "Plex", cachet.Components.Plex, config.GroupMe.Plex)
    checkService(check.teamspeakStatus(), "TeamSpeak", cachet.Components.Teamspeak, config.GroupMe.VGF)
    checkService(check.syncLoungeStatus(), "SyncLounge", cachet.Components.SyncLounge, config.GroupMe.Plex)
    checkService(check.requestStatus(), "Requests", cachet.Components.Requests, config.GroupMe.Plex)
    checkService(check.fileUploadStatus(), "IPv7", cachet.Components.FileUpload, config.GroupMe.SeventhProtocol)



def checkService(service_response, service_name, service_cachet_component, groupme_channel):
    global status_db
    service = service_name.lower()
    service_incident_message = service + "_incident_message"
    service_incident_code = service + "_incident_code"
    if not service_response:
        if status_db[service]:
            # Component is down for the first iteration, let's create the notices.
            print("Error with contacting " + service_name + ", creating Cachet ticket and notifying group.")
            status_db[service] = False
            status_db[service_incident_message] = "On %s EST, there was a missed heartbeat from %s. %s is most likely down at the moment." % (datetime.datetime.now().strftime("%D at %T"), service_name, service_name)
            service_down_payload = {
                "visible": 1,
                "notify": False,
                "status": cachet.IncidentStatus.Investigating,
                "name": "%s Unavailability" % service_name, 
                "message": status_db[service_incident_message], 
                "component_id": service_cachet_component, 
                "component_status": cachet.ComponentStatus.MajorOutage
            } 

            incident_code = cachet.createIncident(service_down_payload)
            status_db[service_incident_code] = incident_code
            
            error_string = "The " + service_name + " server is down. You can track the status of this issue at: " + config.Cachet.URL + "/incidents/" + str(incident_code)
            notifyGroupMe(error_string, groupme_channel)
        else:
            # Service has already been seen as down.
            print(service_name + " continues to be down, a ticket is already open and people have been notified. Continuing in silence.")
    else:
        if not status_db[service]:
            # Service was down, but now it's back up. Close out the notices and notify people it's back.
            print(service_name + " has returned, closing out incident and notifying group.")
            status_db[service] = True
            return_string = status_db[service_incident_message] + "\n\nHowever, as of %s, it appears %s is running nominally." % (datetime.datetime.now().strftime("%D at %T"), service_name)
            cachet.closeIncident(service_cachet_component, status_db[service_incident_code], return_string)
            return_string = "The " + service_name + " server is back up. The incident has been closed out."
            notifyGroupMe(return_string, groupme_channel)
        else:
            # Service was up, and continues to be up.
            print(service_name + " continues to be fine.")
            status_db[service] = True

def notifyGroupMe(message, botID):
    payload = {
        "bot_id": botID,
        "text": message,
    }
    headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",   
    }
    requests.request("POST", "https://api.groupme.com/v3/bots/post", headers=headers, json=payload)


if __name__ == "__main__":
    global status_db
    urllib3.disable_warnings()
    db.initialize()
    status_db = db.status_db
    main()
    db.status_db = status_db
    db.commit()
