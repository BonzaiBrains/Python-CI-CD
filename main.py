#!/usr/bin/env python3
import json
import logging
import subprocess
from flask import Flask, request, Response

# Static JSON file for configuration
JSON_FILE = "example.json"
# Logging initialization
logger = logging.getLogger(__name__)
# Flask initialization
app = Flask(__name__)
app.run(host='0.0.0.0', port=65187)

A class for handeling configuration data
class plugin:
	def get_value_from_json(JSON_FILE, key, sub_key):
		try:
			with open(JSON_FILE) as f:
				data = json.load(f)
				return data[key][sub_key]
		except Exception as err:
			print("ERROR: ", err)

# Initialization of objects
	def __init__(self):
		self.shell_command = get_value_from_json("shell_command")
		self.api_key = get_value_from_json("api_key")
		self.path_to_logs = get_value_from_json("path_to_logs")

# Running commands read by the plugin class
def run_shell_command():
	for sh_cmd in plugin.shell_command():
		return_code = int(subprocess.call(plugin.shell_command(), shell=True))
		if return_code == 0:
			logger.info(sh_cmd + ": successful")
			return 0
		else:
			logger.info(sh_cmd + ": failed")
			return return_code
			continue

# Runs shell commands when webrequest is recieved
def deploy():
	if request.method == 'POST':
		print("Data received from Webhook is: ", request.json)
		run_shell_command()
		return 

def main():
	logging.basicConfig(filename=plugin.path_to_logs(), level=logging.INFO)
	@app.route("/"+ plugin.api_key + "/deploy", methods=["POST"])

if __name__ == '__main__':
    main()
