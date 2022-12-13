try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    import os, sys
    import getopt
    import json
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
def main(d):
# Load variables
    load_dotenv()
    token = os.getenv('INFLUXDB_V2_TOKEN')
    org = os.getenv('INFLUXDB_V2_ORG')
    url = os.getenv('INFLUXDB_V2_URL')
    # make the variables below be set by arguments instead of .env
    # args
    # bucket_downsampled = os.getenv('bucket_downsampled') # done with args
    # bucket_nmea2k = os.getenv('bucket_nmea2k') # done with args
    # start_time = os.getenv('start_time') # done with args
    # stop_time = os.getenv('stop_time') # done with args
    # Connect to DB
    client = InfluxDBClient.from_env_properties()
    query_api = client.query_api()


    # * Check if the reset or config flag has beed checked
    # if d['reset'] == True:
    #     #delete config
    #     print('tehe')
    # if d['config'] == True:
    #     #make a new config
    #     createConfig()


    ##
    #   Query the DB for data
    ##

    # Check if the bucket was given via args if not then use config
    if d == '':
        #read config
        print("No bucket?")
    else:
        print("ok")
        #read from arguments
        bucket = d['bucket']
        measurement = d['measurement']
        field = d['field']
        start_time = d['start_time']
        stop_time = d['stop_time']

        columnname = "_" + measurement + "_" + field
        #use the data from the arguments to get the data and plot it
        data = queryIDBToDF(bucket, start_time, stop_time, measurement, field)

        plotDF(data, columnname)
        return


    # Make an array of the dataframes and merge them
    dfarray = []
    mergedRes = mergeDF(dfarray)
    print(mergedRes) # debug



    return 


def readArgs(argv):
    try:
        opts, args = getopt.getopt(argv, "b:m:f:p:s:oc")
    except getopt.GetoptError as err:
        help_command()
        print(err) 
        sys.exit(2)

    #add this to an array/dictionary and send further
    d = dict()
    for opt, arg in opts:
        print(opt, arg)
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
            d['config'] = True
            createConfig()
        print(d)

    
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
        time.sleep(10)

    except (ValueError, KeyError, AttributeError, IndexError) as err:
        print(err)
    except TimeoutError as err:
        print("Is the IP correct? (.env)" + err)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise