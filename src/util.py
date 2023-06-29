
import zipfile
import subprocess
# import os

def unzip(dirpass, filepass):
    with zipfile.ZipFile(filepass, 'r') as inputFile:
        inputFile.extractall(dirpass)

def pack_epub(foldername: str, filename: str) -> None:
    cmd = ["sh", "compile.sh", foldername, "../" + filename]
    subprocess.run(cmd, stdout=subprocess.DEVNULL)
    print("EPUB packing end.")
    return None