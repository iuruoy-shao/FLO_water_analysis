import csv
import statistics
from datetime import datetime

class Data():
    def __init__(self, csvfile_path):
        self.csvfile_path = csvfile_path
        csvfile = open(self.csvfile_path, newline='')
        reader = csv.reader(csvfile, delimiter=",", quotechar='|')

        data = []
        for row in reader:
            data.append([datetime.strptime(row[1],"%Y-%m-%d %X"),float(row[3])])
        
        self.data = data

    def getintervals(self):
        intervals = []
        for i in range(len(self.data)):
            if self.data[i][1] == 0:
                if intervals == [] or len(intervals[-1]) == 2:
                    intervals.append([i])
                elif len(intervals[-1]) == 1:
                    intervals[-1].append(i)
        return intervals

    def get_points(self,start_point,end_point):
        points = []
        for i in range(start_point,end_point+1):
            points.append(self.data[i])
        return(points)

    def get_slope(self,point_index,direction):
        datapoints = self.data
        if direction == "before":
            duration = datapoints[point_index][0] - datapoints[point_index-1][0]
            slope = (datapoints[point_index][1] - datapoints[point_index-1][1])/(duration.total_seconds())
        elif direction == "after":
            duration = datapoints[point_index+1][0] - datapoints[point_index][0]
            slope = (datapoints[point_index+1][1] - datapoints[point_index][1])/(duration.total_seconds())
        return(slope)

    def compare_slope(self,point_index):
        datapoints = self.data
        slope_before = self.get_slope(datapoints,point_index,"before")
        slope_after = self.get_slope(datapoints,point_index,"after")
        if slope_before == slope_after:
            return(True)
        else:
            return(False)
    
    def get_slope_mean(self,start_point,end_point):
        datapoints = self.data
        unique_slopes = []
        negative_count = 0
        end_point+=1

        for index in range(start_point,end_point):
            if index == 0:
                unique_slopes.append(self.get_slope(datapoints,index,"after"))
            else:
                if self.get_slope(datapoints,index,"before") != self.get_slope(datapoints,index,"after"):
                    slope = self.get_slope(datapoints,index,"after")
                    if abs(slope) != slope:
                        negative_count+=1
                    unique_slopes.append(abs(slope))
        
        if negative_count % 2 == 1:
            negative = True
        else:
            negative = False
        
        return(negative,statistics.geometric_mean(unique_slopes))

    def get_slopes(self,start_point,end_point):
        datapoints = self.data
        unique_slopes = []
        end_point+=1

        for index in range(start_point,end_point):
            if index == 0:
                unique_slopes.append(self.get_slope(datapoints,index,"after"))
            else:
                if self.get_slope(datapoints,index,"before") != self.get_slope(datapoints,index,"after"):
                    slope = self.get_slope(datapoints,index,"after")
                    unique_slopes.append(abs(slope))
        
        return(unique_slopes)

    def count_slopes(self,start_point,end_point):
        return(len(self.get_slopes(self.data,start_point,end_point)))

    def get_duration(self,start_point,end_point):
        duration = self.data[end_point+1][0] - self.data[start_point-1][0]
        return(duration.total_seconds())

# def get_gpm(datapoints,start_point,end_point):
#     if 

# def get_gpm_max(points):

# def get_gpm_avg(points):
    
if __name__ == "__main__":
    path = "dedupe_train_data.csv"
    data = Data(path)
    print(len(data.getintervals()))