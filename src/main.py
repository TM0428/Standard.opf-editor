import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QMessageBox, QFileDialog, QDialog, QVBoxLayout, QWidget, QScrollArea, QToolButton, QMenu, QHBoxLayout, QLayout, QPushButton)
from PyQt6.QtGui import QAction, QIcon
from contents import MetadataContents
from typing import Final, Any, Dict, List, Optional
from contents import (EpubFile, set_content, TextNotFoundException)
import qdarktheme
from util import read_epub, write_epub, ExtendedEpubBook

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
        unepubbutton.triggered.connect(self.epub_to_folder)
        # Epubの作成
        dirbutton = QAction(QIcon("hoge.png"), "Epubの作成", self)
        dirbutton.setShortcut("Ctrl+E")
        dirbutton.triggered.connect(self.folder_to_epub)
        # 終了ボタン
        exitButton = QAction(QIcon("public/icon/exit-24-32.png"), "Exit", self)
        exitButton.setShortcut("Ctrl+Q")
        exitButton.setStatusTip("Exit application")
        exitButton.triggered.connect(QApplication.instance().quit)
        versionbutton = QAction("バージョン", self)
        versionbutton.triggered.connect(self.versiontab)
        fileMenu.addAction(dirbutton)
        fileMenu.addAction(unepubbutton)
        fileMenu.addAction(exitButton)
        helpMenu.addAction(versionbutton)

    def epub_to_folder(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', self.app_dir, "Epubファイル(*.epub)", options=QFileDialog.Option.DontUseNativeDialog)
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
        from contents import EpubFileDialog
        fname = QFileDialog.getExistingDirectory(self, 'Open file', self.app_dir, options=QFileDialog.Option.DontUseNativeDialog)
        if fname == "":
            return
        pathname = os.path.basename(fname)
        dialog = EpubFileDialog(self)
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
        dialog = QMessageBox(parent=self)
        dialog.setWindowTitle("version")
        dialog.setText("0.1.0 beta")
        dialog.setIcon(QMessageBox.Icon.Information)
        dialog.exec()   # Stores the return value for the button pressed


# UIを作成しているウィンドウ
class bodyUI(QWidget):

    parent: Any

    metadata_contents: List[MetadataContents] = []
    book: ExtendedEpubBook
    path: str = "book.epub"

    def __init__(self, parent: QMainWindow):
        super(bodyUI, self).__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):

        # self.change_button = QPushButton("Standard.opfを編集する", self)
        # self.change_button.clicked.connect(self.change)
        # self.search_button = QPushButton("koboで検索...", self)
        # self.search_button.clicked.connect(self.search_kobo)


        # 以下、レイアウトの作成
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        epub_file_w = QWidget()
        # from contents import EpubFile
        self.epub_file = EpubFile()
        self.epub_file.setup_ui(epub_file_w)
        layout.addWidget(epub_file_w)
        self.epub_file.set_epub_selected_method(self.set_data)


        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        tmp = QWidget()
        self.scroll_layout = QVBoxLayout()
        scroll_area.setWidget(tmp)
        tmp.setLayout(self.scroll_layout)

        layout.addWidget(scroll_area)

        add_content_button = QToolButton()
        add_content_button.setIcon(QIcon("public/icon/add-77-32.png"))
        add_content_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        add_content_menu = QMenu()
        add_content_button.setMenu(add_content_menu)

        # アクションを追加する
        action1 = QAction("Title", add_content_button)
        action1.triggered.connect(lambda: self.make_content(action1.text()))
        action2 = QAction("Author", add_content_button)
        action2.triggered.connect(lambda: self.make_content(action2.text()))
        action3 = QAction("Publisher", add_content_button)
        action3.triggered.connect(lambda: self.make_content(action3.text()))
        action4 = QAction("Synopsis", add_content_button)
        action4.triggered.connect(lambda: self.make_content(action4.text()))
        action5 = QAction("Series", add_content_button)
        action5.triggered.connect(lambda: self.make_content(action5.text()))

        for action in [action1, action2, action3, action4, action5]:
            add_content_menu.addAction(action)

        footer_layout: QLayout = QHBoxLayout()
        footer_layout.setContentsMargins(10, 0, 10, 10)
        footer_layout.addWidget(add_content_button)
        footer_layout.addStretch(2)
        exec_button: QPushButton = QPushButton("変更")
        exec_button.clicked.connect(self.exec_epub)
        footer_layout.addWidget(exec_button, 1)

        layout.addLayout(footer_layout)
        # layout.addStretch()
        self.setLayout(layout)
        self.show()

    def make_content(self, action_name: str):
        print(action_name)
        content: MetadataContents = set_content(action_name)
        new_layout = QWidget()
        content.setup_ui(new_layout)
        self.metadata_contents.append(content)
        self.scroll_layout.addWidget(new_layout)

    def set_data(self, path: str):
        # print(path)
        self.path = path
        self.book = read_epub(path)
        # DCタグの探索
        metadata: Dict[Any, Any] = self.book.metadata
        dc: Any = metadata.get("http://purl.org/dc/elements/1.1/")
        # opf: Any = metadata.get('http://www.idpf.org/2007/opf')
        print(self.book.metadata)
        for k, v in dc.items():
            for data in v:
                text = data[0]
                id = data[1].get("id")
                content = set_content(k)
                content.set_default_text(text)
                if id:
                    content.id_name = id
                self.metadata_contents.append(content)
                self.book.reset_metadata("DC", k)

            # print(k, v)

        add_contents = self.book.get_metadata("OPF", None)
        self.book.reset_metadata("OPF", None)
        for add_content in add_contents:
            text = add_content[0]
            prop: Dict[str, str] = add_content[1]
            ref: Optional[str] = prop.get("refines")
            if ref:
                is_append: bool = False
                for content in self.metadata_contents:
                    if content.id_name == ref[1:]:
                        content.set_append_text(text, prop.get("property"))
                        is_append = True
                if not is_append:
                    self.book.add_metadata("OPF", None, add_content[0], add_content[1])
            else:
                self.book.add_metadata("OPF", None, add_content[0], add_content[1])



        for content in self.metadata_contents:
            qw = QWidget()
            content.setup_ui(qw)
            self.scroll_layout.addWidget(qw)

    def exec_epub(self):
        from contents import EpubFileDialog
        if not self.book:
            return
        # self.book.reset_metadata("DC", "title")
        # self.book.add_metadata("DC", "title", "akame ga kiru", {"id": "title"})
        try:
            for content in self.metadata_contents:
                if content.disabled:
                    continue
                content.reset_metadata(self.book)
        except TextNotFoundException as e:
            QMessageBox.warning(self, "エラー", str(e))
            return
        for content in self.metadata_contents:
            if content.disabled:
                continue
            content.set_metadata(self.book)

        pathname = os.path.splitext(os.path.basename(self.path))[0]
        dialog = EpubFileDialog(self)
        dialog.line_edit.setText(pathname)
        result = dialog.exec()
        if result == QDialog.DialogCode.Rejected:
            return
        elif result == QDialog.DialogCode.Accepted:
            t = dialog.getText()
        else:
            t = os.path.basename(self.path)
        print(self.book.metadata)
        write_epub(name="../" + t + ".epub", book=self.book)
        QMessageBox.information(self, "Message", "Epubを作成しました")
        print("End")



def main():
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    mainwindow = MainWindow()
    mainwindow.show()
    app.exec()


if __name__ == "__main__":
    main()