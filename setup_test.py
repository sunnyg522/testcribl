#! /usr/bin/env python

import subprocess
import json
import os
import socket

target_host1 = {'tcp': 9997}
target_host2 = {'tcp':9998}
splitter_host = {'tcp': 9999}
# get hotname dynamically
host = socket.gethostname()

def create_target_config():
    """
        function to create target config folder
    """
    print ("Creating target config dir")
    input_data = target_host1
    app_data = {'mode': 'target'}
    output_data = {'file': 'events.log'}
    create_json_file("./target", input_data, "inputs.json")
    create_json_file("./target", app_data, "app.json")
    create_json_file("./target", output_data, "outputs.json")

def create_splitter_config():
    print("Create splitter config dir")
    input_data = splitter_host
    app_data = {'mode': 'splitter'}
    output_data = {'tcp': [{'host':host, 'port':target_host1['tcp']}, {'host':host, 'port':target_host1['tcp']}]}
    create_json_file("./splitter", input_data, "inputs.json")
    create_json_file("./splitter", app_data, "app.json")
    create_json_file("./splitter", output_data, "outputs.json")

def create_agent_config():
    print("Create agent config dir")
    input_data = {'monitor':"../inputs/large_1M_events.log"}
    app_data = {'mode': 'agent'}
    output_data = {'tcp':{'host':host, 'port':splitter_host['tcp']}}
    create_json_file("./agent", input_data, "inputs.json")
    create_json_file("./agent", app_data, "app.json")
    create_json_file("./agent", output_data, "outputs.json")

def create_json_file(path, data, file_name):
    print("Create a tcpfile in dir "+path+" file "+file_name)
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except Exception as e:
            print(e)
            raise
    with open(os.path.join(path, file_name), 'w') as outfile:
        json.dump(data, outfile)

def start_servers(cmd):
    print("Star npm server with command " + cmd)
    # subprocess.call(cmd, shell=True, to)
    # p = subprocess.Popen(cmd)

def create_configs():
    create_target_config()
    create_splitter_config()
    create_agent_config()

def cleaup():
     subprocess.call('rm -rf ./target', shell=True)
     subprocess.call('rm -rf ./splitter', shell=True)
     subprocess.call('rm -rf ./agent', shell=True)
     subprocess.call('rm *.log', shell=True)
     subprocess.call('pkill node', shell=True)

def validate_event_log():
    print("validating event file")
    num_lines = sum(1 for line in open('events.log'))
    print(num_lines)

def main():
    cleaup()
    create_configs()
    subprocess.call('node app.js ./target >> target.log 2>&1 &', shell=True)
    subprocess.call('node app.js ./splitter >> splitter.log 2>&1 &', shell=True)
    subprocess.call('node app.js ./agent', shell=True)
    validate_event_log()
    subprocess.call('pkill node', shell=True)

if __name__ == "__main__":
    main()