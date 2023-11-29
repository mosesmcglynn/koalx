import tkinter as tk
from tkinter import ttk
import sv_ttk
from tkinter import filedialog
from tkcalendar import DateEntry
from datetime import datetime, date
import time
from tkinter import messagebox
from PIL import ImageTk, Image
import random
from fpdf import FPDF
import ast

window = tk.Tk()
window.title("Bank Management System")
window.geometry("1800x900")
window.resizable(False, False)
window.columnconfigure(0, weight=1)  # Sidenav
window.columnconfigure(1, weight=3)  # Content


window.update_idletasks()

# Get screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate position
position_top = int((screen_height / 2) - (900 / 2))
position_right = int((screen_width / 2) - (1800 / 2))

# Position window
window.geometry(f'{1800}x{900}+{position_right}+{position_top}')


datenow = datetime.now().strftime("%m/%d/%y")
print(datenow)

title = ttk.Style()
title.configure("Title.TLabel", font=("Arial", 18, "bold"))


def join(*args):
    return " ||| ".join(args)

def columns(type):
    transaction = ["Transaction ID", "Date", "Account Number", "Transaction Type", "Debit Amount", "Credit Amount", "Description"]
    customer = ["Customer ID", "Name", "Date of Birth", "Contact Number", "Email Address", "Address", "Employment Status", "Annual Income", "Source of Income", "Identification Type", "Identification Number"]
    account = ["Customer ID", "Account Holder's Name", "Account Number", "Account Type", "Date Opened", "Balance", "Contact Preference"]
    match type:
        case "transaction":
            return transaction
        case "customer":
            return customer
        case "account":
            return account
    

class Display:
    def __init__(self, type, frame):
        self.type = type
        self.frame = frame

    def columns(self):
        transaction = ["Transaction ID", "Date", "Account Number", "Transaction Type", "Debit Amount", "Credit Amount", "Description"]
        customer = ["Customer ID", "Name", "Date of Birth", "Contact Number", "Email Address", "Address", "Employment Status", "Annual Income", "Source of Income", "Identification Type", "Identification Number"]
        account = ["Customer ID", "Account Holder's Name", "Account Number", "Account Type", "Date Opened", "Balance", "Contact Preference"]
        match self.type:
            case "transaction":
                return transaction
            case "customer":
                return customer
            case "account":
                return account
            
    def header(self, *args):
        for i, text in enumerate(args):
            tk.Label(self.frame, text=text, font=("Arial", 12, "bold")).grid(row=0, column=i, padx=5, pady=5)

    def content(self, *args, rows=1):
        for row in range(rows):
            for items in list(args):
                for i, text in enumerate(items[row]):
                    tk.Label(self.frame, text=text, font=("Arial", 12, "bold")).grid(row=row+1, column=i, padx=5, pady=5)
        self.frame.update()
    
    def button(self, *args, direction="vertical", commands=[]):
        if direction == "vertical":
            for items in list(args):
                for i, text in enumerate(items):
                    button = ttk.Button(self.frame, text=text, command=lambda i=i: switchContent(commands[i]))
                    button.grid(row=i, column=0, padx=5, pady=5)
        elif direction == "horizontal":
            print(args)
            print(direction)
            for items in list(args):
                for i, text in enumerate(items):
                    button = ttk.Button(self.frame, text=text, command=lambda i=i: switchContent(commands[i]))
                    button.grid(row=0, column=i, padx=5, pady=5)
        elif direction == "pack":
            for items in list(args):
                for i, text in enumerate(items):
                    button = ttk.Button(self.frame, text=text, command=lambda i=i: switchContent(commands[i]))
                    button.pack(pady=10)
        self.frame.update()

class Transaction:
    def __init__(self, transid=None, date=None, accnum=None, transtype=None, debit=None, credit=None, desc=None):
        self.transid = transid
        self.date = date
        self.accnum = accnum
        self.transtype = transtype
        self.debit = debit
        self.credit = credit
        self.desc = desc
    
    def balance(self):
        try:
            with open("account.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    line = line.split(" ||| ")
                    line = [i.strip() for i in line]

                    if (str(self.accnum) == str(line[2])):
                        return line[5]
                messagebox.showinfo("Balance", "Account number not exist")
                return None
        except FileNotFoundError:
            open("account.txt", "x")
            messagebox.showinfo("Balance", "File not exist")
            return None

    def history(self, limit=-1):
        try:
            with open("transactions.txt", "r") as file:
                lines = file.readlines()
                lines = lines[::-1]
                if (limit == -1):
                    hist = list()
                    for line in lines:
                        hist.append(list([i.strip() for i in line.split(' ||| ')]))
                        # print(line)
                    # print(hist)
                    return hist
                else:
                    for line in lines[:limit]:
                        line = line.split(" ||| ")
                        line = [i.strip() for i in line]
                    return line[:limit]
        except FileNotFoundError:
            open("transactions.txt", "x")
            messagebox.showinfo("Transaction History", "File not exist")
            return None
        
    def withdraw(self, accnum, amount, desc):
        try:
            with open("account.txt", "r") as file:
                lines = file.readlines()
            with open("account.txt", "w") as file:
                for line in lines:
                    line = line.strip()
                    accinfo = line.split(" ||| ")
                    if (accnum == accinfo[2]):
                        fields = [accinfo[0], accinfo[1], accinfo[2], accinfo[3], accinfo[4], str(int(accinfo[5]) - int(amount)), accinfo[6]]
                        for i in range(len(fields)):
                            if (fields[i] == ""):
                                fields[i] = accinfo[i]
                        custid, accname, accnum, acctype, accdate, accbal, accpref = fields
                        file.write(join(custid, accname, accnum, acctype, accdate, accbal, accpref) + "\n")
                        print("Withdraw success")
                        messagebox.showinfo("Withdraw", "Withdraw success")
                        time.sleep(1)
                        switchFrame(accmanage)
                    else:
                        file.write(line + "\n")
        except FileNotFoundError:
            open("account.txt", "x")
            messagebox.showinfo("Withdraw", "File not exist")
            return None
        
    def deposit(self, accnum, amount, desc):
        try:
            with open("account.txt", "r") as file:
                lines = file.readlines()
            with open("account.txt", "w") as file:
                for line in lines:
                    line = line.strip()
                    accinfo = line.split(" ||| ")
                    if (accnum == accinfo[2]):
                        fields = [accinfo[0], accinfo[1], accinfo[2], accinfo[3], accinfo[4], str(int(accinfo[5]) + int(amount)), accinfo[6]]
                        for i in range(len(fields)):
                            if (fields[i] == ""):
                                fields[i] = accinfo[i]
                        custid, accname, accnum, acctype, accdate, accbal, accpref = fields
                        file.write(join(custid, accname, accnum, acctype, accdate, accbal, accpref) + "\n")
                        print("Deposit success")
                        messagebox.showinfo("Deposit", "Deposit success")
                        time.sleep(1)
                        switchFrame(accmanage)
                    else:
                        file.write(line + "\n")
        except FileNotFoundError:
            open("account.txt", "x")
            messagebox.showinfo("Deposit", "File not exist")
            return None


class Admin:
    def __init__(self, adminname):
        self.adminname = adminname
        print(self.adminname)

    @staticmethod
    def login(adminname, adminpass):
        if not all([adminname, adminpass]):
            # empty field
            print("Empty field")
            messagebox.showinfo("Register", "Please fill in all the field")
            return False
        # read file for login
        with open("admin.txt", "r") as file:
            for line in file:
                line = line.strip()
                identity = line.split(" ||| ")
                identity = [i.strip() for i in identity]
                print(identity)
                print(adminname, adminpass)
                if (adminname == identity[0] and adminpass == identity[1]):
                    print("Login success")
                    messagebox.showinfo("Login", "Login success")
                    with open('login_state.txt', 'w') as user:
                        user.write(adminname)
                    time.sleep(1)
                    switchFrame(content,  include=sidenav)
                    return True
            else:
                print("Wrong username or password")
                messagebox.showinfo("Login", "Wrong username or password")
                username.delete(0, 'end')
                password.delete(0, 'end')
                return False
    
    @staticmethod
    def register(adminname, adminpass, adminpass2):
        if not all([adminname, adminpass, adminpass2]):
            #empty field
            print("Empty field")
            messagebox.showinfo("Register", "Please fill in all the field")
            return False
        #check if username already exist
        with open("admin.txt", "r") as file:
            for line in file:
                line.strip()
                print(line)
                identity = line.split(" ||| ")
                if (adminname == identity[0]):
                    print("Username already exist")
                    messagebox.showinfo("Register", "Username already exist")
                    # regusername.delete(0, 'end')
                    # regpassword.delete(0, 'end')
                    # regpassword2.delete(0, 'end')
                    return False
        if (adminpass != adminpass2):
            #password not match
            print("Password not match")
            messagebox.showinfo("Register", "Password not match")
            # regusername.delete(0, 'end')
            # regpassword.delete(0, 'end')
            # regpassword2.delete(0, 'end')
            return False
        else:
            #write file for register
            with open("admin.txt", "a+") as file:
                file.write(adminname.strip() + " ||| " + adminpass + "\n")
                print("Register success")
                messagebox.showinfo("Register", "Register success")
                time.sleep(1)
                # switchFrame(doneregister)
            return True

    @staticmethod
    def logout():
        with open('login_state.txt', 'w') as user:
            user.write('')
        # switchFrame(home)

    @staticmethod
    def user():
        with open('login_state.txt', 'r') as user:
            return user.read()


class Customer:
    def __init__(self, custid, custname, custdob, custphone, custemail, custaddress, custes, custai, custsoi, custit, custinum):
        self.custid = custid
        self.custname = custname
        self.custdob = custdob
        self.custphone = custphone
        self.custemail = custemail
        self.custaddress = custaddress
        self.custes = custes
        self.custai = custai
        self.custsoi = custsoi
        self.custit = custit
        self.custinum = custinum

    def custinfo(self, custid):
        with open("customer.txt", "r") as file:
            exist = False
            for i in file.readlines():
                print(i)
                i = i.strip()
                custinfo = i.split(" ||| ")
                custinfo = [i.strip() for i in custinfo]
                if (custid == custinfo[0]):
                    exist = True
                    return custinfo
            if exist == False:
                print("Customer ID not exist")
                messagebox.showinfo("Customer Information", "Customer ID not exist")
                switchFrame(custmanage)

    def addcust(self):
        #open file for add customer
        with open("customer.txt", "a+") as file:
            fields = [str(lastcustid()), self.custname, self.custdob, self.custphone, self.custemail, self.custaddress, self.custes, self.custai, self.custsoi, self.custit, self.custinum]
            for i in range(len(fields)):
                if (fields[i] == ""):
                    fields[i] = "-"
            file.write(join(*fields) + "\n")
            print("Add customer success")
            messagebox.showinfo("Add Customer", "Add customer success")
            time.sleep(1)
            switchFrame(custmanage)

    def editcust(self, custid, custname, custaddress, custphone, custemail):
        #open file for edit customer
        with open("customer.txt", "r") as file:
            lines = file.readlines()
        with open("customer.txt", "w") as file:
            for line in lines:
                line = line.strip()
                custinfo = line.split(" ||| ")
                if (custid == custinfo[0]):
                    fields = [custid, custname, custaddress, custphone, custemail]
                    for i in range(len(fields)):
                        if (fields[i] == ""):
                            fields[i] = custinfo[i]
                    custid, custname, custaddress, custphone, custemail = fields
                    file.write(join(custid, custname, custaddress, custphone, custemail) + "\n")
                else:
                    file.write(line + "\n")
        print("Edit customer success")
        messagebox.showinfo("Edit Customer", "Edit customer success")
        time.sleep(1)
        switchFrame(custmanage)

    def delcust(self, custid):
        #open file for delete customer
        with open("customer.txt", "r") as file:
            lines = file.readlines()
        with open("customer.txt", "w") as file:
            for line in lines:
                line = line.strip()
                custinfo = line.split(" ||| ")
                if (custid != custinfo[0]):
                    file.write(line + "\n")
        print("Delete customer success")
        messagebox.showinfo("Delete Customer", "Delete customer success")
        time.sleep(1)
        switchFrame(custmanage)

    def searchcust(self, custid):
        #open file for search customer
        with open("customer.txt", "r") as file:
            for line in file:
                line = line.strip()
                custinfo = line.split(" ||| ")
                if (custid == custinfo[0]):
                    print("Customer ID exist")
                    return True
            else:
                print("Customer ID not exist")
                return False

class Account:
    def __init__(self, custid, accname, accnum, acctype, accdate, accbal, accpref):
        self.custid = custid
        self.accname = accname
        self.accnum = accnum
        self.acctype = acctype
        self.accdate = accdate
        self.accbal = accbal
        self.accpref = accpref

    def accinfo(self, accnum):
        with open("account.txt", "r") as file:
            exist = False
            for i in file.readlines():
                print(i)
                i = i.strip()
                accinfo = i.split(" ||| ")
                accinfo = [i.strip() for i in accinfo]
                if (accnum == accinfo[2]):
                    exist = True
                    return accinfo
            if exist == False:
                print("Account number not exist")
                messagebox.showinfo("Account Information", "Account number not exist")
                switchFrame(accmanage)

    def openAccount(self, custid, accname, acctype, accdate, accbal, accpref):
        #open file for add account
        with open("account.txt", "a+") as file:
            accnum = str(random.randint(1000000000, 9999999999))
            file.write(join(custid, accname, accnum, acctype, accdate, accbal, accpref) + "\n")
            print("Add account success")
            messagebox.showinfo("Add Account", "Add account success")
            time.sleep(1)
            switchFrame(accmanage)

    def editAccount(self, accnum, accname, acctype, accpref):
        #open file for edit account
        with open("account.txt", "r") as file:
            lines = file.readlines()
        with open("account.txt", "w") as file:
            for line in lines:
                line = line.strip()
                accinfo = line.split(" ||| ")
                if (accnum == accinfo[2]):
                    fields = [accinfo[0], accname, accnum, acctype, accinfo[4], accinfo[5], accpref]
                    for i in range(len(fields)):
                        if (fields[i] == ""):
                            fields[i] = accinfo[i]
                    custid, accname, accnum, acctype, accdate, accbal, accpref = fields
                    file.write(join(custid, accname, accnum, acctype, accdate, accbal, accpref) + "\n")
                else:
                    file.write(line + "\n")
        print("Edit account success")
        messagebox.showinfo("Edit Account", "Edit account success")
        time.sleep(1)
        switchFrame(accmanage)

    def delacc(self, accnum):
        #open file for delete account
        with open("account.txt", "r") as file:
            lines = file.readlines()
        with open("account.txt", "w") as file:
            for line in lines:
                line = line.strip
    
class Frames:
    def __init__(self, frame):
        self.frame = frame

    def scrollable(self, frame):
        canvas = tk.Canvas(self.frame, bg="white")
        scrollbar = tk.Scrollbar(canvas, orient="horizontal", command=canvas.xview)
        canvas.configure(xscrollcommand=scrollbar.set)
        canvas.bind("<MouseWheel>", lambda e: canvas.xview_scroll(int(-1*(e.delta/120)), "units"))
        scrollbar.bind("<MouseWheel>", lambda e: canvas.xview_scroll(int(-1*(e.delta/120)), "units"))
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="bottom", fill="x")
        return canvas

    def fixed(self):
        frame = ttk.Frame(self.frame, width=(1800/4)*3, height=900)
        frame.pack()
        frame.pack_propagate(0)
        return frame
    
    def fixed2(self):
        frame = ttk.Frame(self.frame)
        frame.grid(row=0, column=1)
        frame.pack_propagate(0)
        return frame
    
    def form(self, label=[], entry=[], button=[], commands=[]):
        frame = tk.Frame(self.frame, width=700, height=500)
        frame.pack()
        frame.pack_propagate(0)
        for i in range(len(label)):
            ttk.Label(frame, text=label[i]).grid(row=i, column=0, padx=5, pady=5)
            ttk.Entry(frame, textvariable=entry[i]).grid(row=i, column=1, padx=5, pady=5)
        for i in range(len(button)):
            ttk.Button(frame, text=button[i], command=commands[i]).grid(row=(len(label)+i+1), column=1, padx=5, pady=5)
        return frame

