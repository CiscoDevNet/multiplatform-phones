# Simple MPP Phone Remote SDK Example

## Requirements

* Python 3.7+

## Host Computer Setup

1. Clone this repository to the host PC:

   ```bash
   git clone https://github.com/CiscoDevNet/multiplatform-phones.git
   ```

   and change into the directory:

   ```bash
   cd mutiplatform-phones
   ```

1. (Optional) Create and activate a [Python virtual environment](https://docs.python.org/3/library/venv.html):

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
1. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

Note: the server websocket port is hard coded as `12345`.  Modify `remote_sdk_play.py` accordingly to change this to another port:

```python
self.server = WebsocketServer(port=12345, host="0.0.0.0", loglevel=LOG_LEVEL)
```
  
## Phone Setup

For MPP 11.3.1 or later phones, go to **Phone** tab, and configure the **Control Server URL** field:
     
```
ws://<script-computer-ip>:12345/
```
   
where `<script_computer-ip>` is the IP of the host computer where the websocket server will be running.
   
> **Note:** The phones must be able to make an outbound HTTP/WebSocket network
     connection to the host computer.
  
## Running the Websocket Server

Launch the websocket server (with debugging enabled):

```bash
python remote_sdk_play.py --debug
```
