# Presearch_API_to_MQTT
Send Presearch API to MQTT (with Home Assistant discovery)

# Limitation
  Presearch API Request Rate Limits:
    * Requests without stats (default, stats=false): Up to 4 requests per minute
    * Requests with stats (stats=true): Up to 4 requests per hour

## Requirements:
  * Python3 & pip3
  * module paho-mqtt (pip3 install paho-mqtt)

## Utilisation:
  1) In both file presearch-discovery.py & presearch.py, modify mqtt variable for connect your broker (ip, port, user, port)
  2) Launch 1 time script "python3 presearch-discovery.py your_api_token"
  3) Create cron (every minute) to run scrupt "python3 presearch.py your_api_token

## How its work:
With your cron the script give the main data from presearch API and every 15 minutes add stats data (limited to 4 requests per hour) and send all to your MQTT broker.

## Credits

This codebase is inspired by
- [presearch-exporter](https://github.com/b-n-space/presearch-exporter)
 Similar service by [Bᴺ Space]([https://github.com/Zibby](https://github.com/b-n-space))
- [How to monitor your PRESEARCH nodes with prometheus and grafana ?](https://libremaster.com/presearch-node-grafana/)
  Amazing guide by [Christophe T.](https://libremaster.com/contact/) on how to implement Prometheus/Grafana monitoring
  for Presearch.
- [A prometheus exporter for presearch.io nodes written in go](https://github.com/Zibby/presearch-node-exporter)
  Similar service by [Zibby](https://github.com/Zibby)

## Todo
- [x] Functional code
- [ ] Cleanup and add more docs on complete installation
- [ ] Improve/Optimize code
- [ ] Add more features & personalization

## Donation
  [Support via PayPal](https://www.paypal.me/byackee/)
  
  Eth: 0x7F57f6ad25c501deb2fcaCA863264F593efe31d8
  
  Flux: t1U3ubvVNhCHFkzGYZV52huyE4a1MGh3ymE
