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
