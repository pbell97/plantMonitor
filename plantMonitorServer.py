import picamera
import time
import os
import json
import datetime
from flask import Flask, jsonify, request, send_file, send_from_directory
from flask_sslify import SSLify
from flask_cors import CORS, cross_origin
import threading


app = Flask(__name__)
sslify = SSLify(app)
CORS(app, support_credentials=True)



# Returns dict of JSON from file
def loadJSON(configPath):
	configDict = {}
	with open(configPath, 'r') as f:
		configDict = json.loads(f.read())
	return configDict

# Saves a JSON
def saveJSON(configPath, config):
	configString = json.dumps(config)
	with open(configPath, 'w') as f:
		f.write(configString)

# Bool if given path exists or not
def directoryExists(directory):
	return os.path.exists(directory)
	
# Makes a given directory
def makeDirectory(directory):
	os.mkdir(directory)

configPath = "/boot/plantConfig.json"
config = loadJSON(configPath)
# int(config['timeInterval']) = int(config['timeInterval'])
# config['rootPicsDirectory'] = config['rootPicsDirectory']
# int(config['startTime']) = int(config['int(config['startTime'])'])
# int(config['endTime']) = int(config['int(config['endTime'])'])
getPics = True
cameraThread = None

# Routinely takes pictures
def takePictures():
	global configPath, config, getPics
	timeSinceLastPic = 0

	while (getPics):
		# Sleeps 5 seconds routinely to check if thread should end
		if (time.time() - timeSinceLastPic < int(config['timeInterval'])):
			time.sleep(5)
			continue


		# Gets time and file names
		now = datetime.datetime.now()
		folderName = str(now.month) + "-" + str(now.day) + "-" + str(now.year)
		fileName = str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)

		# Checks if its within picture taking time
		currentHour = now.hour
		if (now.hour > int(config['endTime']) or now.hour < int(config['startTime'])):
			print("Pic time is not allowed. Designated times are " + str(int(config['startTime'])) +  "-" + str(int(config['endTime'])) + " but got " + str(currentHour))
			time.sleep(int(config['timeInterval']))
			continue


		# Makes the day's folder if it doesn't exist
		if (not directoryExists(config['rootPicsDirectory'] + folderName)):
			makeDirectory(config['rootPicsDirectory'] + folderName)

		# Takes picture
		with picamera.PiCamera() as cam:
			time.sleep(1)
			fullFilePath = config['rootPicsDirectory'] + folderName + "/" + fileName + ".jpg"
			cam.capture(fullFilePath)
			print("Took pic " + str(fileName) )
			timeSinceLastPic = time.time()

	print("GetPics was false! Ending")
		

@app.route('/startCamera/', methods=['GET'])
def startCamera():
	global cameraThread, getPics
	if (not cameraIsOn()):
		getPics = True
		cameraThread = threading.Thread(target=takePictures)
		cameraThread.start()
		print("Started camera thread")
		returnObj = True
	else:
		returnObj = False

	return jsonify(returnObj), 200, {'Access-Control-Allow-Origin': '*'}

@app.route('/stopCamera/', methods=['GET'])
def stopCamera():
	global cameraThread, getPics
	if (cameraIsOn()):
		getPics = False
		time.sleep(6)
		cameraThread = None

	getPics = False

	return jsonify(True), 200, {'Access-Control-Allow-Origin': '*'}

# Status of camera
def cameraIsOn():
	global cameraThread
	if (cameraThread == None):
		return False
	else: 
		return True

@app.route('/cameraIsRunning/', methods=['GET'])
def cameraIsRunning():
	return jsonify(cameraIsOn()), 200, {'Access-Control-Allow-Origin': '*'}

@app.route('/currentView/', methods=['GET'])
@cross_origin(supports_credentials=True)
def getCurrentView():
	# Take a picture
	with picamera.PiCamera() as cam:
		time.sleep(1)
		fullFilePath = config['rootPicsDirectory'] + "currentView.jpg"
		cam.capture(fullFilePath)


	# Checks for a few seconds to see if it exists
	for i in range(5):
		if (os.path.isfile(config['rootPicsDirectory'] + "currentView.jpg")):
			return send_file(config['rootPicsDirectory'] + "currentView.jpg", attachment_filename='currentView.jpg'), 200, {'Access-Control-Allow-Origin': '*'}
		elif (i == 4):
			return "Picture wasn't taken", 500, {'Access-Control-Allow-Origin': '*'}


@app.route('/getPicture/<foldername>/<picture>', methods=['GET'])
@cross_origin(supports_credentials=True)
def getPicture(foldername, picture):
	# Checks for a few seconds to see if it exists
	return send_file(config['rootPicsDirectory'] + foldername + "/" + picture, attachment_filename=picture), 200, {'Access-Control-Allow-Origin': '*'}

@app.route('/getVideo/<foldername>/', methods=['GET'])
@cross_origin(supports_credentials=True)
def getVideo(foldername):
	# Checks for a few seconds to see if it exists
	return send_file(config['rootPicsDirectory'] + foldername + "/" + foldername + ".avi", attachment_filename=foldername + ".avi"), 200, {'Access-Control-Allow-Origin': '*'}


@app.route('/existingFolders/', methods=['GET'])
def getFolders():
	subFoldersAndFiles = os.listdir(config['rootPicsDirectory'])
	os.chdir(config['rootPicsDirectory'])
	subFoldersAndFiles = sorted(subFoldersAndFiles, key=os.path.getatime)
	folders = []
	for item in subFoldersAndFiles:
		if (os.path.isdir(config['rootPicsDirectory'] + item)):
			folders.append(item)
	
	return jsonify(folders), 200, {'Access-Control-Allow-Origin': '*'}

@app.route('/existingFiles/<folder>', methods=['GET'])
def getFiles(folder):
	subFoldersAndFiles = os.listdir(config['rootPicsDirectory'])
	if (folder not in subFoldersAndFiles):
		return "Folder not in root directory", 500, {'Access-Control-Allow-Origin': '*'}

	files = os.listdir(config['rootPicsDirectory'] + folder)
	os.chdir(config['rootPicsDirectory'] + folder)
	files = sorted(files, key=os.path.getatime)
	return jsonify(files), 200, {'Access-Control-Allow-Origin': '*'}

@app.route('/setTimeInterval/<interval>', methods=['GET'])
def setTimeInterval(interval):
	global config, configPath
	config['timeInterval'] = interval
	interval = int(interval)
	saveJSON(configPath, config)
	# int(config['timeInterval']) = interval
	return jsonify(True), 200, {'Access-Control-Allow-Origin': '*'}

@app.route('/setConfigs/', methods=['POST', 'OPTIONS'])
def setConfig():
	global config, configPath
	config = json.loads(request.form['config'])
	saveJSON(configPath, config)
	print(config)

	return jsonify(True), 200, {'Access-Control-Allow-Origin': '*'}

@app.route('/getConfig/', methods=['GET'])
def getConfig():
	global config
	return jsonify(config), 200, {'Access-Control-Allow-Origin': '*'}

@app.route('/', methods=['GET'])
def getMainPage():
	with open("plantPage.html", 'r') as f:
		pageData = f.read()
	return pageData, 200, {'Access-Control-Allow-Origin': '*'}

@app.route('/plantPage.js', methods=['GET'])
def getJSPage():
	return send_from_directory('.', plantPage.js), 200, {'Access-Control-Allow-Origin': '*'}


app.run(host="0.0.0.0", port=80, debug=True, threaded=True)

