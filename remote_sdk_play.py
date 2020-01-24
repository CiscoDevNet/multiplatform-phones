#!/usr/bin/env python
"""
Simple MPP Phone Remote SDK Example

Host Computer Setup:

  1. Copy this script to the host computer and make sure Python 2.7 or
     later is installed.

  2. Use the following command to install Python websocker_server
     package OR download/copy websocket_server.py from
     https://github.com/Pithikos/python-websocket-server to be in
     same directory as script:

        pip install git+https://github.com/Pithikos/python-websocket-server

  3. Note that script's WebSocket server port is hard coded to be 12345.

Phone Setup:

  1. For two MPP 11.3.1 or later phones go to "Phone" tab, and
     configure "Control Server URL" field to be:

       ws://<script-computer-ip>:12345/

     Where <script_computer-ip> is the IP of the host computer where
     script will be running.

  2. The phones must be able to make an HTTP/WebSocket network
     connection to the host computer where script will be running.

Running the script:

  1. Run the script using Python 2.7 or later:

     python remote_sdk_example.py

  2. If you want to 'see' the JSON payloads, run the script using the --debug option:

        python remote_sdk_example.py --debug

     Or modify the script to set:  DEBUG = True

"""

import json
import logging
import sys
import threading
import time
from websocket_server import WebsocketServer

DEBUG = False

class RemotePhone(object):
    def __init__(self, server, client):
        self.response_event = threading.Event()
        self.last_response = None
        self.server = server
        self.client = client

    def reconnected(self, server, client):
        self.server = server
        self.client = client
        self.last_response = None
        # abort if caller is already waiting
        self.response_event.set()
        self.response_event.clear()

    def connection_lost(self, server, client):
        if client != self.client:
            # already reconnected
            return

        # abort if caller is already waiting
        self.client = None
        self.response_event.set()
        self.response_event.clear()

    def make_api_call(self, payload):

        if self.response_event.is_set():
            raise Exception("Only one API call may be in 'in flight' at a time")

        message = json.dumps(payload)
        if DEBUG:
            print("Sending Request {}".format(message))

        self.server.send_message(self.client, message)
        self.response_event.wait(timeout=120)
        self.response_event.clear()
        return self.last_response

    def incoming_message(self, server, client, message):
        message = json.loads(message)
        if message['type'] == 'event':
            if DEBUG:
                print("Ignoring event {}".format(message))
            return
        if DEBUG:
            print("Received Respond {}".format(message))
        self.last_response = message
        # alert that we have a response back to client
        self.response_event.set()

class RemoteSdkServer(object):
    def __init__(self):
        # index clients by IP
        self.phone_dict = {}

        #
        self.client_connected_event = threading.Event()

        #self.server = WebsocketServer(12345, host='0.0.0.0', loglevel=logging.INFO)
        self.server = WebsocketServer(12345, host='0.0.0.0')
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_client_left(self.lost_client)
        self.server.set_fn_message_received(self.new_message)
        t1 = threading.Thread(name='websocket_server_thread',
                              target=self.server.run_forever)
        t1.daemon = True
        t1.start()

    def new_client(self, client, server):
        ip = client['address'][0]

        print("Phone {} connected".format(ip))
        if DEBUG:
            print("Phone {} info:".format(ip, client))

        phone = self.phone_dict.get(ip, None)

        if not phone:
            phone = RemotePhone(server, client)
            self.phone_dict[ip] = phone
        else:
            phone.reconnected(server, client)

        self.client_connected_event.set()
        self.client_connected_event.clear()


    def lost_client(self, client, server):
        ip = client['address'][0]
        print("Phone {} disconnected".format(ip))
        phone = self.phone_dict.get(ip, None)
        if phone:
            phone.connection_lost(server, client)
        self.client_connected_event.clear()

    def new_message(self, client, server, message):
        ip = client['address'][0]
        phone = self.phone_dict.get(ip, None)
        phone.incoming_message(server, client, message)

def basic_call():

    server = RemoteSdkServer()

    print("\nWaiting for phones to connect...")
    while len(server.phone_dict) < 2:
        server.client_connected_event.wait()

    print("\nPhones connected...")
    oPhone1, oPhone2 = list(server.phone_dict.values())[:2]

    print("\nGet Phone2 DND.")
    resp = oPhone2.make_api_call({"Request-URI": "/api/Config/v1/GetParams", 'params': ['DND_Setting']})
    phone2_DND = resp['result']['paramvalues']['DND_Setting']
    print("\nPhone 2 DND is ", phone2_DND)

    print("\nSet Phone2 DND.")
    resp = oPhone2.make_api_call({"Request-URI": "/api/Config/v1/SetParams", 'params': {'DND_Setting':'No'}})


    print("\nGet Phone2's number dynamically from the phone config.")
    resp = oPhone2.make_api_call({"Request-URI": "/api/Config/v1/GetParams", 'params': ['User_ID_1_']})
    phone2_number = resp['result']['paramvalues']['User_ID_1_']

    print('\nCall Phone1 -> Phone2')
    resp = oPhone1.make_api_call({"Request-URI": "/api/Call/v1/Dial", 'line':1, 'number': phone2_number})

    print('\nWait for Phone2 to be ringing...')
    time.sleep(2)

    print('\nAnswer Phone2')
    oPhone2.make_api_call({"Request-URI": "/api/Call/v1/Answer", 'line':1, 'callId': 0})
    time.sleep(2)

    print('\nGet Screen Capture')
    oPhone2.make_api_call({"Request-URI": "/api/Ui/v1/GetDeviceScreenshot", "uploadMethod": "PUT", 'url': "http://10.201.83.50:8000/"})
    
    print('\nGet Status')
    oPhone1.make_api_call({"Request-URI": "/api/Serviceability/v1/GetStatusFile"})
    
    print('\nLeave call up for 5 seconds')
    time.sleep(5)

    print('\nHangup')
    oPhone2.make_api_call({"Request-URI": "/api/Call/v1/Hangup", 'line':1, 'callId': 0})

    print('\nScript finished.')

def do_all():
    global DEBUG
    if len(sys.argv) == 2 and sys.argv[1] == '--debug':
        DEBUG = True
    basic_call()

if __name__ == '__main__':
    do_all()

