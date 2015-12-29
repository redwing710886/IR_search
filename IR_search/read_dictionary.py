import codecs
import time
import re
import jieba
from make_dictionary import *

class Analysis:
    
    d = {}
    qq = Dictionary()
    
    jieba.set_dictionary('dict.txt.big.txt')
    
    def __init__(self):
        self.read_dictionary()
    
    def read_dictionary(self):
        self.d = self.qq.get_dic()
        '''with codecs.open('dictionary.txt','rb','utf-8') as f:
            content = f.readlines()

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
            self.d[term] = t'''

    def get_text(self,query):
        return self.pre_process(query)

    #搜尋文字前處理
    def pre_process(self,find_list):
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
                if i in self.d:
                    continue
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
                        return temp,self.single_find(temp[0])
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
        result = self.check_query(result)

        #若處理後搜尋條件變得不存在
        if result == None:
            return None,None

        last_answer = []
        temp_answer = []

        #進行字串檢索，找出符合條件的文章
        if len(result) != 0:
            if type(result[0]) == str:
                #return result,[self.single_find(result[0])]
                return result,[self.qq.get_rank_sort(result[0])]
            for i in result:
                if i == result[0]:
                    temp_answer = self.choose(result[0])
                    if temp_answer == None or len(temp_answer) == 0:
                        temp_answer = i[2]
                else:
                    if re.search('^/[0-9]+$',i[1]) != None:
                        get = self.choose(i)
                        if temp_answer != None:
                            if get != None:
                                temp_answer = self.choose([temp_answer,'and',get])
                            else:
                                temp_answer = temp_answer
                        else:
                            temp_answer = get

                    else:
                        if temp_answer != None and len(temp_answer) != 0:
                            ccc = [temp_answer,i[0],i[1]]
                            temp_answer = self.choose(ccc)
                        else:
                            temp_answer = i[1]
            
                if temp_answer != None and type(temp_answer) != str and len(temp_answer) != 0:
                    last_answer.insert(0,temp_answer)
        else:
            last_answer = None

        return result,last_answer
            
    #進行詞彙檢測，回傳存在為字典d的單字
    def check_query(self,find_list):
        words = find_list
        final = []
        term = ''

        #單一詞彙
        if type(words[0]) == str:
            if words[0] in self.d:
                return find_list
            else:
                return None

        for i in words:
            temp = i
            if len(i) == 3:
                if i[0] not in self.d:
                    if i[2] not in self.d:
                        continue
                    else:
                        if term != '':
                            final.append([term,i[1],i[2]])
                            term = ''
                        else:
                            term = i[2]
                else:
                    if i[2] not in self.d:
                        term = i[0]
                    else:
                        final.append(i)
            elif len(i) == 2:
                if i[1] not in self.d:
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
    def choose(self,find_list): 
        words = find_list

        #搜尋詞彙化為陣列
        x = []
        y = []

        if type(words[0]) == str:
            '''for n in iter(self.d[words[0]]): 
                x.append(n)'''
            x = self.qq.get_rank_sort(words[0])
        else:
            x = words[0]

        if type(words[2]) == str:
            '''for n in iter(self.d[words[2]]): 
                y.append(n)'''
            y = self.qq.get_rank_sort(words[2])
        else:
            y = words[2]

        if words[1] == 'and' or words[1] == 'AND':
            return self.complex_find(x,y,'and')
        elif words[1] == 'or' or words[1] == 'OR':
            return self.complex_find(x,y,'or')
        elif words[1] == 'not' or words[1] == 'NOT':
            return self.complex_find(x,y,'not')
        elif re.search('^/[0-9]+$',words[1]) != None:
            return self.proximity_search(words,words[1])
        else:
            return None

    #單一搜尋條件
    def single_find(self,find_word):
        if find_word in self.d:
            x = []
            for n in iter(self.d[find_word]): 
                x.append(n)
            return sorted(x)
        else:
            return None

    #有著and,or,not的搜尋
    def complex_find(self,x,y,mode):
        if mode == 'and':
            return list((set(x).union(set(y)))^(set(x)^set(y)))
        elif mode == 'or':
            return list((set(x).union(set(y))))
        elif mode == 'not':
            return list(set(x)^((set(x).union(set(y)))^(set(x)^set(y))))
        else:
            return None

    #精密搜尋
    def proximity_search(self,find_words,distance):
        number = int(distance[1:len(distance)])
        condidate = self.choose([find_words[0],'and',find_words[2]])
        z = []
        vv = []
        for cond in condidate:
            first = self.d[find_words[0]][cond]
            second = self.d[find_words[2]][cond]
            check_close = False
            counter = 0
            for i in first:
                for j in second:
                    if abs(i-j) <= number: 
                        check_close = True
                        counter = counter + 1
            if check_close:
                vv.append([counter,cond])
        vv.sort(reverse=True)
        for i in vv:
            z.append(i[1])
        if len(z) > 0:
            return z
        else:
            return None