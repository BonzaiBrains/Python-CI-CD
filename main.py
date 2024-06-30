#!/usr/bin/env python3
import json
import logging
import subprocess
from flask import Flask, request

# Constant JSON file for configuration
JSON_FILE = "example.json"
# Logging initialization
logger = logging.getLogger(__name__)
# Flask initialization
app = Flask(__name__)


# Read values from configuration JSON file.
def get_values(key):
    try:
        with open(JSON_FILE) as f:
            data = json.load(f)
            return data[key]
    except Exception as err:
        print("ERROR: ", err)
        return err
    
def set_state(sh_cmd, return_code, state):
        return_state = {
            sh_cmd: return_code
        }
        state = dict(state + return_state)

# Iterating and executing through commands provisioned by POST request
def run_shell_command():
    state = {
        "0":"0"
    }
    for sh_cmd in request.json["shell_command"]:
        return_code = str(subprocess.call(sh_cmd, shell=True))
        if return_code == 0: # If the return code is zero then write to log successful
            logger.info("SUCCESSFUL: " + str(return_code))
            return_json = set_state(sh_cmd, return_code, state)
            
        else: 
            logger.info("FAILED: " + str(return_code))
            return_json = set_state(sh_cmd, return_code, state)
    
    return return_json
    
# Listen for webhooks and execute
@app.route(get_values("api_route"), methods=["POST"])
def webhook_listener(): 
    logger.info("Data received from Webhook is: ", request.json)
    if get_values("token") == request.json["token"]:
        return str(run_shell_command())
    else:
        return "AUTH FAILED"

if __name__ == "__main__":
    # Load configuration and run Flask app
    logging.basicConfig(filename=get_values("path_to_logs"), level=logging.INFO)
    app.run(host=get_values("ip_address"), port=get_values("port_number"))