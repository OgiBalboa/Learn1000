import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from database import database
from word_funcs import *
from user import *
from language_pack import language_pack

class quiz():
    def __init__(self, db, udb, wordgroup):
        # ----------------------------------------------------------------
        self.db = db
        self.udb = udb
        self.wordgroup = wordgroup
        self.flag = "new"
        self.res = None
        if self.wordgroup is "auto":
            self.wordlist, \
            self.trlist,\
            self.tablist, \
            self.rowidlist, \
            self.reglist = auto_generate(udb_=self.udb,db_=self.db,param="quiz")
        else:
            self.table = wordgroup
            self.wordlist, self.rowidlist, self.reglist = get_words(self.db, self.table)
            self.trlist = None

        self.new_word()
        # ----------------------------------------------------------------
        if self.word != "":
            self.query = language_pack().text("Aşağıdaki Kelimenin Türkçe Karşılığını Yazınız\n\n") +"'"+ self.word.title()+"'"
        else:
            self.query = ""
        self.ans = ""
        self.info = ""
        self.tru = 0
        self.fls = 0
        self.temp_false_word = []
    def pressed(self, ans):
        self.search = check_word(db_=self.udb, table=self.table, rowid=self.rowid)
        if self.search == None:
            self.udb.insert(self.table, rowid=self.rowid, word=self.word)
        self.ans = ans
        if ans == self.translation.title():
            self.true()
        else:
            self.false()

        self.info += language_pack().text("\nDoğru Sayısı : ") + str(self.tru) + \
                     language_pack().text("\nYanlış sayısı : ") + str(self.fls)

        self.query = "Database güncelleniyor"

        if len(self.reglist) > 1:
            self.new_word()
            if self.word != "":
                self.query =language_pack().text("Aşağıdaki Kelimenin Türkçe Karşılığını Yazınız\n\n")+"'"+ self.word.title() +"'"
            else:
                self.query = ""
        else:
            self.query = ""

    def true(self, ):
        self.res = True
        self.tru += 1
        self.info = language_pack().text("Bildin.")
        self.reglist.remove(self.reg)
        self.udb.update(self.table, rowid=self.rowid, inc_tcount=1, inc_fcount=0)
        self.temp_false_word = None

    def false(self, ):
        self.res = False
        self.info = language_pack().text("YANLIŞ !\nDoğru Cevap : ") + self.translation.title() + \
                    language_pack().text("\nSizin Cevabınız : ") + self.ans

        self.fls += 1
        self.udb.update(self.table, rowid=self.rowid, inc_tcount=0, inc_fcount=1)
        self.temp_false_word = [self.table, self.rowid]

    def count_status(self, ):
        self.info += language_pack().text("\nDoğru Sayısı : ") + str(self.tru) + \
                     language_pack().text("\nYanlış sayısı : ") + str(self.fls)

    def new_word(self):
        if self.wordgroup != "auto":
            self.word, self.translation, self.rowid, self.reg = random_word(wordlist=self.wordlist,
                                                                            rowidlist=self.rowidlist,
                                                                            reglist=self.reglist)
        else:
            self.word, self.translation, self.rowid, self.table, self.reg = random_word(wordlist=self.wordlist,
                                                                                        reglist=self.reglist,
                                                                                        rowidlist=self.rowidlist, \
                                                                                        trlist=self.trlist,
                                                                                        tablist=self.tablist)