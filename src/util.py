import zipfile
import subprocess

# import os
import posixpath as zip_path
from ebooklib.epub import (
    EpubBook,
    EpubReader,
    EpubNcx,
    EpubSMIL,
    EpubCoverHtml,
    EpubHtml,
    EpubCover,
    EpubImage,
    EpubItem,
    EpubNav,
    EpubException,
    EpubWriter,
    NAMESPACES,
    IMAGE_MEDIA_TYPES,
)
from typing import Dict
from lxml import etree
from urllib.parse import unquote

import platform


def unzip(dirpass, filepass):
    with zipfile.ZipFile(filepass, "r") as inputFile:
        inputFile.extractall(dirpass)


def pack_epub(foldername: str, filename: str) -> None:
    print(filename)
    if platform.system() == "Windows":
        # Windowsの場合、バッチファイルを使用
        cmd = ["compile.bat", foldername, "../" + filename]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, shell=True)
    else:
        # それ以外（MacやLinux）の場合、シェルスクリプトを使用
        cmd = ["sh", "compile.sh", foldername, "../" + filename]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, shell=True)

    print("EPUB packing end.")


class ExtendedEpubBook(EpubBook):
    def __init__(self):
        super().__init__()
        self.FOLDER_NAME = "item"

    def reset_metadata(self, namespace, name):
        """Reset Metadata"""
        id_dict = self.get_metadata(namespace, name)
        print(id_dict)

        if namespace in NAMESPACES:
            namespace = NAMESPACES[namespace]

        if namespace not in self.metadata:
            self.metadata[namespace] = {}

        if name not in self.metadata[namespace]:
            self.metadata[namespace][name] = []

        self.metadata[namespace][name] = []


class ExtendedEpubHtml(EpubHtml):
    def get_content(self, default=None):
        return self.content


class ExtendedEpubNav(ExtendedEpubHtml):
    def __str__(self):
        return "<EpubNav:%s:%s>" % (self.id, self.file_name)


class ExtendedEpubWriter(EpubWriter):
    def _write_opf_spine(self, root, ncx_id):
        spine_attributes = {"toc": ncx_id or "ncx"}
        if self.book.direction and self.options["spine_direction"]:
            spine_attributes["page-progression-direction"] = self.book.direction

        spine = etree.SubElement(root, "spine", spine_attributes)

        for _item in self.book.spine:
            # this is for now
            # later we should be able to fetch things from tuple

            is_linear = True
            opts: Dict[str, str]
            if isinstance(_item, tuple):
                item = _item[0]

                if len(_item) > 1:
                    if _item[1] == "no":
                        is_linear = False
            elif isinstance(_item, dict):
                opts = _item
            else:
                item = _item
                if isinstance(item, EpubHtml):
                    opts = {"idref": item.get_id()}

                    if not item.is_linear or not is_linear:
                        opts["linear"] = "no"
                elif isinstance(item, EpubItem):
                    opts = {"idref": item.get_id()}

                    if not item.is_linear or not is_linear:
                        opts["linear"] = "no"
                else:
                    opts = {"idref": item}

            try:
                itm = self.book.get_item_with_id(item)

                if not itm.is_linear or not is_linear:
                    opts["linear"] = "no"
                elif is_linear:
                    opts["linear"] = "yes"
            except BaseException:
                pass
            print(opts)

            etree.SubElement(spine, "itemref", opts)


