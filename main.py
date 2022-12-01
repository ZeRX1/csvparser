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

def SemiRandomSamples(client, bucket):
    arrcity = ["New York", "Old York", "Test town", "Calm East", "Wild West", "Bruh town", "Warsaw", "Barcelona", "Madrid", "Berlin", "London", "Detroit", "Los Angeles", "London", "San Francisco"]

    randcity = arrcity[random.randrange(0,5)]
    randtemp = round(random.uniform(-10.00, 45.00), 2)

    for a in range(1,10,1):
        writeToInflux(client, bucket, 'my_measurement', 'location', randcity, "temperature", randtemp)
        pass
    pass

def QueryCSV(bucket, time_range):
    csv_result = query_api.query_csv(f'from(bucket:"{bucket}") |> range(start: {time_range})',
        dialect=Dialect(header=False, 
        delimiter=",",
        comment_prefix="#", 
        annotations=[],
        date_time_format="RFC3339")
        )
    return csv_result

##
# * Main function
##

if __name__ == "__main__":

    ##
    #* Loading .env and connecting to influxDB
    ##
    load_dotenv()
    bucket = 'testing2'
    time_range = '-1h'
    token = os.getenv('INFLUXDB_V2_TOKEN')
    org = os.getenv('INFLUXDB_V2_ORG')
    url = os.getenv('INFLUXDB_V2_URL')
    
    # TODO: make it connect with the db automatically without specifying arguments
    # TODO: [Here](https://github.com/influxdata/influxdb-client-python#via-environment-properties)

    client = InfluxDBClient(url=url, token=token, org=org)

    query_api = client.query_api()

    SemiRandomSamples(client, bucket)
    # CSV query and reading it line by line
    
    print(CSVToTable(QueryCSV(bucket, time_range)))
    

    with open('influxdata.csv', 'w', encoding="UTF-8") as f:
        for rows in QueryCSV(bucket, time_range):
            writer = csv.writer(f)
            writer.writerow(rows)
            pass
    
    df = pd.read_csv("influxdata.csv")
    df.head()
    plt.bar(df['temperature'], df['temperature'])
    plt.xlabel("Temperature")
    plt.ylabel("Temperature")
    plt.title("Testing")
    plt.xticks(df["temperature"])
    plt.show()


    client.close

