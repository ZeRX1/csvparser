try:
    from influxdb_client import InfluxDBClient, Point, WriteOptions
    from influxdb_client import InfluxDBClient, Point, Dialect
    from influxdb_client.client.write_api import SYNCHRONOUS
    from reactivex import operators as ops
    from collections import OrderedDict
    import matplotlib.pyplot as plt
    from dotenv import load_dotenv
    from functions import *
    from tabulate import tabulate
    from csv import DictReader
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
##*#
# *   Sources used:
# *   https://github.com/influxdata/influxdb-client-python
##*#

##*#
# * Main function
##*#
if __name__ == "__main__":
    try:

        #! Most of the variables are stored in .env file for convinience!

        # Load variables
        load_dotenv()
        token = os.getenv('INFLUXDB_V2_TOKEN')
        org = os.getenv('INFLUXDB_V2_ORG')
        url = os.getenv('INFLUXDB_V2_URL')
        bucket_downsampled = os.getenv('bucket_downsampled')
        bucket_nmea2k = os.getenv('bucket_nmea2k')
        start_time = os.getenv('start_time')
        stop_time = os.getenv('stop_time')
        columns = os.getenv('columns')
        # Connect to DB
        client = InfluxDBClient.from_env_properties()
        query_api = client.query_api()
        

        ##
        #   Query the DB for data
        ##

        query_api = client.query_api()

        dfdatanmea2k = query_api.query(f'from(bucket:"{bucket_nmea2k}") |> range(start: {start_time}, stop: {stop_time}) |> filter(fn: (r) => r._measurement == "Wind_Data") |> filter(fn: (r) => r._field == "awd" or r._field == "aws")')
        dfdatadownsampled = query_api.query(f'from(bucket:"{bucket_downsampled}") |> range(start: {start_time}, stop: {stop_time})')

        # Table with the data from the DB

        dataframe_downsampled = pd.DataFrame(dfdatadownsampled, columns=["_measurement", "_timestamp", "_field", "_value"])
        dataframe_nmea2k = pd.DataFrame(dfdatanmea2k, columns=["_measurement", "_timestamp", "_field", "_value"])

        print(dataframe_downsampled)
        
        exportCSVToFile(dataframe_downsampled, 'downsampled')

    except ValueError as err:
        print(err)
    except KeyError as err:
        print(err)
    except TimeoutError as err:
        print("Is the IP correct? (.env)" + err)
    except AttributeError as err:
        print(err)
    except IndexError as err:
        print(err)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise