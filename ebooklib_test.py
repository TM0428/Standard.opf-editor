import sys
import os
import ebooklib
from ebooklib import epub

book = epub.read_epub('./デート・ア・ライブ　アンコール.epub')

titles = book.get_metadata('DC', 'title')
creator = book.get_metadata('DC', 'creator')
publisher = book.get_metadata('DC', 'publisher')
language = book.get_metadata('DC', 'language')
metas = book.get_metadata('OPF', None)

epub.change_epub('./デート・ア・ライブ　アンコール.epub',book)

#print(creator) # 執筆者

#for i in creator:
#    id = i[1].get("id")
#    refine = book.get_refinedata(id,"file-as")
#    print(refine)

#print(titles) # タイトル
#print(creator) # 執筆者
#print(publisher) # 発行人
#print(book.container)
#print(language) # 言語
#print(book.metadata['http://www.idpf.org/2007/opf'])
#print(metas)
#print(book.metadata)

