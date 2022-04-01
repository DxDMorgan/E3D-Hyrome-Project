from influxdb import InfluxDBClient

json_body = [
    {
        "measurement": "brushEvents",
        "tags": {
            "user": "Carol",
            "brushId": "1bd86a69-d9e7-4711-8ee7-8ec2965d86b6"
        },
        "fields": {
            "duration": 127
        }
    },
    {
        "measurement": "brushEvents",
        "tags": {
            "user": "Antoine",
            "brushId": "832e1bdc-c23d-44c3-a939-3b964befd0a2"
        },
        "fields": {
            "duration": 132
        }
    },
    {
        "measurement": "brushEvents",
        "tags": {
            "user": "Sebastien",
            "brushId": "3c307007-f9ee-470e-8a84-f931c421b292"
        },
        "fields": {
            "duration": 129
        }
    }
]


client = InfluxDBClient(host='localhost', port=8086)
#client = InfluxDBClient(host='mydomain.com', port=8086, username='myuser', password='mypass' ssl=True, verify_ssl=True)
client.switch_database('pytest')
client.write_points(json_body)
