'''
     K-Means Algorithm
     -----------------
'''

import csv
import random
import math
import pygal

def read_csv_fieldnames(filename, separator):
    """
    Inputs:
      filename  - name of CSV file
      separator - character that separates fields
    Ouput:
      A dictionary of tuple consist of x-y value in
      the given CSV file and the maximum key value
    """
    dict_location = {}
    with open(filename, "rt", newline='') as csvfile:
        csvreader = csv.reader(csvfile,
                               delimiter=separator)
        index = 0
        for row in csvreader:
            dict_location[index] = tuple(row)
            index = index + 1
    return dict_location, index - 1

def distance_between(first_value, second_value):
    """
    Inputs:
        Two coordinate for which distance to be calculated
    Oututs:
        Distance
    """

    x_coor = float(first_value[0]) - float(second_value[0])
    y_coor = float(first_value[1]) - float(second_value[1])
    sum_of_square = x_coor**2 + y_coor**2
    distance = math.sqrt(sum_of_square)
    return distance

def nearest_mean(plot_value, cluster_index):
    """
    Inputs:
        plot_value - tuple of x-y value
        cluster_index - dictionary of list containing the
                        k-mean value
    Output:
        Key of the cluster_index to which plot_value is nearer to 
    """
    key = -1
    min_dist = 99999
    for index in cluster_index:
        dist = distance_between(plot_value, cluster_index[index])
        if dist < min_dist:
            min_dist = dist
            key = index
    return key        

def cal_new_mean(dict_location, cluster_list, k_value):
    """
    Input:
        dict_location - dictionary of tuple representing plots
        cluster_list - list representing cluster number of each plots
        k-value - Number of cluster
    Output:
        Calculate the new mean for each cluster
    """
    
    new_means = {i : [0, 0] for i in range(k_value)}
    no_of_points = {i : 0 for i in range(k_value)}
    for plot in dict_location:
        cluster_no = cluster_list[plot]
        new_means[cluster_no][0] = new_means[cluster_no][0] + float(dict_location[plot][0])
        new_means[cluster_no][1] = new_means[cluster_no][1] + float(dict_location[plot][1])
        no_of_points[cluster_no] = no_of_points[cluster_no] + 1
    for value in new_means:
        new_means[value][0] = str(new_means[value][0]/no_of_points[value])
        new_means[value][1] = str(new_means[value][1]/no_of_points[value])
    return new_means
        
    
def check_similarity(old_means, new_means):
    """
    Check for similarity
    """
    if old_means==new_means:
        return 1
    else:
        return 0
        
def calc_cluster(kmeaninfo, dict_location, max_key):
    """
    Inputs:
        kmeaninfo - information dictionary
        dict_location - dictionary of tuple consist of x-y value
        max_key - maximum value of key
    Oututs:
        A list representing plot cluster number
    """
    cluster_list = [-1 for i in range(max_key + 1)]
    cluster_index = {i : [0, 0] for i in range(int(kmeaninfo['k_value']))}
    #print(cluster_index) 
    tag = 0
    random_index = random.sample(range(max_key+1), int(kmeaninfo['k_value']))
    #print(random_index)
    index = 0
    for plot_index in random_index:
        cluster_index[index][0] = dict_location[plot_index][0]
        cluster_index[index][1] = dict_location[plot_index][1]
        index = index + 1 
    #print(cluster_index)
    
    while tag == 0:
        for plot_index in dict_location:
            key = nearest_mean(dict_location[plot_index], cluster_index)
            cluster_list[plot_index] = key
        #print(cluster_list)
        new_means = cal_new_mean(dict_location, cluster_list, int(kmeaninfo['k_value']))
        #print(new_means)
        tag = check_similarity(cluster_index, new_means)
        #print(tag)
        cluster_index = new_means
        #print("-----------------")
    return cluster_list    

def render_cluster(dict_location, cluster_list):
    """
    Input:
        dict_location - dictionary of tuple consist of x-y value
        cluster_list - list representing cluster number of each plots
    Output:
        render the cluster in browser
    """
    cluster0 = []
    cluster1 = []
    cluster2 = []
    for plot_no in dict_location:
        if cluster_list[plot_no] == 0:
            tup = tuple([float(dict_location[plot_no][0]), float(dict_location[plot_no][1])])
            cluster0.append(tup)
        elif cluster_list[plot_no] == 1:
            tup = tuple([float(dict_location[plot_no][0]), float(dict_location[plot_no][1])])
            cluster1.append(tup)
        else:
            tup = tuple([float(dict_location[plot_no][0]), float(dict_location[plot_no][1])])
            cluster2.append(tup)
    xy_chart = pygal.XY(stroke=False)
    xy_chart.title = 'Cluster Plot'
    xy_chart.add('Cluster 0', cluster0)
    xy_chart.add('Cluster 1', cluster1)
    xy_chart.add('Cluster 2', cluster2)
    xy_chart.render_in_browser()
            
            
def output_cluster(kmeaninfo, outputfile):
    (dict_location, max_key) = read_csv_fieldnames(kmeaninfo['data_file'], kmeaninfo['separator'])
    #print(dict_location, max_key)
    cluster_list = calc_cluster(kmeaninfo, dict_location, max_key)
    #print(cluster_list)
    with open(outputfile, "w") as writefile:
        for row in dict_location:
            writefile.write(str(row) + ' ' + str(cluster_list[row]) + '\n')
    render_cluster(dict_location, cluster_list)        

def test_kmean():
    '''
        code to implement the k-means algorithm and use it
        to cluster the n locations into k clusters, such that
        the locations in the same cluster are geographically
        close to each other.
    '''
    kmeaninfo = {
        "data_file" : "kmeans_data.csv",
        "separator" : ",",
        "k_value" : "3"
        }
    
    output_cluster(kmeaninfo, "output.txt")
    
test_kmean()    