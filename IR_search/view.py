from read_dictionary import *

find = input('請輸入要尋找的單字：')
oo = Analysis()
w,answer = oo.get_text(find)

print (w)

#顯示結果文章
if answer != None and len(answer) != 0:
    for i in answer:
        print (i)
else:
    print ('符合檢索條件檔案不存在')