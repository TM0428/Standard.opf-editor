import os
from PyQt6.QtWidgets import (QWidget, QGroupBox, QLabel, QVBoxLayout, QPushButton, QFileDialog, QHBoxLayout, QTextEdit, QDialog, QLineEdit)
from typing import Any, Optional
from util import ExtendedEpubBook

class QGrowingTextEdit(QTextEdit):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.document().contentsChanged.connect(self.sizeChange)
        self.document().documentLayout().documentSizeChanged.connect(self.sizeChange)

        self.heightMin = 0
        self.heightMax = 65000

    def sizeChange(self):
        docHeight: int = int(self.document().size().height())
        if self.heightMin <= docHeight <= self.heightMax:
            self.setMinimumHeight(docHeight + 10)

    def setText(self, text):
        super().setText(text)


class EpubFileDialog(QDialog):
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

class TextNotFoundException(Exception):
    pass

class MetadataContents:
    win: QWidget
    id_name: str
    main_layout: QVBoxLayout
    main_box_layout: QGroupBox
    disabled: bool = False

    def __init__(self):
        self.id_name = ""
        self.disabled = False
        return

    def add_footer(self):

        id_label = QLabel("id", None)
        self.id_text = QLineEdit()
        self.id_text.setText(self.id_name)
        self.delete_button = QPushButton("削除")
        self.delete_button.clicked.connect(self.remove)

        # layouts

        layout = QHBoxLayout()
        layout.addWidget(id_label, 1)
        layout.addWidget(self.id_text, 1)
        layout.addStretch(1)
        layout.addWidget(self.delete_button, 1)
        self.main_layout.addLayout(layout)


    def remove(self):
        self.disabled = True
        self.win.deleteLater()

    def setup_ui(self, win: QWidget) -> None:
        self.win = win
        self.main_box_layout = QGroupBox("Template")
        self.main_layout = QVBoxLayout()
        self.main_box_layout.setLayout(self.main_layout)

    def set_default_text(self, text: str) -> None:
        return

    def set_append_text(self, text: str, prop: str | None) -> None:
        return

    def set_metadata(self, book: ExtendedEpubBook) -> None:
        return

    def check_validation(self):
        self.id_name = self.id_text.text()
        return

    def reset_metadata(self, book: ExtendedEpubBook) -> None:
        self.check_validation()
        return


class EpubFile(MetadataContents):
    win: QWidget
    epub_sel: Any = None

    def setup_ui(self, win: QWidget) -> None:
        super().setup_ui(win=win)
        self.main_box_layout.setTitle("Epub Files")

        epub_file_label = QLabel("Epubファイル")
        self.epub_path_text = QLineEdit()
        self.epub_path_text.setPlaceholderText("path/to/your/epub")
        self.button_pass = QPushButton("パスを選択...", win)
        self.button_pass.clicked.connect(lambda: self.ShowDialog())

        layout = QHBoxLayout()
        layout.addWidget(epub_file_label, 1)
        layout.addWidget(self.epub_path_text, 2)
        layout.addWidget(self.button_pass, 1)

        self.main_layout.addLayout(layout)

        v_main_layout = QVBoxLayout(win)
        v_main_layout.setContentsMargins(10, 10, 10, 0)
        v_main_layout.addWidget(self.main_box_layout)

    def set_epub_selected_method(self, m):
        self.epub_sel = m

    def ShowDialog(self):
        if self.epub_path_text.text() != "":
            text = self.epub_path_text.text()
        else:
            text = os.getcwd()
        fname = QFileDialog.getOpenFileName(self.win, 'Open file', text, "epubファイル(*.epub)", options=QFileDialog.Option.DontUseNativeDialog)
        self.epub_path_text.setText(fname[0])
        if fname[0] != "" and self.epub_sel:
            self.epub_sel(fname[0])

    def set_default_text(self, text: str) -> None:
        self.epub_path_text.setText(text)



