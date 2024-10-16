import sys
import numpy as np

def read(input_file):
    data = []
    with open(input_file, 'r') as file:
        for line in file:
            data_ = line.strip().split('\t')
            id = int(data_[0])
            x, y = float(data_[1]), float(data_[2])
            data.append((id, x, y))
    return data

def euc(p1, p2):
    x1, y1 = float(p1[1]), float(p1[2])
    x2, y2 = float(p2[1]), float(p2[2])
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def neighborList(data, pid, eps):
    nl = []  # neighbor list
    for i in range(len(data)):
        if i != pid and euc(data[pid], data[i]) <= eps:
            nl.append(i)
    return nl

def DBSCAN(data, eps, minPts):
    cluster = [[]]
    cid = 0  # cluster ID
    flag = [0] * len(data)
    
    for core in range(len(data)):
        if flag[data[core][0]] != 0:  # if already processed
            continue
        nl = neighborList(data, core, eps)
        if len(nl) < minPts:  # no enough neighbors
            flag[data[core][0]] = -1  # set as noise
        else:
            cluster.append([])  # add new cluster
            cid += 1
            while nl: 
                i = nl.pop()
                if flag[data[i][0]] == -1: #no double checking noises
                    flag[data[i][0]] = cid
                elif flag[data[i][0]] == 0:
                    flag[data[i][0]] = cid
                    nl_ = neighborList(data, i, eps) #reculsively expand cluster
                    if len(nl_) >= minPts: #enough to be core point
                        nl.extend(nl_)
    
    for core in range(len(flag)):  # final assign
        if flag[core] > 0:
            cluster[flag[core]].append(core)
    
    return cluster

def write(cluster, input_file, n):
    for core in range(min(n, len(cluster))):
        with open(f"{input_file}_cluster_{core}.txt", 'w') as output:
            for i in cluster[core + 1]:
                output.write('%d\n' % i)

if __name__ == "__main__":
    input_file = sys.argv[1]
    n = int(sys.argv[2])
    eps = float(sys.argv[3])
    minPts = int(sys.argv[4])
    
    data = read(input_file)
    cluster = DBSCAN(data, eps, minPts)
    write(cluster, input_file, n)
