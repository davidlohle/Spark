import requests, urllib3, datetime, socket

import db, cachet, check, config

def main():
    global status_db

    # PLEX HEALTH CHECKING
    if not check.plexStatus():
        if status_db["plex"]:
            # Plex is down for the first iteration, let's create the notices.
            print("Error with contacting Plex, creating Cachet ticket and notifying group.")
            status_db["plex"] = False
            status_db["plex_incident_message"] = "On %s EST, there was a missed heartbeat from Outer Heaven. Plex is most likely down at the moment." % datetime.datetime.now().strftime("%D at %T")
            plex_down_payload = {
                "visible": 1,
                "notify": False,
                "status": cachet.IncidentStatus.Investigating,
                "name": "Plex Unavailability", 
                "message": status_db["plex_incident_message"], 
                "component_id": cachet.Components.Plex, 
                "component_status": cachet.ComponentStatus.MajorOutage
            } 
            incident_code = cachet.createIncident(plex_down_payload)
            status_db["plex_incident"] = incident_code
            
            error_string = "The Plex server is down. You can track the status of this issue at: " + config.Cachet.URL + "/incidents/" + str(incident_code)
            notifyGroupMe(error_string, config.GroupMe.Plex)
        else:
            # Plex has already been seen as down.
            print("Plex continues to be down, a ticket is already open and people have been notified. Continuing in silence.")
    else:
        if not status_db["plex"]:
            # Plex was down, but now it's back up. Close out the notices and notify people it's back.
            print("Plex has returned, closing out incident and notifying group.")
            status_db["plex"] = True
            return_string = status_db["plex_incident_message"] + "\n\nHowever, as of %s, it appears Plex is running nominally." % datetime.datetime.now().strftime("%D at %T")
            cachet.closeIncident(cachet.Components.Plex, status_db["plex_incident"], return_string)
            return_string = "The Plex server is back up. The incident has been closed out."
            notifyGroupMe(return_string, config.GroupMe.Plex)
        else:
            # Plex was up, and continues to be up.
            print("Plex continues to be fine.")
            status_db["plex"] = True

    # TEAMSPEAK HEALTH CHECKING
    if not check.teamspeakStatus():
        if status_db["teamspeak"]:
            # Teamspeak is down for the first iteration, let's create notices
            print("Error with contacting Teamspeak, creating Cachet ticket and notifying group.")
            status_db["teamspeak"] = False
            status_db["teamspeak_incident_message"] = "On %s EST, the Teamspeak server did not respond to a health query. Teamspeak is most likely down at the moment." % datetime.datetime.now().strftime("%D at %T")
            teamspeak_down_payload = {
                "visible": 1,
                "notify": False,
                "status": cachet.IncidentStatus.Investigating,
                "name": "Teamspeak Unavailability", 
                "message": status_db["teamspeak_incident_message"], 
                "component_id": cachet.Components.Teamspeak, 
                "component_status": cachet.ComponentStatus.MajorOutage
            }
            incident_code = cachet.createIncident(teamspeak_down_payload)
            status_db["teamspeak_incident"] = incident_code

            error_string = "The Teamspeak server is down. You can track the status of this issue at: " + config.Cachet.URL + "/incidents/" + str(incident_code)
            notifyGroupMe(error_string, config.GroupMe.VGF)
        else:
            # Teamspeak has already been seen as down.
            print("Teamspeak continues to be down, a ticket is already open and people have been notified. Continuing in silence.")
    else:
        if not status_db["teamspeak"]:
            # Teamspeak was down, but now it's back up. Close out the notices and notify people it's back.
            print("Teamspeak has returned, closing out incident and notifying group.")
            status_db["teamspeak"] = True
            return_string = status_db["teamspeak_incident_message"] + "\n\n However, as of %s, it appears Teamspeak has returned." % datetime.datetime.now().strftime("%D at %T")
            cachet.closeIncident(cachet.Components.Teamspeak, status_db["teamspeak_incident"], return_string)
            return_string = "The Teamspeak server is back up. The incident has been closed out."
            notifyGroupMe(return_string, config.GroupMe.VGF)
        else:
            # Teamspeak was up, and contiues to be up.
            print("Teamspeak continues to be fine.")
            status_db["teamspeak"] = True



def notifyGroupMe(message, botID):
    payload = {
        "bot_id": botID,
        "text": message,
    }
    headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",   
    }
    response = requests.request("POST", "https://api.groupme.com/v3/bots/post", headers=headers, json=payload)








if __name__ == "__main__":
    global status_db
    urllib3.disable_warnings()
    db.initialize()
    status_db = db.status_db
    main()
    db.status_db = status_db
    db.commit()
