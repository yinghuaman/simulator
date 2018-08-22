import io
from io import StringIO
from tkinter import *
import time
import datetime
import pandas as pd
from tkinter import messagebox
import psycopg2
from sqlalchemy import create_engine

class my_GUI():
    def __init__(self,master):
        self.master = master

    #GUI版面设计
    def set_master(self):
        self.master.title("数据上传模拟器")
        self.master.geometry("800x400")
        self.master.resizable(0,0)

        self.var_IP = StringVar()
        self.var_IP.set("")
        Entry(self.master,textvariable = self.var_IP,width=20,font = ("Verdana",15) ).place(x=130,y=30)
        Label(self.master,text = "IP:".encode("utf-8"),width = 10,font = ("Arial",15)).place(x=15,y=30)
        Label(self.master,text = "*".encode("utf-8"),fg="red",font=10).place(x=87,y=30)

        self.var_port = StringVar()
        self.var_port.set("")
        Entry(self.master, textvariable=self.var_port, width=20, font=("Verdana", 15)).place(x=525, y=30)
        Label(self.master, text="port:".encode("utf-8"), width=10, font=("Arial", 15)).place(x=415, y=30)
        Label(self.master, text="*".encode("utf-8"), fg="red", font=10).place(x=493, y=30)

        self.var_db = StringVar()
        self.var_db.set("")
        Entry(self.master, textvariable=self.var_db, width=20, font=("Verdana", 15)).place(x=130, y=130)
        Label(self.master, text="database:".encode("utf-8"), width=10, font=("Arial", 15)).place(x=15, y=130)
        Label(self.master, text="*".encode("utf-8"), fg="red", font=10).place(x=117, y=130)

        self.var_user = StringVar()
        self.var_user.set("")
        Entry(self.master, textvariable=self.var_user, width=20, font=("Verdana", 15)).place(x=525, y=130)
        Label(self.master, text="user:".encode("utf-8"), width=10, font=("Arial", 15)).place(x=415, y=130)
        Label(self.master, text="*".encode("utf-8"), fg="red", font=10).place(x=493, y=130)

        self.var_password = StringVar()
        self.var_password.set("")
        Entry(self.master, textvariable=self.var_password, width=20, font=("Verdana", 15)).place(x=130, y=230)
        Label(self.master, text="password:".encode("utf-8"), width=10, font=("Arial", 15)).place(x=15, y=230)
        Label(self.master, text="*".encode("utf-8"), fg="red", font=10).place(x=117, y=230)

        self.var_time = StringVar()
        self.var_time.set("")
        Entry(self.master, textvariable=self.var_time, width=20, font=("Verdana", 15)).place(x=525, y=230)
        Label(self.master, text="time:".encode("utf-8"), width=10, font=("Arial", 15)).place(x=415, y=230)

        b1 = Button(self.master,text="取消",width=10,font = ("宋体",10),command = self.cancel)
        b1.bind("<Return>",self.cancel)
        b1.bind("<Button-1>",self.cancel)
        b1.place(x=270,y=350)
        b2 = Button(self.master, text="上传", width=10, font=("宋体", 10), command=self.upload)
        b2.bind("<Return>", self.upload)
        b2.bind("<Button-1>", self.upload)
        b2.place(x=420, y=350)

        Label(self.master,text="*为必填项",width=20,fg="red",font=("Arial", 10)).place(x=10,y=270)

    #读取本地文件
    def Loaddata(self,filename):
        data = pd.read_csv(filename,sep="\t")
        return data

    #判断是否链接成功
    def is_connected(self):
        user = self.var_user.get()
        ip = self.var_IP.get()
        password = self.var_password.get()
        database = self.var_db.get()
        port = self.var_port.get()
        flag = 1
        try:
            messagebox.showinfo("开始链接数据库")
            conn = psycopg2.connect(database = database,user=user,password=password,host=ip,port=port)
            return flag
        except:
            flag=0
            messagebox.showinfo("链接数据库失败")
            return flag

    def write_to_sql(self,flag,tablename):
        if flag == 1:
            messagebox.showinfo("数据库连接成功")
            user = self.var_user.get()
            ip = self.var_IP.get()
            password = self.var_password.get()
            db = self.var_db.get()
            port = self.var_port.get()
            engine = create_engine("postgresql+psycopg2://"+user+":"+password+"@"+ip+":"+str(port)+"/"+db)
            for name in tablename:
                df = self.Loaddata("data/%s.txt"%name)
                output = StringIO()
                df.to_csv(output,sep="\t",index=False,header=False)
                output.getvalue()
                output.seek(0)
                conn = engine.raw_connection()
                cur = conn.cursor()
                cur.copy_from(output,name,null='')
                conn.commit()
                cur.close()

    #定义上传函数
    def upload(self,event):
        flag = self.is_connected()
        self.write_to_sql(flag)

    def cancel(self,event):
        self.var_port.set("")
        self.var_db.set("")
        self.var_password.set("")
        self.var_IP.set("")
        self.var_user.set("")

def gui_start():
    root = Tk()
    myApp = my_GUI(root)
    myApp.set_master()
    root.mainloop()

gui_start()



