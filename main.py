#!/usr/bin/env python3
import json
import logging

def get_value_from_json(json_file, key, sub_key):
		try:
			with open(json_file) as f:
				data = json.load(f)
				return data[key][sub_key]
		except Exception as e:
			print("ERROR: ", e)

def main():
    shell_command: get_value_from_json("shell_command")
    

if __name__ == '__main__':
    main()
