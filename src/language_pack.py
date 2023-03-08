# ---------------------------------
# Module Name : Language Pack
# author : @ogibalboa
# "This module can be used freely"
# last edit : 28.02.2020
# --------------------------------
from database import database
import settings

settings.refresh()
udb = database(settings.user_db)


class language_pack:
    def __init__(self):
        self.language = udb.fetchall("settings")[0][2]

    def translate_to_english(self, word):
        words = ["Hoş Geldiniz.... Kurulum için aşağıdaki bilgileri giriniz.",
                 "İsim :", "Kelime öğrenmeyi istediğiniz dili seçiniz.",
                 "Çalışmak için ayıracağınız süre ?\n(Daha sonra tekrar değiştirebilirsiniz.)",
                 "Kelime Grupları : Temel     |   Yaygın  |   Nadir   |   İleri   |   GENEL  \n" + " " * 32,
                 "Hoş Geldin len ", "İlerleme Durumunuz \n",
                 "Öğrendiğiniz kelime sayısı : ",
                 "TÜM BİLGİLERİNİN SIFIRLANACAK !",
                 " KELİMELER BİTTİ !\n Yeni kelimeler öğren ve tekrar buraya gel !",
                 "Hoş Geldiniz\nBaşlamak için 'Onayla' butonuna basınız",
                 "KELİMELER BİTTİ", "Şimdi Quiz yap ve tekrar buraya gel",
                 "Öğren !", "Durumu Görüntüle", "Quiz", "Ayarlar", "Çıkış",
                 "Quiz zorluğu seçiniz", "Kelime : ", "Çevirisi : ",
                 "Başlamak için Next'e basınız",
                 "Dinle",
                 "Kelime         Doğru Sayısı        Yanlış Sayısı        Durum       İlerleme",
                 "Aşağıdaki Kelimenin Türkçe Karşılığını Yazınız\n\n",
                 "Bildin.",
                 "Tüm bilgileriniz sıfırlanacak ve öğrenmeye baştan başlayacaksınız ! \nOnaylıyor musunuz ?",
                 "Quiz zorluğunu seçiniz.\nOtomatik mod,bilgi seviyenize göre sınav oluşturacaktır. ",
                 "Evet", "Hayır", "<Dil Seçiniz>", "Almanca", "İptal",
                 "0-10 dk", "10-60 dk", "60 dkdan fazla",
                 "<Süre Seçiniz>", "Otomatik", "Temel", "Yaygın", "Nadir",
                 "İleri", "Onayla",
                 "Uygulama geliştirme aşamasındadır, lütfen öneri ve şikayetlerinizi ogibalboa@outlook.com adresinden ulaştırınız.",
                 "AYARLAR", "        Dil :", "Yeni", "İyi", "Kötü", "Başarılı",
                 "Öğreniliyor", "TEMEL KELİMELER",
                 "YAYGIN KULLANILAN", "NADİR KULLANILAN", "İLERİ SEVİYE",
                 "GENEL İLERLEYİŞ", "Güncelleme !",

                 ]

        translations = [
            "Welcome.... Please enter the information below to continue.",
            "Name :", "Choose the language you want to learn words",
            "How long time you want to spend to learn words ?\nYou can change later",
            "Word Groups : Basic  | Common |  Rare  |  Advantage  |  GENERAL \n" + " " * 32,
            "Welcome ", "Progress \n",
            "Total words you learned : ", "ALL INFORMATIONS WILL BE RESET !",
            " WORDS FINISHED !\n Learn new words and come again !",
            "Welcome !\n Press 'Submit' to start. ",
            "WORDS FINISHED !", "Now, make a quiz and come again !",
            "Learn !", "View Learn Status", "Quiz", "Settings", "Exit",
            "Select Quiz Difficulty", "Word : ", "Translation : ",
            "Press 'Next' to start",
            "Listen",
            "Word           True Count        False Count        Status       Progress",
            "Write the translation of the following word \n\n", "Correct",
            "All informations will be reset and you will start learning again\nDo you confirm ?",
            "Select Quiz Difficulty\nAutomatic mode will generate the quiz by your knowledge",
            "Yes", "No", "<Choose Language>", "German", "Cancel", "0-10 mins",
            "10-60 mins", "more than 60 mins",
            "<Choose Time>", "Automatic", "Basic", "Common", "Rare",
            "Advantage", "Submit",
            "The app is on development phase, please send bugs and suggestions to us from ogibalboa@outlook.com.",
            "SETTINGS", "Language :", "New", "Good", "Bad", "Successful",
            "Learning", "BASIC WORDS",
            "COMMON WORDS", "RARE WORDS", "ADVANCED WORDS", "GENERAL PROGRESS",
            "Update !",

            ]
        if self.language == "English":
            for i in range(0, len(words)):
                if word == words[i]:
                    return str(translations[i])
        elif self.language == "Turkish":
            for i in range(0, len(translations)):
                if word == translations[i]:
                    return str(words[i])
        return word

    def text(self, word):
        if self.language == "Turkish":
            return self.translate_to_english(word)
        elif self.language == "English":
            return self.translate_to_english(word)
        else:
            return word

    def prg(self, word):
        if word == "new":
            out = self.text("Yeni")
        elif word == "learning":
            out = self.text("Öğreniliyor")
        elif word == "good":
            out = self.text("İyi")
        elif word == "bad":
            out = self.text("Kötü")
        elif word == "success":
            out = self.text("Başarılı")
        else:
            out = ""
        return out
