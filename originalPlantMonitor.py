import picamera
import time
import os

files = os.listdir('/home/pi/Desktop/plantPics/')
latestNumber = 0

if (len(files) != 0):
        files.sort()
        latestFile = files[-1]
        latestNumber = latestFile.split('image')[-1].split('.jpg')[0]
        latestNumber = int(latestNumber)

latestNumber += 1
timeBetweenPics = 600


while (True):
        with picamera.PiCamera() as cam:
            imageName = '/home/pi/Desktop/plantPics/image' + str(latestNumber) + '.jpg'
            cam.capture(imageName)
            print("Took pic number " + str(latestNumber) )
            latestNumber += 1
            time.sleep(timeBetweenPics)