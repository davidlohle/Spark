import requests

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

def sendDiscordMessage(message, webhook_url):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    response = requests.request("POST", webhook_url, json=message, headers=headers)
