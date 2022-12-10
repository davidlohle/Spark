import requests, config

def generateDownDiscordMessage(service, error):
    payload = {
        "content": None,
        "embeds": [
            {
            "title": f"{service.Name} is currently unavailable",
            "description": f"Unable to reach the {service.Name} server after a set amount of attempts. \nError received: {error}",
            "color": 16734296,
            "thumbnail": {
                "url": f"{service.Icon}"
                }
            }   
            ],
            "attachments": []
        }
    sendDiscordMessage(payload, service.DiscordHook)

def generateUpDiscordMessage(service):
    payload = {
        "content": None,
        "embeds": [
            {
            "title": f"{service.Name} is back up",
            "description": f"{service.Name} is responding to health checks again. It's most likely nominal.",
            "color": 3980080,
            "thumbnail": {
                "url": f"{service.Icon}"
                }
            }   
            ],
            "attachments": []
        }
    sendDiscordMessage(payload, service.DiscordHook)

def generatePowerLossDiscordMessage(event):
    payload = {
        "content": None,
        "embeds": [
            {
            "title": f"{event['title']}",
            "description": f"{event['message']}",
            "color": 16205125,
            "fields": [
                {
                "name": "Estimated Runtime",
                "value": f"{event['estimated_runtime']} minutes",
                "inline": True
                },
                {
                "name": "Battery Percentage",
                "value": f"{event['battery_percentage']}%",
                "inline": True
                }
            ],
            "thumbnail": {
                "url": "https://f.ipv7.sh/ovyqto.png"
            }
            }
        ],
        "username": "Spark",
        "attachments": []
    }
    sendDiscordMessage(payload, config.Spark.GeneralDiscordHook)

def generatePowerReturnDiscordMessage(event):
    payload = {
        "content": None,
        "embeds": [
            {
            "title": f"{event['title']}",
            "description": f"{event['message']}",
            "color": 3980080,
            "thumbnail": {
                "url": "https://f.ipv7.sh/hkdilj.png"
            }
            }
        ],
        "username": "Spark",
        "attachments": []
    }
    sendDiscordMessage(payload, config.Spark.GeneralDiscordHook)

def generateInternalErrorDiscordMessage(message):
    payload = {
        "content": f"{message}",
        "embeds": None,
        "username": "Spark",
        "attachments": []
    }
    sendDiscordMessage(payload, config.Spark.InternalWebhook)

def sendDiscordMessage(message, webhook_url):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    response = requests.request("POST", webhook_url, json=message, headers=headers)
