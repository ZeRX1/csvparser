# Imports
from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client import InfluxDBClient, Point, Dialect
from influxdb_client.client.write_api import SYNCHRONOUS
from reactivex import operators as ops
from collections import OrderedDict
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from tabulate import tabulate
from csv import DictReader
import reactivex as rx
import seaborn as sns
import pandas as pd
import os, sys
import random
import csv

load_dotenv()
client = InfluxDBClient.from_env_properties()
query_api = client.query_api()
token = os.getenv('INFLUXDB_V2_TOKEN')
org = os.getenv('INFLUXDB_V2_ORG')
url = os.getenv('INFLUXDB_V2_URL')

# * get the count of every row (Need to eliminate None values from queries as they break the dtype)
# * from(bucket: "downsampled")|> range(start: -30d)|> group(columns: ["host", "_field"], mode:"by")|> filter(fn: (r) => r._measurement == "V1P" or r._measurement == "V1S" or r._measurement == "Headstay") |> count()


# * Query the chosen bucket for CSV from the data (If the time range is not specified it will default to 1h)
def QueryCSV(bucket, time_range, stop_range):
    if not time_range:
        time_range = '-1h'
        stop_range = 'now()'
    csv_result = query_api.query_csv(f'from(bucket:"{bucket}") |> range(start: {time_range}, stop: {stop_range}) |> fill(usePrevious:true)',
        dialect=Dialect(header=False, 
        delimiter=",",
        comment_prefix="#", 
        annotations=[],
        date_time_format="RFC3339")
        )
    return csv_result
    
def parseCount(value):
    asd = pd.DataFrame(value, columns=['a','as','asd','asdf','asdfg','asdfgh','asdfghj','here'])
    count = asd['here'].values[4]
    return count
def saveCSVToFile(bucket, time_range):
    with open('influxdata.csv', 'w', encoding="UTF-8") as f:
        for rows in QueryCSV(bucket, time_range):
            writer = csv.writer(f)
            writer.writerow(rows)
            pass