import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
def hammingdistance(string1,string2):
    distance = 0
    L = len(string1)
    for i in range(L):
        if string1[i] != string2[i]:
            distance += 1
    return distance

def findMin(arry):
    for i in range(len(arry)):
        if min(arry) == arry[i]:
            return i

def same(arr1, arr2, k):
    for i in range(k):
        for j in range(2):
            if arr1[i][j] != arr2[i][j]:
                return 1
    return 0


def KMeans(points,k):
    #random sample
    seedsHD=points.sample(n=k)
    seedsHD.index = [0,1,2,3,4,5,6,7]
    #temporary matrix for the first pass to work
    back = [[1.0,1.0],[1.0,1.0],[1.0,1.0],[1.0,1.0],[1.0,1.0],[1.0,1.0],[1.0,1.0],[1.0,1.0]]
    test = True
    #repeate
    while test == True:
        clust = []
        for i in range(points.shape[0]):
            tmp = []
            #finding the index in seeds that the point is closest to
            for index, row in seedsHD.iterrows():
                xp, yp = points.at[i,'x'], points.at[i,'y']
                xs, ys = row['x'], row['y']
                distance = math.sqrt((xp-xs)**2 + (yp-ys)**2)
                tmp.append(distance)
            clust.append(findMin(tmp))
        #assign each point to closest centroid
        points['cluster'] = clust
        #getting new mean
        seeds = []
        for i, row in seedsHD.iterrows():
            tmp = points.loc[points['cluster'] == i]
            seeds.append([tmp['x'].mean(),tmp['y'].mean()])
        seedsHD=pd.DataFrame(seeds,columns=['x','y'])
        #check if they are the same values
        if same(back,seeds,k) == 0:
            test = False
        back = seeds
    return points

#Reading sequences
filename = "DNASequence.fas"
myfile = open(filename)
data = []
#removing extra stuff
for j in myfile:
    if j[0] == 'C':
        data.append(j)
#Calculating hamming distance
hammings = []
for i in data:
    tmp = []
    for j in data:
        tmp.append(hammingdistance(i,j))
    hammings.append(tmp)
dataHD = pd.DataFrame(hammings)
#MDS from hamming distance
import sklearn.manifold
mds = sklearn.manifold.MDS(dissimilarity = 'precomputed', n_init = 10, max_iter = 1000)
data2D = mds.fit_transform(dataHD)
#Displaying the 2D data
data2D = pd.DataFrame(data2D, columns=['x', 'y'], index = dataHD.index)
ax = data2D.plot.scatter(x='x', y='y')
plt.show()
#Number of clusters is 8 now we run KMeans and get the output
data2D = data2D.assign(cluster = 9)
means2D = KMeans(data2D,8)
plt.scatter(means2D.x,means2D.y,s=300,c=means2D.cluster)
plt.show()
