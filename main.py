# Imports
from tabulate import tabulate
import os, sys
from influxdb_client import InfluxDBClient, Point, Dialect
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv
from collections import OrderedDict
from csv import DictReader
import reactivex as rx
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from reactivex import operators as ops
from influxdb_client import InfluxDBClient, Point, WriteOptions
  ## gran autismo
####
# *   Sources used:
# *   https://github.com/influxdata/influxdb-client-python
####

##
# * Functions
##

def writeToInflux(client, bucket, name, tag1, tag2, field1, field2):
    write_api = client.write_api(write_options=SYNCHRONOUS)
    p = Point(name).tag(tag1, tag2).field(field1, field2)
    write_api.write(bucket=bucket, org=org, record=p)
    pass

##
# * Main function
##

if __name__ == "__main__":

    ##
    #* Loading .env and connecting to influxDB
    ##
    load_dotenv()
    bucket = 'testing'
    time_range = '-24h'
    token = os.getenv('INFLUXDB_V2_TOKEN')
    org = os.getenv('INFLUXDB_V2_ORG')
    url = os.getenv('INFLUXDB_V2_URL')
    
    # TODO: make it connect with the db automatically without specifying arguments
    # TODO: [Here](https://github.com/influxdata/influxdb-client-python#via-environment-properties)

    client = InfluxDBClient(url=url, token=token, org=org)

    query_api = client.query_api()

    ##
    #* This one is for adding values to the DB to test things
    ##

    # for a in range(1,10,1):
    #     writeToInflux(client, 'testing', 'my_measurement', 'location', 'Old York', "temperature", 13.1)


    # CSV query and reading it line by line
    csv_result = query_api.query_csv(f'from(bucket:"{bucket}") |> range(start: {time_range})',
        dialect=Dialect(header=False, 
        delimiter=",",
        comment_prefix="#", 
        annotations=[],
        date_time_format="RFC3339")
        )
    

    i = 0
    x = 0
    table = [[1],[2],[3]]
    for csv_line in csv_result:
        i += 1
        if not len(csv_line) == 0:
            for csv_entry in csv_line:
                x += 1
                if not len(csv_entry) == 0:
                    print(csv_entry + str(i) + str(x))
                    table[i][x] = csv_result[i][x]

        print(f"\n (mt)")



    # for csv_line in csv_result:
    #     if not len(csv_line) == 0:
    #         print(f'Temperature in {csv_line[9]} is {csv_line[6]}')


    client.close

