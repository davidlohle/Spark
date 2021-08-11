import requests, urllib3, datetime

import db, cachet, check, config

def main():
    global status_db
    print("==> " + datetime.datetime.now().strftime("%D at %T"))
    checkService(check.plexStatus(), 5, "Plex", cachet.Components.Plex, config.GroupMe.VGF)
    checkService(check.teamspeakStatus(), 2, "TeamSpeak", cachet.Components.Teamspeak, config.GroupMe.VGF)
    checkService(check.minecraftStatus(), 5, "Minecraft", cachet.Components.Minecraft, config.GroupMe.VGF)
    checkService(check.syncLoungeStatus(), 5, "SyncLounge", cachet.Components.SyncLounge, config.GroupMe.SeventhProtocol)
    checkService(check.requestStatus(), 10, "Requests", cachet.Components.Requests, config.GroupMe.SeventhProtocol)
    checkService(check.fileUploadStatus(), 3, "IPv7", cachet.Components.FileUpload, config.GroupMe.SeventhProtocol)
    summarizeStatus()


def summarizeStatus():
    global status_db
    summary = []
    for service in config.Spark.Services:
        if status_db[service] != 0:
            summary.append(service + ": DOWN (" + str(status_db[service]) + ")")
        else:
            summary.append(service + ": OK")
    print(" | ".join(summary))

def checkService(service_response, error_threshold, service_name, service_cachet_component, groupme_channel):
    global status_db
    service = service_name.lower()
    service_incident_message = service + "_incident_message"
    service_incident_code = service + "_incident_code"
    if not service_response:
        # Component is down, increment error count
        status_db[service] += 1
        print("Error with contacting " + service_name + ", incrementing error counter.")
        if status_db[service] == error_threshold:
            # Component is down past threshold, create tickets and alert.
            print(service_name + " has hit error threshold, opening a ticket and notifying groups.")
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
            
            error_string = "The " + service_name + " server is down. Status: " + config.Cachet.URL + "/incidents/" + str(incident_code)
            notifyGroupMe(error_string, groupme_channel)
        elif status_db[service] > error_threshold:
            # Service has already violated error threshold and tickets opened.
            print(service_name + " has already violated error threshold and alerted. Continuing in silence.")
        else:
            # Service has not yet violated error threshold.
            print(service_name + " has not yet violated error threshold. Not yet alerting.")
    else:
        if status_db[service] >= error_threshold:
            # Service was down past error threshold, but now it's back up. Close out the notices and notify people it's back.
            print(service_name + " has returned, closing out incident and notifying group.")
            status_db[service] = 0
            return_string = status_db[service_incident_message] + "\n\nHowever, as of %s, it appears %s is running nominally." % (datetime.datetime.now().strftime("%D at %T"), service_name)
            cachet.closeIncident(service_cachet_component, status_db[service_incident_code], return_string)
            return_string = "The " + service_name + " server is back up."
            notifyGroupMe(return_string, groupme_channel)
        elif status_db[service] > 0:
            # Service was down, but never violated error threshold. Resetting counter and continuing in silence.
            print(service_name + " previously had issues, but no longer. Since it never violated threshold, continuing in silence.")
            status_db[service] = 0
        else:
            # Service was up, and continues to be up.
            # print(service_name + " continues to be fine.")
            status_db[service] = 0

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
    try:
        main()
    except Exception as err:
        print("Error while running Spark: " + str(err))
    db.status_db = status_db
    db.commit()
