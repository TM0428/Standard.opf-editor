
import zipfile
import subprocess
# import os
import posixpath as zip_path
from ebooklib.epub import (
    EpubBook, EpubReader, EpubNcx, EpubSMIL, EpubNav, EpubCoverHtml, EpubHtml, EpubCover, EpubImage, EpubItem,
    NAMESPACES, IMAGE_MEDIA_TYPES
)
from urllib.parse import unquote

def unzip(dirpass, filepass):
    with zipfile.ZipFile(filepass, 'r') as inputFile:
        inputFile.extractall(dirpass)

def pack_epub(foldername: str, filename: str) -> None:
    cmd = ["sh", "compile.sh", foldername, "../" + filename]
    subprocess.run(cmd, stdout=subprocess.DEVNULL)
    print("EPUB packing end.")
    return None

class ExtendedEpubBook(EpubBook):
    def __init__(self):
        super().__init__()
        self.FOLDER_NAME = "item"


class ExtendedEpubHtml(EpubHtml):
    def get_content(self, default=None):
        return self.content


class ExtendedEpubReader(EpubReader):

    def __init__(self, epub_file_name, options=None):
        super().__init__(epub_file_name, options)
        self.book = ExtendedEpubBook()
        print(self.book.FOLDER_NAME)

    def _load_manifest(self):
        for r in self.container.find('{%s}%s' % (NAMESPACES['OPF'], 'manifest')):
            if r is not None and r.tag != '{%s}item' % NAMESPACES['OPF']:
                continue

            media_type = r.get('media-type')
            _properties = r.get('properties', '')

            if _properties:
                properties = _properties.split(' ')
            else:
                properties = []

            # people use wrong content types
            if media_type == 'image/jpg':
                media_type = 'image/jpeg'

            if media_type == 'application/x-dtbncx+xml':
                ei = EpubNcx(uid=r.get('id'), file_name=unquote(r.get('href')))

                ei.content = self.read_file(zip_path.join(self.opf_dir, ei.file_name))
            elif media_type == 'application/smil+xml':
                ei = EpubSMIL(uid=r.get('id'), file_name=unquote(r.get('href')))

                ei.content = self.read_file(zip_path.join(self.opf_dir, ei.file_name))
            elif media_type == 'application/xhtml+xml':
                if 'nav' in properties:
                    ei = EpubNav(uid=r.get('id'), file_name=unquote(r.get('href')))

                    ei.content = self.read_file(zip_path.join(self.opf_dir, r.get('href')))
                elif 'cover' in properties:
                    ei = EpubCoverHtml()

                    ei.content = self.read_file(zip_path.join(self.opf_dir, unquote(r.get('href'))))
                else:
                    ei = ExtendedEpubHtml()

                    ei.id = r.get('id')
                    ei.file_name = unquote(r.get('href'))
                    ei.media_type = media_type
                    ei.media_overlay = r.get('media-overlay', None)
                    ei.media_duration = r.get('duration', None)
                    ei.content = self.read_file(zip_path.join(self.opf_dir, ei.get_name()))
                    ei.properties = properties
            elif media_type in IMAGE_MEDIA_TYPES:
                if 'cover-image' in properties:
                    ei = EpubCover(uid=r.get('id'), file_name=unquote(r.get('href')))

                    ei.media_type = media_type
                    ei.content = self.read_file(zip_path.join(self.opf_dir, ei.get_name()))
                else:
                    ei = EpubImage()

                    ei.id = r.get('id')
                    ei.file_name = unquote(r.get('href'))
                    ei.media_type = media_type
                    ei.content = self.read_file(zip_path.join(self.opf_dir, ei.get_name()))
            else:
                # different types
                ei = EpubItem()

                ei.id = r.get('id')
                ei.file_name = unquote(r.get('href'))
                ei.media_type = media_type

                ei.content = self.read_file(zip_path.join(self.opf_dir, ei.get_name()))

            self.book.add_item(ei)


def read_epub(name, options=None):
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