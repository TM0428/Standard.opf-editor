# Standard.opf-editor
standard.opfの編集を楽にするツール

実行
```command
python standard-opf.py
```
exeにする場合
```command
pyinstaller standard-opf.py --noconsole --onefile
```

## 使用ライブラリ
- PyQt5

---

現在、standard.opf_editor.pyにて、epubファイルを解凍しなくても編集できるように変更を加えています。それに対応するため、新たにebooklibを導入しています。