#switch frame
def switchFrame(frame, *frames, include=None, exclude=None, arg=None):
    if frames:
        for i in frames:
            if i != exclude:
                i.destroy()
    else:
        for i in window.winfo_children():
            if i != exclude:
                i.destroy()
    if include != None:
        include()
    if arg != None:
        frame(arg)
    else:
        frame()

def switchContent(frame):
    try:
        for i in content.winfo_children():
            i.destroy()
    except AttributeError:
        pass
    frame(content)

def sidenav():
    sidenav = tk.Frame(window, width=450, height=900, bg="#2c3e50")
    sidenav.grid(row=0, column=0, sticky="nsew")
    sidenav.pack_propagate(0)

    display = Display("sidenav", sidenav)
    button = ["Dashboard", "Customer Management", "Account Management", "Transaction History", "Withdraw/Deposit", "Transfer", "Logout"]
    commands = [dashboard, customerManagement, accountManagement, transmanage, depwith, transfer, Admin.logout]
    display.button(button, direction="pack", commands=commands)


    # ttk.Button(sidenav, text="Dashboard", command=lambda: switchContent(dashboard)).pack(pady=10)
    # ttk.Button(sidenav, text="Customer Management", command=lambda: switchContent(customerManagement)).pack(pady=10)
    # ttk.Button(sidenav, text="Account Management", command=lambda: switchContent(accountManagement)).pack(pady=10)
    # ttk.Button(sidenav, text="Transaction History", command=lambda: switchContent(transmanage)).pack(pady=10)
    # ttk.Button(sidenav, text="Withdraw/Deposit", command=lambda: switchContent(report)).pack(pady=10)
    # ttk.Button(sidenav, text="Transfer", command=lambda: switchContent(report)).pack(pady=10)
    # ttk.Button(sidenav, text="Logout", command=lambda: Admin.logout(dashboard)).pack(pady=10)

