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
password = 'xxxxx'
############### MODIFY VARIABLE END################

token = sys.argv[1] 
#liste pour définir les devices_class & les unit_of_measurement pour chaque type
liste = {
 "connected": ["connectivity", "\u200B"],
 "blocked": ["problem", "\u200B"],
 "in_current_state_since": ["\u200B", "timestamp"],
 "minutes_in_current_state": ["\u200B", "min"],
 "total_requests" : ["\u200B", "\u200B"],
 "successful_requests": ["\u200B", "\u200B"],
 "avg_success_rate": ["\u200B", "%"],
 "avg_success_rate_score": ["\u200B", "%"],
 "avg_reliability_score": ["\u200B", "%"],
 "avg_staked_capacity_percent": ["\u200B", "%"],
 "avg_utilization_percent": ["\u200B", "%"],
 "total_pre_earned": ["\u200B", "\u200B"],
 "rewardable_requests": ["\u200B", "\u200B"]
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
    print(f"Requesting {url=}")
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

        for x, valeurs in liste.items():
            if x == ["connected", "blocked"]: #binary_sensor
                discoveryTopic = f"homeassistant/binary_sensor/presearch/{node_id}_{x}/config";
                payload = '{"unique_id": "' + f"{node_id}_{x}" + '" , ' + '"name": "' + node["meta"]["description"] + '.' + x + '", "stat_t": "' + f"presearch_nodes/{node_id}/status/{x}" +'", ' + '"device_class": "' + valeurs[0] + '", "payload_on": true, "payload_off": false, "device": {"identifiers": ["'+ f"{g_deviceModel}_{node_id}"'"], "name": "' + node["meta"]["description"] + '", "model": "' + f"{g_deviceModel}" + '", "manufacturer": "' + f"{g_manufacturer}" + '", "sw_version": "' + f"{g_swVersion}" '+" }}'

            else:
                discoveryTopic = f"homeassistant/sensor/presearch/{node_id}_{x}/config";
                payload = '{"unique_id": "' + f"{node_id}_{x}" + '" , ' + '"name": "' + node["meta"]["description"] + '.' + x + '", ' +' "stat_t": "' + f"presearch_nodes/{node_id}/stats/{x}" +'", ' + '"unit_of_measurement": "' + valeurs[1] + '", "device": {"identifiers": ["' + f"{g_deviceModel}_{node_id}"'"], "name": "' + node["meta"]["description"] + '", "model": "' + f"{g_deviceModel}" + '", "manufacturer": "' + f"{g_manufacturer}" + '", "sw_version": "' + f"{g_swVersion}" + '" }}'

            client.publish(discoveryTopic,payload,0,retain=True)

def run():
    client = connect_mqtt()
    parse(client)
   
if __name__ == '__main__':
    run()