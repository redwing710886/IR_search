import codecs
import os
import time
import jieba

jieba.set_dictionary('dict.txt.big.txt')

file_path = '../desktop/IRdata/'

file_list = []

for file in os.listdir(file_path):
    file_list.append(file)     
    
t = {}

count = 1

for file in file_list:
    with codecs.open(file_path+file,'rb','utf-8') as f:
        content = f.read()
        #print (os.path.splitext(file)[0])
        
        words = jieba.tokenize(content)
        for word in words:
            if word[0] not in t:
                t[word[0]] = {file:[word[1]]}
            else:
                if file not in t[word[0]]:
                    t[word[0]][file] = [word[1]]
                else:
                    t[word[0]][file].append(word[1])
            
        '''if count == 10:
            break
        if count % 100 == 0:
            print (count)
        count = count + 1'''

'''ccc = ''
block = ''

for term_cut in iter(t):
    block = block + term_cut + '#'
    for doc_cut in iter(t[term_cut]):
        block = block + doc_cut + '@'
        block = block + '---'.join(str(t[term_cut][doc_cut]))
        block = block + '$'
    block = block + '&&&'
    ccc = ccc + block
    block = ''

print (ccc)'''


block = ''

with codecs.open('dictionary.txt','w','utf-8') as f:
    for term_cut in iter(t):
        block = block + term_cut + '#'
        for doc_cut in iter(t[term_cut]):
            block = block + doc_cut + '#'
            for g in t[term_cut][doc_cut]: 
                block = block + str(g) + '$'
            block = block + '#'
        f.write(block+'\n')
        block = ''



        
    
        
'''for n in iter(t):
    if len(t[n]) > 400:
        print (n,len(t[n]))'''
        
'''find = input('請輸入要尋找的單字：')

check2 = True
while check2:
    if find in t:
        x = []
        for n in iter(t[find]): 
            x.append(n)
        for s in iter(sorted(x)):
            print (s)
        print ()
    else:
        print ('字元並不存在')
    con = input('請問是否繼續？[y]/n：')
    if con == 'n':
        check2 = False
    elif con == 'y':
        find = input('請輸入要尋找的單字：')
    else:
        print ('再見')
        break'''

