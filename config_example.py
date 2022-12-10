import os

class Spark:
    Services = ["plex", "teamspeak", "synclounge", "requests", "ipv7", "minecraft"]
    LockFilePath = "."
    PrometheusExportFile = "./metrics"

class Servers:
    Hosts = ["server-01", "server-02", "server-03"]
    User = "ups_admin"
    SSHKeyPath = "/opt/lockdown/ssh_key"
    ShutdownCommand = "wall test" # This should be something like `shutdown -h now`, but test it with `wall` first.

class Jellyfin:
    URL = "https://myjellyfininstance.com/health"

class Plex:
    URL = "https://myplexserver.com/"
    Token = "MYTOKEN"
    Name = "Plex"
    Retries = 5
    Icon = "https://f.ipv7.sh/lruu.png"
    DiscordHook = "https://discord.com/api/webhooks/WEBHOOK_URL"

class Minecraft:
    Host = "myminecraftserver.com"
    Port = 25565
    Icon = "https://f.ipv7.sh/drhcix.png"
    Name = "Minecraft"
    Retries = 3
    DiscordHook = "https://discord.com/api/webhooks/WEBHOOK_URL"

class SyncLounge:
    URL = "https://mysynclounge.com"
    Name = "SyncLounge"
    Retries = 5
    Icon = "https://f.ipv7.sh/oncqc.png"
    DiscordHook = "https://discord.com/api/webhooks/WEBHOOK_URL"

class Requests:
    URL = "https://mycontentserver.com/v5/api/status"
    Name = "Requests"
    Retries = 10
    Icon = "https://f.ipv7.sh/enrqiy.png"
    DiscordHook = "https://discord.com/api/webhooks/WEBHOOK_URL"

class FileUpload:
    RemoteFile = "https://f.ipv7.sh/fahqlx.png"
    Upload_API = "https://mypomfapi.com/upload.php"
    Name = "IPv7"
    Retries = 3
    Icon = "https://f.ipv7.sh/agfkal.png"
    DiscordHook = "https://discord.com/api/webhooks/WEBHOOK_URL"

class DB:
    FilePath = os.path.dirname(os.path.abspath(__file__)) + "/statusDB.json"

class Teamspeak:
    Host = "myteamspeakserver.com"
    Name = "Teamspeak"
    Retries = 2
    Icon = "https://f.ipv7.sh/mwsqq.png"
    DiscordHook = "https://discord.com/api/webhooks/WEBHOOK_URL"