def content():
    global content
    contentFrame = ttk.Frame(window, width=1800/4*3, height=900)
    contentFrame.grid(row=0, column=1, sticky="nsew")

    content = ttk.Frame(contentFrame, width=1800/4*3, height=900)
    content.pack()
    content.pack_propagate(0)
    

def home():
    home = Frames(window)
    homeframe = home.fixed()
    ttk.Label(homeframe, text="Welcome to Bank Management System", style="TLabel").pack(pady=10)
    ttk.Label(homeframe, text="Please login to continue", font=("Arial", 12)).pack(pady=10)
    ttk.Button(homeframe, text="Login", command=lambda: switchFrame(loginForm)).pack(pady=10)
    ttk.Button(homeframe, text="Register", command=lambda: switchFrame(registerForm)).pack(pady=10)

#login frame
def loginForm():
    login = Frames(window)
    loginframe = login.fixed()
    global username
    global password
    title = ttk.Label(loginframe, text="Login")
    title.configure(style="Title.TLabel")
    title.update()
    title.pack(pady=10)
    ttk.Label(loginframe, text="Username").pack(pady=10)
    username = ttk.Entry(loginframe)
    username.pack(pady=10)
    ttk.Label(loginframe, text="Password").pack(pady=10)
    password = ttk.Entry(loginframe, show="*")
    password.pack(pady=10)
    login_button = ttk.Button(loginframe, text="Login", command=lambda: Admin(username.get()).login(username.get(), password.get()))
    login_button.pack(pady=10)
    home_button = ttk.Button(loginframe, text="Home", command=lambda: switchFrame(home))
    home_button.pack(pady=10)


