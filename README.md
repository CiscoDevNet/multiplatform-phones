# Simple MPP Phone Remote SDK Example

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