class ExtendedEpubReader(EpubReader):
    def __init__(self, epub_file_name, options=None):
        super().__init__(epub_file_name, options)
        self.book = ExtendedEpubBook()

    def _load_manifest(self):
        for r in self.container.find("{%s}%s" % (NAMESPACES["OPF"], "manifest")):
            if r is not None and r.tag != "{%s}item" % NAMESPACES["OPF"]:
                continue

            media_type = r.get("media-type")
            _properties = r.get("properties", "")

            if _properties:
                properties = _properties.split(" ")
            else:
                properties = []

            # people use wrong content types
            if media_type == "image/jpg":
                media_type = "image/jpeg"

            if media_type == "application/x-dtbncx+xml":
                ei = EpubNcx(uid=r.get("id"), file_name=unquote(r.get("href")))

                ei.content = self.read_file(zip_path.join(self.opf_dir, ei.file_name))
            elif media_type == "application/smil+xml":
                ei = EpubSMIL(uid=r.get("id"), file_name=unquote(r.get("href")))

                ei.content = self.read_file(zip_path.join(self.opf_dir, ei.file_name))
            elif media_type == "application/xhtml+xml":
                if "nav" in properties:
                    ei = ExtendedEpubNav(
                        uid=r.get("id"), file_name=unquote(r.get("href"))
                    )

                    ei.content = self.read_file(
                        zip_path.join(self.opf_dir, r.get("href"))
                    )
                elif "cover" in properties:
                    ei = EpubCoverHtml()

                    ei.content = self.read_file(
                        zip_path.join(self.opf_dir, unquote(r.get("href")))
                    )
                else:
                    ei = ExtendedEpubHtml()

                    ei.id = r.get("id")
                    ei.file_name = unquote(r.get("href"))
                    ei.media_type = media_type
                    ei.media_overlay = r.get("media-overlay", None)
                    ei.media_duration = r.get("duration", None)
                    ei.content = self.read_file(
                        zip_path.join(self.opf_dir, ei.get_name())
                    )
                    ei.properties = properties
            elif media_type in IMAGE_MEDIA_TYPES:
                if "cover-image" in properties:
                    ei = EpubCover(uid=r.get("id"), file_name=unquote(r.get("href")))

                    ei.media_type = media_type
                    ei.content = self.read_file(
                        zip_path.join(self.opf_dir, ei.get_name())
                    )
                else:
                    ei = EpubImage()

                    ei.id = r.get("id")
                    ei.file_name = unquote(r.get("href"))
                    ei.media_type = media_type
                    ei.content = self.read_file(
                        zip_path.join(self.opf_dir, ei.get_name())
                    )
            else:
                # different types
                ei = EpubItem()

                ei.id = r.get("id")
                ei.file_name = unquote(r.get("href"))
                ei.media_type = media_type

                ei.content = self.read_file(zip_path.join(self.opf_dir, ei.get_name()))

            self.book.add_item(ei)

    def _load_container(self):
        super()._load_container()
        # print(zip_path.basename(self.opf_file))
        # TODO
        # いずれは、content.opf固定ではないファイル命名にする

    def _load_spine(self):
        spine = self.container.find("{%s}%s" % (NAMESPACES["OPF"], "spine"))

        # spineは、Dict型で保存を行う
        # self.book.spine = [(t.get('idref'), t.get('linear', 'yes'), t.get('properties', None)) for t in spine]
        self.book.spine = [dict(t.attrib) for t in spine]

        toc = spine.get("toc", "")
        self.book.set_direction(spine.get("page-progression-direction", None))

        # should read ncx or nav file
        nav_item = next(
            (item for item in self.book.items if isinstance(item, EpubNav)), None
        )
        if toc:
            if not self.options.get("ignore_ncx") or not nav_item:
                try:
                    ncxFile = self.read_file(
                        zip_path.join(
                            self.opf_dir, self.book.get_item_with_id(toc).get_name()
                        )
                    )
                except KeyError:
                    raise EpubException(-1, "Can not find ncx file.")

                self._parse_ncx(ncxFile)


def write_epub(name, book, options=None):
    """
    Creates epub file with the content defined in EpubBook.

    >>> ebooklib.write_epub('book.epub', book)

    :Args:
      - name: file name for the output file
      - book: instance of EpubBook
      - options: extra opions as dictionary (optional)
    """
    epub = ExtendedEpubWriter(name, book, options)

    epub.process()

    try:
        epub.write()
    except IOError:
        pass


def read_epub(name: str, options=None) -> ExtendedEpubBook:
    """
    Creates new instance of EpubBook with the content defined in the input file.

    >>> book = ebooklib.read_epub('book.epub')

    :Args:
      - name: full path to the input file
      - options: extra options as dictionary (optional)

    :Returns:
      Instance of EpubBook.
    """
    reader = ExtendedEpubReader(name, options)

    book = reader.load()
    reader.process()

    return book