def registerForm():
    register = Frames(window)
    registerframe = register.fixed()
    global regusername
    global regpassword
    global regpassword2
    title = ttk.Label(registerframe, text="Register", style="Title")
    title.pack(pady=10)
    ttk.Label(registerframe, text="Username").pack(pady=10)
    regusername = ttk.Entry(registerframe)
    regusername.pack(pady=10)
    ttk.Label(registerframe, text="Password").pack(pady=10)
    regpassword = ttk.Entry(registerframe, show="*")
    regpassword.pack(pady=10)
    ttk.Label(registerframe, text="Confirm Password").pack(pady=10)
    regpassword2 = ttk.Entry(registerframe, show="*")
    regpassword2.pack(pady=10)
    register_button = ttk.Button(registerframe, text="Register", command=lambda: Admin.register(regusername.get(), regpassword.get(), regpassword2.get()))
    register_button.pack(pady=10)


def dashboard(frame):
    title = ttk.Label(frame, text="Dashboard")
    title.pack(pady=10)
    title.configure(font=("Arial", 18, "bold"))

    transaction = Frames(frame)
    transaction = transaction.fixed()
    display = Display("transaction", transaction)
    display.header(*columns("transaction"))
    # print(*Transaction.history(Transaction))
    display.content(Transaction.history(Transaction), rows=10)

def customerManagement(frame):
    global custmanage
    title = ttk.Label(frame, text="Customer Management")
    title.pack(pady=10)
    title.configure(font=("Arial", 18, "bold"))

    custmanage = Frames(frame)
    custmanage = custmanage.fixed()

    display = Display("customer", custmanage)
    button = ["Customer Information", "Add Customer", "Edit Customer", "Delete Customer"]
    commands = [custinfo, addcust, editcust, delcust]
    display.button(button, direction="vertical", commands=commands)

def custinfo(frame):
    title = ttk.Label(frame, text="Customer Information")
    title.pack(pady=10)
    title.configure(font=("Arial", 18, "bold"))

    custinfo = Frames(frame)
    custinfo = custinfo.fixed()

    custid = tk.StringVar()
    ttk.Label(custinfo, text="Customer ID").grid(row=0, column=0, padx=5, pady=5)
    ttk.Entry(custinfo, textvariable=custid).grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(custinfo, text="Search", command=lambda: Customer.custinfo(Customer, custid.get())).grid(row=0, column=2, padx=5, pady=5)

