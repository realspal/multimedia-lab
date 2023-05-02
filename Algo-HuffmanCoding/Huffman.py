# implementation of Huffman Coding algorithm of variable length coding scheme
# Soumyadeep Pal (IT UG3, Roll 002011001113)

# importing required libraries
import math
import heapq
import csv
import json
from collections import Counter

# tree node class definition
class HuffmanNode:
    def __init__(self,symbol=None,freq=0,left=None,right=None):
        self.symbol=symbol
        self.freq=freq
        self.left=left
        self.right=right
    def __lt__(self,other):
        return self.freq<other.freq

# encoder class definition     
class HuffmanEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj,HuffmanNode):
            return {"symbol":obj.symbol,"freq":obj.freq,"left":obj.left,"right":obj.right}
        return super().default(obj)

# function to implement Huffman coding        
def huffman_encoding(data,maxbits):
    if not data:
        return None, None, None, None
    freq_dict={}
    for symbol in data:
        freq_dict[symbol]=freq_dict.get(symbol,0)+1
    heap=[]
    for symbol,freq in freq_dict.items():
        heapq.heappush(heap,HuffmanNode(symbol=symbol,freq=freq))
    while len(heap)>1:
        node1=heapq.heappop(heap)
        node2=heapq.heappop(heap)
        merged_node=HuffmanNode(freq=node1.freq+node2.freq,left=node1,right=node2)
        heapq.heappush(heap,merged_node)
    root=heap[0]
    code_dict={} 
    def traverse(node,code):
        if node.symbol:
            code_dict[node.symbol]=code
            return
        traverse(node.left,code+"0")
        traverse(node.right,code+"1")
    traverse(root,"")
    symbol_table={symbol:code for symbol,code in code_dict.items()}
    encoded_data="".join([code_dict[symbol] for symbol in data])
    coding_tree=json.dumps(root,cls=HuffmanEncoder,indent="    ")
    compression_ratio=(1-len(encoded_data)/(maxbits*len(data)))*100
    # Calculate the average code length
    code_lengths=[len(code_dict[symbol]) for symbol in freq_dict]
    avg_code_length=sum(code_lengths[i]*freq_dict[list(freq_dict.keys())[i]] for i in range(len(freq_dict)))/len(data)
    # Calculate the entropy of the data
    entropy=-sum(freq_dict[symbol]/len(data)*math.log(freq_dict[symbol]/len(data),2) for symbol in freq_dict)
    # Calculate the efficiency of the compression
    efficiency=(entropy/avg_code_length)*100
    return encoded_data,coding_tree,symbol_table,compression_ratio,avg_code_length,entropy,efficiency

# main
print('------------------------------------------------------------------------------------------')
msg=input('Enter message         :  ')
data=Counter(msg);
datarange=(str(data)).count(':')
print('Number of characters  : ',datarange)
print('Character frequencies : ',(str(data))[8:-1])
maxbits=math.ceil(math.log(datarange,2))
b0=len(msg)*maxbits
print('Original message size : ',b0,' bits')
encdata,tree,symboltable,compratio,avgcodelen,entropy,efficiency=huffman_encoding(msg,maxbits)
print('Encoded message       : ',encdata)
b1=len(encdata)
print('Encoded message size  : ',b1,' bits')
print('Compression ratio     :  %.2f%%' % compratio)
print('------------------------------------------------------------------------------------------')
print('Average code length   :  %.2f bits/symbol' % avgcodelen)
print('Entropy               :  %.2f bits/symbol' % entropy)
print('Efficiency            :  %.2f' % efficiency)
textfile=open("HuffmanValues.txt","w")
textfile.write('Average code length   :  %.2f bits/symbol \n' % avgcodelen)
textfile.write('Entropy               :  %.2f bits/symbol \n' % entropy)
textfile.write('Efficiency            :  %.2f' % efficiency)
textfile.close()
print('------------------------------------------------------------------------------------------')
print("Symbol  Code  (Table exported in CSV file)")
codetable=[];
for symbol,code in symboltable.items():
    print(f"{symbol}       {code}")
    codetable.append([symbol,code])
fields=['Symbol','Code']
with open('HuffmanSymbolCodeTable.csv','w',newline='') as csvfile:
    csvwriter=csv.writer(csvfile)
    csvwriter.writerow(fields)
    csvwriter.writerows(codetable)
print('------------------------------------------------------------------------------------------')
print('Coding Tree  (Tree exported in JSON file)')
print(tree)
with open('HuffmanCodingTree.json','w') as f:
    json.dump(tree,f)
print('------------------------------------------------------------------------------------------')