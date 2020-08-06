import os
from tkinter import *
from tkinter import messagebox
from typing import Tuple
from configparser import ConfigParser
from main import Main
from database import Database
from cryptography.fernet import Fernet
from utilities.sdebugger import Decorators


@Decorators.timecheck
class LoginPage(Tk, Database):

    def __init__(self):
        # initialise tkinter
        Tk.__init__(self)
        Database.__init__(self)
        # initial parameters (name, width, height etc.)
        self.title("ITM")
        self.acc_level = ""
        # self.config_parser = ConfigParser()
        # self.config_parser.read("setting/config.ini")
        # self.config_login = self.config_parser["LOGIN"]
        self.background_image = PhotoImage(file='assets/bg.png')
        self.width = 550
        self.height = 350
        self.geometry('{}x{}'.format(self.width, self.height))
        self.canvas = Canvas(self, width=self.width, height=self.height)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_image)

        # frame section
        self.box1 = Frame(self.canvas, borderwidth=0, relief="solid")
        self.box2_1 = Frame(self.canvas, borderwidth=1, relief="solid")
        self.box2_2 = Frame(self.canvas, borderwidth=1, relief="solid")
        self.box3 = Frame(self.canvas, borderwidth=1, relief="solid")

        self.pleaselogin = PhotoImage(file='assets/pleaselogin.png')
        self.pleaselogin_label = Label(self.box1, image=self.pleaselogin)

        self.username_label = Label(self.box2_1,
                                    text="Username:",
                                    font=("helvetica",
                                          12))
        self.username_txt = StringVar()
        self.username_edit = Entry(self.box2_1, textvariable=self.username_txt, bg="white", width=20)
        self.password_label = Label(self.box2_2,
                                    text="Password:",
                                    font=("helvetica",
                                          12))
        self.password_txt = StringVar()
        self.password_edit = Entry(self.box2_2, textvariable=self.password_txt, bg="white", width=20, show="*")
        self.login_btn = Button(self.box3, text="LOG IN", width=25, command=self.log_in)
        self.check_var = IntVar()
        self.rmb_btn = Checkbutton(self.box3, text="Remember me", width=15, var=self.check_var)
        username, passw = self.check_config()

        key = 'pVK5w74j3iGPEKZCEFXv-cE5_uMqu4KK0P2kg7C2PE0='
        self.fernet = Fernet(key)
        username = self.fernet.decrypt(username.encode())
        passw = self.fernet.decrypt(passw.encode())
        #print(username, passw)
        username = username.decode()
        passw = passw.decode()
        #print(username, passw)
        self.username_txt.set(username)
        self.password_txt.set(passw)
        #print(self.username_txt.get())
        #print(self.password_txt.get())

        self.box1.pack(pady=(50, 0))
        self.box2_1.pack(pady=(25, 25))
        self.box2_2.pack()
        self.box3.pack(pady=(25, 25))
        self.pleaselogin_label.pack()
        self.username_label.pack(side=LEFT)
        self.username_edit.pack(side=LEFT)
        self.password_label.pack(side=LEFT)
        self.password_edit.pack(side=LEFT)
        self.login_btn.pack()
        self.rmb_btn.pack()
        self.resizable(False, False)

    def check_config(self) -> Tuple[str, str]:
        if os.path.exists("config.txt"):
            with open("config.txt", "r") as f:
                username, passw = f.readlines()
                self.check_var.set(1)
        else:
            username, passw = "", ""
        return username.strip(), passw.strip()

    def run_gif(self):
        loading = Label(self.canvas, text="Loading...")
        loading.pack(padx=4, pady=4)
        self.config(cursor="wait")
        self.update()

    def log_in(self) -> None:
        username = self.username_txt.get()
        passw = self.password_txt.get()
        if len(username) * len(passw) == 0:
            messagebox.showwarning(
                "WARNING",
                "Your username or password is empty!")
            self.password_txt.set("")
            return
            # result = [dic for dic in admin_accounts if dic["username"] == username]
        sql_command = "SELECT pass_word, privilege from users where username = '{}'".format(username)
        self.cursor.execute(sql_command)
        result = self.cursor.fetchall()
        if len(result) == 0:
            messagebox.showwarning(
                "WARNING",
                "Your username doesnt exist!"
            )
            return
        else:
            pw, acc_level = result[0][0], result[0][1]
            self.acc_level = acc_level
        if pw == passw:
            if self.check_var.get() == 1:
                with open("config.txt", "w+") as f:
                    encrypteduser = self.username_txt.get()
                    encryptedpass = self.password_txt.get()
                    encrypteduser = self.fernet.encrypt(encrypteduser.encode())
                    encryptedpass = self.fernet.encrypt(encryptedpass.encode())
                    f.write(encrypteduser.decode())
                    f.write('\n')
                    f.write(encryptedpass.decode())
            else:
                if os.path.exists("config.txt"):
                    os.remove("config.txt")
            self.run_gif()
            Main(self, self.acc_level).mainloop()
        else:
            messagebox.showwarning(
                "WARNING",
                "Your password is incorrect!"
            )
            self.password_txt.set("")
            return


if __name__ == '__main__':
    LoginPage().mainloop()
