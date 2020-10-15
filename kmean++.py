from sklearn.cluster import KMeans
import numpy as np

import matplotlib.pyplot as plt

with open("kmeans_data.csv") as f:
    lines = f.readlines()

locations = np.zeros( ( len(lines), 2 ) )    
for i in range(len(lines) ):
    x , y = lines[i].split(",")
    locations[i, 0],locations[i, 1] = float(x), float(y)
    
k_mean = KMeans( init = "k-means++",
                 n_clusters = 3
                 )
y = k_mean.fit_predict(locations)

centroids = k_mean.cluster_centers_


plt.figure( figsize = (50, 50) )

plt.plot(locations[:,0], locations[:,1],".k",color = "r", markersize = 40)

plt.scatter( centroids[:, 0], centroids[:, 1], marker = 'x', s = 40, color = 'b' )

plt.show()


with open("output.txt", "w") as f2:
    for i in range(len(lines)):
        f2.write( str(i) + " " + str(y[i]) + "\n" )
f2.close()