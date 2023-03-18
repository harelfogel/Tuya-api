import logging
from tuya_connector import TuyaOpenAPI, TUYA_LOGGER

from flask import Flask, request
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

API_ENDPOINT = os.getenv('API_ENDPOINT')
ACCESS_ID = os.getenv('ACCESS_ID')
DEVICE_ID = os.getenv('DEVICE_ID')
ACCESS_KEY = os.getenv('ACCESS_KEY')


@app.route('/status', methods=["GET"])
def status():
    # Enable debug log
    TUYA_LOGGER.setLevel(logging.DEBUG)

    # Init OpenAPI and connect
    openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
    openapi.connect()

    # Get the status of a single device
    return openapi.get("/v1.0/iot-03/devices/{}/status".format(DEVICE_ID))


@app.route('/control', methods=['POST'])
def control_device():
    openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
    openapi.connect()

    data = request.json

    commands = {'commands': [data]}
    return openapi.post('/v1.0/iot-03/devices/{}/commands'.format(DEVICE_ID), commands)