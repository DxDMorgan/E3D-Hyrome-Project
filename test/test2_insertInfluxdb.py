import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "<mesure_data>"
org = "<my-org>"
token = "<my-token>"
# Store the URL of your InfluxDB instance
url="http://localhost:8086"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

write_api = client.write_api(write_options=SYNCHRONOUS)

data = influxdb_client.Point("my_measurement").tag("location", "Prague").field("temperature", 25.3)
client.write_points(data, database='mesure_data', time_precision='ms', batch_size=10000, protocol='line')