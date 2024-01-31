import tkinter as tk
from tkinter import *
import os
import sqlite3
import re
import smtplib, ssl
import random
from tkinter import messagebox

#connecting to old database
logdb=sqlite3.connect("login.db")

#create cursor
c=logdb.cursor()

root = Tk()
root.geometry("{0}x{0}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.state('zoomed')
root.configure(bg="gray25")
root.title("password recovery")

regex = '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'

l1=tk.Label(root,text="Mask Detection System \n Password Recovery",fg="snow",relief="raised",borderwidth=4,font=("calibri",40),bg="#5e3594")
l1.pack(side=TOP,fill=X)

fpl = tk.Label(root,bg="gray60",text="Enter your registered email ID",relief="raised",fg="black",font=("times new roman",20))
fpl.place(bordermode=OUTSIDE,relheight=0.04,relwidth=0.27,relx = 0.27, rely = 0.37)
global fpe
fpe = tk.Entry(root,bg="cyan2",fg="black",font=("times new roman",20))
fpe.place(bordermode=OUTSIDE,relheight=0.037,relwidth=0.35,relx = 0.22, rely = 0.42)

def goback():
        import app

def goback1():
        window.destroy()


def sendemail():
        # validate otp
        def verifyotp():
                        if lotp.get()==otp:
                                c.execute("SELECT password FROM info DESC WHERE email=?",(fpedb,))
                                records=c.fetchall()
                                for row in records:
                                        passfor=row[0]
                                  # create smtp session 
                                s = smtplib.SMTP("smtp.gmail.com" , 587)  # 587 is a port number
                                # start TLS for E-mail security 
                                s.starttls()
                                # Auto Log in to your gmail account
                                s.login("g9fmds09@gmail.com" , "G9FMDS@fmds09")
                                #send email
                                subject = 'Mask Detection System Password Recovery'
                                body = 'This is Email for the Request of password recovery registered with this email id\n The password is :'

                                msg = f'Subject: {subject}\n\n{body}\n{passfor}'
                                s.sendmail("tejasharal003@gmail.com" , fpe.get(),msg)
                                print("Email sent succesfully..")
                                messagebox.showinfo("Recovery Email sent successfully","PASSWORD Recovery Email has been succesfully sent to\n"+fpedb.upper())
                                fpe.delete(0,25)
                                # close smtp session
                                s.quit()
                                root.destroy()
                                import app
                
        global otp
         # create smtp session 
        s = smtplib.SMTP("smtp.gmail.com" , 587)  # 587 is a port number
        # start TLS for E-mail security 
        s.starttls()
        # Auto Log in to your gmail account
        s.login("g9fmds09@gmail.com" , "G9FMDS@fmds09")
        otp = random.randint(1000, 9999)
        otp = str(otp)
                
        s.sendmail("tejasharal003@gmail.com" , fpe.get(), otp)
        print("OTP sent succesfully..")
        # close smtp session
        s.quit()
        l4=Label(root,text="OTP sent successfully ! ",fg="red",font=("times new roman",18))
        l4.place(bordermode=OUTSIDE,relheight=0.04,relwidth=0.4,relx=0.25, rely=0.75)
        l4.after(3000, lambda: l4.destroy())

        window = tk.Toplevel(root)
        window.geometry('550x370+800+170')
        window.configure(bg="gray25")
        window.title("OTP Verification")
        
        l1=tk.Label(window,text="Mask Detection System \n OTP Verification",fg="snow",relief="raised",borderwidth=4,font=("calibri",40),bg="#5e3594")
        l1.pack(side=TOP,fill=X)
        
        loptl = tk.Label(window,bg="gray60",text="Enter your OTP:",relief="raised",fg="black",font=("times new roman",20))
        loptl.place(bordermode=OUTSIDE,relheight=0.11,relwidth=0.35,relx = 0.37, rely = 0.42)

        lotp = tk.Entry(window,bg="cyan2",fg="black",font=("times new roman",20))
        lotp.place(bordermode=OUTSIDE,relheight=0.11,relwidth=0.35,relx = 0.37, rely = 0.54)
        
        fpeo=tk.Button(window,text=" Verify ",bg="#5e3594",fg="black",command=verifyotp,font=("times new roman",15))
        fpeo.place(relheight=0.09,relwidth=0.35,relx=0.37,rely=0.73)

        back1=tk.Button(window,text=" GO Back To Login ",bg="#5e3594",fg="black",command=goback1,font=("times new roman",15))
        back1.place(relheight=0.09,relwidth=0.35,relx=0.37,rely=0.87)


def pasrec():
        if not re.search(regex,fpe.get()):
                l4=Label(root,text="Invalid email id",fg="red")
                l4.place(bordermode=OUTSIDE,relheight=0.04,relwidth=0.15,relx=0.7, rely=0.42)
                l4.after(3000, lambda: l4.destroy())
        elif re.search(regex,fpe.get()):
                c.execute("SELECT * FROM info ORDER BY id DESC")
                records=c.fetchall()
                for row in records:
                        if row[3] != "end":
                                global fpedb
                                fpedb=row[3]
                                if str(row[3])==fpe.get():#this one is a string:
                                        otpid=row[0]
                                        print("called")
                                        try:
                                                sendemail()
                                                break
                                        except:
                                                raise
                                                l4=Label(root,text="Some technical error Occured!!! \n Please Try Again",fg="red",font=("times new roman",18))
                                                l4.place(bordermode=OUTSIDE,relheight=0.05,relwidth=0.4,relx=0.25, rely=0.75)
                                                l4.after(2000, lambda: l4.destroy())
                                                break
                                                
                        else:
                                print("called else")
                                l4=Label(root,text="Email id not Registered! Try Another !",fg="red")
                                l4.place(bordermode=OUTSIDE,relheight=0.04,relwidth=0.25,relx=0.7, rely=0.42)
                                l4.after(2000, lambda: l4.destroy())
                                fpe.delete(0,25)
                                break
                        
fpeb=tk.Button(root,text=" SUBMIT ",bg="#5e3594",fg="black",command=pasrec,font=("times new roman",15))
fpeb.place(relheight=0.05,relwidth=0.2,relx=0.3,rely=0.5)

back=tk.Button(root,text=" GO Back To Login ",bg="#5e3594",fg="black",command=goback,font=("times new roman",15))
back.place(relheight=0.05,relwidth=0.2,relx=0.3,rely=0.58)


root.mainloop()
