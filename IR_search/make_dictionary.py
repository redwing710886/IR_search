import codecs
import os
import jieba
from math import log

class Dictionary():

    jieba.set_dictionary('dict.txt.big.txt')
    file_path = '../desktop/IRdata/'
    d = {}
    r = {}
    t = {}
    
    def __init__(self):
        self.make_dic()
        self.make_rank()
    
    def make_dic(self):
        
        file_list = []

        for file in os.listdir(self.file_path):
            file_list.append(file)     

        for file in file_list:
            with codecs.open(self.file_path+file,'rb','utf-8') as f:
                content = f.read()
                #print (os.path.splitext(file)[0])
                words = jieba.tokenize(content)
                self.t[file] = {}
                
                for word in words:
                    if word[0] not in self.d:
                        self.d[word[0]] = {file:[word[1]]}
                    else:
                        if file not in self.d[word[0]]:
                            self.d[word[0]][file] = [word[1]]
                        else:
                            self.d[word[0]][file].append(word[1])

                    if word[0] not in self.t[file]:
                        self.t[file][word[0]] = [word[1]]
                    else:
                        self.t[file][word[0]].append(word[1])
                
                            
    def make_rank(self):
        for words in iter(self.d):
            df = len(self.d[words])
            self.r[words] = {}
            li = []
            for txt in iter(self.d[words]):
                tf = len(self.d[words][txt])
                self.r[words][txt] = round((1+log(tf,2)) * log(1200/df,2),5)
    
                 
    def get_dic(self):
        return self.d
    
    def get_dic_text(self,text):
        if text not in self.d:
            return None
        return self.d[text]
    
    def get_rank(self):
        return self.r
    
    def get_rank_sort(self,term):
        li = []
        ans = []
        if term not in self.r:
            return None
        for i in iter(self.r[term]):
            li.append([self.r[term][i],i])
        li.sort(reverse=True)
        for j in li:
            ans.append(j[1])
        return ans
    
    def get_term(self):
        return self.t
    
    def get_term_file(self,file):
        if file not in self.t:
            return None
        return self.t[file]