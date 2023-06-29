import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QInputDialog, QDialog, QLabel, QVBoxLayout, QLineEdit, QPushButton
from PyQt6.QtGui import QAction, QIcon
from typing import Final
import qdarktheme

class MainWindow(QMainWindow):
    title: Final[str] = "Epub Metadata Editor"
    creator: Final[str] = "TM"
    app_dir: str

    def __init__(self):
        super().__init__()
        self.app_dir = os.getcwd()
        self.initUI()

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
        text, ok = QInputDialog.getText(self, 'Epubのファイル名を指定...', 'Epubのファイル名を指定...', text=pathname)
        if ok:
            t = str(text)
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
        layout = QVBoxLayout()

        self.label = QLabel(".epub", self)
        self.line_edit = QLineEdit(self)
        self.button = QPushButton("OK", self)

        layout.addWidget(self.line_edit)
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.setLayout(layout)

        self.button.clicked.connect(self.accept)

def main():
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    mainwindow = MainWindow()
    mainwindow.show()
    app.exec()


if __name__ == "__main__":
    main()