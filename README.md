# Cisco DevNet Model Driven Telemetry with TIG
[![Telegraf](https://img.shields.io/badge/Telegraf-1.26-red.svg)](https://hub.docker.com/_/telegraf)
[![Influx DB](https://img.shields.io/badge/InfluxDB-2.7-blue.svg)](https://hub.docker.com/_/influxdb)
[![Grafana](https://img.shields.io/badge/Grafana-9.4.1-yellow.svg)](https://hub.docker.com/r/grafana/grafana)

## What is it ?
Automated Telegraf, InfluxDB and Grafana (TIG) setup via Docker and Jinja template to collect Model Driven Telemetry (MDT):
<p align="center">
<img width="550" alt="image" src="https://github.com/xaviervalette/cisco-devnet-mdt-tig/assets/28600326/5182eab6-14ec-466b-bade-2c7ebe69fc7e">
<p>
 
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
  

  You can log in using the `$USERNAME` and `$PASSWORD` that you define in the `.env` file (`admin:admin` in the example)

 ## What's next ?
 
 You can start creating your own dashboards.
 
 To help you at this stage, I've created ready to use dashboards: 
 <details>
   <summary>
   <a href="https://github.com/xaviervalette/cisco-devnet-mdt-tig/blob/main/grafana/dashboards/cisco-meraki_global-stats.json">Cisco Meraki - Global stats</a>
  </summary>
  
   <h3 align="center">Dashboard</h3><hr>
  
  <p align="center">
<img width="800" alt="image" src="https://github.com/xaviervalette/cisco-devnet-mdt-tig/assets/28600326/45ae9888-d0e3-4475-8f5b-cd6253dd01b7">
  </p>
  
   <h3 align="center">Data</h3><hr>
 <hr></details>
 
  <details>
   <summary>
   <a href="https://github.com/xaviervalette/cisco-devnet-mdt-tig/blob/main/grafana/dashboards/cisco-catalyst-9800_clients-stats.json">Cisco Catalyst 9800 - Clients stats</a>
  </summary>
   
   <h3 align="center">Dashboard</h3><hr>
  <p align="center">
<img width="800" alt="image" src="https://github.com/xaviervalette/cisco-devnet-mdt-tig/assets/28600326/d0c90212-dda5-46a0-a713-3d6eaeb196bf">   </p>
   
   <h3 align="center">Data</h3><hr>

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
 </details>


## Going beyond
 
  If you want to securely access to your application (InfluxDB, Grafana) from outside your network, you can deploy a [Duo Network Gateway](https://duo.com/docs/dng) (reverse proxy + SAML IDP) → Check my repository [Cisco Duo Network Gateway Raspberry PI](https://github.com/xaviervalette/cisco-duo-network-gateway-raspberry-pi) for more details.
 
 <p align="center">
<img width="550" alt="image" src="https://github.com/xaviervalette/cisco-devnet-mdt-tig/assets/28600326/6c70093c-d5d3-42a1-813a-a3b736da104b">
 </p>
 

