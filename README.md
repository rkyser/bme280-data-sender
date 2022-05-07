# BME280 Data Sender

Reads environment data from a BME280 sensor and sends it periodically to an InfluxDB2 instance.

## Getting Started

1. Clone this repo to your Raspberry PI
2. `cd` to the repo's root directory
2. Run the following commands
```
pip3 install pipenv
pipenv install
pipenv --three
pipenv shell
python3.9 bme280-data-sender [see args below]
```

- `--sample-period` : Sleep time between sensor reads (optional)
- `--influxdb-url` : InfluxDB URL to connect to (required)
- `--influxdb-org` : InfluxDB organization (required)
- `--influxdb-token` : InfluxDB token to authenticate with (required)
- `--influxdb-bucket` : InfluxDB bucket to write the data (required)

## TODO

1. Add systemd start script for installing on Raspberry PI
   - https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/
2. Find a pipenv-free method of installing on RPI
