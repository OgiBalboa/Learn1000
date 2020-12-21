from database import database
from random import randint
global check_word
global get_words
global random_word
def check_word(db_, table, rowid):
    result = db_.search(table=table, select_="*", rowid=rowid)
    return result

def get_words(db_, table):
    rowidlist = ["NULL"]
    words = db_.fetchall(table)
    words = ["NULL"] + words
    for i in range(1, len(words)):
        rowidlist.append(i)
    reglist = rowidlist
    return words, rowidlist, reglist

def random_word(wordlist, rowidlist, reglist=None, trlist=None, tablist=None):
    if reglist == None:
        reglist = rowidlist
    if len(reglist) <= 1:
        if trlist is None:
            return "", "", "", ""
        else:
            return "", "", "", "", ""
    random = randint(1, len(reglist) - 1)
    reg = reglist[random]
    rowid = rowidlist[reg]
    if trlist is None:
        word = wordlist[reg][1]
        translation = wordlist[reg][2]
        return word, translation, rowid, reg
    else:
        word = wordlist[reg]
        translation = trlist[reg]
        table = tablist[reg]
        return word, translation, rowid, table, reg

def auto_generate(udb_, db_, learnlimit=20, param=None):
    global wordlist
    global trlist
    global datas
    global progress
    global reg
    global count
    count = 0
    wordlist = ["NULL"]
    trlist = ["NULL"]
    tablist = ["NULL"]
    rowidlist = ["NULL"]
    reglist = ["NULL"]
    progress = udb_.fetchall("progress")

    def verify(progress, param):
        if param == "learn":
            if progress == None or progress == "bad":
                return True
            else:
                return False
        else:
            if progress == "new" or progress == "bad" or progress == "learning":
                return True
            else:
                return False

    def add_words(table, limit=1000, ):
        global count
        datas = db_.fetchall(table)
        for data in range(0, len(datas)):  # SEARCH FOR WORD PROGRESS
            word_progress = udb_.search(table=table, select_="Progress", \
                                        where_="Word", rowid=datas[data][1])
            if verify(word_progress, param=param):  # verify progress
                wordlist.append(datas[data][1])
                trlist.append(datas[data][2])
                tablist.append(table)
                rowidlist.append(datas[data][3])
                count += 1
            if count >= learnlimit or count >= limit:
                break
        for i in range(0, len(wordlist) - 1):
            reglist.append(i + 1)

    if progress[0][0] < 50 or progress[0] == None:
        add_words(table="basic", limit=learnlimit)

    elif progress[0][0] < 100:
        add_words(table="basic", limit=learnlimit * 0.8)
        add_words(table="common", limit=learnlimit * 0.2)

    elif progress[0][1] < 100 or progress[0][1] == None:
        add_words(table="common", limit=learnlimit)

    elif progress[0][2] < 100:
        add_words(table="rare", limit=learnlimit)

    return wordlist, trlist, tablist, rowidlist, reglist


def Capital(text,lang = None):

    if lang != "Turkish":
        return text.title()
    text = text.split(" ")
    for i in range(0, len(text)):
        try:
            if text[i][0] == "i":
                text[i] = "İ" + text[i][1::]
            else:
                text[i] = text[i].capitalize()
        except:
            pass
    return " ".join(text)
