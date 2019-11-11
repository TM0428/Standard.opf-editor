# Standard.opf-editor
standard.opfの編集を楽にするツール

実行
```command
python standard.opf_editor.py
```
exeにする場合
```command
pyinstaller standard.opf_editor.py --noconsole --onefile
```

### standard.opf_editor
現行のツールです。PyQt5,ebooklibを使用しています。タイトル、著者、出版社、あらすじが変更できます。

### Standard-opf.py
こちらは旧型の編集ツールのため、現在は更新していません。
opfファイルが表示できる状態(epubを解凍した状態)にしないと使用できないため、廃止となりました。
### change_standard-opf.py
上記スクリプトを廃止に伴い、同時に廃止されました。


## 使用ライブラリ
- PyQt5
- ebooklib
---
