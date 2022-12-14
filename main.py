try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    import os, sys
    import getopt
    import json
    from os.path import exists
    from influxdb_client import InfluxDBClient
    from dotenv import load_dotenv
    from csv import DictReader
    from functions import *

    import time

except ImportError as err:
    print("Couldn't load modules " + err)
except Exception as err:
    print(f"Unexpected {err=}, {type(err)=}")
    raise
##*#
# *   Sources used:
# *   https://github.com/influxdata/influxdb-client-python
# *   Not only this one just didn't save all the links
##*#

# main using the arguments passed
# bucket, measurement, fields, start_time, stop_time
# all passed via a dictionary

# ! Main
def main(d):
# Load variables
    load_dotenv()
    token = os.getenv('INFLUXDB_V2_TOKEN')
    org = os.getenv('INFLUXDB_V2_ORG')
    url = os.getenv('INFLUXDB_V2_URL')
    # Connect to DB
    client = InfluxDBClient.from_env_properties()
    query_api = client.query_api()
    
    print(d.get('config'))

    # Handling arguments
    if not d:
        if exists("config.json"):
            with open("config.json") as input:
                if not input:
                    print("The config file is empty. Use -c to create one!")
                    return
                configjson = json.load(input)
        else:
            print("The config file doesn't exist. Use -c to create one!")
            return
        dflist = []
        columns = []
        for element in configjson:
            dflist.append(queryIDBToDF(element['bucket'], element['start_time'], element['stop_time'], element['measurement'], element['field']))
            column = element['measurement'] + "_" + element['field']
            columns.append(column)

        mergedRes = mergeDF(dflist)
        plotDF(mergedRes, columns)


    elif d.get("reset") == True:
        print("You'll now delete the config file")
        os.remove('config.json')
        print("Config succesfully removed, use -c to make a new one!")
        return
    elif d.get("config") == True:
        createConfig()
        return
    elif d.get('bucket'):
        os.system("cls")
        print("Reading data from the arguments...")
        #read from arguments
        bucket = d.get('bucket')
        measurement = d.get('measurement')
        field = d.get('field')
        start_time = d.get('start_time')
        stop_time = d.get('stop_time')
        #do funny things for plotDF to work
        columnname = [measurement + "_" + field]
        #use the data from the arguments to get the data and plot it
        data = queryIDBToDF(bucket, start_time, stop_time, measurement, field)
        print(data)
        plotDF(data, columnname)
        return
    elif d.get('json'):
        json = json.load(d.get('json'))
        dflist = []
        columns = []
        for element in json:
            dflist.append(queryIDBToDF(element['bucket'], element['start_time'], element['stop_time'], element['measurement'], element['field']))
            column = element['measurement'] + "_" + element['field']
            columns.append(column)

        mergedRes = mergeDF(dflist)
        plotDF(mergedRes, columns)
    return 


def readArgs(argv):
    try:
        opts, args = getopt.getopt(argv, "b:m:f:p:s:c:j:oe")
    except getopt.GetoptError as err:
        help_command()
        print(err) 
        sys.exit(2)

    #add this to an array/dictionary and send further
    d = dict()
    for opt, arg in opts:
        if opt in ('-b'):
            d['bucket'] = arg
        elif opt in ('-m'):
            d['measurement'] = arg
        elif opt in ('-f'):
            d['field'] = arg
        elif opt in ('-p'):
            d['stop_time'] = arg
        elif opt in ('-s'):
            d['start_time'] = arg
        elif opt in('-o'):
            d['reset'] = True
        elif opt in('-c'):
            d['config'] = arg
        elif opt in('-e'):
            d['export'] = True
        elif opt in('-n'):
            d['no_plot'] = True 
        elif opt in('-j'):
            d['json'] = arg
    main(d)
    return

def help_command():
    print("Help")
    print("python main.py [options]")
    print("Here's the list of possible arguments:")
    print("-b - \t<bucket>\t Choose a bucket from the db to use by the script")
    print("-m - \t<measurement>\t Choose a measurement from the bucket to use by the script")
    print("-f - \t<field>\t\t Choose a field from the measurement to use by the script")
    print("-p - \t<range_stop>\t Choose earliest time of the desired data (-<amount><d/h/m/s> / Unix / Absolute time range)")
    print("-s - \t<range_start>\t Choose latest time of the desired data (-<amount><d/h/m/s> / Unix / Absolute time range)")
    print("-o - \t\t\t Reset config")
    print("-c - \t\t\t Create config")
    return

##*#
# * Main function
##*#
if __name__ == "__main__":
    try:
        # read arguments
        readArgs(sys.argv[1:])

        time.sleep(2)

    except (ValueError, KeyError, AttributeError, IndexError) as err:
        print(f"{err} Type={type(err)}")
    except TimeoutError as err:
        print("Is the IP correct? (.env)" + err)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise