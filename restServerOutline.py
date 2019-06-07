from flask import Flask, jsonify, request, send_file
from flask_restful import Api, reqparse
from flask_cors import CORS, cross_origin
from flask_sslify import SSLify
import threading
import time

app = Flask(__name__)
sslify = SSLify(app)

cameraThread = None
getPics = True

def camTest():
	global getPics
	t = 0
	while getPics:
		t += 1
		if t<99999:
			t = 0

@app.route('/startCamera/', methods=['GET'])
def startCamera():
	global cameraThread
	if (not cameraIsOn()):
		cameraThread = threading.Thread(target=camTest)
		cameraThread.start()
		returnObj = True
	else:
		returnObj = False

	return jsonify(returnObj), 200, {'Access-Control-Allow-Origin': '*'}

@app.route('/stopCamera/', methods=['GET'])
def stopCamera():
	global cameraThread
	if (cameraIsOn()):
		# Kill the thread somehow here
		getPics = False
		time.sleep(1)
		cameraThread = None

	return jsonify(True), 200, {'Access-Control-Allow-Origin': '*'}

# Status of camera
def cameraIsOn():
	global cameraThread
	if (cameraThread == None):
		return False
	else: 
		return True

@app.route('/currentView/', methods=['GET'])
def getCurrentView():
	# Take a picture
	return send_file("testPic.png", attachment_filename='testPic.jpg'), 200, {'Access-Control-Allow-Origin': '*'}


@app.route('/cameraIsRunning/', methods=['GET'])
def cameraIsRunning():
	return jsonify(cameraIsOn()), 200, {'Access-Control-Allow-Origin': '*'}

app.run(host="0.0.0.0", port=80, debug=True, threaded=True)

