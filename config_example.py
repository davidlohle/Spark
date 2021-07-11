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
    SeventhProtocol = "idontactuallylikegroupmeallthatmuch"

class Minecraft:
    Host = "myminecraftserver.com"
    Port = "25565"

class SyncLounge:
    URL = "https://mysyncserver.com/health"

class Requests:
    URL = "https://myrequestserver.com/v1/api/status"

class FileUpload:
    RemoteFile = "https://myserver.com/my-favorite-image.png"
    Upload_API = "https://mypomfserver.com/upload.php"

class DB:
    FilePath = os.path.dirname(os.path.abspath(__file__)) + "/statusDB.json"

class Teamspeak:
    Host = "teamiespeakie.com"