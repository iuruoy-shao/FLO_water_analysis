import csv
from datetime import datetime
import pandas as pd

raw_data="7_29_22.csv"
new_csv="train_data.csv"
deduped_csv="dedupe_train_data.csv"

def remove_zeroes(raw_data,new_csv):
    with open(raw_data, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",", quotechar='|')
        data = list(reader)

        with open(new_csv, 'w', encoding='UTF8') as new_csvfile:
            writer = csv.writer(new_csvfile)

            for i in range(len(data)):
                row = data[i]
                
                if i != 0:
                    prerow = data[i-1]
                    
                    if float(row[3]) != 0:
                        if float(prerow[3]) == 0:
                            new_timestamp = datetime.strptime(prerow[1],"%Y-%m-%d %X")
                            new_row = [int(prerow[0]),new_timestamp,float(prerow[2]),float(prerow[3])]
                            writer.writerow(new_row)
                        new_timestamp = datetime.strptime(row[1],"%Y-%m-%d %X")
                        new_row = [int(row[0]),new_timestamp,float(row[2]),float(row[3])]
                        writer.writerow(new_row)
                        
                        if i != len(data)-1 and float(data[i+2][3]) == 0:
                            postrow = data[i+1]
                            new_timestamp = datetime.strptime(postrow[1],"%Y-%m-%d %X")
                            new_row = [int(postrow[0]),new_timestamp,float(postrow[2]),float(postrow[3])]
                            writer.writerow(new_row)
                            
                elif i == 0:
                    if float(data[i][3]) != 0:
                        new_timestamp = datetime.strptime(row[1],"%Y-%m-%d %X")
                        new_row = [int(row[0]),new_timestamp,float(row[2]),float(row[3])]
                        writer.writerow(new_row)

def dedupe(old_csv,deduped_csv):
    with open(old_csv, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",", quotechar='|')
        data = list(reader)
        
        with open(deduped_csv, 'w', encoding='UTF8') as new_csvfile:
            writer = csv.writer(new_csvfile)

            indices = []
            timestamps = []

            for row in data:
                if row[0] not in indices and row[1] not in timestamps:
                    indices.append(row[0])
                    timestamps.append(row[1])
                    writer.writerow(row)

if __name__ == "__main__":
    dedupe(new_csv,deduped_csv)