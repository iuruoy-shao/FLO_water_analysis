import matplotlib.pyplot as plt
from data_points import Data

path = "dedupe_train_data.csv"
data = Data(path)
intervals = data.getintervals()

class Event():
    def __init__(self):
        pass

    def add_points(self,start,end):
        self.start_index = start
        self.end_index = end
    
    def add_label(self,label):
        self.label = label
    
    def get_event(self):
        return([self.start_index,self.end_index,self.label])

# points taken in the form [timestamp,gpm]
def plot(points):
    timestamps = []
    gpms = []
    for point in points:
        timestamps.append(point[0])
        gpms.append(point[1])
    plt.plot_date(timestamps,gpms,"-bo")
    plt.xlabel("timestamp")
    plt.ylabel("gpm")
    plt.ylim(0,4)
    plt.show()

def getgraph(id):
    points = data.get_points(intervals[id][0],intervals[id][1])
    plot(points)


if __name__ == "__main__":
    print(getgraph(0))