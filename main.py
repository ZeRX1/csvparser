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
from additional import *
from dbhandling import *
import reactivex as rx
import seaborn as sns
import pandas as pd
import os, sys
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
# * Main function
##*#
if __name__ == "__main__":

    #*#
    #* Loading .env and connecting to influxDB
    #*#
    load_dotenv()
    #! Values are set here \/
    bucket = 'downsampled'
    time_range = '-90d' # ! Remember to set this to a negative number
    token = os.getenv('INFLUXDB_V2_TOKEN')
    org = os.getenv('INFLUXDB_V2_ORG')
    url = os.getenv('INFLUXDB_V2_URL')
    
    # TODO: make it connect with the db automatically without specifying arguments
    # TODO: [Here](https://github.com/influxdata/influxdb-client-python#via-environment-properties)
    client = InfluxDBClient.from_env_properties()
    query_api = client.query_api()

    # Printing out an array from the csv data pulled from the DB
    # print(CSVToTable(QueryCSV(bucket, time_range)))
    
    df = pd.DataFrame(QueryCSV(bucket, time_range), columns=['','','','TimeStamp1','TimeStamp2','Timestamp3','Force','load_value','measurename','','bool','numer'])

    print(df)
    print(df['Force'])

    # Matplotlib graph (to be fixed ('temperature' not found or something))
    # df = pd.read_csv("influxdata.csv", columns=['idk', 'id', 'idk', 'idk', 'idk', 'value', 'name', 'where in bucket', 'city'])
    df.head()
    plt.plot(df['TimeStamp3'], df['Force'])
    plt.xlabel("Time")
    plt.ylabel("Force")
    plt.title("Ratio")
    plt.xticks(df['TimeStamp3'])
    plt.show()
    
    # close the connection to the database
    client.close