def addcust(frame):
    title = ttk.Label(frame, text="Add Customer")
    title.pack(pady=10)
    title.configure(font=("Arial", 18, "bold"))

    addcust = Frames(frame)
    addcust = addcust.fixed()

    custname = tk.StringVar()
    custdob = tk.StringVar()
    custphone = tk.StringVar()
    custemail = tk.StringVar()
    custaddress = tk.StringVar()
    custes = tk.StringVar()
    custai = tk.StringVar()
    custsoi = tk.StringVar()
    custit = tk.StringVar()
    custinum = tk.StringVar()

    ttk.Label(addcust, text="Name").grid(row=0, column=0, padx=5, pady=5)
    ttk.Entry(addcust, textvariable=custname).grid(row=0, column=1, padx=5, pady=5)
    ttk.Label(addcust, text="Date of Birth").grid(row=1, column=0, padx=5, pady=5)
    ttk.Entry(addcust, textvariable=custdob).grid(row=1, column=1, padx=5, pady=5)
    ttk.Label(addcust, text="Contact Number").grid(row=2, column=0, padx=5, pady=5)
    ttk.Entry(addcust, textvariable=custphone).grid(row=2, column=1, padx=5, pady=5)
    ttk.Label(addcust, text="Email Address").grid(row=3, column=0, padx=5, pady=5)
    ttk.Entry(addcust, textvariable=custemail).grid(row=3, column=1, padx=5, pady=5)
    ttk.Label(addcust, text="Address").grid(row=4, column=0, padx=5, pady=5)
    ttk.Entry(addcust, textvariable=custaddress).grid(row=4, column=1, padx=5, pady=5)
    ttk.Label(addcust, text="Employment Status").grid(row=5, column=0, padx=5, pady=5)
    ttk.Entry(addcust, textvariable=custes).grid(row=5, column=1, padx=5, pady=5)
    ttk.Label(addcust, text="Annual Income").grid(row=6, column=0, padx=5, pady=5)
    ttk.Entry(addcust, textvariable=custai).grid(row=6, column=1, padx=5, pady=5)
    ttk.Label(addcust, text="Source of Income").grid(row=7, column=0, padx=5, pady=5)
    ttk.Entry(addcust, textvariable=custsoi).grid(row=7, column=1, padx=5, pady=5)
    ttk.Label(addcust, text="Identification Type").grid(row=8, column=0, padx=5, pady=5)
    ttk.Entry(addcust, textvariable=custit).grid(row=8, column=1, padx=5, pady=5)
    ttk.Label(addcust, text="Identification Number").grid(row=9, column=0, padx=5, pady=5)
    ttk.Entry(addcust, textvariable=custinum).grid(row=9, column=1, padx=5, pady=5)
    ttk.Button(addcust, text="Add Customer", command=lambda: Customer.addcust(Customer, custname.get(), custdob.get(), custphone.get(), custemail.get(), custaddress.get(), custes.get(), custai.get(), custsoi.get(), custit.get(), custinum.get())).grid(row=10, column=1, padx=5, pady=5)

def editcust(frame):
    title = ttk.Label(frame, text="Edit Customer")
    title.pack(pady=10)
    title.configure(font=("Arial", 18, "bold"))

    editcust = Frames(frame)
    editcust = editcust.fixed()

    custid = tk.StringVar()
    custname = tk.StringVar()
    custaddress = tk.StringVar()
    custphone = tk.StringVar()
    custemail = tk.StringVar()

    customer = Customer.custinfo(Customer, custid.get())


    form = Frames(editcust)
    label = ["Customer ID", "Name", "Address", "Contact Number", "Email Address"]
    entry = [custid, custname, custaddress, custphone, custemail]
    button = ["Edit Customer"]
    commands = [lambda: customer.editcust(customer, custid.get(), custname.get(), custaddress.get(), custphone.get(), custemail.get())]
    form.form(label=label, entry=entry, button=button, commands=commands)
    form.pack(pady=10)

    # ttk.Label(editcust, text="Customer ID").grid(row=0, column=0, padx=5, pady=5)
    # ttk.Entry(editcust, textvariable=custid).grid(row=0, column=1, padx=5, pady=5)
    # ttk.Label(editcust, text="Name").grid(row=1, column=0, padx=5, pady=5)
    # ttk.Entry(editcust, textvariable=custname).grid(row=1, column=1, padx=5, pady=5)
    # ttk.Label(editcust, text="Address").grid(row=2, column=0, padx=5, pady=5)
    # ttk.Entry(editcust, textvariable=custaddress).grid(row=2, column=1, padx=5, pady=5)
    # ttk.Label(editcust, text="Contact Number").grid(row=3, column=0, padx=5, pady=5)
    # ttk.Entry(editcust, textvariable=custphone).grid(row=3, column=1, padx=5, pady=5)
    # ttk.Label(editcust, text="Email Address").grid(row=4, column=0, padx=5, pady=5)
    # ttk.Entry(editcust, textvariable=custemail).grid(row=4, column=1, padx=5, pady=5)
    # ttk.Button(editcust, text="Edit Customer", command=lambda: Customer.editcust(Customer, custid.get(), custname.get(), custaddress.get(), custphone.get(), custemail.get())).grid(row=5, column=1, padx=5, pady=5)

