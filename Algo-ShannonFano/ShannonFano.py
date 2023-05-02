# implementation of Shannon Fano algorithm of variable length coding scheme
# Soumyadeep Pal (IT UG3, Roll 002011001113)

# importing required libraries
import math
import heapq
import csv
import json
from collections import Counter

# tree node class definition
class Node:
    def __init__(self,symbol,freq,left=None,right=None):
        self.symbol=symbol
        self.freq=freq
        self.left=left
        self.right=right    
    def __lt__(self,other):
        return self.freq<other.freq    
    def __eq__(self,other):
        if other==None:
            return False
        if not isinstance(other,Node):
            return False
        return self.freq==other.freq

# function to build tree    
def build_tree(data):
    heap=[Node(symbol,freq) for symbol,freq in data.items()]
    heapq.heapify(heap)    
    while len(heap)>1:
        left=heapq.heappop(heap)
        right=heapq.heappop(heap)
        parent = Node(None,left.freq+right.freq,left,right)
        heapq.heappush(heap, parent)        
    return heap[0]

# function to assign codes   
def assign_codes(node,code_dict,code=''):
    if node is None:
        return    
    if node.symbol is not None:
        code_dict[node.symbol]=code
        return
    
    assign_codes(node.left,code_dict,code+'0')
    assign_codes(node.right,code_dict,code+'1')

# function to implement Shannon Fano coding   
def shannon_fano_coding(data):
    tree=build_tree(data)
    code_dict={}
    assign_codes(tree,code_dict)    
    return tree, code_dict

# compress function
def compress(data, code_dict):
    return ''.join(code_dict[symbol] for symbol in data)

# main
print('------------------------------------------------------------------------------------------')
msg=input('Enter message         :  ')
data=Counter(msg);
datarange=(str(data)).count(':')
print('Number of characters  : ',datarange)
print('Character frequencies : ',(str(data))[8:-1])
b0=len(msg)*math.ceil(math.log(datarange,2))
print('Original message size : ',b0,' bits')
tree,codedict=shannon_fano_coding(data)
compdata=compress(data,codedict)
print('Encoded message       : ',compdata)
b1=len(compdata)
print('Encoded message size  : ',b1,' bits')
compratio=b0/b1
print('Compression ratio     : ',compratio)
print('------------------------------------------------------------------------------------------')
print("Symbol  Code  (Table exported in CSV file)")
codetable=[];
for symbol,code in codedict.items():
    print(f"{symbol}       {code}")
    codetable.append([symbol,code])
fields=['Symbol','Code']
with open('symbolCodeTable.csv','w',newline='') as csvfile:
    csvwriter=csv.writer(csvfile)
    csvwriter.writerow(fields)
    csvwriter.writerows(codetable)
print('------------------------------------------------------------------------------------------')
def node_to_dict(node):
    if node.symbol is not None:
        return {'symbol':node.symbol,'freq':node.freq}
    else:
        return {'freq':node.freq,'left':node_to_dict(node.left),'right':node_to_dict(node.right)}
treedict = node_to_dict(tree)
with open('codingTree.json','w') as f:
    json.dump(treedict, f)
print('Coding Tree  (Tree exported in JSON file)')
print(json.dumps(treedict,indent=4))
print('------------------------------------------------------------------------------------------')