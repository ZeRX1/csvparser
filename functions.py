import csv
import pandas as pd


def dataToDF(data):
    tables = []
    for table in data:
        for line in table.records:
            oneresulttable = []
            oneresulttable.append(line.get_time())
            oneresulttable.append(line.get_value())
            tables.append(oneresulttable)
            value_name = "_" + line.get_measurement() + "_" + line.get_field()
    
    df = finishDF(tables,value_name)
    return df


def finishDF(tables, value_name):
    df = pd.DataFrame(tables, columns=["_timestamp", value_name])
    return df

def exportDFToFile(df, name):
    df.to_csv(f'influx_{name}.csv', encoding='UTF-8',index=False)
    return "Action completed succesfully"