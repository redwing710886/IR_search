import codecs
import os
import jieba

class Dictionary():

    jieba.set_dictionary('dict.txt.big.txt')
    file_path = '../desktop/IRdata/'
    d = {}
    
    def __init__(self):
        self.make_dic()
    
    def make_dic(self):
        
        file_list = []

        for file in os.listdir(self.file_path):
            file_list.append(file)     

        for file in file_list:
            with codecs.open(self.file_path+file,'rb','utf-8') as f:
                content = f.read()
                #print (os.path.splitext(file)[0])

                words = jieba.tokenize(content)
                for word in words:
                    if word[0] not in self.d:
                        self.d[word[0]] = {file:[word[1]]}
                    else:
                        if file not in self.d[word[0]]:
                            self.d[word[0]][file] = [word[1]]
                        else:
                            self.d[word[0]][file].append(word[1])
                            
    def get_dic(self):
        return self.d

