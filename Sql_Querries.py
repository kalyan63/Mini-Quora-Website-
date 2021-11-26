import sqlite3
import os
import hashlib
from datetime import datetime

def CheckUser(Uname):
    conn=sqlite3.connect('quora.db')
    cur=conn.cursor()
    cur.execute("Select Count(*) from User where User_name = ?",(Uname,))
    ct=cur.fetchone()
    conn.close()
    return(ct[0])

def CheckMail(Mail):
    conn=sqlite3.connect('quora.db')
    cur=conn.cursor()
    cur.execute("Select Count(*) from User where Email = ?",(Mail,))
    ct=cur.fetchone()
    conn.close()
    return(ct[0])

def InsertUser(Uname,Mail,Password):
    salt=os.urandom(8)
    hash=hashlib.pbkdf2_hmac('sha256', Password.encode('utf-8'), salt, 100000)
    Cur_date=str(datetime.now())
    arg=(Uname,hash,salt,Mail,Cur_date)
    conn=sqlite3.connect('quora.db')
    cur=conn.cursor()
    cur.execute("Insert into User(User_name,Password,Salt,Email,LastLogin) values(?,?,?,?,?)",arg)
    conn.commit()
    conn.close()

def CheckLogin(Uname,Password):
    conn=sqlite3.connect('quora.db')
    cur=conn.cursor()
    cur.execute("Select Password,Salt from User where User_name=?",(Uname,))
    res=cur.fetchone()
    conn.close()
    if(not res):
        return 0
    DbPassword,salt=res[0],res[1]
    if(hashlib.pbkdf2_hmac('sha256', Password.encode('utf-8'), salt, 100000)==DbPassword):
        return 1
    else:
        return 0

def GetUserId(Uname):
    conn=sqlite3.connect('quora.db')
    cur=conn.cursor()
    cur.execute("Select user_id from User where User_name=?",(Uname,))
    res=cur.fetchone()
    conn.close()
    return res[0]

def GetUserName(U_Id):
    conn=sqlite3.connect('quora.db')
    cur=conn.cursor()
    cur.execute("Select User_name from User where user_id=?",(U_Id,))
    res=cur.fetchone()
    conn.close()
    return res[0]

def GetUserMail(U_id):
    conn=sqlite3.connect('quora.db')
    cur=conn.cursor()
    cur.execute("Select Email from User where user_id=?",(U_id,))
    res=cur.fetchone()
    conn.close()
    return res[0]

def DisplayQues(): 
    conn = sqlite3.connect('quora.db') 
    cur = conn.cursor() 
    cur.execute("select * from Questions") 
    data = cur.fetchall()  
    conn.close()
    return(data)

def InsertQues(user_id,Q_Text,An):
    Cur_date=str(datetime.now())
    arg=(user_id,Q_Text,An,Cur_date)
    conn=sqlite3.connect('quora.db')
    cur=conn.cursor()
    cur.execute("Insert into Questions(user_id,Q_Text,Anonymous,Date) values(?,?,?,?)",arg)
    conn.commit()
    conn.close()

def GetQuestion(Q_id):
    conn=sqlite3.connect('quora.db')
    cur=conn.cursor()
    cur.execute("Select * from Questions where Q_id=?",(Q_id,))
    Ques=cur.fetchall()
    cur.execute("Select * from Answer where Q_id=?",(Q_id,))
    Ans=cur.fetchall()
    conn.close()
    return {"Ques":Ques[0],"Ans":Ans}

def GetAnswer(A_id):
    conn=sqlite3.connect('quora.db')
    cur=conn.cursor()
    cur.execute("Select * from Answer where A_id=?",(A_id,))
    Ans=cur.fetchall()
    cur.execute("Select * from Comments where A_id=?",(A_id,))
    Com=cur.fetchall()
    conn.close()
    return {"Ans":Ans[0],"Com":Com}

def DeleteQuestion(Q_id):
    conn=sqlite3.connect('quora.db')
    cur=conn.cursor()
    cur.execute("Delete from Questions where Q_id=?",(Q_id,))
    conn.commit()
    conn.close()

def DeleteAnswer(A_id):
    conn=sqlite3.connect('quora.db')
    cur=conn.cursor()
    cur.execute("Delete from Answer where A_id=?",(A_id,))
    conn.commit()
    conn.close()

def InsertAns(Q_id,user_id,A_text,An):
    conn=sqlite3.connect('quora.db')
    cur=conn.cursor()
    cur.execute("Insert into Answer(Q_id,user_id,A_Text,Date,Anonymous) values(?,?,?,?,?)",(Q_id,user_id,A_text,str(datetime.now()),An))
    conn.commit()
    cur.execute("Select A_id from Answer where Q_id=? and user_id=? and A_text=?",(Q_id,user_id,A_text))
    res=cur.fetchone()
    conn.close()
    return res[0]

def UpVote_Answer(user_id,A_id):
    conn=sqlite3.connect('quora.db')
    cur=conn.cursor()
    cur.execute("")
    conn.commit()
    conn.close()

def DownVote(user_id,A_id):
    conn=sqlite3.connect('quora.db')
    cur=conn.cursor()
    cur.execute()
    conn.commit()
    conn.close()   

def InsertFiles(A_id,loc):
    conn=sqlite3.connect('quora.db')
    cur=conn.cursor()
    cur.execute("Insert into Media(A_id,File_loc) values(?,?)",(A_id,loc))
    conn.commit()
    conn.close()

def GetFileLoc(A_id):
    conn=sqlite3.connect('quora.db')
    cur=conn.cursor()
    cur.execute("Select File_loc from Media where A_id=?",(A_id,))
    res=cur.fetchone()
    conn.close()
    if(res):
        return res[0]
    else:
        return None    
