import picamera
import time
import os
import json
import datetime

# Returns dict of JSON from file
def loadJSON(configPath):
    configDict = {}
    with open(configPath, 'r') as f:
        configDict = json.loads(f.read())
    return configDict

# Bool if given path exists or not
def directoryExists(directory):
    return os.path.exists(directory)
    
# Makes a given directory
def makeDirectory(directory):
    os.mkdir(directory)

configPath = "/boot/plantConfig.json"
config = loadJSON(configPath)
timeBetweenPics = int(config['timeInterval'])
rootDirectory = config['rootPicsDirectory']
startTime = int(config['startTime'])
endTime = int(config['endTime'])
getPics = True

while (getPics):
    # Gets time and file names
    now = datetime.datetime.now()
    folderName = str(now.month) + "-" + str(now.day) + "-" + str(now.year)
    fileName = str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)

    # Checks if its within picture taking time
    currentHour = now.hour
    if (now.hour > endTime or now.hour < startTime):
        print("Pic time is not allowed. Designated times are" + str(startTime) +  "-" + str(endTime) + " but got " + str(currentHour))
        time.sleep(timeBetweenPics)
        continue


    # Makes the day's folder if it doesn't exist
    if (not directoryExists(rootDirectory + folderName)):
        makeDirectory(rootDirectory + folderName)

    # Takes picture
    with picamera.PiCamera() as cam:
        fullFilePath = rootDirectory + folderName + "/" + fileName + ".jpg"
        cam.capture(fullFilePath)
        print("Took pic " + str(fileName) )

    # Waits designated time b/w pics
    time.sleep(timeBetweenPics)