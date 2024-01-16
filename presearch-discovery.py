# python 3.6
 
import uuid
import json
import time
import sys
from datetime import timedelta, datetime
from os import environ
 
from requests import get
from paho.mqtt import client as mqtt_client

############### MODIFY VARIABLE BELOW #############
broker = '192.168.xxx.xxx'
port = 1883
topic = "presearch_nodes"
# Generate a Client ID with the publish prefix.
client_id = 'presearch'
username = 'mqtt'
password = 'xxxxxx'
############### MODIFY VARIABLE END################

token = sys.argv[1]
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
 
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
 
def parse(client): 
    url = f"https://nodes.presearch.org/api/nodes/status/{token}"
    res = get(url=url,  verify=False)
    data = res.json()
    nodes = data.pop("nodes", {})
    if res.status_code != 200:
        print(f"Error {data}")
 
    g_deviceModel = "Presearch";                           
    g_swVersion = "0.9";                                     
    g_manufacturer = "Byackee";                              
    g_deviceName = "Presearch";

    # Create metrics per node
    for node_pub, node in nodes.items():
        node_id = uuid.uuid5(uuid.NAMESPACE_DNS, node_pub).hex.upper()
        print(node)


        #boucle pour binary_sensor
        data = ["connected", "blocked"]
        for i in data:
            #Payload for status connection
            discoveryTopic = f"homeassistant/binary_sensor/presearch/{node_id}_{i}/config";
            payload = '{"unique_id": "' + f"{node_id}_{i}" + '" , ' + '"name": "' + node["meta"]["description"] + '.' + i + '", "stat_t": "' + f"presearch_nodes/{node_id}/status/{i}" +'", ' + '"payload_on": true, "payload_off": false, "device": {"identifiers": ["'+ f"{g_deviceModel}_{node_id}"'"], "name": "' + node["meta"]["description"] + '", "model": "' + f"{g_deviceModel}" + '", "manufacturer": "' + f"{g_manufacturer}" + '", "sw_version": "' + f"{g_swVersion}" '+" }}'
            client.publish(discoveryTopic,payload,0,retain=True)

        #boucle pour stats
        data = ["in_current_state_since", "minutes_in_current_state", "total_requests", "successful_requests", "avg_success_rate", "avg_success_rate_score", "avg_reliability_score", "avg_staked_capacity_percent", "avg_utilization_percent", "total_pre_earned", "rewardable_requests"]
        for s in data:
            #Payload for stats/successful_requests
            discoveryTopic = f"homeassistant/sensor/presearch/{node_id}_{s}/config";
            payload = '{"unique_id": "' + f"{node_id}_{s}" + '" , ' + '"name": "' + node["meta"]["description"] + '.' + s + '", ' +' "stat_t": "' + f"presearch_nodes/{node_id}/stats/{s}" +'", ' + '"device": {"identifiers": ["'+ f"{g_deviceModel}_{node_id}"'"], "name": "' + node["meta"]["description"] + '", "model": "' + f"{g_deviceModel}" + '", "manufacturer": "' + f"{g_manufacturer}" + '", "sw_version": "' + f"{g_swVersion}" '+" }}'
            client.publish(discoveryTopic,payload,0,retain=True)
 
 
 
def run():
    client = connect_mqtt()
    parse(client)
 
   
if __name__ == '__main__':
    run()
