import time, os

import status, config

def getLock():
    try:
        # use 'X' mode to fail if this file already exists.
        with open(".spark_is_running", 'x') as lockfile:
            lockfile.write(str(int(time.time())))
    except:
        print("Error trying to grab lockfile, is another Spark instance running?")
        # notify me to get feedback on whether or not lockfile contention is an issue
        status.notifyGroupMe("Error grabbing lockfile", config.GroupMe.SeventhProtocol)
        raise

def releaseLock():
    os.remove(".spark_is_running")