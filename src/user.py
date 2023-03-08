def update_udb(db_, param=None):
    from database import database
    # UPDATE ALL VARIABLES THAT NEED TO BE CALCULATED AGAIN
    if param == None:
        tables = ["basic", "common"]
    variables = ["True_Count", "False_Count"]
    results = []
    for table in tables:
        dcount = len(db_.fetchall(table))  # FETCH DATA COUNT
        for rowid in range(1, dcount + 1):
            for variable in variables:
                results.append(
                    db_.search(table=table, select_=variable, rowid=rowid))
            if results[0] != None:
                progress, progress_percent = calculations(int(results[0][0]),
                                                          int(results[1][0]),
                                                          wg=table)
                db_.update(table=table, rowid=rowid, percent=progress_percent,
                           progress=progress)
            results = []


global calculations


def calculations(tc, fc, wg):
    global th
    global progress_
    global progress_percent_
    global pc
    global sums
    sums = tc + fc
    pc = tc * 100 / sums
    if sums == 0:
        progress_ = "new"
        progress_percent_ = 0
        return progress_, progress_percent_

    if wg == "basic":  # KELİME ZORLUĞUNA GÖRE EŞİK DEĞERİ DEĞİŞİR
        th = 2
    elif wg == "common":
        th = 2

    if sums < th:
        if pc < 100:
            progress_ = "bad"

        else:
            progress_ = "learning"
        progress_percent_ = int(sums) * 20 / th
    elif th <= sums < th * 2:
        if pc > 75:
            progress_ = "learning"
        else:
            progress_ = "bad"
        progress_percent_ = int(sums) * 20 / th
    elif sums >= th * 2:
        if pc >= 90:
            progress_ = "success"
            progress_percent_ = 100
        elif pc > 70:
            progress_ = "good"
            progress_percent_ = pc
        elif pc <= 70:
            progress_ = "bad"
            progress_percent_ = pc

    elif th * 2 < sums <= th * 3:
        if pc > 85:
            progress_ = "success"
            progress_percent_ = 100
        elif pc >= 70:
            progress_ = "good"
            progress_percent_ = 50 + sums + pc / 10 * 2
        elif pc < 70:
            progress_ = "bad"
            progress_percent_ = pc
    elif pc > 85 and sums > th * 3:
        progress_ = "success"
        progress_percent_ = 100
    return progress_, progress_percent_


def cal_progress(udb):
    basic = udb.fetchall("basic")
    common = udb.fetchall("common")
    b_kwn = 0
    c_kwn = 0  # bilinen kelime sayısı
    for b_var in basic:
        try:
            b_kwn += int(b_var[
                             4]) / 100  # Her kelimeyi ilerleme yüzdesine göre 0 - 1 arasında değerlendirir.
        except ZeroDivisionError:
            pass
    for c_var in common:
        try:
            c_kwn += int(c_var[4]) / 100
        except ZeroDivisionError:
            pass
    try:
        basic_progress = b_kwn / 2.5
    except ZeroDivisionError:
        basic_progress = 0
    try:
        common_progress = c_kwn / 2.5
    except ZeroDivisionError:
        common_progress = 0
    try:
        general_progress = (b_kwn + c_kwn) / 10
    except ZeroDivisionError:
        general_progress = 0
    udb.execute_update(table="progress", where_=1, set_="basic",
                       value=basic_progress)
    udb.execute_update(table="progress", where_=1, set_="common",
                       value=common_progress)
    udb.execute_update(table="progress", where_=1, set_="general",
                       value=general_progress)
