#!/usr/bin/env python3
import json
import logging
import subprocess
#import get_values
from flask import Flask, request, Response

# Static JSON file for configuration
JSON_FILE = "example.json"
# Logging initialization
logger = logging.getLogger(__name__)

app = Flask(__name__)

def get_values(key):
        try:
            with open(JSON_FILE) as f:
                data = json.load(f)
                return data[key]
        except Exception as err:
            print("ERROR: ", err)

# Running commands read by the get_values class
def run_shell_command():
    for sh_cmd in get_values("shell_command"):
        return_code = int(subprocess.call(sh_cmd, shell=True))
        if return_code == 0:
            logger.info(sh_cmd + ": successful")
            print(sh_cmd)
            return return_code
        else:
            logger.info(sh_cmd + ": failed")
            return return_code
  
def main():
    logging.basicConfig(filename=get_values("path_to_logs"), level=logging.INFO)
    # Flask initialization
    @app.route("/", methods=["GET"])
    def deploy():
        if request.method == 'GET':
            foo = print("Data received from Webhook is: ", request.json)
            run_shell_command()
            return foo 
        else:
            print("Request failed")
    
    app.run(host=get_values("ip_address"), port=get_values("port_number"))

if __name__ == "__main__":
	main()