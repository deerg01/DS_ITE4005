import pandas as pd
import math
import sys

class DTree(object):
    def __init__(self, data):
        self.data = data
        self.attn = None #Attribute name
        self.classn = data.columns[-1] #name of predicted class
        self.labeln = None #name of predicted 'value'
        self.child = dict() #dictionary works better on managing unknown number of children
    
    def split(self):
        #print(gentropy(self.data))
        if gentropy(self.data) == 0.0: #is leaf node
            name = self.data[self.classn] #find leaf class name
            self.labeln = name.unique()[0] #extract representative values for each labels

            return
        else: #need to split
            bestAtt = maxGain(self.data) #select best path(attribute)
            #print('>>>>' + bestAtt)
            self.attn = bestAtt #add to attribute list
            
            for i in self.data[bestAtt].unique(): #separate data with attribute
                subData = self.data[self.data[bestAtt] == i] #collect data with att 'i'
                subTree = DTree(data = subData)
                self.child[i] = subTree
                subTree.split()

    def decide(self, series):
        #print(series)
        #print(self.attn)
        if self.labeln != None: #classified
            return str(self.labeln) #return classification result
        else: #unclassified
            subTree = self.child[series[self.attn]]
            for c in self.child: 
                for v in series.values:
                    #print(c, v)
                    if c == v: #if c contained in test series
                        return subTree.decide(series)
                    else:
                        self.classn = self.data.iloc[:, -1].value_counts().idxmax()
                        return str(self.classn)
            
def maxGain(data):
    tmp = 0.0
    bestAtt = None
    for i in data.columns[:-1]: #for all attributes
        gain_ = gain(data, i) #get gain
        if gain_ > tmp:
            tmp = gain_
            bestAtt = i
    
    return bestAtt
def gain(data, att):
    info = gentropy(data)
    infoA = 0.0
    v = data[att].unique() #each values for selected attribute
    for j in v:
        subData = data[data[att] == j] #split datas along value 'j'
        infoA += (len(subData) / len(data)) * gentropy(subData) #calculate entropy

    return (info - infoA)
def gentropy(data): #get entropy
    info  = 0.0 
    size = len(data)
    m = data.iloc[:, -1].value_counts().to_dict() #count number of classes. save as dictionary type
    for i in m.values(): #for each class. calculate entropy
        p = i / size
        info -= p * math.log2(p)
    
    return info
def write(tree):
    test = pd.read_table(sys.argv[2], sep='\t')
    out = open(sys.argv[3], 'w')
    tmp = ''
    for item in (tree.data.columns[: -1]): #write Attribute names
        tmp += str(item) + '\t' 
    tmp += tree.classn + '\n'
   
    for i in test.index: #row 개수만큼 반복
        for j in test.iloc[i]: #row 정보 읽기
            tmp += str(j) + '\t'
        v = tree.decide(test.iloc[i]) #label 입력하기
        tmp += str(v) + '\n'

    out.write(tmp)
    out.close()


if __name__ == '__main__':
    tree = DTree(pd.read_table(sys.argv[1], sep='\t'))
    
    tree.split() #train
    #print(tree.attn)
    #print('########################training complete########################')
    #print(tree.classn)
    write(tree) #test
    #print('#############################test complete#############################')                