#---------------------------------
# Module Name : Settings
# author : @ogibalboa
# last edit : 28.02.2020
#--------------------------------
import sys
from database import database
from program_files import program_files
#import urllib.request
udb = database("User-Database")
connection = False
"""
def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host) #Python 3.x
        return True
    except:
        return False
"""
def connect():
    return True
def default_settings():
    udb.cur.execute("INSERT INTO settings (username,learnlimit ,lang ,dict) VALUES (?,?,?,?);",
                    ("New", 10, "english", "none"))
    udb.db.commit()
def apply_settings(nm = None,lm = None, lang = None,dict = None):
    global udb
    oldsets = udb.fetchall(table="settings")
    name,learnlimit,language,dictionary = oldsets[0]
    if nm != None:
        name = nm
    if lm != None:
        learnlimit = lm
    if lang != None:
        language = lang
    if dict != None :
        dictionary = dict
    udb.cur.execute("UPDATE settings SET username =? ,learnlimit =? ,lang =?,dict =? WHERE rowid =?",
                    (name, learnlimit, language,dictionary, 1))
    udb.db.commit()

def refresh ():
    global user_name
    global dict_db
    global language
    global learnlimit
    global dictionary
    global user_db
    settings = udb.fetchall(table="settings")
    user_name = settings[0][0]
    learnlimit = settings[0][1]
    language = settings[0][2]
    dictionary = settings[0][3]
    dict_db = dictionary.capitalize() + "-" + language.capitalize()
    user_db = "User-Database"

class sizes:
    def __init__(self):
        self.picture = 9
        self.font = 2

class globals:
    def __init__(self):
        self.pause = False
def errorlog(error):
    return error
