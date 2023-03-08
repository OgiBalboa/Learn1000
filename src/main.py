# *-*coding: utf-8 *-*
# ---------------------------------
# Module Name : Main App
# author : @ogibalboa
# "All rights reserved."
# last edit : 28.02.2020
# --------------------------------
import sys

sys.path
sys.path.append("")
sys.platform = 'linux2'
import os
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.progressbar import ProgressBar
from src import circular_progress_bar
from kivy.uix.behaviors.focus import FocusBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.spinner import Spinner
from kivy.lang import Builder
import settings
from settings import errorlog
from .firebase import firebase
from settings import globals


def update():
    try:
        settings.refresh()
        settings.connection = settings.connect()
    except Exception as e:
        print(e)
        settings.default_settings()
        settings.refresh()
    try:
        if not settings.connection == False:
            FIREBASE.version_control()
            if FIREBASE.status == "update":
                print("An update have done")
            elif FIREBASE.status == "major":
                print("MAJOR UPDATE NEEDED")
        else:
            print("PLEASE CONNECT TO INTERNET TO CHECK FOR UPDATES")
    except Exception as e:
        print("Update failed, ERROR : ", errorlog(e))


update()
# -------------------IMPORT UPDATED MODULES-------------------------------
from database import database
from word_funcs import *
from threading import Thread
from quiz import Quiz
from src.learn import learn
import user
import src.sounds.pronounces as pronounces
import platform
from language_pack import language_pack

# Window.size = (720,1230)
"""
if platform.system() == "Linux":
    Window.size = (540,852)
"""
Config.set('kivy', 'exit_on_escape', '0')
Window.clearcolor = (0, 0, 0.1, 1)
wordgroup = "basic"
udb = database("User-Database")


class LoadScreen(Screen):
    user_name_ = ObjectProperty(None)
    learnlimit_ = ObjectProperty(None)
    dictionary_ = ObjectProperty(None)
    lgp = language_pack()
    sizes = settings.sizes()

    class DropDown(DropDown):
        pass

    def load_conf(self, name, dbname, ):
        settings.refresh()
        global db
        if dbname == "Almanca" or "German":
            dbname = "German"
        if name == "":
            return False
        settings.apply_settings(nm=name, )
        db = database(dbname.capitalize() + "-" + settings.language)
        return True

    def set_lang(self, lang):
        settings.apply_settings(lang=lang)
        for i in self.walk():
            try:
                i.text = language_pack().text(i.text)
            except:
                pass

    def set_dict(self, lang):
        settings.apply_settings(dict="German")

    def set_learnlimit(self, param):
        if param == "az":
            settings.apply_settings(lm=5)
        if param == "orta":
            settings.apply_settings(lm=10)
        if param == "cok":
            settings.apply_settings(lm=20)


class HelloScreen(Screen):
    def popup(self, *args):
        show = InfoBox()
        try:
            print("stat :", FIREBASE.status)
            if FIREBASE.status == "major":
                show.infolbl.text = "Uygulamanız eski sürümde , lütfen uygun olduğunuzda mağaza sayfasından güncelleme yapınız.\n Teşekkürler :)"
            elif FIREBASE.status == "update":
                show.infolbl.text = FIREBASE.admin_info
            elif FIREBASE.status == "terminate":
                show.infolbl.text = FIREBASE.admin_info
            else:
                return
            print("stat : ", FIREBASE.status)
            welcome = Popup(title=language_pack().text("Güncelleme !"),
                            content=show, size_hint=(None, None),
                            size=(400, 400))
            welcome.open()
        except Exception as e:
            print(e)

    def hello_(self):
        if FIREBASE.status == "terminate":
            return None
        if settings.dictionary == "none":
            return False
        else:
            global db
            settings.refresh()
            db = database(
                settings.dictionary.capitalize() + "-" + settings.language.capitalize())
            return True


