import time
import pprint
from sensors import FakeBME280Sensor, BME280Sensor
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import argparse

def create_sensor(fake: bool):
    if (fake):
        return FakeBME280Sensor()
    else:
        return BME280Sensor()

parser = argparse.ArgumentParser(description='Reads ')
parser.add_argument('-p', '--sample-period', type=int, default=1,
                    help='sleep time between sensor reads')
parser.add_argument('-f', '--fake-bme280', action='store_true',
                    help='specify to use the fake BME280 data source')
parser.add_argument('-i', '--influxdb-url', type=str, required=True,
                    help='InfluxDB URL to write the data')
parser.add_argument('-o', '--influxdb-org', type=str, required=True,
                    help='InfluxDB organization')
parser.add_argument('-t', '--influxdb-token', type=str, required=True,
                    help='InfluxDB token to authenticate')
parser.add_argument('-b', '--influxdb-bucket', type=str, required=True,
                    help='InfluxDB bucket to write the data')
args = parser.parse_args()

sample_period = 1
if args.sample_period and args.sample_period > 0:
    sample_period = args.sample_period

sensor = create_sensor(args.fake_bme280)

bucket = args.influxdb_bucket
client = InfluxDBClient(
    url=args.influxdb_url,
    token=args.influxdb_token,
    org=args.influxdb_org)
write_api = client.write_api(write_options=SYNCHRONOUS)

print(F"Sample Period: {sample_period}")
print(F"InfluxDB URL: {client.url}")
print(F"InfluxDB Org: {bucket}")
print(F"InfluxDB Bucket: {client.org}")

while True:
    print(F"reading from {sensor.name}...")
    
    sample = sensor.get_sample()

    point = Point("hygropi") \
        .tag("sensor", sensor.name) \
        .field("humidity", sample.humidity) \
        .field("pressure", sample.pressure) \
        .field("temp_c", sample.temp_c) \
        .field("temp_f", sample.temp_f)

    # point = Point.from_dict({
    #     'measurement': 'hygropi',
    #     'tags': {
    #         'sensor': sensor.name
    #     },
    #     'fields': sample.dict(),
    #     'time': sample.timestamp
    # }, write_precision=WritePrecision.NS)

    pprint.pprint(point.to_line_protocol())

    write_api.write(bucket=bucket, record=point)

    time.sleep(sample_period)
