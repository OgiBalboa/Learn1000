#---------------------------------
# Module Name : Learn Words
# author : @ogibalboa
# "All rights reserved"
# last edit : 28.02.2020
#--------------------------------

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from database import database
from word_funcs import *
from user import *
class learn:
    def __init__(self,db,udb,wordgroup = "auto"):
#-------------------------------------------------------------------------------
        self.db = db
        self.udb = udb
        self.settings = udb.fetchall(table="settings")[0]
        if wordgroup != "auto":
            self.table = wordgroup
            self.wordgroup  = wordgroup
        self.wordlist,self.trlist,self.tablist,self.rowidlist,self.reglist = auto_generate(udb_=self.udb,db_=self.db,learnlimit = self.settings[1],param="learn")
        self.rowid = 1
#-------------------------------------------------------------------------------
    def next_(self,):   
        self.word = self.wordlist[self.rowid]
        self.translate = self.trlist[self.rowid]
        self.table = self.tablist[self.rowid]
        self.search = check_word(db_ = self.udb,table = self.table,rowid = self.rowidlist[self.rowid])
        if self.search == None:
            self.udb.insert(self.table,rowid = self.rowidlist[self.rowid],word = self.word)
        self.rowid += 1
        self.word = Capital(self.word)
        self.translate = Capital(self.translate)
        return self.word,self.translate,self.table