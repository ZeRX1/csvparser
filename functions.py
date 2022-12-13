import csv
import os
import pandas as pd
import json
import matplotlib.pyplot as plt
from influxdb_client import InfluxDBClient, Point, WriteOptions, Dialect
import pandas as pd
client = InfluxDBClient.from_env_properties()
query_api = client.query_api()

# Functions
def dataToDF(data):
    # Create a DataFrame
    value_name = ''
    columns = []
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
            columns.append(value_name)
    
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
    DF = dataToDF(query_api.query(f'from(bucket:"{bucket}") |> range(start: {start_time}, stop: {stop_time}) |> filter(fn: (r) => r._measurement == "{measurement}") |> filter(fn: (r) => r._field == "{field}")'))
    return DF

    
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

def createConfig():
    
    print("Welcome to config creator!")
    config = {
        'ip': input("Please enter IP and port of influxDB (template: http://127.0.0.1:8086/): \n"),
        'org': input("Please enter Organisation name of influxDB: \n"),
        'token': input("Please enter Token from influxDB \nLog in to influx -> ⬆ -> API Tokens -> Generate API Token\n"),
        'buckets': []
        }
    bucket_amount = int(input("How many buckets do you want to plot? (INT): \n"))

    configjsonstr = json.dumps(config)
    configjson = json.loads(configjsonstr)
    if bucket_amount > 1:
        print('Now I\'ll ask you to input information needed')
        while bucket_amount > 0:
            template_bucket = {
            'bucket': input("What's the name of the bucket? \n"),
            'measurement': input("What's the name of the measurement? \n"),
            'field': input("What's the name of the field \n"),
            'start_time': input("What's the earliest you want to see? \n"),
            'stop_time': input("What's the latest you want to see? \n")
            }
            os.system('cls')
            configjson["buckets"].append(template_bucket)
            bucket_amount -= 1
    else:
        template_bucket = {
            'bucket': input("What's the name of the bucket?"),
            'measurement': input("What's the name of the measurement?"),
            'field': input("What's the name of the field"),
            'start_time': input("What's the earliest you want to see?"),
            'stop_time': input("What's the latest you want to see?")}
        configjson["buckets"].append(template_bucket)
        
    with open('config.json', 'w') as outfile:
        json.dump(configjsonstr, outfile)
    print("Config succesfully created!")
    return
    


def plotDF(DF, columnname):
    # plotting the graph

    legend = []
    plt.plot(DF._timestamp, DF[columnname])
    plt.legend(legend)
    plt.xlabel('Date')
    plt.ylabel('Values')
    plt.title('Load Cell data')
    plt.grid()
    plt.show()
    return