def delcust(frame):
    title = ttk.Label(frame, text="Delete Customer")
    title.pack(pady=10)
    title.configure(font=("Arial", 18, "bold"))

    delcust = Frames(frame)
    delcust = delcust.fixed()

    custid = tk.StringVar()
    ttk.Label(delcust, text="Customer ID").grid(row=0, column=0, padx=5, pady=5)
    ttk.Entry(delcust, textvariable=custid).grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(delcust, text="Delete Customer", command=lambda: Customer.delcust(Customer, custid.get())).grid(row=1, column=1, padx=5, pady=5)

def accountManagement(frame):
    title = ttk.Label(frame, text="Account Management")
    title.pack(pady=10)
    title.configure(font=("Arial", 18, "bold"))
    accmanage.update()

    accmanage = Frames(frame)
    accmanage = accmanage.fixed()

    display = Display("account", accmanage)
    button = ["Account Information", "Open Account", "Edit Account", "Delete Account"]
    commands = [accinfo, openacc, editacc, delacc]
    display.button(button, direction="vertical", commands=commands)

def accinfo(frame):
    title = ttk.Label(frame, text="Account Information")
    title.pack(pady=10)
    title.configure(font=("Arial", 18, "bold"))

    accinfo = Frames(frame)
    accinfo = accinfo.fixed()

    accnum = tk.StringVar()
    ttk.Label(accinfo, text="Account Number").grid(row=0, column=0, padx=5, pady=5)
    ttk.Entry(accinfo, textvariable=accnum).grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(accinfo, text="Search", command=lambda: Account.accinfo(Account, accnum.get())).grid(row=0, column=2, padx=5, pady=5)

def openacc(frame):
    title = ttk.Label(frame, text="Open Account")
    title.pack(pady=10)
    title.configure(font=("Arial", 18, "bold"))

    openacc = Frames(frame)
    openacc = openacc.fixed()

    custid = tk.StringVar()
    accname = tk.StringVar()
    acctype = tk.StringVar()
    accdate = tk.StringVar()
    accbal = tk.StringVar()
    accpref = tk.StringVar()



    ttk.Label(openacc, text="Customer ID").grid(row=0, column=0, padx=5, pady=5)
    ttk.Entry(openacc, textvariable=custid).grid(row=0, column=1, padx=5, pady=5)
    ttk.Label(openacc, text="Account Name").grid(row=1, column=0, padx=5, pady=5)
    ttk.Entry(openacc, textvariable=accname).grid(row=1, column=1, padx=5, pady=5)
    ttk.Label(openacc, text="Account Type").grid(row=2, column=0, padx=5, pady=5)
    ttk.Entry(openacc, textvariable=acctype).grid(row=2, column=1, padx=5, pady=5)
    ttk.Label(openacc, text="Account Date").grid(row=3, column=0, padx=5, pady=5)
    ttk.Entry(openacc, textvariable=accdate).grid(row=3, column=1, padx=5, pady=5)
    ttk.Label(openacc, text="Account Balance").grid(row=4, column=0, padx=5, pady=5)
    ttk.Entry(openacc, textvariable=accbal).grid(row=4, column=1, padx=5, pady=5)
    ttk.Label(openacc, text="Account Preference").grid(row=5, column=0, padx=5, pady=5)
    ttk.Entry(openacc, textvariable=accpref).grid(row=5, column=1, padx=5, pady=5)
    ttk.Button(openacc, text="Open Account", command=lambda: Account.openAccount(Account, custid.get(), accname.get(), acctype.get(), accdate.get(), accbal.get(), accpref.get())).grid(row=6, column=1, padx=5, pady=5)

def editacc(frame):
    title = ttk.Label(frame, text="Edit Account")
    title.pack(pady=10)
    title.configure(font=("Arial", 18, "bold"))

    editacc = Frames(frame)
    editacc = editacc.fixed()

    accnum = tk.StringVar()
    accname = tk.StringVar()
    acctype = tk.StringVar()
    accpref = tk.StringVar()

    ttk.Label(editacc, text="Account Number").grid(row=0, column=0, padx=5, pady=5)
    ttk.Entry(editacc, textvariable=accnum).grid(row=0, column=1, padx=5, pady=5)
    ttk.Label(editacc, text="Account Name").grid(row=1, column=0, padx=5, pady=5)
    ttk.Entry(editacc, textvariable=accname).grid(row=1, column=1, padx=5, pady=5)
    ttk.Label(editacc, text="Account Type").grid(row=2, column=0, padx=5, pady=5)
    ttk.Entry(editacc, textvariable=acctype).grid(row=2, column=1, padx=5, pady=5)
    ttk.Label(editacc, text="Account Preference").grid(row=3, column=0, padx=5, pady=5)
    ttk.Entry(editacc, textvariable=accpref).grid(row=3, column=1, padx=5, pady=5)
    ttk.Button(editacc, text="Edit Account", command=lambda: Account.editAccount(Account, accnum.get(), accname.get(), acctype.get(), accpref.get())).grid(row=4, column=1, padx=5, pady=5)

