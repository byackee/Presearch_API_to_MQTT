# Presearch_API_to_MQTT
Send Presearch API to MQTT (with Home Assistant discovery)

Presearch API Request Rate Limits:
  * Requests without stats (default, stats=false): Up to 4 requests per minute
  * Requests with stats (stats=true): Up to 4 requests per hour

Requirements:
  * Python3 & pip3
  * module paho-mqtt (pip3 install paho-mqtt)

Utilisation:
  1) In both file presearch-discovery.py & presearch.py, modify mqtt variable for connect your broker (ip, port, user, port)
  2) Launch 1 time script "python3 presearch-discovery.py your_api_token"
  3) Create cron (every minute) to run scrupt "python3 presearch.py your_api_token
