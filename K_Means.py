########################################################################
# Data processing for K-Mean method. 
########################################################################
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans

# Step 0: Load data
data_knn = pd.read_csv('C:/Your search path/tXX_data_KNN.csv')

# Step 1: Extract RGB columns
R = data_knn.iloc[:, 0].values  # R values
G = data_knn.iloc[:, 1].values  # G values
B = data_knn.iloc[:, 2].values  # B values

# Step 2: Find shortest length
min_len = min(len(R), len(G), len(B))

# Step 3: Truncate all arrays to same length
cluster1 = R[:min_len]
cluster2 = G[:min_len]
cluster3 = B[:min_len]

# Step 4: create matrix X of arrays
X = pd.DataFrame({'R': cluster1, 'G': cluster2, 'B': cluster3})

# Alternative Step, for restriction for K-Mean centroids 
#initial_centroids = np.array([
#    [129, 129, 129],  # dark
#    [225, 129, 129],  # red
#    [129, 225, 129],  # green
#    [129, 129, 225]   # blue
#])

# Step 5: KMeans clustering, k = n_clusters (defines the number of clusters being created)
kmeans = KMeans(n_clusters=5, random_state=42)
#kmeans = KMeans(n_clusters = 5, init=initial_centroids, n_init=1, random_state = 42) # only set centroid position once
kmeans.fit(X)
labels = kmeans.predict(X)
centroids = kmeans.cluster_centers_

print("Centroids are:\n", centroids)

# Step 6: set 3D Plot
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Step 7: Convert to NumPy array for indexing
X_np = X.values

# Step 8: Plot each cluster
colors = ['black', 'gray', 'red','blue','green']
for i in range(5):
    ax.scatter(X_np[labels == i, 0], X_np[labels == i, 1], X_np[labels == i, 2],
               color=colors[i], label=f'Cluster {i}')


# Step 9: Plot centroids
ax.scatter(centroids[:, 0], centroids[:, 1], centroids[:, 2],
           marker='x', s=200, linewidths=3,
           color='black', label='Centroids')

# Axis labels
ax.set_xlabel('Red')
ax.set_ylabel('Green')
ax.set_zlabel('Blue')
ax.set_title('K-Means Clustering on RGB Data')
ax.legend()
plt.show()

# Count samples per cluster
unique, counts = np.unique(labels, return_counts=True)
cluster_counts = dict(zip(unique, counts))

# Print amounth of measurments from each clusters
print("Samples per cluster:")
for cluster_id, count in cluster_counts.items():
    print(f"Cluster {cluster_id}: {count} samples")

#####################################################################################
# Euclidean distance calculation of centroid to optimal center
#####################################################################################
import math

def euclidean_3D_dist(point1, point2):
    dst = math.sqrt((point1[0] - point2[0])**2 + 
                     (point1[1] - point2[1])**2 + 
                     (point1[2] - point2[2])**2)
    return dst

"""
# Possible optimisation for setting color center for each centeroid
a = centroids[0,:]
b = centroids[1,:]
c = centroids[2,:]
d = centroids[3,:]
e = centroids[4,:]

arr = [a,b,c,d,e]
white = []
yellow = []
red = []
green = []
blue = []
dark = []
outlier = []
# Define centroid color (each threshold needs to be reavaluated for each specific color measurment, suggestion using the maximum and minimum value +- 10-20 unit)
for i in range(0, len(arr)-1):
    if arr[i][0] >= 140 and arr[i][1] >= 180 and arr[i][2] >= 180:
        white = arr[i]
    elif arr[i][0] >= 170 and arr[i][2] >= 180:
        yellow = arr[i]
    elif arr[i][0] >= 170 :
        red = arr[i]
    elif arr[i][1] >= 180 :
        green = arr[i]
    elif arr[i][2] >= 180:
        blue = arr[i]
    elif arr[i][0] <= 160 and arr[i][1] <= 160 and arr[i][2] <= 160:
        dark = arr[i]
    else:
        outlier = arr[i]

"""
# Step 0: manually add the centroid coordinates and decide colorisation
a =  ()#(220.46043656, 217.73942701, 232.39427012) #white
b = (132.24191617, 241.28982036, 132.96287425)#(198.6 ,       217.61014493, 129.10144928) #green
c = (129.33701657, 130.34622468, 169.32780847)#(220.41152263, 129.14814815, 232.34430727) #outliear
d = (193.31986532, 130.67452301, 130.23905724)#(201.36962751, 129.06303725, 129.06017192) #red
e = (131.63829787, 132.06508135, 247.97246558)#(129.17007673, 188.92327366, 232.41176471) #blue
p = (130.64701782, 130.81990705, 129.51951975)#dark

# Optimal center matrix
f = (255,255,255) #white
g = (129,255,129) #green
i = (129,129,255) #blue
j = (255,129,129) #red
o = (129,129,129) #dark

# Calculate the distance and printing it out in the terminal for observation
dstMAX = euclidean_3D_dist((255,255,255), (0,0,0))
print(dstMAX)

dstA = euclidean_3D_dist(p,o) #a,f
print(dstA)

dstA = euclidean_3D_dist(b,g) #b,g
print(dstA)

dstA = euclidean_3D_dist(d,j) #d,j
print(dstA)

dstA = euclidean_3D_dist(e,i) #e,i
print(dstA)