class Title(MetadataContents):
    id_name: str = "title"
    title_name: str = ""
    title_yomi_name: str = ""

    def __init__(self, title_name: str = "", title_yomi_name: str = "") -> None:
        self.title_name = title_name
        self.title_yomi_name = title_yomi_name
        pass

    def setup_ui(self, win: QWidget) -> None:
        # layout = QFormLayout()
        # layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        super().setup_ui(win=win)
        self.main_box_layout.setTitle("Title")
        title_label = QLabel("タイトル", None)
        title_yomi_label = QLabel("タイトル (カタカナ)", None)
        self.title_text = QLineEdit()
        self.title_text.setText(self.title_name)
        self.title_yomi_text = QLineEdit()
        self.title_yomi_text.setText(self.title_yomi_name)

        # layouts

        layout1 = QHBoxLayout()
        layout1.addWidget(title_label, 1)
        layout1.addWidget(self.title_text, 3)
        layout2 = QHBoxLayout()
        layout2.addWidget(title_yomi_label, 1)
        layout2.addWidget(self.title_yomi_text, 3)
        self.main_layout.addLayout(layout1)
        self.main_layout.addLayout(layout2)

        v_main_layout = QVBoxLayout(win)
        v_main_layout.setContentsMargins(10, 0, 10, 0)
        v_main_layout.addWidget(self.main_box_layout)
        self.add_footer()

    def set_default_text(self, text: str) -> None:
        self.title_name = text

    def set_append_text(self, text: str, prop: Optional[str]) -> None:
        if prop == "file-as":
            self.title_yomi_name = text

    def set_metadata(self, book: ExtendedEpubBook) -> None:
        book.add_metadata("DC", "title", self.title_text.text(), {'id': self.id_name})
        book.add_metadata(None, 'meta', self.title_yomi_text.text(), {'refines': '#' + self.id_name,
                                                                      'property': 'file-as',
                                                                      'scheme': 'marc:relators'})

    def check_validation(self):
        super().check_validation()
        if self.title_text.text() == "":
            raise TextNotFoundException("タイトルを入れてください。")
        if self.title_yomi_text.text() != "" and self.id_name == "":
            raise TextNotFoundException("タイトルのIDを入力してください。")


    def reset_metadata(self, book: ExtendedEpubBook) -> None:
        super().reset_metadata(book=book)
        book.reset_metadata("DC", "title")


class Author(MetadataContents):
    id_name: str = "creator"
    num: int = 1
    creator_name: str = ""
    creator_yomi_name: str = ""

    def __init__(self, creator_name: str = "", creator_yomi_name: str = "", num: int = 1) -> None:
        super().__init__()
        self.num = num
        self.creator_name = creator_name
        self.creator_yomi_name = creator_yomi_name


    def setup_ui(self, win: QWidget) -> None:
        super().setup_ui(win=win)
        self.main_box_layout.setTitle("Author")
        creator_label = QLabel("著者名" + str(self.num), None)
        creator_yomi_label = QLabel("著者名" + str(self.num) + "(カタカナ)", None)
        self.creator_text = QLineEdit()
        self.creator_text.setText(self.creator_name)
        self.creator_yomi_text = QLineEdit()
        self.creator_yomi_text.setText(self.creator_yomi_name)

        # layouts

        layout1 = QHBoxLayout()
        layout1.addWidget(creator_label, 1)
        layout1.addWidget(self.creator_text, 3)
        layout2 = QHBoxLayout()
        layout2.addWidget(creator_yomi_label, 1)
        layout2.addWidget(self.creator_yomi_text, 3)
        self.main_layout.addLayout(layout1)
        self.main_layout.addLayout(layout2)

        v_main_layout = QVBoxLayout(win)
        v_main_layout.setContentsMargins(10, 0, 10, 0)
        v_main_layout.addWidget(self.main_box_layout)
        self.add_footer()

    def set_default_text(self, text: str) -> None:
        self.creator_name = text

    def set_append_text(self, text: str, prop: str | None) -> None:
        if prop == "file-as":
            self.creator_yomi_name = text

    def check_validation(self):
        if self.creator_text.text() == "":
            raise TextNotFoundException("著者名を入れてください。")

    def reset_metadata(self, book: ExtendedEpubBook) -> None:
        super().reset_metadata(book=book)
        book.reset_metadata("DC", "creator")

class Publisher(MetadataContents):
    id_name: str = "publisher"
    publisher_name: str = ""
    publisher_yomi_name: str = ""

    def __init__(self, publisher_name: str = "", publisher_yomi_name: str = "") -> None:
        super().__init__()
        self.publisher_name = publisher_name
        self.publisher_yomi_name = publisher_yomi_name
        pass

    def setup_ui(self, win: QWidget) -> None:
        super().setup_ui(win=win)
        self.main_box_layout.setTitle("Publisher")
        publisher_label = QLabel("出版社", None)
        publisher_yomi_label = QLabel("出版社 (カタカナ)", None)
        self.publisher_text = QLineEdit()
        self.publisher_text.setText(self.publisher_name)
        self.publisher_yomi_text = QLineEdit()
        self.publisher_yomi_text.setText(self.publisher_yomi_name)

        # layouts

        layout1 = QHBoxLayout()
        layout1.addWidget(publisher_label, 1)
        layout1.addWidget(self.publisher_text, 3)
        layout2 = QHBoxLayout()
        layout2.addWidget(publisher_yomi_label, 1)
        layout2.addWidget(self.publisher_yomi_text, 3)
        self.main_layout.addLayout(layout1)
        self.main_layout.addLayout(layout2)

        v_main_layout = QVBoxLayout(win)
        v_main_layout.setContentsMargins(10, 0, 10, 0)
        v_main_layout.addWidget(self.main_box_layout)
        self.add_footer()

    def set_default_text(self, text: str) -> None:
        self.publisher_name = text

    def set_append_text(self, text: str, prop: str | None) -> None:
        if prop == "file-as":
            self.publisher_yomi_name = text

    def check_validation(self):
        if self.publisher_text.text() == "":
            raise TextNotFoundException("出版社を入れてください。")

    def reset_metadata(self, book: ExtendedEpubBook) -> None:
        super().reset_metadata(book=book)
        book.reset_metadata("DC", "publisher")

