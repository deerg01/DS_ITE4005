from itertools import combinations

def readFile(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            i = list(map(int, line.strip().split()))  
            data.append(i)
    data = [set(item) for item in data] #avoid duplicates in single transaction
    return data
def calcSup(data, itemset):
    count = 0
    for i in data:
        if all(item in i for item in itemset):
            count += 1
    return ((count / len(data))*100)
def calcConf(data, A, B):
    return (((calcSup(data, A + B)) / calcSup(data, A))*100)
def getFreq(data, supmin):
    single = set(item for transaction in data for item in transaction)
    isets = []
    for idx in range(1, len(single) + 1):
        itemsets = combinations(single, idx) 
        for itemset in itemsets:
            sup = calcSup(data, itemset)
            if sup >= supmin:
                isets.append((itemset, sup))
    return isets
def getAsso(data, supmin, confmin): #get associations
    f_itemset = getFreq(data, supmin)
    asr = []
    for itemset, sup in f_itemset:
        if len(itemset) > 1:
            for i in range(1, len(itemset)):
                for A in combinations(itemset, i):
                    B = tuple(item for item in itemset if item not in A)
                    confidence = calcConf(data, A, B)
                    if confidence >= confmin:
                        asr.append((A, B, sup, confidence))
    return asr
'''
if __name__ == "__main__":
    file_path = "./input.txt"
    supmin = 10
    confmin = 60

    data = readFile(file_path)
    rules = getAsso(data, supmin, confmin)

    for A, B, support, confidence in rules:
        print("{" + ",".join(map(str, A)) + "}", "{" + ",".join(map(str, B)) + "}", '{:.2f}'.format(support), '{:.2f}'.format(confidence))
'''
if __name__ == "__main__":
    file_path = "./input.txt"
    output_file_path = "output.txt"
    supmin = 10
    confmin = 0

    data = readFile(file_path)
    rules = getAsso(data, supmin, confmin)

    #with open(output_file_path, 'w') as output_file:
    output_file = open(output_file_path, 'w')
    for A, B, support, confidence in rules:
        #print("{" + ",".join(map(str, A)) + "} {" + ",".join(map(str, B)) + "} {:.2f} {:.2f}\n".format(support, confidence))
        s = "{{{}}} {{{}}} {:.2f} {:.2f}\n".format(",".join(map(str, A)), ",".join(map(str, B)), support, confidence)

        output_file.write(s)
    
    output_file.close()
