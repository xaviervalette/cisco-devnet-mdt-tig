# Cisco DevNet Model Driven Telemetry with TIG

## What is it ?
Telegraf, InfluxDB and Grafana (TIG) setup via Docker to collect Model Driven Telemetry (MDT):
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
+   ├── .env
    ├── docker-compose.yml
    ├── telegraf/
    │    └── ...
    ├── influxdb/
    │    └── ...
    └──  grafana/
         └── ...

```
 
3. In the `.env` file, add the following variables:
 
```env 
USERNAME=<your-username>
PASSWORD=<your-password>
INFLUXDB_ORG=<your-influxdb-org> 
INFLUXDB_BUCKET=<your-influxdb-bucket>
```
 
 <details>
   <summary> 
       <ins>Example</ins>
  </summary>
 
 ```env
USERNAME=admin
PASSWORD=admin
INFLUXDB_ORG=valettefamily.com
INFLUXDB_BUCKET=devnet
 ```
 </details>
  
⚠️ In the configurations files, I've set `INFLUXDB_ORG` to `valettefamily.com`and `ÌNFLUXDB_BUCKET` to `devnet`. If you decide to change those values, you will need to change them in the configuration files of telegraf, grafana and directly in the docker-compose.yml.

  
4. Go to `cisco-devnet-mdt-tig`, and start the TIG stack:
 ```console
 docker-compose up
 ```

 <details>
   <summary> 
       <ins>Expected output</ins>
  </summary>
  
 ```console
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
  | Output | <img width="300" alt="image" src="https://github.com/xaviervalette/cisco-devnet-mdt-tig/assets/28600326/6e200e1e-701a-43a2-97e8-d4c5eada2dfb"> | <img width="300" alt="image" src="https://github.com/xaviervalette/cisco-devnet-mdt-tig/assets/28600326/263a51de-911d-415b-9a9d-4176c86c6871"> |

  You can log in using the `$USERNAME` and `$PASSWORD` that you define in the `.env` file (`admin:admin` in the example)
