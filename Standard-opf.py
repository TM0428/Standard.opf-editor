import os
import sys
import zipfile
import subprocess
import change_standard_opf
import webbrowser
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

text_dir = os.getcwd()

class maindata:
    title = ""


# メインとなるウィンドウ
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.title = "Opf file editor"
        self.title_text = ""
        self.initUI()
        
        
    def initUI(self):               
        #設定
        self.setWindowTitle(self.title)
        self.resize(600, 600)
        self.center()
        self.statusBar().showMessage("Made by TM")
        mainMenu = self.menuBar() 
        fileMenu = mainMenu.addMenu("File")
        helpMenu = mainMenu.addMenu("Help")
        exitButton = QAction(QIcon("exit24.png"), "Exit", self)
        exitButton.setShortcut("Ctrl+Q")
        exitButton.setStatusTip("Exit application")
        exitButton.triggered.connect(self.close)
        dirbutton = QAction(QIcon("hoge.png"), "Epubの作成", self)
        dirbutton.setShortcut("Ctrl+E")
        dirbutton.triggered.connect(self.dir_def)
        unepubbutton = QAction(QIcon("hoge.png"), "Epubの解凍", self)
        unepubbutton.setShortcut("Ctrl+R")
        unepubbutton.triggered.connect(self.epub_to_zip)
        versionbutton = QAction(QIcon("hoge.png"), "バージョン", self)
        versionbutton.triggered.connect(self.versiontab)
        fileMenu.addAction(dirbutton)
        fileMenu.addAction(unepubbutton)
        fileMenu.addAction(exitButton)
        helpMenu.addAction(versionbutton)
        tmp = UI(self)

        self.setCentralWidget(tmp)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def epub_to_zip(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', text_dir,"Epubファイル(*.epub)")
        root, ext = os.path.splitext(fname[0])
        if fname[0] == "" or ext != ".epub":
            return
        dirname = os.path.dirname(fname[0])
        basename = os.path.basename(fname[0])
        bname, ext = os.path.splitext(basename)
        os.rename(fname[0], os.path.join(dirname,bname + ".zip"))
        unzip(dirname + "/" + bname, dirname + "/" + bname + ".zip")
        os.remove(dirname + "/" + bname + ".zip")
        QMessageBox.question(self, "Message", "Epubを解凍しました", QMessageBox.Ok, QMessageBox.Ok)
        
    def dir_def(self):
        fname = QFileDialog.getExistingDirectory(self, 'Open file', text_dir)
        text,ok = QInputDialog.getText(self, 'Epubのファイル名を指定...', 'Epubのファイル名を指定...',QLineEdit.Normal,maindata.title)
        if ok:
            t = str(text)
        else:
            t = os.path.basename(fname)
        if fname == "":
            return
        Epub_gene_full(fname)
        cmd1 = "zip -0 -X ../\"" + t + ".epub\" mimetype"
        cmd2 = "zip -r ../\"" + t + ".epub\" * -x mimetype"
        subprocess.call(cmd1)
        subprocess.call(cmd2)
        QMessageBox.question(self, "Message", "Epubを作成しました", QMessageBox.Ok, QMessageBox.Ok)

    def versiontab(self):
        QMessageBox.question(self, "Version", "0.0.5 beta", QMessageBox.Ok, QMessageBox.Ok)

def unzip(dirpass,filepass):
    with zipfile.ZipFile(filepass,'r') as inputFile:
        inputFile.extractall(dirpass)

def Epub_gene_full(fname):
    os.chdir(fname)

#UIを作成しているウィンドウ
class UI(QWidget):
    def __init__(self, parent=None):
        super(UI, self).__init__(parent)
        self.initUI()

    def initUI(self):
        standard_opf = QLabel("Standard.opf...", self)
        title_label = QLabel("タイトル", self)
        title_label2 = QLabel("タイトル(カタカナ)", self)
        author_label1 = QLabel("著者名1", self)
        author_label1_2 = QLabel("著者名1(カタカナ)", self)
        author_label2 = QLabel("著者名2", self)
        author_label2_2 = QLabel("著者名2(カタカナ)", self)
        publisher_label = QLabel("出版社", self)
        publisher_label2 = QLabel("出版社(カタカナ)", self)
        description_label = QLabel("あらすじ", self)

        self.standard_opf_text = QLineEdit(self)
        self.title_text = QLineEdit(self)
        self.title_text.textChanged[str].connect(self.onChanged)
        self.title_text.setText("hoge")
        self.title_yomi_text = QLineEdit(self)
        self.author1_text = QLineEdit(self)
        self.author1_yomi_text = QLineEdit(self)
        self.author2_text = QLineEdit(self)
        self.author2_yomi_text = QLineEdit(self)
        self.publisher_text = QLineEdit(self)
        self.publisher_yomi_text = QLineEdit(self)
        self.description_text = QTextEdit(self)

        self.button_pass = QPushButton("パスを選択...", self)
        self.button_pass.clicked.connect(self.ShowDialog)
        self.change_button = QPushButton("Standard.opfを編集する",self)
        self.change_button.clicked.connect(self.change)
        self.search_button = QPushButton("koboで検索...",self)
        self.search_button.clicked.connect(self.search_kobo)

        layout = QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(standard_opf,0,0)
        layout.addWidget(title_label,1,0)
        layout.addWidget(title_label2,2,0)
        layout.addWidget(author_label1,3,0)
        layout.addWidget(author_label1_2,4,0)
        layout.addWidget(author_label2,5,0)
        layout.addWidget(author_label2_2,6,0)
        layout.addWidget(publisher_label,7,0)
        layout.addWidget(publisher_label2,8,0)
        layout.addWidget(description_label,9,0)
        layout.addWidget(self.standard_opf_text,0,1,1,2)
        layout.addWidget(self.button_pass,0,3)
        layout.addWidget(self.title_text,1,1,1,3)
        layout.addWidget(self.title_yomi_text,2,1,1,3)
        layout.addWidget(self.author1_text,3,1,1,3)
        layout.addWidget(self.author1_yomi_text,4,1,1,3)
        layout.addWidget(self.author2_text,5,1,1,3)
        layout.addWidget(self.author2_yomi_text,6,1,1,3)
        layout.addWidget(self.publisher_text,7,1,1,3)
        layout.addWidget(self.publisher_yomi_text,8,1,1,3)
        layout.addWidget(self.description_text,9,1,1,3)
        layout.addWidget(self.search_button,10,0)
        layout.addWidget(self.change_button,10,1,1,3)
        self.setLayout(layout)

        self.show()

    @pyqtSlot()
    def ShowDialog(self):
        if self.standard_opf_text.text() != "":
            text = self.standard_opf_text.text()
        else:
            text = text_dir
        fname = QFileDialog.getOpenFileName(self, 'Open file',text,"opfファイル(*.opf)")
        path = fname[0]
        if path != "":
            f = open(path,'r',encoding="utf-8_sig")
            lines = f.readlines()
            lines_strip = [line.strip() for line in lines]

            ######################

            l_title = [line for line in lines_strip if 'dc:title' in line]
            if l_title != []:
                title = l_title[0]
                title = title.replace('<dc:title id="title">', '').replace('</dc:title>', '')
            else:
                title = ""

            ######################

            l_title_yomi = [line for line in lines_strip if '<meta refines="#title" property="file-as">' in line]
            if l_title_yomi != []:
                title_yomi = l_title_yomi[0]
                title_yomi = title_yomi.replace('<meta refines="#title" property="file-as">','').replace('</meta>','')
            else:
                title_yomi = ''

            ######################
            creator = []
            l_creator1 = [line for line in lines_strip if '<dc:creator id="creator01">' in line]
            if l_creator1 != []:
                creator_1 = l_creator1[0]
                creator_1 = creator_1.replace('<dc:creator id="creator01">','').replace('</dc:creator>','')
                creator.append(creator_1)
            l_creator2 = [line for line in lines_strip if '<dc:creator id="creator02">' in line]
            if l_creator2 != []:
                creator_2 = l_creator2[0]
                creator_2 = creator_2.replace('<dc:creator id="creator02">','').replace('</dc:creator>','')
                creator.append(creator_2)


            #####################

            l_creator_yomi = [line for line in lines_strip if '<meta refines="#creator01" property="file-as">' in line]
            if l_creator_yomi != []:
                creator_yomi1 = l_creator_yomi[0]
                creator_yomi1 = creator_yomi1.replace('<meta refines="#creator01" property="file-as">','').replace('</meta>','')
            else:
                creator_yomi1 = ""
            l_creator_yomi = [line for line in lines_strip if '<meta refines="#creator02" property="file-as">' in line]
            if l_creator_yomi != []:
                creator_yomi2 = l_creator_yomi[0]
                creator_yomi2 = creator_yomi2.replace('<meta refines="#creator02" property="file-as">','').replace('</meta>','')
            else:
                creator_yomi2 = ""
            
            #####################

            l_description = [line for line in lines_strip if 'dc:description' in line]
            if l_description != []:
                description = l_description[0]
                description = description.replace('<dc:description>', '').replace('</dc:description>', '')
            else:
                description = ""
            
            #####################

            l_publisher = [line for line in lines_strip if 'dc:publisher' in line]
            if l_publisher != []:
                publisher = l_publisher[0]
                publisher = publisher.replace('<dc:publisher id="publisher">', '').replace('</dc:publisher>', '')
            else:
                publisher = ""

            #####################

            l_publisher = [line for line in lines_strip if '<meta refines="#publisher" property="file-as">' in line]
            if l_publisher != []:
                publisher_yomi = l_publisher[0]
                publisher_yomi = publisher_yomi.replace('<meta refines="#publisher" property="file-as">', '').replace('</meta>', '')
            else:
                publisher = ""

            #####################

            self.title_text.setText(title)
            self.title_yomi_text.setText(title_yomi)
            if creator != []:
                self.author1_text.setText(creator[0])
                if len(creator) == 2:
                    self.author2_text.setText(creator[1])
            self.author1_yomi_text.setText(creator_yomi1)
            self.author2_yomi_text.setText(creator_yomi2)
            self.description_text.setText(description)
            self.standard_opf_text.setText(path)
            self.publisher_text.setText(publisher)
            self.publisher_yomi_text.setText(publisher_yomi)
    
    def change(self):
        path = self.standard_opf_text.text()
        title = self.title_text.text()
        title_yomi = self.title_yomi_text.text()
        author1 = self.author1_text.text()
        author1_yomi = self.author1_yomi_text.text()
        author2 = self.author2_text.text()
        author2_yomi = self.author2_yomi_text.text()
        publisher = self.publisher_text.text()
        publisher_yomi = self.publisher_yomi_text.text()
        description = self.description_text.toPlainText()
        change_standard_opf.change_standard_opf(path,title,title_yomi,author1,author1_yomi,author2,author2_yomi,publisher,publisher_yomi,description)
        QMessageBox.question(self, "Message", "Changed!!", QMessageBox.Ok, QMessageBox.Ok)
    def search_kobo(self):
        title = self.title_text.text()
        b = bytes (title, 'eucjp')
        c = str(b)
        c = c.lstrip('b').replace(r'\x','%').strip("\'")
        url = 'https://books.rakuten.co.jp/search/nm?sv=30&h=30&o=0&v=2&spv=2&s=1&e=&b=1&g=101&sitem=' + c + '&x=0&y=0'
        webbrowser.open(url)
    def onChanged(self):
        maindata.title = self.title_text.text()



def main():
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()








