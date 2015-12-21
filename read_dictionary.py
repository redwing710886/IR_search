import codecs
import time
import re

file_path = '../desktop/IRdata/'

content = []

#讀取字典
with codecs.open('dictionary.txt','rb','utf-8') as f:
    content = f.readlines()

d = {}    

#字典檔分解
for n in content:
    t = {}
    temp = n.split('#')
    temp.pop()
    if len(temp) == 0:
        continue
    term = temp[0]
    temp.pop(0)
    count = 1
    word = ''
    for x in temp:
        if count % 2 == 1:
            word = x
        else:
            num = x.split('$')
            num.pop()
            num = list(map(int, num))
            t[word] = num
            word = ''
        count = count + 1
    d[term] = t

def pre_process(find_list):
    result = []
    temp = find_list.split()
    count = 0
    
    if len(temp) == 1:
        return single_find(find_list)
    
    check_head = False
    
    while len(temp) > 1:
        if re.search('^/[0-9]+$',temp[1]) != None:
            count = 2
            result.append([temp[0],temp[1],temp[2]])
        elif temp[1].lower() == 'and' or temp[1].lower() == 'or' or temp[1].lower() == 'not':
            if not check_head:
                result.append([temp[0],temp[1],temp[2]])
            else:
                result.append([temp[1],temp[2]])
            count = 2
        else:
            if not check_head:
                result.append([temp[0],'and',temp[1]])
            else:
                result.append(['and',temp[1]])
            count = 1
            
        for i in range(count):
            temp.pop(0)
        count = 0
        
        check_head = True
    
    last_answer = []

    if len(result) != 0:
        for i in result:
            if i == result[0]:
                last_answer = choose(result[0])
            else:
                if re.search('^/[0-9]+$',i[1]) != None:
                    last_answer = choose([last_answer,'and',choose(i)])
                else:
                    ccc = i
                    ccc.insert(0,last_answer)
                    last_answer = choose(ccc)
    else:
        last_answer = None
        
    return last_answer
        

def choose(find_list): 
    words = find_list
    
    x = []
    y = []
    
    if type(words[0]) == str:
        for n in iter(d[words[0]]): 
            x.append(n)
    else:
        x = words[0]
    
    if type(words[2]) == str:
        for n in iter(d[words[2]]): 
            y.append(n)
    else:
        y = words[2]
        
    if words[1] == 'and' or words[1] == 'AND':
        return complex_find(x,y,'and')
    elif words[1] == 'or' or words[1] == 'OR':
        return complex_find(x,y,'or')
    elif words[1] == 'not' or words[1] == 'NOT':
        return complex_find(x,y,'not')
    elif re.search('^/[0-9]+$',words[1]) != None:
        #return complex_find(words,words[1])
        return proximity_search(words,words[1])
    else:
        return None
        
def single_find(find_word):
    if find_word in d:
        x = []
        for n in iter(d[find_word]): 
            x.append(n)
        return sorted(x)
    else:
        return None

def complex_find(x,y,mode):
    if mode == 'and':
        return sorted(list((set(x).union(set(y)))^(set(x)^set(y))))
    elif mode == 'or':
        return sorted(list((set(x).union(set(y)))))
    elif mode == 'not':
        return sorted(list(set(x)^((set(x).union(set(y)))^(set(x)^set(y)))))
    else:
        return None

def proximity_search(find_words,distance):
    number = int(distance[1:len(distance)])
    condidate = choose([find_words[0],'and',find_words[2]])
    z = []
    for cond in condidate:
        first = d[find_words[0]][cond]
        second = d[find_words[2]][cond]
        for i in first:
            for j in second:
                if abs(i-j) <= number: #需再修正，/k是單字而非位置
                    z.append(cond)
    if len(z) > 0:
        return sorted(z)
    else:
        return None
        
find = input('請輸入要尋找的單字：')
#answer = choose(find)
answer = pre_process(find)
if answer != None:
    for i in answer:
        print (i)
else:
    print ('符合檢索條件檔案不存在')

