import csv
import math

def read_csv_as_dict(filename, separator):
    """
    Inputs:
      filename  - name of CSV file
      keyfield  - field to use as key for rows
      quote     - character used to optionally quote fields
    Output:
      Returns a dictionary  to the corresponding row in the
      CSV file and the number of cluster.  
    """
    filedict = {}
    with open(filename, "rt", newline='') as csvfile:
        csvreader = csv.reader(csvfile,
                                   delimiter=separator)
        cluster_index = 0
        for row in csvreader:
            filedict[int(row[0])] = int(row[1])
            if int(row[1]) > cluster_index:
                cluster_index = int(row[1])
    return filedict, cluster_index + 1 

def class_entropy(cp_matrix, c_index, p_index):
    total_data = cp_matrix[c_index][p_index]
    cluster_entropy = 0
    partition_entropy = 0
    for row in range(c_index):
        c_prob = cp_matrix[row][p_index]/total_data
        cluster_entropy += -c_prob * math.log2(c_prob)
    for col in range(p_index):
        p_prob = cp_matrix[c_index][col]/total_data
        partition_entropy += -p_prob * math.log2(p_prob)
    return cluster_entropy, partition_entropy
    
    
def cond_class_entropy(cp_matrix, c_index, p_index):
    cond_entropy = 0
    for row in range(c_index):
        cluster_data = cp_matrix[row][p_index]
        clus_cond_entropy = 0
        for col in range(p_index):
            if cp_matrix[row][col] != 0:
                cond_prob = cp_matrix[row][col]/cluster_data
                clus_cond_entropy += -cond_prob * math.log2(cond_prob)
        #print(clus_cond_entropy)        
        cond_entropy += 1/c_index * clus_cond_entropy
    return cond_entropy   
    
    
def mutual_info(cp_matrix, c_index, p_index, partition_entropy):
    cond_entropy = cond_class_entropy(cp_matrix, c_index, p_index)
    #print(cond_entropy)
    mut_info = partition_entropy - cond_entropy
    return mut_info
    
    
def norm_mutual_info(cp_matrix, c_index, p_index):
    (cluster_entropy, partition_entropy) = class_entropy(cp_matrix, c_index, p_index)
    #print(cluster_entropy, partition_entropy)
    mut_info = mutual_info(cp_matrix, c_index, p_index, partition_entropy)
    #nmi1 = 2*mut_info/(cluster_entropy + partition_entropy)
    nmi = mut_info/math.sqrt(cluster_entropy * partition_entropy)
    return nmi
    
    
    
def true_positive(cp_matrix, c_index, p_index):
    tp = 0
    for row in range(c_index):
        for col in range(p_index):
            if cp_matrix[row][col] != 0:
                tp += (cp_matrix[row][col] * (cp_matrix[row][col] - 1))/2
    return tp            

def false_positive(cp_matrix, c_index, p_index, tp):
    fp = 0
    for col in range(p_index):        
        fp += (cp_matrix[c_index][col] * (cp_matrix[c_index][col] - 1))/2    
    fp = fp - tp
    return fp
    
def false_negative(cp_matrix, c_index, p_index, tp):
    fn = 0
    for row in range(c_index):        
        fn += (cp_matrix[row][p_index] * (cp_matrix[row][p_index] - 1))/2    
    fn = fn - tp
    return fn
    
def true_negative(cp_matrix, c_index, p_index, tp, fn, fp):
    total_data = cp_matrix[c_index][p_index]
    total_pair = (total_data * (total_data - 1))/2
    tn = total_pair - (tp + fn + fp)
    return tn
    

def jaccard_coeff(cp_matrix, c_index, p_index):
    tp = true_positive(cp_matrix, c_index, p_index)
    fp = false_positive(cp_matrix, c_index, p_index, tp)
    fn = false_negative(cp_matrix, c_index, p_index, tp)
    tn = true_negative(cp_matrix, c_index, p_index, tp, fn, fp)
    #print(tp, fp, fn, tn)
    jac_coef = tp/(tp + fp + fn)
    return jac_coef

def cluster_partition_matrix(cluster, c_index, partition, p_index):
    """
    Input:
        cluster - dictionary of cluster for test clustering
        c_index - number of cluster in test clustering
        partition - dictionary of cluster for ground truth
        p_index - number of cluster in ground truth
    Output:
        An 2D list or list of list of combined cluster and
        partition representation
    """
    cp_matrix = []
    for t_cluster in range(c_index):
        row = []
        for truth_cluster in range(p_index):
            row.append(0)
        cp_matrix.append(row)
    for row in cluster:
        cp_matrix[cluster[row]][partition[row]] += 1
    x_index = 0
    col_sum_list = [0 for i in range(p_index)]
    for row in cp_matrix:
        row_sum = 0
        y_index = 0
        for col in row:
            row_sum += col
            col_sum_list[y_index] += col
            y_index = y_index + 1
        cp_matrix[x_index].append(row_sum)
        x_index = x_index + 1
    col_sum_list.append(sum(col_sum_list))
    cp_matrix.append(col_sum_list)
    return cp_matrix


def test_cluster(cluster_filename, partition_filename):
    """
    for the clustering and ground truth filename will write
    a file showing the cluster validation
    """
    (cluster, c_index) = read_csv_as_dict(cluster_filename, ' ')
    (partition, p_index) = read_csv_as_dict(partition_filename, ' ')
    cp_matrix = cluster_partition_matrix(cluster, c_index, partition, p_index)
    #print(cp_matrix)
    nmi = norm_mutual_info(cp_matrix, c_index, p_index)
    jac_coef = jaccard_coeff(cp_matrix, c_index, p_index)
    return nmi, jac_coef

def cluster_validation():
    (nmi_1, jac_coeff_1) = test_cluster('clustering_1.txt', 'partitions.txt')
    (nmi_2, jac_coeff_2) = test_cluster('clustering_2.txt', 'partitions.txt')
    (nmi_3, jac_coeff_3) = test_cluster('clustering_3.txt', 'partitions.txt')
    (nmi_4, jac_coeff_4) = test_cluster('clustering_4.txt', 'partitions.txt')
    (nmi_5, jac_coeff_5) = test_cluster('clustering_5.txt', 'partitions.txt')
    
    with open("scores.txt", "w") as writefile:
        writefile.write(str(nmi_1) + ' ' + str(jac_coeff_1) + '\n')
        writefile.write(str(nmi_2) + ' ' + str(jac_coeff_2) + '\n')
        writefile.write(str(nmi_3) + ' ' + str(jac_coeff_3) + '\n')
        writefile.write(str(nmi_4) + ' ' + str(jac_coeff_4) + '\n')
        writefile.write(str(nmi_5) + ' ' + str(jac_coeff_5) )
            
            
print(test_cluster('clustering_1.txt', 'partitions.txt'))
print(test_cluster('clustering_2.txt', 'partitions.txt'))
print(test_cluster('clustering_3.txt', 'partitions.txt'))
print(test_cluster('clustering_4.txt', 'partitions.txt'))
print(test_cluster('clustering_5.txt', 'partitions.txt'))
cluster_validation()