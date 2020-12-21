import compileall
import os

os.chdir("..")
from program_files import program_files
pf = program_files()

os.chdir("_bin")
compileall.compile_dir(os.getcwd())
os.chdir("__pycache__")

path = os.getcwd()
for file in os.listdir(path):
    print(file)
    if file.endswith('.pyc'):
        print(file)
        newName = file.split(".")[0] +'.' + file.split(".")[-1]
        os.rename(os.path.join(path, file),os.path.join(path, newName))
        pf.move(os.path.join(path, newName),os.path.join(pf.uploads, newName))