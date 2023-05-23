# Cisco DevNet Model Driven Telemetry with TIG
[![Telegraf](https://img.shields.io/badge/Telegraf-1.26-red.svg)](https://hub.docker.com/_/telegraf)
[![Influx DB](https://img.shields.io/badge/InfluxDB-2.7-blue.svg)](https://hub.docker.com/_/influxdb)
[![Grafana](https://img.shields.io/badge/Grafana-9.4.1-yellow.svg)](https://hub.docker.com/r/grafana/grafana)

## What is it ?
Automated Telegraf, InfluxDB and Grafana (TIG) setup via Docker, Python and Jinja templates to collect Model Driven Telemetry (MDT):
<p align="center">
<img width="550" alt="image" src="https://github.com/xaviervalette/cisco-devnet-mdt-tig/assets/28600326/9fbc077f-1c55-48ea-a842-9a56abe092c6">

This project will help you to deploy a TIG stack in order to leverage quickly the MDT.
 
## Get started
 
1. Clone or download this repo

```console
git clone https://github.com/xaviervalette/cisco-devnet-mdt-tig
```

 2. Create the .env file as follow:
```diff
└── cisco-devnet-mdt-tig/
+   ├── config.yml
    ├── src/
    │   └── ...
    └── template/
        └── ...
```
 
3. In the `config.yml` file, add the following variables:
 
```yml
#config.yml
---
host: <your_host>
username: <your-username>
password: <your-password>
influxdb_org: <your-influxdb-org> 
influxdb_bucket: <your-influxdb-bucket>
influxdb_token: <your-token>
...

```
 
 <details>
   <summary> 
       <ins>Example</ins>
  </summary>
 
<p align="center">  <img width="550" alt="image" src="https://github.com/xaviervalette/cisco-devnet-mdt-tig/assets/28600326/807f1293-2854-4dc3-b2c1-f9ba45c06a50"></p>

 ```yml
#config.yml
---
host: 10.142.78.4
username: admin
password: admin
influxdb_org: valettefamily.com
influxdb_bucket: devnet
influxdb_token: test-token
...
 ```
 </details>
  
⚠️ After creating the `config.yml` file, you will need to generate the `docker-compose.yml` file and the required configuration files. To make it smooth, I've created template with `Jinja2`, so you will just have to run the following command:
```console
python3 src/generate-conf.py
```

The following files should be created:
```diff
└── cisco-devnet-mdt-tig/
    ├── config.yml
    ├── src/
    │   └── ...
    └── template/
    │   └── ...
+   ├── docker-compose.yml
+   ├── telegraf/
+   │   └── ...
+   └── grafana/
+       └── ...

```
  
4. Go to `cisco-devnet-mdt-tig`, and start the TIG stack:
 ```console
 docker-compose up
 ```

 <details>
   <summary> 
       <ins>Expected output</ins>
  </summary>
  
 ```console
xvalette@raspberrypi4:~$ cd cisco-devnet-mdt-tig/
xvalette@raspberrypi4:~/cisco-devnet-mdt-tig$ docker-compose up
Starting influxdb ... done
Starting telegraf ... done
Starting grafana  ... done
Attaching to influxdb, telegraf, grafana
...
 ```
 </details>

 5. Check that you have access to the following pages:
  
  
  | Service | InfluxDB GUI | Grafana GUI |
  | ------------- | ------------- | ------------- |
  | URL | `http://<your-device-IP>:8086` | `http://<your-device-IP>:3000` |
  | Example | `http://10.142.78.4:8086` | `http://10.142.78.4:3000` |
  | Output | <img width="400" alt="image" src="https://github.com/xaviervalette/cisco-devnet-mdt-tig/assets/28600326/6e200e1e-701a-43a2-97e8-d4c5eada2dfb"> | <img width="400" alt="image" src="https://github.com/xaviervalette/cisco-devnet-mdt-tig/assets/28600326/263a51de-911d-415b-9a9d-4176c86c6871"> |
  

  You can log in using the `username` and `password` that you define in the `config.yml` file (`admin:admin` in the example)

 ## What's next ?
 
 You can start creating your own dashboards.
 
 To help you at this stage, I've created ready to use dashboards: 
 <details>
   <summary>
   <a href="https://github.com/xaviervalette/cisco-devnet-mdt-tig/blob/main/grafana/dashboards/cisco-meraki_global-stats.json">Cisco Meraki - Global stats</a>
  </summary>
  <hr>
   <h3 align="center">Dashboard</h3>
  
  <p align="center">
<img width="800" alt="image" src="https://github.com/xaviervalette/cisco-devnet-mdt-tig/assets/28600326/01329fae-b918-4a97-ab3b-eef7e2c9e7f4">  </p>
  
   <h3 align="center">Data</h3>
  
  ```python
import requests
import json
from datetime import datetime, timedelta
import yaml
import time

def get_previous_hour_timestamp():
    # get the current time
    now = datetime.now()
    # subtract an hour from the current time
    previous_hour = now - timedelta(hours=1)
    previous_hour = previous_hour.replace(minute=0,second=0, microsecond=0)
    return(int(previous_hour.timestamp()))


def write_data_to_influxdb(host, org, bucket, precision, auth_token, payload):
    # Create the URL for writing data to the InfluxDB database
    url = f"http://{host}:8086/api/v2/write?org={org}&bucket={bucket}&precision={precision}"

    # Set the HTTP headers for the request
    headers = {
        "Authorization": f"Token {auth_token}",
        "Content-Type": "text/plain; charset=utf-8",
        "Accept": "application/json"
    }

    # Make the API request to write the data to the InfluxDB database
    response = requests.post(url, headers=headers, data=payload)

    # Return the status code of the API response
    return response.status_code


def get_poe_consumption():
    # Open the config.yml file and load its contents into the 'config' variable
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)

        # Loop through each network defined in the config file
        for network in config["meraki"]["networks"]:

            # Loop through each network defined in the config file
            for switch in network["devices"]["switches"]:
                
                # Get the current timestamp
                #current_timestamp = int(time.time())
                timestamp = get_previous_hour_timestamp()

                # Create the URL for retrieving all VLANs in the network
                url = f"https://api.meraki.com/api/v1/devices/{switch}/switch/ports/statuses?timespan=3600"

                # Set the HTTP headers for the request
                headers = {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "X-Cisco-Meraki-API-Key": config["meraki"]["api_key"]
                }

                # Empty payload
                payload = {}

                # Make the API request using the requests library
                response = requests.get(url, headers=headers, data=json.dumps(payload))

                # Print the status code of the response
                print("\nRequest status code : " + str(response.status_code) + "\n")

                # Parse the response as JSON
                responseJson = response.json()

                total_switch_poe = 0

                # Iterate through each port in the response
                for port in responseJson:
                    # Skip over ports 9 and 10
                    if port["portId"] not in ["9", "10"]:
                        # Calculate the POE usage for the current port
                        poe_usage = port["powerUsageInWh"]
                        total_switch_poe = total_switch_poe + port["powerUsageInWh"]
                
                payload = f'meraki,device={switch} poeUsage={total_switch_poe} {timestamp}'

                # Print the payload string
                print(payload)

                # Write the payload data to the InfluxDB database
                status_code = write_data_to_influxdb(
                    host=config["influxdb"]["host"],
                    org=config["influxdb"]["org"],
                    bucket=config["influxdb"]["bucket"],
                    precision="s",
                    auth_token=config["influxdb"]["api_key"],
                    payload=payload
                )

                # Print the status code of the write_data() API response
                print(status_code)



def get_clients_usage():
    # Open the config.yml file and load its contents into the 'config' variable
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)

        # Loop through each network defined in the config file
        for network in config["meraki"]["networks"]:

            # Get the current timestamp
            current_timestamp = int(time.time())

            # Create the URL for retrieving all VLANs in the network
            url = f"https://api.meraki.com/api/v1/networks/{network['network_id']}/clients?timespan=600"
            print(url)

            # Set the HTTP headers for the request
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-Cisco-Meraki-API-Key": config["meraki"]["api_key"]
            }

            # Empty payload
            payload = {}

            # Make the API request using the requests library
            response = requests.get(url, headers=headers, data=json.dumps(payload))

            # Print the status code of the response
            print("\nRequest status code : " + str(response.status_code) + "\n")

            # Parse the response as JSON
            responseJson = response.json()
            print(responseJson)

            for client in responseJson:
                # Iterate through each port in the response
                # Format the payload string with the POE usage data
                payload = f'meraki,client={client["mac"]} downloadKbytes={client["usage"]["recv"]} {current_timestamp}'

                # Write the payload data to the InfluxDB database
                status_code = write_data_to_influxdb(
                    host=config["influxdb"]["host"],
                    org=config["influxdb"]["org"],
                    bucket=config["influxdb"]["bucket"],
                    precision="s",
                    auth_token=config["influxdb"]["api_key"],
                    payload=payload
                )

                payload = f'meraki,client={client["mac"]} uploadKbytes={client["usage"]["sent"]} {current_timestamp}'
                
                # Write the payload data to the InfluxDB database
                status_code = write_data_to_influxdb(
                    host=config["influxdb"]["host"],
                    org=config["influxdb"]["org"],
                    bucket=config["influxdb"]["bucket"],
                    precision="s",
                    auth_token=config["influxdb"]["api_key"],
                    payload=payload
                )

            # Print the status code of the write_data() API response
            print(status_code)
 ``` 
 <hr></details>
 
  <details>
   <summary>
   <a href="https://github.com/xaviervalette/cisco-devnet-mdt-tig/blob/main/grafana/dashboards/cisco-catalyst-9800_clients-stats.json">Cisco Catalyst 9800 - Clients stats</a>
  </summary>
   <hr>
   <h3 align="center">Dashboard</h3>
  <p align="center">
<img width="800" alt="image" src="https://github.com/xaviervalette/cisco-devnet-mdt-tig/assets/28600326/d0c90212-dda5-46a0-a713-3d6eaeb196bf">   </p>
   
   <h3 align="center">Data</h3>

  Example of configuration required on the C9800 to send the expected telemetry:
 
  <p align="center">
 <img width="400" alt="image" src="https://github.com/xaviervalette/cisco-devnet-mdt-tig/assets/28600326/03ff5717-f108-499b-ada3-b6a3c1d78ad6">
   </p>
   
  ```config
!
! TRAFFIC STATS
!
telemetry ietf subscription 101
 encoding encode-kvgpb
 filter xpath /client-oper-data/traffic-stats/bytes-tx
 source-address 192.168.1.98
 stream yang-push
 update-policy periodic 60000
 receiver ip address 10.142.78.4 57000 protocol grpc-tcp
!
telemetry ietf subscription 102
 encoding encode-kvgpb
 filter xpath /client-oper-data/traffic-stats/bytes-rx
 source-address 192.168.1.98
 stream yang-push
 update-policy periodic 60000
 receiver ip address 10.142.78.4 57000 protocol grpc-tcp
!
! CLIENTS STATS
!
telemetry ietf subscription 110
 encoding encode-kvgpb
 filter xpath /wireless-mobility-oper:mobility-oper-data/wlan-client-limit
 source-address 192.168.1.98
 stream yang-push
 update-policy on-change
 receiver ip address 10.142.78.4 57000 protocol grpc-tcp
```
   <hr>
 </details>
 
   <details>
   <summary>
    Cisco Catalyst 9300 - Sustanability
  </summary>
  Coming...<hr>
 <hr></details>


## Going beyond
 
  If you want to securely access to your application (InfluxDB, Grafana) from outside your network, you can deploy a [Duo Network Gateway](https://duo.com/docs/dng) (reverse proxy + SAML IDP) → Check my repository [Cisco Duo Network Gateway Raspberry PI](https://github.com/xaviervalette/cisco-duo-network-gateway-raspberry-pi) for more details.
 
 <p align="center">
<img width="550" alt="image" src="https://github.com/xaviervalette/cisco-devnet-mdt-tig/assets/28600326/6c70093c-d5d3-42a1-813a-a3b736da104b">
 </p>
 