class Synopsis(MetadataContents):
    synopsis_name: str = ""

    def __init__(self, synopsis_name: str = "") -> None:
        super().__init__()
        self.synopsis_name = synopsis_name
        pass

    def setup_ui(self, win: QWidget) -> None:
        super().setup_ui(win=win)
        self.main_box_layout.setTitle("Synopsis")
        synopsis_label = QLabel("あらすじ", None)
        self.synopsis_text = QGrowingTextEdit()
        self.synopsis_text.textChanged.connect(lambda: self.synopsis_text.sizeChange())
        self.synopsis_text.setText(self.synopsis_name)

        # layouts
        layout = QHBoxLayout()
        layout.addWidget(synopsis_label, 1)
        layout.addWidget(self.synopsis_text, 3)
        self.main_layout.addLayout(layout)

        v_main_layout = QVBoxLayout(win)
        v_main_layout.setContentsMargins(10, 0, 10, 0)
        v_main_layout.addWidget(self.main_box_layout)
        self.add_footer()

    def set_default_text(self, text: str) -> None:
        self.synopsis_name = text

    def reset_metadata(self, book: ExtendedEpubBook) -> None:
        book.reset_metadata("DC", "description")

class Identifier(MetadataContents):
    identifier_name: str

    def __init__(self, identifier_name: str = "") -> None:
        super().__init__()
        self.identifier_name = identifier_name
        pass

    def setup_ui(self, win: QWidget) -> None:
        super().setup_ui(win=win)
        self.main_box_layout.setTitle("Identifier")
        identifier_label = QLabel("Unique ID", None)
        self.identifier_text = QLineEdit()
        self.identifier_text.setText(self.identifier_name)
        self.identifier_text.setDisabled(True)

        # layouts
        layout = QHBoxLayout()
        layout.addWidget(identifier_label, 1)
        layout.addWidget(self.identifier_text, 3)
        self.main_layout.addLayout(layout)

        v_main_layout = QVBoxLayout(win)
        v_main_layout.setContentsMargins(10, 0, 10, 0)
        v_main_layout.addWidget(self.main_box_layout)

    def set_default_text(self, text: str) -> None:
        self.identifier_name = text

    def reset_metadata(self, book: ExtendedEpubBook) -> None:
        book.reset_metadata("DC", "identifier")

class Language(MetadataContents):
    language_name: str

    def __init__(self, language_name: str = "") -> None:
        super().__init__()
        self.language_name = language_name
        pass

    def setup_ui(self, win: QWidget) -> None:
        # layout = QFormLayout()
        # layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        layout = QHBoxLayout()
        glayout = QGroupBox("Language")
        glayout.setLayout(layout)
        language_label = QLabel("language", None)
        self.language_text = QLineEdit()
        self.language_text.setText(self.language_name)

        # layouts

        layout.addWidget(language_label, 1)
        layout.addWidget(self.language_text, 3)

        v_main_layout = QVBoxLayout(win)
        v_main_layout.setContentsMargins(10, 0, 10, 0)
        v_main_layout.addWidget(glayout)

    def set_default_text(self, text: str) -> None:
        self.language_name = text

    def reset_metadata(self, book: ExtendedEpubBook) -> None:
        book.reset_metadata("DC", "language")

def set_content(name: str) -> MetadataContents:
    content = MetadataContents()
    if name == "Title" or name == "title":
        content = Title()
    elif name == "Author" or name == "creator":
        content = Author()
    elif name == "Publisher" or name == "publisher":
        content = Publisher()
    elif name == "Synopsis" or name == "description":
        content = Synopsis()
    elif name == "Identifier" or name == "identifier":
        content = Identifier()
    elif name == "Language" or name == "language":
        content = Language()
    else:
        # ERROR DEFAULT
        content = Title()

    return content


class metadata():
    author: str