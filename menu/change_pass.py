from tkinter import *
from tkinter import messagebox
from utilities.database import Database
from utilities.utilities import Util
from configparser import ConfigParser
import os
from cryptography.fernet import Fernet


class ChangepassPage(Toplevel, Database, Util):
    def __init__(self):
        Toplevel.__init__(self)
        Database.__init__(self)
        Util.__init__(self, self)
        self.title = "Myacc"
        self.width = 600
        self.height = 800
        self.currentuser = ""
        self.currentpass = ""
        with open("config.txt", "r") as f:
            username, passw = f.readlines()
        key = 'pVK5w74j3iGPEKZCEFXv-cE5_uMqu4KK0P2kg7C2PE0='
        self.fernet = Fernet(key)
        username = self.fernet.decrypt(username.encode())
        passw = self.fernet.decrypt(passw.encode())
        username = username.decode()
        passw = passw.decode()
        self.currentuser = username
        self.currentpass = passw

        self.user = Label(self, text="Username:")
        self.user.grid(row=self.max_row, column=0)
        self.usertext = StringVar()
        self.usertext.set(self.currentuser)
        self.userdisplay = Entry(self, textvariable=self.usertext)
        self.userdisplay.grid(row=self.max_row, column=1)
        self.userdisplay.configure(state="readonly")

        self.password = Label(self, text="Current password:")
        self.password.grid(row=self.max_row+1, column=0)
        self.passwordentry = Entry(self,show="*")
        self.passwordentry.grid(row=self.max_row, column=1)

        self.newpassword = Label(self, text="New password:")
        self.newpassword.grid(row=self.max_row+1, column=0)
        self.newpassentry = Entry(self,show="*")
        self.newpassentry.grid(row=self.max_row, column=1)

        self.confirmpassword = Label(self, text="Confirm password:")
        self.confirmpassword.grid(row=self.max_row+1, column=0)
        self.confirmpassentry = Entry(self,show="*")
        self.confirmpassentry.grid(row=self.max_row, column=1)

        self.changepass = Button(self, text="Change password", command=self.change_pass)
        self.changepass.grid(row=self.max_row+1, column=1)
        
    def change_pass(self) -> None:
        self.passwordtyped = str(self.passwordentry.get())
        self.newpass = self.newpassentry.get()
        self.confirmpass = self.confirmpassentry.get()
        self.passwordtyped.strip()
        self.currentpass.strip()
        self.currentpass = os.linesep.join([s for s in self.currentpass.splitlines() if s])
        self.currentuser.strip()
        self.currentuser = os.linesep.join([s for s in self.currentuser.splitlines() if s])

        if len(self.passwordtyped) * len(self.newpass) * len(self.confirmpass) == 0:
            messagebox.showwarning("WARNING", "No empty password allowed!")
            return
        if not self.passwordtyped == self.currentpass:
            messagebox.showwarning("WARNING", "The current password you typed is wrong!")
            return
        elif not self.newpass == self.confirmpass:
            messagebox.showwarning("WARNING", "The new password you typed does not match!")
            return
        else:
            sql_command = "UPDATE users SET pass_word = '{pw}' WHERE username = '{user}'".format(pw = self.newpass, user=self.currentuser)
            sql_command2 = "UPDATE users SET pass_word = 'wick' WHERE username = 'john'"
            self.cursor.execute(sql_command)
            self.mydb.commit()
            messagebox.showwarning("WARNING", "The password has been changed!")
            return
        

if __name__ == '__main__':
    Changepasspage().mainloop()
