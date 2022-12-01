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
import random
import csv

####
# *   Sources used:
# *   https://github.com/influxdata/influxdb-client-python
####

##
# * Functions
##

def CSVToTable(csv_result):
    table = []
    for csv_line in csv_result:
        col = []
        if not len(csv_line) == 0:
            for csv_entry in csv_line:
                if not len(csv_entry) == 0:
                    col.append(csv_entry)
                table.append(col)
    return table

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


    arrcity = ["New York", "Old York", "Test town", "Calm East", "Wild West", "Bruh town"]

    randcity = arrcity[random.randrange(0,5)]
    randtemp = round(random.uniform(-10.00, 45.00), 2)

    for a in range(1,10,1):
        writeToInflux(client, 'testing', 'my_measurement', 'location', randcity, "temperature", randtemp)


    # CSV query and reading it line by line
    csv_result = query_api.query_csv(f'from(bucket:"{bucket}") |> range(start: {time_range})',
        dialect=Dialect(header=False, 
        delimiter=",",
        comment_prefix="#", 
        annotations=[],
        date_time_format="RFC3339")
        )
    
    print(CSVToTable(csv_result))



    print(table)
    
    
    
    df = pd.read_csv(csv_result)
    df.head()
    plt.bar(df['location'], df['temperature'])
    plt.xlabel("Location")
    plt.ylabel("Temperature")
    plt.title("Testing")
    plt.xticks(df["location"])
    plt.show()




    client.close

