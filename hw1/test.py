from itertools import combinations
import sys

def readFile(file_path):
    tr = [] #transaction

    with open(file_path, 'r') as file:
        for line in file:
            i = list(map(int, line.strip().split()))  
            tr.append(i)
    
    tr = [set(item) for item in tr] #avoid duplicates in single transaction

    return tr
def calcSup(tr, iset):
    cnt = sum(1 for tr in tr if iset.issubset(tr)) #get number of itemsets in
    return (cnt / len(tr) * 100)
def calcConf(freqs, A, B):
    pass
def genCand(freqs, idx): #generate candidates
    cand = [] #candidate itemsets
    cnt = len(freqs)

    for i in range(cnt):
        for j in range(i+1, cnt):
            freqs1, sup1 = freqs[i] #call two itemsets
            freqs2, sup2 = freqs[j]
            nset = freqs1.union(freqs2) #union
            if len(nset) == idx: #if union s equal to idx
                cand.append(nset)
    return cand
def findFreqsets(tr, minsup):
    freqs = [] #list of frequent itemsets

    #single element itemsets
    single = set(item for transaction in tr for item in transaction)
    freqsingle = [(item, calcSup(tr, item)) for item in single]
    freqs.extend([itemset for itemset, support in freqsingle if support >= minsup]) #pass single only if support >= minsup
    #multiple
    idx = 2
    while True:
        cand = genCand(freqs, idx)
        if not cand:
            break
        #freq_idx = [] #temporary list for current index
        for item in cand:
            if calcSup(tr, item) >= minsup:
                freqs.append(item)

        if not freqs: #no more frequent itemsets
            break

        idx += 1 #to next index
    return freqs
def genAsso(freqs, minconf): #generate association rules
    rules = []
    #A -> B 
    for i in range(1, len(freqs) + 1):
        pass
        
    return rules

# Example usage
if __name__ == "__main__":
    file_path = "./input.txt"
    minsup = 0.4
    minconf = 0.6

    transactions = readFile(file_path)
    freqsets = findFreqsets(transactions, minsup)
    print(freqsets)
    #rules = genAsso(freqsets, minconf)

    '''
    for A, B, support, confidence in rules:
        print("{", ",".join(map(str, A)), "}", "{", ",".join(map(str, B)), "}", '{:.2f}'.format(support), '{:.2f}'.format(confidence))
    '''

