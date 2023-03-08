import os
class program_files:
    def __init__(self):
        self.main = os.getcwd()
        os.chdir("src")
        self.bin = os.getcwd()
        self.version = self.bin+"/version.txt"
        os.chdir("pics")
        self.pics = os.getcwd()
        os.chdir("..")
        os.chdir("dictionary")
        self.dictionary = os.getcwd()
        os.chdir("..")
        os.chdir("dev")
        try:
            os.chdir("downloads") # NO SUCH FILE
        except:
            os.mkdir("downloads")
            os.chdir("downloads")
        self.downloads = os.getcwd()
        os.chdir("..")
        try:
            os.chdir("uploads")
        except :
            os.mkdir("uploads")
            os.chdir("uploads")
        self.uploads = os.getcwd()
        os.chdir("..")
        try:
            self.version_dev = os.getcwd() +  "/version.txt"
        except:
            with open(vesion.txt,"w") as a:
                self.version_dev = os.getcwd() +  "/version.txt"
        os.chdir("..")
        try:
            os.chdir("sounds")
        except :
            os.mkdir("sounds")
            os.chdir("sounds")
        self.sounds = os.getcwd()
        os.chdir(self.main)
    def go_to(self,path):
        os.chdir(path)
    def delete(self,file):
        os.remove(file)
    def listdir(self,path):
        os.chdir(path)
        return os.listdir()
    def move (self,file,dir):
        os.replace(file,dir)
    def clear_dir (self,path):
        files = self.listdir(path)
        for i in files:
            delt = path+"/"+i
            try:
                self.delete(delt)
            except :
                pass
