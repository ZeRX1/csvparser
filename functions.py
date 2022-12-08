import csv


def dataToDataFrame(data):
    tables=[]
    df = 0
    for table in data:
        for line in table.records:
            oneresulttable = []
            oneresulttable.append(line.get_time())
            oneresulttable.append(line.get_value())
            tables.append(oneresulttable)

        
    return df

def exportCSVToFile(df, name):
    df.to_csv(f'influx_{name}.csv', encoding='UTF-8',index=False)
    return "Action completed succesfully"