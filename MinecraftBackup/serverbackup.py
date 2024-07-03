import os
from datetime import datetime
import subprocess
import argparse
import sys
import atexit
import signal

isBackupStarted = False
isBackupDone = False

def exit_handler():
    if isBackupStarted is True and isBackupDone is not True:
        with open("latest.dat", "r+") as file:
            lines = file.readlines()
            file.seek(0)
            file.truncate()
            lines = lines[:-1]
            for line in lines:
                file.write(line)
        print(f"Backup is cancelled.")

def kill_handler(*args):
    sys.exit(0)

atexit.register(exit_handler)
signal.signal(signal.SIGINT, kill_handler)
signal.signal(signal.SIGTERM, kill_handler)


def argumentParser():
    parser = argparse.ArgumentParser(description="Backs up Minecraft server")

    parser.add_argument("-server", metavar='path_to_server', 
                        type=str, nargs=1, required=True, 
                        help="Path of the server folder")
    parser.add_argument("-backup", metavar='path_to_save', 
                        type=str, nargs=1, required=True, 
                        help="Path to save the backup of the server")
    args = parser.parse_args()
    serverLocation = args.server[0]
    backupLocation = args.backup[0]
    return serverLocation, backupLocation

def readTimeFromFile(backupPath : str):
    dataFilePath = os.path.join(backupPath, "latest.dat")
    if(os.path.exists(dataFilePath) == False):
        with open(dataFilePath, 'w') as file: pass
    with open(dataFilePath, 'r') as file:
        lines = file.readlines()
        latestLine = ""
        if(len(lines) > 0):
            print(f"List of current backups:")
            for line in lines:
                print(f"{line.strip()}")
            latestLine = lines[-1]
            print(f"Latest backup date: {latestLine.strip()}")

def removeOldBackup(oldBackupNames : str, backupPath : str):
    for oldBackupName in oldBackupNames:
        backupName = "BackupServer-" + oldBackupName.strip() + ".7z"
        print(f"File to be removed : {os.path.join(backupPath, backupName)}")

        if os.path.exists(os.path.join(backupPath, backupName)):
            os.remove(os.path.join(backupPath, backupName))
            print(f"Old backup {backupName} was deleted.")
        else:
            print(f"Old backup does not exist! Removing the backup entry")

def saveTimeToFile(timeStr : str, backupPath : str):
    maxLines = 3
    lines = []
    dataFilePath = os.path.join(backupPath, "latest.dat")
    with open(dataFilePath, 'r') as file:
        lines = file.readlines()

    with open(dataFilePath, 'w') as file:
        if len(lines) > maxLines - 1:
            diffLines = len(lines) - maxLines + 1
            oldbackupNames = lines[0:diffLines]
            removeOldBackup(oldbackupNames, backupPath)
            lines = lines[diffLines:]

        for line in lines:
            file.write(line)

        print(f"Saved backup entry at {timeStr}")
        file.write(timeStr+"\n")
        global isBackupStarted
        isBackupStarted = True
    
def main():
    global isBackupDone
    serverLocation, backupLocation = argumentParser()

    if os.path.exists(serverLocation) == False:
        print(f"Server folder does not exist!")
        return -1
    if os.path.exists(backupLocation) == False:
        print(f"Backup folder does not exist!")
        return -1
    
    print(f"Minecraft Server Backup program")
    readTimeFromFile(backupLocation)

    print(f"Backing up now: ")
    timeStr = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    saveTimeToFile(timeStr, backupLocation)

    backupName = "BackupServer-" + timeStr + ".7z"
    serverPath = os.path.join(serverLocation)
    backupPath = os.path.join(backupLocation, backupName)
    print(f"Minecraft server location: {serverPath.__str__()}")
    subprocess.check_call(["7z", "a", backupPath.__str__(), serverPath.__str__(), "-xr!backups"])

    print(f"Backup {backupName} is complete")
    isBackupDone = True

if __name__ == '__main__':
    main()