import csv
import os
import pandas as pd
from influxdb_client import InfluxDBClient, Point, WriteOptions, Dialect
import pandas as pd
client = InfluxDBClient.from_env_properties()
query_api = client.query_api()

# Functions
def dataToDF(data):
    # Create a DataFrame
    value_name = ''
    tables = []
    for table in data:
        for line in table.records:
            # Make a clear table append needed values and then
            # add it to tables in order to make a dataframe right away
            oneresulttable = []
            oneresulttable.append(line.get_time())
            oneresulttable.append(line.get_value())
            tables.append(oneresulttable)
            # Name the columns for merging later
            value_name = "_" + line.get_measurement() + "_" + line.get_field()
    
    return pd.DataFrame(tables, columns=["_timestamp", value_name])

# export the dataframe to file 
# queryIDBToDF as the df, and name is just some identification stuff
# if you dont want to replace files
def exportDFToFile(df, name):
    df.to_csv(f'influx_{name}.csv', encoding='UTF-8',index=False)
    return "Action completed succesfully"

def queryIDBToDF(bucket, start_time, stop_time, measurement, field):
    # Make default values for start/stop_time and bucket
    # ! Make it better faster stronger
    return dataToDF(query_api.query(f'from(bucket:"{bucket}") |> range(start: {start_time}, stop: {stop_time}) |> filter(fn: (r) => r._measurement == "{measurement}") |> filter(fn: (r) => r._field == "{field}")'))

def mergeDF(dflist):
    # Loop through the dataframes in an array and merge them together
    iterator = 0
    for element in dflist:
        if iterator == 0:
            dataframe1 = element
            iterator += 1
            continue
        else:
            dataframe1 = pd.merge(dataframe1, element, on ='_timestamp', how ="outer")
        iterator += 1
    return dataframe1