def transmanage(frame):
    title = ttk.Label(frame, text="Transaction History")
    title.pack(pady=10)
    title.configure(font=("Arial", 18, "bold"))

    transmanage = Frames(frame)
    transmanage = transmanage.fixed()

    top = tk.Frame(transmanage)
    top.pack()

    ttk.Label(top, text="Account Number").grid(row=0, column=0, padx=5, pady=5)
    accnum = tk.StringVar()
    ttk.Entry(top, textvariable=accnum).grid(row=0, column=1, padx=5, pady=5)
    ttk.Label(top, text="Transaction Type").grid(row=1, column=0, padx=5, pady=5)
    transtype = tk.StringVar()
    ttk.OptionMenu(top, transtype, "All", "Deposit", "Withdraw", "Transfer").grid(row=1, column=1, padx=5, pady=5)
    ttk.Label(top, text="Date").grid(row=2, column=0, padx=5, pady=5)
    fromdate = tk.StringVar()
    todate = tk.StringVar()
    DateEntry(top, textvariable=fromdate, date_pattern="mm/dd/yy").grid(row=2, column=1, padx=5, pady=5)
    DateEntry(top, textvariable=todate, date_pattern="mm/dd/yy").grid(row=3, column=1, padx=5, pady=5)
    ttk.Button(top, text="Search", command=lambda: search(accnum.get(), transtype.get(), fromdate.get(), todate.get())).grid(row=4, column=1, padx=5, pady=5)

    bottom = tk.Frame(transmanage)
    bottom.pack()

    display = Display("transaction", transmanage)
    display.fixed()

def depwith(frame):
    title = ttk.Label(frame, text="Withdrawals/Deposits")
    title.pack(pady=10)
    title.configure(font=("Arial", 18, "bold"))

    withdraw = Frames(frame)
    withdraw = withdraw.fixed()

    accnum = tk.StringVar()
    amount = tk.StringVar()
    desc = tk.StringVar()
    ttk.Label(withdraw, text="Account Number").grid(row=0, column=0, padx=5, pady=5)
    ttk.Entry(withdraw, textvariable=accnum).grid(row=0, column=1, padx=5, pady=5)
    ttk.Label(withdraw, text="Amount").grid(row=1, column=0, padx=5, pady=5)
    ttk.Entry(withdraw, textvariable=amount).grid(row=1, column=1, padx=5, pady=5)
    ttk.Label(withdraw, text="Description").grid(row=2, column=0, padx=5, pady=5)
    ttk.Entry(withdraw, textvariable=desc).grid(row=2, column=1, padx=5, pady=5)
    transaction = Transaction(accnum, amount, desc)
    ttk.Button(withdraw, text="Withdraw", command=lambda: transaction.withdraw(transaction, accnum.get(), amount.get(), desc.get())).grid(row=3, column=1, padx=5, pady=5)
    ttk.Button(withdraw, text="Deposit", command=lambda: transaction.deposit()).grid(row=4, column=1, padx=5, pady=5)

def transfer(frame):
    title = ttk.Label(frame, text="Transfer")
    title.pack(pady=10)
    title.configure(font=("Arial", 18, "bold"))

    transfer = Frames(frame)
    transfer = transfer.fixed()

    accnum = tk.StringVar()
    amount = tk.StringVar()
    desc = tk.StringVar()

    # from
    ttk.Label(transfer, text="From Account Number").grid(row=0, column=0, padx=5, pady=5)
    ttk.Entry(transfer, textvariable=accnum).grid(row=0, column=1, padx=5, pady=5)

    # to
    ttk.Label(transfer, text="To Account Number").grid(row=1, column=0, padx=5, pady=5)
    ttk.Entry(transfer, textvariable=accnum).grid(row=1, column=1, padx=5, pady=5)

    # amount
    ttk.Label(transfer, text="Amount").grid(row=2, column=0, padx=5, pady=5)
    ttk.Entry(transfer, textvariable=amount).grid(row=2, column=1, padx=5, pady=5)

    # submit
    transaction = Transaction(accnum, amount, desc)
    ttk.Button(transfer, text="Transfer", command=lambda: transaction.transfer()).grid(row=3, column=1, padx=5, pady=5)

if __name__ == "__main__":
    loginForm()
    sv_ttk.set_theme("dark")

# Configure the columns to resize with the window
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=4)

window.mainloop()