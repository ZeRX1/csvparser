try:
    from influxdb_client import InfluxDBClient, Point, WriteOptions, Dialect
    # not needed? \/
    from influxdb_client.client.write_api import SYNCHRONOUS
    from dotenv import load_dotenv
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    import os, sys
    from csv import DictReader
    import csv
    from functions import *
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

        dfdatanmea2k = query_api.query(f'from(bucket:"{bucket_nmea2k}") |> range(start: {start_time}, stop: {stop_time}) |> filter(fn: (r) => r._measurement == "Wind_Data") |> filter(fn: (r) => r._field == "aws")')
        dfdatadownsampled = query_api.query(f'from(bucket:"{bucket_downsampled}") |> range(start: {start_time}, stop: {stop_time})')
        nmea2kdf = dataToDF(dfdatanmea2k)
        downsampleddf = dataToDF(dfdatadownsampled)

        # All tables to Data Frames
        awsdf = dataToDF(query_api.query(f'from(bucket:"{bucket_nmea2k}") |> range(start: {start_time}, stop: {stop_time}) |> filter(fn: (r) => r._measurement == "Wind_Data") |> filter(fn: (r) => r._field == "aws")'))
        awddf = dataToDF(query_api.query(f'from(bucket:"{bucket_nmea2k}") |> range(start: {start_time}, stop: {stop_time}) |> filter(fn: (r) => r._measurement == "Wind_Data") |> filter(fn: (r) => r._field == "aws")'))
        V1Pdf = dataToDF(query_api.query(f'from(bucket:"{bucket_downsampled}") |> range(start: {start_time}, stop: {stop_time}) |> filter(fn: (r) => r._measurement == "V1P") |> filter(fn: (r) => r._field == "load_value")'))
        V1Sdf = dataToDF(query_api.query(f'from(bucket:"{bucket_downsampled}") |> range(start: {start_time}, stop: {stop_time}) |> filter(fn: (r) => r._measurement == "V1S") |> filter(fn: (r) => r._field == "load_value")'))
        Headstaydf = dataToDF(query_api.query(f'from(bucket:"{bucket_downsampled}") |> range(start: {start_time}, stop: {stop_time}) |> filter(fn: (r) => r._measurement == "Headstay") |> filter(fn: (r) => r._field == "load_value")'))

        # Joining the Data Frames
        print(awsdf)
        plt.scatter(awsdf._timestamp, awsdf.Wind_Data_aws)
        plt.grid()
        plt.show()



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