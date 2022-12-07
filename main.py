# Imports
try:
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
except ImportError as err:
    print("Couldn't load modules " + err)
except Exception as err:
    print(f"Unexpected {err=}, {type(err)=}")
    raise
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
    try:
        load_dotenv()
        #! Values are set here \/
        bucket = 'downsampled'
        time_range = '-30d' # ! Remember to set this to a negative number
        stop_range = '-1d'
        token = os.getenv('INFLUXDB_V2_TOKEN')
        org = os.getenv('INFLUXDB_V2_ORG')
        url = os.getenv('INFLUXDB_V2_URL')
        
        # TODO: make it connect with the db automatically without specifying arguments
        # TODO: [Here](https://github.com/influxdata/influxdb-client-python#via-environment-properties)
        client = InfluxDBClient.from_env_properties()
        query_api = client.query_api()
    except ValueError as err:
        print(err)
    except KeyError as err:
        print(err)
    except TimeoutError as err:
        print("Is the IP correct? (.env)" + err)
    except AttributeError as err:
        print(err)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise


    # * Buildinf a dataframe and making a graph
    # * SELECT SUM(count) FROM (SELECT *,count::INTEGER FROM MyMeasurement GROUP BY count FILL(1))
    # * ^ query used to count rows // no its not 🥴

    # from(bucket: "downsampled")
    # |> range(start: -30d)
    # |> group(columns: ["host", "_field"], mode:"by")
    # |> filter(fn: (r) => r._measurement == "V1P" or r._measurement == "V1S" or r._measurement == "Headstay")
    # |> count()
    # this is used to count the rows (unfortunately slow but works fine)
    # first check one and try to parse everything except last entry then do the same for the rest and build it into a dataframe
    try:    
        if not time_range:
            time_range = '-1h'
            stop_range = 'now()'
        V1Pcount = query_api.query_csv(f'from(bucket: "downsampled") |> range(start: {time_range}, stop: {stop_range}) |> group(columns: ["host", "_field"], mode:"by") |> filter(fn: (r) => r._measurement == "V1P") |> count()')
        V1Scount = query_api.query_csv(f'from(bucket: "downsampled") |> range(start: {time_range}, stop: {stop_range}) |> group(columns: ["host", "_field"], mode:"by") |> filter(fn: (r) => r._measurement == "V1P") |> count()')
        Headstaycount = query_api.query_csv(f'from(bucket: "downsampled") |> range(start: {time_range}, stop: {stop_range}) |> group(columns: ["host", "_field"], mode:"by") |> filter(fn: (r) => r._measurement == "V1P") |> count()')

        V1Ppcount = parseCount(V1Pcount)
        V1Spcount = parseCount(V1Scount)
        Headstaypcount = parseCount(Headstaycount)

        print(V1Ppcount)

        df = pd.DataFrame(QueryCSV(bucket, time_range, stop_range), 
        columns=['empty','what','series_number','timestamp1','timestamp2','timestamp3','force','load_value','measurement','health_status','bool','serial_number'])
        print(df)

        plt.plot(df['Force'], df['TimeStamp3'])
        plt.xlabel("Time")
        plt.ylabel("Force")
        plt.title("Ratio")
        plt.xticks(df['TimeStamp3'])
        plt.show()

    except ValueError as err:
        print(err)
    except KeyError as err:
        print(err)
    except TimeoutError as err:
        print("Is the IP correct? (.env)" + err)
    except AttributeError as err:
        print(err)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
        
    # close the connection to the database
    client.close