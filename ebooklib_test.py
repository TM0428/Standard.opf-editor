import sys
import os
import ebooklib
from ebooklib import epub

book = epub.read_epub('./デート・ア・ライブ　アンコール.epub')

title = book.get_metadata('DC', 'title')
creator = book.get_metadata('DC', 'creator')
publisher = book.get_metadata('DC', 'publisher')
language = book.get_metadata('DC', 'language')

print(title) # タイトル
print(creator) # 執筆者
print(publisher) # 発行人
print(language) # 言語