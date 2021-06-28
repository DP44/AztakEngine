#!/usr/bin/env python3
import os
import subprocess
from time import sleep

def print_status(msg):  print(f"[\033[1;34m*\033[1;m] {msg}")
def print_failure(msg): print(f"[\033[1;31m-\033[1;m] {msg}")

# --------------------------------------------------------------------------
# DESCRIPTION:  Returns the process ID for the bot.
# --------------------------------------------------------------------------
def get_aztak_pid():
    procs = subprocess.check_output("ps aux | grep AztakEngine.py", 
                                    shell=True).decode().split('\n')
    bot_proc = ""

    proc_names = [
        "python3 /home/ec2-user/AztakEngine/AztakEngine.py",
        "sudo python3 AztakEngine.py"
    ]

    for proc in procs:
        # There's probably a cleaner way of doing this, but this 
        # is the only way i know of checking for multiple strings.
        for name in proc_names:
            if name in proc:
                bot_proc = proc
                break

    # If we find an empty string then that 
    # means there's no active bot process.
    if bot_proc == "":
        return ""

    proc_data = bot_proc.split(" ")

    # Iterate from end of list.
    for i in range(len(proc_data) - 1, -1, -1):
        # Remove any empty entries in proc_data.
        if proc_data[i] == "":
            proc_data.pop(i)

    # Return the second entry of the list as that is our process ID.
    return proc_data[1]

# --------------------------------------------------------------------------
# DESCRIPTION:  Parses the process output to get the PID and kills it, then
#               proceeds to open a new bot process.
# --------------------------------------------------------------------------
def proc_management():
    # Get the process ID of the bot.
    aztak_pid = get_aztak_pid()

    if aztak_pid != "":
        print_status("There's a process of the bot already running, " + 
                     "killing process.")

        # Kill the previous bot process.
        subprocess.Popen(f"kill {aztak_pid}", shell=True)

        # This is useless, it just feels more comfortable to do though.
        sleep(1) # Wait for 1 second.

    print_status("Running bot script.")

    # Start a new process.
    subprocess.Popen("python3 /home/ec2-user/AztakEngine/AztakEngine.py &", 
                     shell=True)

# --------------------------------------------------------------------------
# DESCRIPTION:  Our code entrypoint.
# --------------------------------------------------------------------------
def main():
    if os.getuid() == 0:
        # This is useless, it just feels more comfortable to do though.
        sleep(1) # Wait for 1 second.
        os.system('clear') # Clear the screen.
        sleep(0.5) # Wait for half a second

        # Run our actual code.
        proc_management()
    else:
        print_failure("Root privileges required!\n")

if __name__ == '__main__':
    main()
