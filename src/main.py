import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QDialog, QLabel, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QWidget, QGridLayout, QTextEdit
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import QObject
from typing import Final, Optional
import qdarktheme

class MainWindow(QMainWindow):
    title: Final[str] = "Epub Metadata Editor"
    creator: Final[str] = "TM"
    app_dir: str

    def __init__(self):
        super().__init__()
        self.app_dir = os.getcwd()
        self.initUI()
        ui = bodyUI(self)
        self.setCentralWidget(ui)

    def initUI(self):
        # 設定
        self.setWindowTitle(self.title)  # ウィンドウのタイトル
        self.setGeometry(100, 100, 600, 600)  # ウィンドウの位置と大きさ
        self.statusBar().showMessage("Made by " + self.creator)
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        helpMenu = mainMenu.addMenu("Help")
        # EPUBの解凍
        unepubbutton = QAction(QIcon("hoge.png"), "Epubの解凍", self)
        unepubbutton.setShortcut("Ctrl+R")
        unepubbutton.triggered.connect(self.epub_to_zip)
        # Epubの作成
        dirbutton = QAction(QIcon("hoge.png"), "Epubの作成", self)
        dirbutton.setShortcut("Ctrl+E")
        dirbutton.triggered.connect(self.folder_to_epub)
        # 終了ボタン
        exitButton = QAction(QIcon("public/icon/exit-24-32.png"), "Exit", self)
        exitButton.setShortcut("Ctrl+Q")
        exitButton.setStatusTip("Exit application")
        exitButton.triggered.connect(self.close)
        versionbutton = QAction("バージョン", self)
        versionbutton.triggered.connect(self.versiontab)
        fileMenu.addAction(dirbutton)
        fileMenu.addAction(unepubbutton)
        fileMenu.addAction(exitButton)
        helpMenu.addAction(versionbutton)

    def epub_to_zip(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', self.app_dir, "Epubファイル(*.epub)")
        root, ext = os.path.splitext(fname[0])
        if fname[0] == "" or ext != ".epub":
            return
        dirname = os.path.dirname(fname[0])
        basename = os.path.basename(fname[0])
        bname, ext = os.path.splitext(basename)
        os.rename(fname[0], os.path.join(dirname, bname + ".zip"))
        from util import unzip
        unzip(dirname + "/" + bname, dirname + "/" + bname + ".zip")
        os.remove(dirname + "/" + bname + ".zip")
        QMessageBox.question(self, "Message", "Epubを解凍しました")

    def folder_to_epub(self):
        fname = QFileDialog.getExistingDirectory(self, 'Open file', self.app_dir)
        if fname == "":
            return
        pathname = os.path.basename(fname)
        dialog = CustomDialog(self)
        dialog.label.setText(".epub")
        dialog.line_edit.setText(pathname)
        result = dialog.exec()
        if result == QDialog.DialogCode.Rejected:
            return
        elif result == QDialog.DialogCode.Accepted:
            t = dialog.getText()
        else:
            t = os.path.basename(fname)
        from util import pack_epub
        pack_epub(fname, t + ".epub")
        QMessageBox.information(self, "Message", "Epubを作成しました")



    def versiontab(self):
        dialog = QMessageBox(parent=self, text="0.0.0 beta")
        dialog.setIcon(QMessageBox.Icon.Information)
        dialog.setWindowTitle("versions")
        dialog.exec()   # Stores the return value for the button pressed


class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ファイル名")
        layout1 = QVBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QHBoxLayout()

        self.label = QLabel(".epub", self)
        self.line_edit = QLineEdit(self)
        self.cancel_button = QPushButton("Cancel", self)
        self.ok_button = QPushButton("OK", self)

        layout2.addWidget(self.line_edit)
        layout2.addWidget(self.label)

        layout3.addWidget(self.cancel_button)
        layout3.addWidget(self.ok_button)

        layout1.addLayout(layout2)
        layout1.addLayout(layout3)

        self.setLayout(layout1)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def getText(self):
        return self.line_edit.text()

# UIを作成しているウィンドウ
class bodyUI(QWidget):

    parent: QObject = None

    def __init__(self, parent=None):
        super(bodyUI, self).__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        standard_opf = QLabel("Epubファイル", self)
        title_label = QLabel("タイトル", self)
        title_label2 = QLabel("タイトル(カタカナ)", self)
        creator01_label = QLabel("著者名1", self)
        creator01_label_2 = QLabel("著者名1(カタカナ)", self)
        creator02_label = QLabel("著者名2", self)
        creator02_label_2 = QLabel("著者名2(カタカナ)", self)
        publisher_label = QLabel("出版社", self)
        publisher_label2 = QLabel("出版社(カタカナ)", self)
        description_label = QLabel("あらすじ", self)

        self.epub_path_text = QLineEdit(self)
        self.epub_path_text.setPlaceholderText("path/to/your/epub")
        self.title_text = QLineEdit(self)
        # self.title_text.textChanged[str].connect(self.onChanged)
        self.title_text.setPlaceholderText("鬼滅の刃")
        self.title_yomi_text = QLineEdit(self)
        self.creator01_text = QLineEdit(self)
        self.creator01_yomi_text = QLineEdit(self)
        self.creator02_text = QLineEdit(self)
        self.creator02_yomi_text = QLineEdit(self)
        self.publisher_text = QLineEdit(self)
        self.publisher_yomi_text = QLineEdit(self)
        self.description_text = QTextEdit(self)

        self.button_pass = QPushButton("パスを選択...", self)
        self.button_pass.clicked.connect(self.ShowDialog)
        self.change_button = QPushButton("Standard.opfを編集する", self)
        # self.change_button.clicked.connect(self.change)
        self.search_button = QPushButton("koboで検索...", self)
        # self.search_button.clicked.connect(self.search_kobo)

        layout = QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(standard_opf, 0, 0)
        layout.addWidget(title_label, 1, 0)
        layout.addWidget(title_label2, 2, 0)
        layout.addWidget(creator01_label, 3, 0)
        layout.addWidget(creator01_label_2, 4, 0)
        layout.addWidget(creator02_label, 5, 0)
        layout.addWidget(creator02_label_2, 6, 0)
        layout.addWidget(publisher_label, 7, 0)
        layout.addWidget(publisher_label2, 8, 0)
        layout.addWidget(description_label, 9, 0)
        layout.addWidget(self.epub_path_text, 0, 1, 1, 2)
        layout.addWidget(self.button_pass, 0, 3)
        layout.addWidget(self.title_text, 1, 1, 1, 3)
        layout.addWidget(self.title_yomi_text, 2, 1, 1, 3)
        layout.addWidget(self.creator01_text, 3, 1, 1, 3)
        layout.addWidget(self.creator01_yomi_text, 4, 1, 1, 3)
        layout.addWidget(self.creator02_text, 5, 1, 1, 3)
        layout.addWidget(self.creator02_yomi_text, 6, 1, 1, 3)
        layout.addWidget(self.publisher_text, 7, 1, 1, 3)
        layout.addWidget(self.publisher_yomi_text, 8, 1, 1, 3)
        layout.addWidget(self.description_text, 9, 1, 1, 3)
        layout.addWidget(self.search_button, 10, 0)
        layout.addWidget(self.change_button, 10, 1, 1, 3)
        self.setLayout(layout)

        self.show()

    # epubからメタデータを取得
    def ShowDialog(self):
        if self.epub_path_text.text() != "":
            text = self.epub_path_text.text()
        else:
            text = self.parent.app_dir
        fname = QFileDialog.getOpenFileName(self, 'Open file', text, "epubファイル(*.epub)")
        print(fname[0])



def main():
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    mainwindow = MainWindow()
    mainwindow.show()
    app.exec()


if __name__ == "__main__":
    main()