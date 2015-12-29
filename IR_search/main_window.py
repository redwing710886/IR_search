import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from read_dictionary import *
import codecs

class Findpage(QWidget):
    
    oo = Analysis()
    file_path = '../desktop/IRdata/'
    
    def __init__(self, parent = None):
        super(Findpage, self).__init__(parent)
        self.createLayout()
        self.createConnection()

    def search(self):
        self.textBrowser.clearHistory()
        self.textBrowser.setText('')
        word = self.lineEdit.text()
        w,answer = self.oo.get_text(word)
        
        if answer != None and len(answer) != 0:
            count = 0
            for i in answer[0]:
                with codecs.open(self.file_path+i,'rb','utf-8') as f:
                    #self.textBrowser.append("<span style=\" color:#ff0000;\" >"+f.readline()+"</span>")
                    self.textBrowser.append('<a href=%s>%s</a>' % (i,i))
                    self.textBrowser.append('<p>'+f.readline()+'</p>')
                    count = count + 1
                    if count == 10:
                        break
                
                    
    def createLayout(self):
        self.lineEdit = QLineEdit()
        self.goButton = QPushButton("&GO")
        h1 = QHBoxLayout()
        h1.addWidget(self.lineEdit)
        h1.addWidget(self.goButton)

        self.quitButton = QPushButton("&Quit")
        h2 = QHBoxLayout()
        h2.addStretch(1)
        h2.addWidget(self.quitButton)

        self.textBrowser = QTextBrowser(self)
        self.textBrowser.setOpenLinks(False)
        
        layout = QVBoxLayout()
        layout.addLayout(h1)
        layout.addWidget(self.textBrowser)
        layout.addLayout(h2)
        
        self.dialogTextBrowser = Secondpage(self)
        
        self.setLayout(layout)
        self.setWindowTitle("Main")
        self.setFixedSize(800,600)

    def createConnection(self):
        self.lineEdit.returnPressed.connect(self.search)
        self.lineEdit.returnPressed.connect(self.lineEdit.selectAll)
        self.goButton.clicked.connect(self.search)
        self.goButton.clicked.connect(self.lineEdit.selectAll)
        self.quitButton.clicked.connect(self.close)
        
        self.textBrowser.anchorClicked.connect(self.on_pushButton_clicked)
        
    def on_pushButton_clicked(self,url):
        print (url.toString())
        self.dialogTextBrowser.set_word(url.toString())
        self.dialogTextBrowser.exec_()

class Secondpage(QDialog):
    
    file_path = '../desktop/IRdata/'
    
    def __init__(self, parent = None):
        super(Secondpage, self).__init__(parent)
        self.createLayout()
        self.createConnection()
        
    def createLayout(self):
        self.textBrowser = QTextBrowser(self)

        layout = QVBoxLayout()
        layout.addWidget(self.textBrowser)
        
        self.quitButton = QPushButton("&Quit")
        h2 = QHBoxLayout()
        h2.addStretch(1)
        h2.addWidget(self.quitButton)
        
        self.setLayout(layout)
        layout.addLayout(h2)
        self.setWindowTitle("Result")
        self.setFixedSize(800,600)
        
    def createConnection(self):
        self.quitButton.clicked.connect(self.close)
        
    def set_word(self,url):
        with codecs.open(self.file_path+url,'rb','utf-8') as f:
            self.textBrowser.setText(f.read())

app = QApplication(sys.argv)

findpage = Findpage()
findpage.show()

app.exec_()