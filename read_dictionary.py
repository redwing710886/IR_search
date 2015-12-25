import codecs
import time
import re
import jieba

jieba.set_dictionary('dict.txt.big.txt')

content = []

#讀取字典
with codecs.open('dictionary.txt','rb','utf-8') as f:
    content = f.readlines()

d = {}    

#將dictionary.txt內字典檔分解形成d
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


#搜尋文字前處理
def pre_process(find_list):
    result = [] 
    temp = find_list.split()
    count = 0
    
    #判斷使用者是否有輸入搜尋條件
    if len(temp) == 0:
        print ('無輸入')
        return None,None
    
    #長字串斷詞
    ax = []
    
    for i in temp:
        ax.append(i)
        if i.lower() != 'and' and i.lower() != 'or' and i.lower() != 'not' and re.search('^/[0-9]+$',i) == None:
            sam = jieba.lcut_for_search(i)
            for j in sam:
                if j != i:
                    ax.append('and')
                    ax.append(j)   
    temp = ax
    
    check_head = False #檢查是否為搜尋條件開頭
    
    #判斷是否搜尋條件僅為單一字詞
    if type(temp[0]) == str and len(temp) == 1:
        result.append(temp[0])
    
    #將搜尋條件分割
    while len(temp) > 1:
        if re.search('^/[0-9]+$',temp[1]) != None: #是否為/k
            count = 2
            result.append([temp[0],temp[1],temp[2]])
        elif temp[1].lower() == 'and' or temp[1].lower() == 'or' or temp[1].lower() == 'not': #是否為and,or,not
            if len(temp) == 2:
                if len(result) == 0:
                    return temp,single_find(temp[0])
            elif not check_head:
                result.append([temp[0],temp[1],temp[2]])
            else:
                result.append([temp[1],temp[2]])
            count = 2
        else: #2單獨字詞
            if not check_head:
                result.append([temp[0],'and',temp[1]])
            else:
                result.append(['and',temp[1]])
            count = 1
            
        for i in range(count):
            temp.pop(0)
        count = 0
        
        check_head = True    
    
    #進行詞彙檢測
    result = check_query(result)
    
    #若處理後搜尋條件變得不存在
    if result == None:
        return None,None
    
    last_answer = []
    first_term = ''
    
    #進行字串檢索，找出符合條件的文章
    if len(result) != 0:
        if type(result[0]) == str:
            return result,single_find(result[0])
        for i in result:
            if i == result[0]:
                last_answer = choose(result[0])
            else:
                if re.search('^/[0-9]+$',i[1]) != None:
                    get = choose(i)
                    if last_answer != None:
                        if get != None:
                            last_answer = choose([last_answer,'and',get])
                        else:
                            last_answer = last_answer
                    else:
                        last_answer = get       
                else:
                    if last_answer != None and len(last_answer) != 0:
                        la = choose([last_answer,i[0],i[1]])
                        if len(la) != 0:
                            last_answer = la
                    else:
                        last_answer = choose([first_term,i[0],i[1]])
            first_term = i[-1]
        if last_answer == None or len(last_answer) == 0:
            last_answer = single_find(result[0][0])
    else:
        last_answer = None
            
    return result,last_answer
            
#進行詞彙檢測，回傳存在為字典d的單字
def check_query(find_list):
    words = find_list
    final = []
    term = ''
    
    #單一詞彙
    if type(words[0]) == str:
        if words[0] in d:
            return find_list
        else:
            return None
    
    for i in words:
        temp = i
        if len(i) == 3:
            if i[0] not in d:
                if i[2] not in d:
                    continue
                else:
                    if term != '':
                        final.append([term,i[1],i[2]])
                        term = ''
                    else:
                        term = i[2]
            else:
                if i[2] not in d:
                    term = i[0]
                else:
                    final.append(i)
        elif len(i) == 2:
            if i[1] not in d:
                continue
            else:
                if term != '':
                    i.insert(0,term)
                    term = ''
                    final.append(i)
                else:
                    if len(final) ==0:
                        term = i[1]
                    else:
                        final.append(i)
    if term != '':
        final.append(term)
    return final

#選擇以哪種邏輯檢測
def choose(find_list): 
    words = find_list
    
    #搜尋詞彙化為陣列
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
        return proximity_search(words,words[1])
    else:
        return None

#單一搜尋條件
def single_find(find_word):
    if find_word in d:
        x = []
        for n in iter(d[find_word]): 
            x.append(n)
        return sorted(x)
    else:
        return None

#有著and,or,not的搜尋
def complex_find(x,y,mode):
    if mode == 'and':
        return sorted(list((set(x).union(set(y)))^(set(x)^set(y))))
    elif mode == 'or':
        return sorted(list((set(x).union(set(y)))))
    elif mode == 'not':
        return sorted(list(set(x)^((set(x).union(set(y)))^(set(x)^set(y)))))
    else:
        return None

#精密搜尋
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
w,answer = pre_process(find)

qword = ''

print (w)

#搜尋詞彙字典化
if w != None:
    if type(w[0]) == str:
        qword = w[0]
    else:
        for i in w:
            for j in i:
                qword = qword + j + '@'
            qword = qword[0:len(qword)-1]
            qword = qword + '#'
        qword = qword[0:len(qword)-1]

#顯示結果文章
if answer != None and len(answer) != 0:
    print (qword)
    '''with codecs.open('result.txt','w','utf-8') as f:
        f.write(qword+'\n')
        for i in answer:
            print (i)
            f.write(i+'\n')'''
    for i in answer:
        print (i)
else:
    print ('符合檢索條件檔案不存在')