import os

class Cachet:
    URL = "https://mycachetserver.com"
    Token = "mytoken"

class Plex:
    URL = "https://myplexserver.com"
    Token = "mytoken"

class GroupMe:
    VGF = "groupmebotchannel"
    Plex = "groupmebotchanel"

class SyncLounge:
    Host = "https://mysyncserver.com/health"

class DB:
    FilePath = os.path.dirname(os.path.abspath(__file__)) + "/statusDB.json"

class Teamspeak:
    Host = "teamiespeakie.com"