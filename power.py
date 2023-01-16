#!/usr/bin/python3

# This is a special file that's run on the RasPi connected to the UPS powering
# my homelab. This is intended to be called by the NUT daemon to then spin
# off other routines. The `NOTIFYMSG` config of NUT has been modified to execute
# this script with either OFFLINE_NOTIFY, LOWBATT_NOTIFY, or SHUTDOWN_NOTIFY when
# evens occur.


import discord, nut2, sys
import power_control as control


def main(mode):
    from nut2 import PyNUTClient
    nutclient = PyNUTClient()
    current_status = nutclient.list_vars("ups")
    event = {}

    match mode:
        case "ONBATT_NOTIFY":
            # UPS just lost power from outlet
            event["title"] = "Power Failure Detected"
            event["message"] = "SeventhProtocol hardware is now running on a battery backup due to loss of power. Services will continue to operate on battery power; if power is not restored shortly, the servers will automatically shutdown to preserve hardware & data integrity."
            event["estimated_runtime"] = str(int(int(current_status["battery.runtime"].split(".")[0]) / 60))
            event["battery_percentage"] = str(int(current_status["battery.charge"].split(".")[0]))
            message_output = discord.generatePowerLossDiscordMessage(event)

        case "LOWBATT_NOTIFY" | "SHUTDOWN_NOTIFY" | "SHUTDOWN":
            # Low Battery, shut things down and message out
            event["title"] = "Servers Shutting Down Due to Power Outage"
            event["message"] = "SeventhProtocol hardware has been running on a battery backup that is now depleted. To protect the hardware & data integrity, the servers will now safely shutdown. They will not automatically return once power is restored. All SeventhProtocol services except Discord will be affected."
            event["estimated_runtime"] = str(int(int(current_status["battery.runtime"].split(".")[0]) / 60))
            event["battery_percentage"] = str(int(current_status["battery.charge"].split(".")[0]))
            message_output = discord.generatePowerLossDiscordMessage(event)
            control.hostsShutdown()

        case "ONLINE_NOTIFY":
            # UPS regained power, cancel all events
            event["title"] = "Power Event Concluded"
            event["message"] = "SeventhProtocol hardware is no longer running on a battery backup as line-power has been restored. Services are no longer intending to shut down."
            message_output = discord.generatePowerReturnDiscordMessage(event)

        case "COMMBAD":
           discord.generateInternalErrorDiscordMessage("Disconnected from UPS, communications bad")

        case "COMMOK":
           discord.generateInternalErrorDiscordMessage("Connection restored to UPS, monitoring power health")

        case _:
            # Unknown Argument
            print(f"Unknown mode '{mode}', not proceeding.")
            discord.generateInternalErrorDiscordMessage(f"Got unknown mode from NUT when running: {mode} ::: argv: {sys.argv}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Missing argument, need something like 'SHUTDOWN_NOTIFY'")
        sys.exit(1)

    try:
        main(sys.argv[1])
    except Exception as err:
        print("Error while running SparkPower: " + str(err))
        discord.generateInternalErrorDiscordMessage("Error while running SparkPower, check logs.")
        raise