class Draft(Screen):
    info = ObjectProperty(None)
    sizes = settings.sizes()

    def on_pre_enter(self, *args):
        try:
            self.info.text = FIREBASE.admin_info
            if len(FIREBASE.admin_info) < 2:
                self.info.text = "Uygulamanızın şu anki versiyonu çalışmak için uygun değildir. Lütfen mağaza" \
                                 "sayfasından uygulamayı güncelleyiniz. Anlayışınız için teşekkür ederiz."
        except:
            self.info.text = "Uygulamanızın şu anki versiyonu çalışmak için uygun değildir. Lütfen mağaza" \
                             "sayfasından uygulamayı güncelleyiniz. Anlayışınız için teşekkür ederiz."


class ProgressWindow(GridLayout):
        sizes = settings.sizes()
        lgp = language_pack()
        pbar_basic = ObjectProperty(None)
        pbar_common = ObjectProperty(None)
        pbar_rare = ObjectProperty(None)
        pbar_advantage = ObjectProperty(None)
        pbar_general = ObjectProperty(None)

        def upd(self):
            for i in udb.fetchall("progress"):
                self.pbar_basic.value, self.pbar_common.value, self.pbar_rare.value, self.pbar_advantage.value, self.pbar_general.value = int(
                    i[0]) * 10, int(i[1]) * 10, int(i[2]) * 10, int(
                    i[3]) * 10, int(i[4]) * 10,
                if self.pbar_basic.value == 0: self.pbar_basic.value = 5
                if self.pbar_common.value == 0: self.pbar_common.value = 5
                if self.pbar_rare.value == 0: self.pbar_rare.value = 5
                if self.pbar_advantage.value == 0: self.pbar_advantage.value = 5
                if self.pbar_general.value == 0: self.pbar_general.value = 5


class MainMenu(Screen):
    user_info = ObjectProperty(None)
    scr = ObjectProperty(None)
    sizes = settings.sizes()
    bgsize = Window.size
    pbar_primary = ObjectProperty(None)
    pbar = ObjectProperty(None)
    wd = os.getcwd()

    def on_pre_enter(self, *args):
        for i in self.walk():
            try:
                i.text = language_pack().text(i.text)
            except:
                pass
        self.scr.text = str(Window.size)

    def upd(self):
        settings.refresh()
        user.cal_progress(udb=udb)
        self.user_info.text = language_pack().text("Hoş Geldin len ") + str(
            settings.user_name) + " ! \n\n"
        self.user_info.text += language_pack().text("İlerleme Durumunuz \n")
        for i in udb.fetchall("progress"):
            self.pbar_basic, self.pbar_common, self.pbar_rare, self.pbar_advantage, self.pbar_general = int(
                i[0]) * 10, int(i[1]) * 10, int(i[2]) * 10, int(i[3]) * 10, int(
                i[4]) * 10,
            self.pbar_primary.value = max(self.pbar_basic, self.pbar_common,
                                          self.pbar_rare, self.pbar_advantage,
                                          self.pbar_general)
            if self.pbar_primary.value == self.pbar_basic: self.pbar.text = language_pack().text(
                "TEMEL KELİMELER")
            if self.pbar_primary.value == self.pbar_common: self.pbar.text = language_pack().text(
                "YAYGIN KULLANILAN")
            if self.pbar_primary.value == self.pbar_rare: self.pbar.text = language_pack().text(
                "NADİR KULLANILAN")
            if self.pbar_primary.value == self.pbar_advantage: self.pbar.text = language_pack().text(
                "İLERİ SEVİYE")


    def show_progress(self):
        global progresswindow
        show = ProgressWindow()
        show.upd()
        progresswindow = Popup(title=language_pack().text("İlerleme Durumunuz"),
                               content=show, size_hint=(None, None),
                               size=(400, 400))
        progresswindow.open()


