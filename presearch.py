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
DEFAULT_SINCE_MINUTES = 15
ALLOWED_STATS_MINUTES = [0, 15, 30, 45]
 
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
    utcnow = datetime.utcnow()
    stats = utcnow.minute in ALLOWED_STATS_MINUTES
    url = f"https://nodes.presearch.org/api/nodes/status/{token}"
    params = {}
    if stats:
        start_date = utcnow - timedelta(minutes=DEFAULT_SINCE_MINUTES)
        params = {
            "start_date": start_date.strftime("%Y-%m-%d %H:%M"),
            "stats": "true"
        }
    print(f"Requesting {url=}, {params=}")
    res = get(url=url, params=params, verify=False)
    data = res.json()
    nodes = data.pop("nodes", {})
    #print(f"{data}")
    if res.status_code != 200:
        print(f"Error {data}")
 
    # Create metrics per node
    for node_pub, node in nodes.items():
        node_id = uuid.uuid5(uuid.NAMESPACE_DNS, node_pub).hex.upper()
        result = client.publish(f"{topic}/{node_id}/node_description", node["meta"]["description"] )
        result = client.publish(f"{topic}/{node_id}/sw_version", node["meta"]["version"] )
        result = client.publish(f"{topic}/{node_id}/url", node["meta"]["url"] )
        result = client.publish(f"{topic}/{node_id}/gateway_pool", node["meta"]["gateway_pool"] )
        result = client.publish(f"{topic}/{node_id}/remote_addr", node["meta"]["remote_addr"] )
        result = client.publish(f"{topic}/{node_id}/status/connected", node["status"]["connected"] )
        result = client.publish(f"{topic}/{node_id}/status/blocked", node["status"]["blocked"] )


        #stats
        if stats:
            result = client.publish(f"{topic}/{node_id}/stats/in_current_state_since", node["status"]["in_current_state_since"] )
            result = client.publish(f"{topic}/{node_id}/stats/minutes_in_current_state", node["status"]["minutes_in_current_state"] )
            result = client.publish(f"{topic}/{node_id}/stats/total_requests", node["period"]["total_requests"] )
            result = client.publish(f"{topic}/{node_id}/stats/successful_requests", node["period"]["successful_requests"] )
            result = client.publish(f"{topic}/{node_id}/stats/avg_success_rate", node["period"]["avg_success_rate"] )
            result = client.publish(f"{topic}/{node_id}/stats/avg_success_rate_score", node["period"]["avg_success_rate_score"] )
            result = client.publish(f"{topic}/{node_id}/stats/avg_reliability_score", node["period"]["avg_reliability_score"] )
            result = client.publish(f"{topic}/{node_id}/stats/avg_staked_capacity_percent", node["period"]["avg_staked_capacity_percent"] )
            result = client.publish(f"{topic}/{node_id}/stats/avg_utilization_percent", node["period"]["avg_utilization_percent"] )
            result = client.publish(f"{topic}/{node_id}/stats/total_pre_earned", node["period"]["total_pre_earned"] )
            result = client.publish(f"{topic}/{node_id}/stats/rewardable_requests", node["period"]["rewardable_requests"] )




        # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send successfull to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")
 
 
 
def run():
    client = connect_mqtt()
    client.loop_start()
    parse(client)
   
if __name__ == '__main__':
    run()
 
