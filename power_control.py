
import config, subprocess, discord

def hostsShutdown():
    # Shutdown the Proxmox hosts first, then the NAS.
    discord.generateInternalErrorDiscordMessage("⚠️ All hardware beginning power down; battery is depleted ⚠️")
    for server in config.Servers.Hosts:
        subprocess.Popen(f"ssh {config.Servers.User}@{server}.local -i {config.Servers.SSHKeyPath} {config.Servers.ShutdownCommand}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).wait()
        discord.generateInternalErrorDiscordMessage(f"🔻{server.capitalize()} successfully shutdown")
    discord.generateInternalErrorDiscordMessage("⚠️ ALL HARDWARE POWERED OFF ::: SPARK STOP ⚠️")