class Learn(Screen):
    word = ObjectProperty(None)
    sentence = ObjectProperty(None)
    pronounce = ObjectProperty(None)
    translate = ObjectProperty(None)
    _word_ = ObjectProperty(None)
    _tr_ = ObjectProperty(None)
    sizes = settings.sizes()

    def on_pre_enter(self, *args):
        self._word_.text = language_pack().text("Başlamak için Next'e basınız")
        self.word.text = ""
        self._tr_.text = ""
        for i in self.walk():
            for i in self.walk():
                try:
                    i.text = language_pack().text(i.text)
                except:
                    pass

    def next_(self):
        self._word_.text = language_pack().text("Kelime : ")
        self._tr_.text = language_pack().text("Çevirisi : ")
        if self.word.text == "":
            global l
            l = learn(db=db,
                      udb=udb)  # Eğer kelime yoksa kelime havuzu oluştur.
        if l.rowid <= len(l.wordlist) - 1:  # kelimeler bitene kadar öğret
            self.word.text, self.translate.text, self.table = l.next_()
        else:
            self._word_.text = language_pack().text("KELİMELER BİTTİ")
            self.word.text = " "
            self.translate.text = ""
            self._tr_.text = language_pack().text(
                "Şimdi Quiz yap ve tekrar buraya gel")

    def click(self):
        pronounces.play()

    def reset(self):
        global l
        l = None
        self.word.text = ""
        self.translate.text = ""


class Quiz(Screen):
    query = ObjectProperty(None)
    answer = ObjectProperty(None)
    info = ObjectProperty(None)
    acpt = ObjectProperty(None)
    start = ObjectProperty(None)
    quizlayout = ObjectProperty(None)
    sizes = settings.sizes()

    def __init__(self, **kwargs):
        super(Quiz, self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)

    def res(self, value=None):
        self.answer.text = ""

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if self.answer.focus and keycode == 40:  # 40 - Enter key
            if self.answer.text == "":
                return
            if list(self.answer.text)[0] == "\n":
                self.answer.text = self.answer.text[1::]
            self.ok()
            Clock.schedule_once(self.res, 0.2)
            self.answer.text = ""
        if keycode == 27:
            print("vayaq")
            wmgr.current = "main"

    class QuizSelect(GridLayout):
        lgp = language_pack()
        sizes = settings.sizes()

        def auto(self):
            global wordgroup
            global popupWindow
            wordgroup = "auto"
            global q
            q = Quiz(db=db, udb=udb, wordgroup=wordgroup)
            popupWindow.dismiss()

        def basic(self):
            global wordgroup
            wordgroup = "basic"
            global q
            q = Quiz(db=db, udb=udb, wordgroup=wordgroup)
            popupWindow.dismiss()

        def common(self):
            global wordgroup
            wordgroup = "common"
            global q
            q = Quiz(db=db, udb=udb, wordgroup=wordgroup)
            popupWindow.dismiss()

        def rare(self):
            global wordgroup
            wordgroup = "rare"
            global q
            q = Quiz(db=db, udb=udb, wordgroup=wordgroup)
            popupWindow.dismiss()

        def advantage(self):
            global wordgroup
            wordgroup = "advantage"
            global q
            q = Quiz(db=db, udb=udb, wordgroup=wordgroup)
            popupWindow.dismiss()

    def quiz_difficulty(self):
        global popupWindow
        show = Quiz_Select()
        popupWindow = Popup(title=language_pack().text("Quiz zorluğu seçiniz"),
                            content=show)
        popupWindow.open()

    def on_pre_enter(self, value=None):
        self.info.text = "Hoş Geldiniz\nBaşlamak için 'Onayla' butonuna basınız"
        for i in self.walk():
            for i in self.walk():
                try:
                    i.text = language_pack().text(i.text)
                except:
                    pass

    def ok(self, value=None, ans=None):
        global q
        try:
            if q.flag == "new":
                self.query.text, self.info.text = q.query, q.info
        except:
            pass
        if self.answer.text == "" or self.answer.text == "\n":
            return
        if ans != None:
            q.pressed(Capital(ans))
        else:
            q.pressed(Capital(self.answer.text, settings.language))
        if q.res == False:
            self.acpt.opacity = 1
        self.query.text = q.query
        self.info.text = q.info
        # self.answer.text = ""
        q.ans = ""
        if q.flag == "Done":
            self.query.text = language_pack().text(
                " KELİMELER BİTTİ !\n Yeni kelimeler öğren ve tekrar buraya gel !")

    def reset(self):
        global q
        q = None
        self.info.text = language_pack().text(
            "Hoş Geldiniz\nBaşlamak için 'Onayla' butonuna basınız")
        self.query.text = ""

    def accept_as_true(self, ):
        self.acpt.opacity = 0
        global q
        if q.temp_false_word != None:
            q.fls -= 1
            q.tru += 1
            q.udb.update(table=q.temp_false_word[0], rowid=q.temp_false_word[1],
                         inc_tcount=1, inc_fcount=-1)
            q.info = language_pack().text("Doğru Kabul Edildi.\n")
            q.count_status()
            self.info.text = q.info
            q.temp_false_word = None
        else:
            return


