import urllib3, datetime, time

import db, check, config, lock, discord

def main():
    global status_db
    print("==> " + datetime.datetime.now().strftime("%D at %T"))
    if not check.sanityStatus():
        print("Error while running sanity check, halting.")
        raise Exception("No network access.")
    checkService(check.plexStatus(), config.Plex)
    checkService(check.teamspeakStatus(), config.Teamspeak)
    checkService(check.minecraftStatus(), config.Minecraft)
    checkService(check.syncLoungeStatus(), config.SyncLounge)
    checkService(check.requestStatus(), config.Requests)
    checkService(check.fileUploadStatus(), config.FileUpload)
    generatePrometheusExport()
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


def checkService(service_response, service_config):
    global status_db
    service = service_config.Name.lower()
    service_name = service_config.Name
    error_threshold = service_config.Retries
    if not service_response[0]:
        # Component is down, increment error count
        status_db[service] += 1
        print("Error with contacting " + service + ", incrementing error counter.")
        if status_db[service] == error_threshold:
            # Component is down past threshold, alert.
            print(service_name + " has hit error threshold, notifying groups.")
            discord.generateDownDiscordMessage(service_config, service_response[1])
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
            discord.generateUpDiscordMessage(service_config)
        elif status_db[service] > 0:
            # Service was down, but never violated error threshold. Resetting counter and continuing in silence.
            print(service_name + " previously had issues, but no longer. Since it never violated threshold, continuing in silence.")
            status_db[service] = 0
        else:
            # Service was up, and continues to be up.
            # print(service_name + " continues to be fine.")
            status_db[service] = 0


def generatePrometheusExport():
    global status_db
    with open(config.Spark.PrometheusExportFile, "w") as exporter:
        exporter.write(f"# TYPE spark_status counter\n")
        for service in config.Spark.Services:
            exporter.write("spark_status{service=\"" + str(service) + "\"} " + str(status_db[service]) + "\n")

if __name__ == "__main__":
    lock.getLock()
    global status_db
    urllib3.disable_warnings()
    db.initialize()
    status_db = db.status_db
    try:
        main()
    except Exception as err:
        print("Error while running Spark: " + str(err))
        # Fatal error in Spark, but should still save DB to prevent duplicate errors.
        db.status_db = status_db
        db.commit()
        lock.releaseLock()
    db.status_db = status_db
    db.commit()
    lock.releaseLock()
