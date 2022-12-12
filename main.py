try:
    from influxdb_client import InfluxDBClient
    from dotenv import load_dotenv
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    import os, sys
    import getopt
    from csv import DictReader
    from functions import *

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
def main():
# Load variables
    load_dotenv()
    token = os.getenv('INFLUXDB_V2_TOKEN')
    org = os.getenv('INFLUXDB_V2_ORG')
    url = os.getenv('INFLUXDB_V2_URL')
    # make the variables below be set by arguments instead of .env
    # args
    bucket_downsampled = os.getenv('bucket_downsampled')
    bucket_nmea2k = os.getenv('bucket_nmea2k')
    start_time = os.getenv('start_time')
    stop_time = os.getenv('stop_time')
    # Connect to DB
    client = InfluxDBClient.from_env_properties()
    query_api = client.query_api()
        

    ##
    #   Query the DB for data
    ##

    # All tables to Data Frames
    awsdf = queryIDBToDF("nmea2k", "-18d", "-16d", "Wind_Data", "aws")
    awddf = queryIDBToDF("nmea2k", "-18d", "-16d", "Wind_Data", "awd")
    V1Pdf = queryIDBToDF("downsampled", "-18d", "-16d", "V1P", "load_value")
    V1Sdf = queryIDBToDF("downsampled", "-18d", "-16d", "V1S", "load_value")
    Headstaydf = queryIDBToDF("downsampled", "-18d", "-16d", "Headstay", "load_value")

    # Make an array of the dataframes and merge them
    dfarray = [awsdf, awddf, V1Pdf, V1Sdf, Headstaydf]
    mergedRes = mergeDF(dfarray)
    print(mergedRes)

    # plotting the graph
    plt.plot(mergedRes._timestamp, mergedRes._Wind_Data_aws)
    plt.plot(mergedRes._timestamp, mergedRes._Headstay_load_value)
    plt.plot(mergedRes._timestamp, mergedRes._V1S_load_value)
    plt.plot(mergedRes._timestamp, mergedRes._V1P_load_value)
    legend = ['Average wind speed', 'Load Value Headstay', 'Load Value V1S', 'Load Value V1P']
    plt.legend(legend)
    plt.xlabel('Date')
    plt.ylabel('Values')
    plt.title('Load Cell data')
    plt.grid()
    plt.show()
    return 0


def readArgs(argv):
    try:
        opts, args = getopt.getopt(argv, "b:m:f:p:s:o:")
    except getopt.GetoptError as err:
        print(err) 
        sys.exit(2)

    #add this to an array/dictionary and send further
    array = []
    for opt, arg in opts:
        if opt in ('-b'):
            bucket = arg
        elif opt in ('-m'):
            measurement = arg
        elif opt in ('-f'):
            field = arg
        elif opt in ('-p'):
            stop_time = arg
        elif opt in ('-s'):
            start_time = arg
        elif opt in('-o'):
            setup = arg
        
    return array

##*#
# * Main function
##*#
if __name__ == "__main__":
    try:
        # read arguments
        #readArgs(sys.argv[1:])
        main()
    except (ValueError, KeyError, AttributeError, IndexError) as err:
        print(err)
    except TimeoutError as err:
        print("Is the IP correct? (.env)" + err)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise