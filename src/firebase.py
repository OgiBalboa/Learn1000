import pyrebase
from program_files import program_files
import compileall


class firebase:
    def __init__(self):
        self.pf = program_files()
        self.status = "init"
        self.admin_info = ""
        self.version = 0
        self.config = {
            "apiKey": "AIzaSyA62aPRDgEi15LvacdO-qFQb22mY5_JAv4",
            "authDomain": "learn1000-1582992687676.firebaseapp.com",
            "databaseURL": "https://learn1000-1582992687676.firebaseio.com",
            "projectId": "learn1000-1582992687676",
            "storageBucket": "learn1000-1582992687676.appspot.com",
            "messagingSenderId": "345204312156",
            "appId": "1:345204312156:web:eaca0b5895f31a20f97e99",
            "measurementId": "G-5402KNKKZG",
        }
        self.firebase = pyrebase.initialize_app(self.config)
        self.storage = self.firebase.storage()

    def upload(self, file_path, receiver):
        self.storage.child(receiver).put(file_path)

    def download(self, file_path, downloads):
        self.storage.child(file_path).download(downloads)

    def version_control(self):
        try:
            with open(PROGRAM_FILES.version, "r") as old_vers:
                old_vers = int(old_vers.readlines()[0].split("=")[-1])
            self.pf.delete(self.pf.version)
        except Exception as e:
            print(e)
        self.storage.child("AppInfo/version.txt").download(
            self.pf.version)  # DOWNLOAD NEW VERSION FILE
        with open(PROGRAM_FILES.version, "r") as vers:
            self.version = int(
                vers.readlines()[0].split("=")[-1])  # FETCH VERSION DATA
            vers.seek(0)
            recipe = vers.readlines()[3].split(",")
            vers.seek(0)
            self.admin_info = vers.readlines()[4]
            vers.seek(0)
            self.action = str(vers.readlines()[2])
            if self.action == "terminate\n" or self.action == "terminate":
                self.status = "terminate"
                return

        if self.version - old_vers == 1:
            print("Auto update activated !")
            self.update(recipe)
            print("update completed.")
            self.status = "update"
        elif self.version - old_vers > 1:
            self.update("major")
            self.status = "major"
        else:
            self.status = "okay"

    def update(self, recipe=None):
        if recipe == "major":
            return
        for elm in recipe:
            if len(recipe) < 1:
                break
            if elm[-1] == "\n": elm = elm[:-1]
            fname = elm.split("/")[-1]
            print(elm)
            self.download("Update" + "/" + fname, PROGRAM_FILES.main + "/" + elm)
            compileall.compilefile(PROGRAM_FILES.main + "/" + elm)
        return "Completed"


PROGRAM_FILES = program_files()