class Settings_(Screen):
    global ConfirmReset
    lgp = language_pack()
    learnlimit_ = ObjectProperty(None)
    sizes = settings.sizes()
    lbl = ObjectProperty(None)

    class DropDown(DropDown):
        pass

    def on_pre_enter(self, value=None):
        for i in self.walk():
            try:
                i.text = language_pack().text(i.text)
            except Exception as e:
                print(e)
                pass
        self.lbl.text = "İnternet Bağlantısı : "
        if settings.connection == True:
            self.lbl.text += "Başarılı\n"
        else:
            self.lbl.text += "Başarısız\n"
        self.lbl.text += "Versiyon No : "
        try:
            self.lbl.text += str(FIREBASE.version) + "\nDurum : " + str(
                FIREBASE.status) + "\nAdmin İnfo : " + str(FIREBASE.admin_info)
        except Exception as e:
            print(e)

    class ConfirmReset(GridLayout):
        lgp = language_pack()

        def reset_db_ok(self):
            udb.reset()
            confirm_reset.dismiss()

        def reset_db_cancel(self):
            confirm_reset.dismiss()

    def set_lang(self, langg):
        settings.apply_settings(lang=langg)
        settings.refresh()

    def reset_db(self):
        show = ConfirmReset()
        confirmreset = Popup(
            title=language_pack().text("TÜM BİLGİLERİNİN SIFIRLANACAK !"),
            content=show)
        confirmreset.open()


class Knowns(Screen):
    sizes = settings.sizes()
    info = ObjectProperty(None)
    infotext = ObjectProperty(None)
    known_words = ObjectProperty(None)
    known_fcount = ObjectProperty(None)
    known_tcount = ObjectProperty(None)
    known_prg = ObjectProperty(None)
    known_pc = ObjectProperty(None)
    layout_content = ObjectProperty(None)

    def show(self, param=None):
        self.infotext.text = language_pack().text(self.infotext.text)
        if param == None:
            known_basic = udb.fetchall("basic")
            known_common = udb.fetchall("common")
            known_rare = udb.fetchall("rare")
            known_advantage = udb.fetchall("advantage")
            known_all = known_basic + known_common + known_rare + known_advantage
        elif param == "basic":
            known_all = udb.fetchall("basic")
        elif param == "common":
            known_all = udb.fetchall("common")
        elif param == "rare":
            known_all = udb.fetchall("rare")
        elif param == "advantage":
            known_all = udb.fetchall("advantage")
        self.layout_content.bind(
            minimum_height=self.layout_content.setter('height'))
        self.info.text = language_pack().text(
            "Öğrendiğiniz kelime sayısı : ") + str(len(known_all))
        self.known_words.text = ""
        self.known_tcount.text = ""
        self.known_fcount.text = ""
        self.known_prg.text = ""
        self.known_pc.text = ""
        if len(known_all) > 0:
            for w in known_all:
                self.known_words.text += "\n  " + str(w[5]) + "\n "
                self.known_tcount.text += "\n " + str(w[2]) + "\n "
                self.known_fcount.text += "\n " + str(w[3]) + "\n"
                self.known_prg.text += "\n " + language_pack().prg(
                    str(w[1])) + "\n"
                self.known_pc.text += "\n %" + str(int(w[4])) + "\n"



class InfoBox(GridLayout):
    infolbl = ObjectProperty(None)
    sizes = settings.sizes()


class WindowManager(ScreenManager):
    wmgr = ObjectProperty(None)



class LernenApp(App):
    def build(self):
        return Builder.load_file("mainmenu.kv")

    def on_start(self):
        pass

FIREBASE = firebase()


if __name__ == "__main__":
    LernenApp().run()
