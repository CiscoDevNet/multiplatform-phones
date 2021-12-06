# Simple MPP Phone Remote SDK Example

## Host Computer Setup

  1. Copy this script to the host computer and make sure Python 2.7 or
     later is installed.
     
  1. Use the following command to install Python `websocker_server`
     package:
     
     ```bash
     pip install git+https://github.com/Pithikos/python-websocket-server
     ```
      
      OR
      
      Download/copy `websocket_server.py` from https://github.com/Pithikos/python-websocket-server to be in same directory as script
      
  > Note: the script's WebSocket server port is hard coded to be `12345`
  
## Phone Setup

  1. For MPP 11.3.1 or later phones go to **Phone** tab, and
     configure **Control Server URL** field to be:
     
     ```
     ws://<script-computer-ip>:12345/
     ```
     
     Where `<script_computer-ip>` is the IP of the host computer where
     script will be running.
     
  > The phones must be able to make an HTTP/WebSocket network
     connection to the host computer where script will be running.
  
## Running the script

1. Run the script using Python 2.7 or later:
    
    ```bash
    python remote_sdk_example.py
    ``` 
    
1. To view the JSON payloads, run the script using the `--debug` option:

    ```bash
    python remote_sdk_example.py --debug
    ```
  
  Or modify the script to set:  `DEBUG = True`
