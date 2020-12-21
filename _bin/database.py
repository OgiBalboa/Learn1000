#---------------------------------
# Module Name : Database Functions
# author : @ogibalboa
# "This module can be used freely"
# last edit : 28.02.2020
#--------------------------------

import sqlite3
from user import calculations
from program_files import program_files
class database:
    def __init__(self,name):
        pfiles= program_files()
        self.name = name
        execute = pfiles.dictionary + "/" +str(name)+".db"
        with sqlite3.connect(execute) as self.db:
            self.cur = self.db.cursor()
    def fetchall(self,table):
        execute = "SELECT * FROM "+ table 
        self.cur.execute(execute)
        datas = self.cur.fetchall()
        return datas
    
    def insert(self,table,rowid,word,progress = "new",tcount = 0,fcount = 0,p_percent = 0):
        self.values = [int(rowid),str(progress),int(tcount),int(fcount)\
                        ,float(p_percent),str(word)]
        print(self.values)
        execute = "INSERT INTO "+str(table)+ """ (Word_ID,Progress,True_Count,False_Count,
                    Progress_Percent,Word) VALUES (?,?,?,?,?,?);"""
        self.cur.execute(execute,self.values)
        self.db.commit()

    def update(self,table,rowid,inc_tcount = 0,inc_fcount = 0,\
               tcount = None,fcount = None,inc_percent = None,percent = None,progress = None):
        
        self.tcount = int(self.search(table,select_ = "True_Count",rowid = rowid))
        self.fcount = int(self.search(table,select_ = "False_Count",rowid = rowid))
        
        if inc_tcount>0 or inc_fcount >0:
            self.tcount += inc_tcount
            self.fcount += inc_fcount
            self.execute_update(table,where_=rowid,set_="True_Count",value =self.tcount)
            self.execute_update(table,where_= rowid,set_="False_Count",value =self.fcount)
        progress,percent = calculations(self.tcount,self.fcount,table)    
        if progress != None:
            self.execute_update(table,where_ = rowid,set_="Progress",value = progress)
            self.execute_update(table,where_ = rowid,set_="Progress_Percent",value = percent)
            
    def execute_update(self,table,set_,where_,value):
        execute = "UPDATE "+str(table)+" SET "+str(set_)+ "=? WHERE Word_ID=?"
        self.cur.execute(execute,(value,where_,))
        self.db.commit()
    
    def search(self,table,select_,rowid,where_ = "Word_ID"): #select_ = variable name
        execute = "SELECT "+str(select_)+" FROM "+str(table)+\
                  " WHERE "+str(where_)+"=?"

        self.cur.execute(execute,(rowid,))
        result = self.cur.fetchone()
        if result is None:
            return None
        else :
            return result[0]

    def reset (self,table = "all"):
        if table is "all":
            tables = ["basic","common","rare","advanced"]
            for tab in tables:
                execut = "SELECT Word_ID from " + tab
                self.cur.execute(execut)
                rowids = self.cur.fetchall()
                for i in rowids:
                    execute ="DELETE from " + tab+ " WHERE Word_ID = ?"
                    self.cur.execute(execute,(i[0],))
            self.db.commit()
