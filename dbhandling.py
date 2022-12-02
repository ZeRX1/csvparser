# * Query the chosen bucket for CSV from the data (If the time range is not specified it will default to 1h)
def QueryCSV(bucket, time_range):
    if not time_range:
        time_range = "-1h"
    csv_result = query_api.query_csv(f'from(bucket:"{bucket}") |> range(start: {time_range})',
        dialect=Dialect(header=False, 
        delimiter=",",
        comment_prefix="#", 
        annotations=[],
        date_time_format="RFC3339")
        )
    return csv_result

