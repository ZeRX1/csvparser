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

# ! TODO:
# ! Figure out how to use dataframes
# ! Make the graphs work
# ! Jupyter notebook
# ! Try to use modules instead of having a spaghetti of functions on the top
# ! Make the code work properly with the load cell data
# ? Timestream

##*#
# *   Sources used:
# *   https://github.com/influxdata/influxdb-client-python
##*#

##*#
# * Functions
##*#

# * Parsing the CSV data from DB to an array
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

# * Write to the database (Most likely wont be needed later)
def writeToInflux(client, bucket, name, tag1, tag2, field1, field2):
    write_api = client.write_api(write_options=SYNCHRONOUS)
    p = Point(name).tag(tag1, tag2).field(field1, field2)
    write_api.write(bucket=bucket, org=org, record=p)
    pass


# * used for the samples
# ? probably temporary (
def randcity():
    arrcity = ["New York", "Old York", "Test town", "Calm East", "Wild West", "Bruh town", "Warsaw", "Barcelona", "Madrid", "Berlin", "London", "Detroit", "Los Angeles", "London", "San Francisco"]

    randcity = arrcity[random.randrange(0,14)]
    return randcity
def randtemp():
    asd = random.randrange(0,50)
    return asd
def randadditional():
    asd = random.randrange(0,50)
    return asd
# ? )

# TODO: Try adding a second field to test if the graphs would work this way
# * function for adding sample data to the database 
# ? (probably temporary)
def SemiRandomSamples(client, bucket):
    for a in range(1,10,1):
        writeToInflux(client, bucket, 'my_measurement', 'location', randcity(), "lamps", randadditional())
        writeToInflux(client, bucket, 'my_measurement', 'location', randcity(), "temperature", randtemp())
    print("written")
    pass


# * Query the chosen bucket for CSV from the data (If the time range is not specified it will default to 1h)
def QueryCSV(bucket, time_range):
    if not time_range:
        time_range = "-1h"
    csv_result = query_api.query_csv(f'from(bucket:"{bucket}") |> range(start: {time_range})',
        dialect=Dialect(header=False, 
        delimiter=",",
        comment_prefix="#", 
        annotations=[],
        date_time_format="RFC3339")
        )
    return csv_result

##*#
# * Main function
##*#
if __name__ == "__main__":

    #*#
    #* Loading .env and connecting to influxDB
    #*#
    load_dotenv()
    bucket = 'testing2'
    time_range = '-1h' # ! Remember to set this to a negative number
    token = os.getenv('INFLUXDB_V2_TOKEN')
    org = os.getenv('INFLUXDB_V2_ORG')
    url = os.getenv('INFLUXDB_V2_URL')
    
    # TODO: make it connect with the db automatically without specifying arguments
    # TODO: [Here](https://github.com/influxdata/influxdb-client-python#via-environment-properties)
    client = InfluxDBClient(url=url, token=token, org=org)
    query_api = client.query_api()


    # * This function is adding sample data to the chosen database
    #SemiRandomSamples(client, bucket)


    # Printing out an array from the csv data pulled from the DB (debugging)
    # print(CSVToTable(QueryCSV(bucket, time_range)))
    
    # Saving the csv data for proper reading by matplotlib
    with open('influxdata.csv', 'w', encoding="UTF-8") as f:
        for rows in QueryCSV(bucket, time_range):
            writer = csv.writer(f)
            writer.writerow(rows)
            pass
    
    # Matplotlib graph (to be fixed ('temperature' not found or something))
    df = pd.read_csv("influxdata.csv")
    df.head()
    plt.bar(df['lamps'], df['temperature'])
    plt.xlabel("lamps")
    plt.ylabel("temperature")
    plt.title("Ratio")
    plt.xticks(df["lamps"])
    plt.show()
    
    # close the connection to the database
    client.close