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
password = 'xxxx'
############### MODIFY VARIABLE END################

token = sys.argv[1] 
#liste pour définir les devices_class & les unit_of_measurement pour chaque type
liste = {
 "connected":  ["connectivity", "none"],
 "blocked":  ["problem", "none"],
 "in_current_state_since": ["none", "timestamp"],
 "minutes_in_current_state": ["none", "min"],
 "total_requests" : ["none", "none"],
 "successful_requests": ["none", "none"],
 "avg_success_rate": ["none", "none"],
 "avg_success_rate_score": ["none", "none"],
 "avg_reliability_score": ["none", "none"],
 "avg_staked_capacity_percent": ["", "%"],
 "avg_utilization_percent": ["none", "%"],
 "total_pre_earned": ["none", "none"],
 "rewardable_requests": ["none", "none"]
 }



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

        #boucle pour binary_sensor
        data = ["connected", "blocked"]
        for i in data:
            for x, valeurs in liste.items():
                if x == i:
                    #Payload for status connection
                    discoveryTopic = f"homeassistant/binary_sensor/presearch/{node_id}_{i}/config";
                    payload = '{"unique_id": "' + f"{node_id}_{i}" + '" , ' + '"name": "' + node["meta"]["description"] + '.' + i + '", "stat_t": "' + f"presearch_nodes/{node_id}/status/{i}" +'", ' + '"devices_class": "' + valeurs[0] + '", "payload_on": true, "payload_off": false, "device": {"identifiers": ["'+ f"{g_deviceModel}_{node_id}"'"], "name": "' + node["meta"]["description"] + '", "model": "' + f"{g_deviceModel}" + '", "manufacturer": "' + f"{g_manufacturer}" + '", "sw_version": "' + f"{g_swVersion}" '+" }}'
                    client.publish(discoveryTopic,payload,0,retain=True)
                    #print(payload)

        #boucle pour stats
        data = ["in_current_state_since", "minutes_in_current_state", "total_requests", "successful_requests", "avg_success_rate", "avg_success_rate_score", "avg_reliability_score", "avg_staked_capacity_percent", "avg_utilization_percent", "total_pre_earned", "rewardable_requests"]
        for s in data:
            for x, valeurs in liste.items():
                if x == s:
                    #Payload for stats/successful_requests
                    discoveryTopic = f"homeassistant/sensor/presearch/{node_id}_{s}/config";
                    payload = '{"unique_id": "' + f"{node_id}_{s}" + '" , ' + '"name": "' + node["meta"]["description"] + '.' + s + '", ' +' "stat_t": "' + f"presearch_nodes/{node_id}/stats/{s}" +'", ' + '"unit_of_measurement": "' + valeurs[0] + '", "device": {"identifiers": ["' + f"{g_deviceModel}_{node_id}"'"], "name": "' + node["meta"]["description"] + '", "model": "' + f"{g_deviceModel}" + '", "manufacturer": "' + f"{g_manufacturer}" + '", "sw_version": "' + f"{g_swVersion}" + '" }}'
                    client.publish(discoveryTopic,payload,0,retain=True)
                    #print(payload)
 
 
def run():
    client = connect_mqtt()
    parse(client)
   
if __name__ == '__main__':
    run()