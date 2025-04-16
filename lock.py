import time, os

import status, config

def getLock():
    try:
        # use 'X' mode to fail if this file already exists.
        with open(f"{config.Spark.LockFilePath}/.spark_is_running", 'x') as lockfile:
            lockfile.write(str(int(time.time())))
    except:
        print("Error trying to grab lockfile, is another Spark instance running?")
        raise

def releaseLock():
    os.remove(f"{config.Spark.LockFilePath}/.spark_is_running")