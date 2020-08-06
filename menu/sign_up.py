from tkinter import *
from tkinter import messagebox
from utilities.database import Database
from utilities.utilities import Util


class SignUpPage(Toplevel, Database, Util):
    def __init__(self):
        Toplevel.__init__(self)
        Database.__init__(self)
        Util.__init__(self, self)
        self.title = "Sign Up"
        self.width = 600
        self.height = 800
        self.cursor.execute("SELECT employee_id, first_name FROM employees where employee_id not in (SELECT employee_id from users);")
        self.emp_ids = ["{}, {}".format(i[0], i[1]) for i in self.cursor.fetchall()]
        self.signup_u = Label(self, text="Username:")
        self.signup_u.grid(row=self.max_row + 1, column=0)
        self.signup_utext = StringVar()
        self.signup_uedit = Entry(self, textvariable=self.signup_utext)
        self.signup_uedit.grid(row=self.max_row, column=1)
        # self.signup_p = Label(self, text="Password:")
        # self.signup_p.grid(row=1, column=0)
        # self.signup_ptext = StringVar()
        # self.signup_pedit = Entry(self, textvariable=self.signup_ptext, show="*")
        # self.signup_pedit.grid(row=1, column=1)
        # self.signup_confirm_label = Label(self, text="Confirm password:")
        # self.signup_confirm_label.grid(row=2, column=0)
        # self.signup_confirm_text = StringVar()
        # self.signup_confirm_edit = Entry(self, textvariable=self.signup_confirm_text, show="*")
        # self.signup_confirm_edit.grid(row=2, column=1)
        self.signup_emp_var = StringVar()
        self.signup_emp_var.set(self.emp_ids[-1])
        self.signup_emp_lab = Label(self, text="Employee ID:")
        self.signup_emp_lab.grid(row=self.max_row + 1, column=0)
        self.signup_emp_opt = OptionMenu(self, self.signup_emp_var, *self.emp_ids)
        self.signup_emp_opt.grid(row=self.max_row, column=1, sticky="ew")
        self.signup_al_lab = Label(self, text="Privilege")
        self.signup_altext = StringVar()
        self.signup_altext.set("Logistics")
        self.signup_al_drop = OptionMenu(self, self.signup_altext,
                                         "Human Resource", "Finance", "Logistics")
        self.signup_al_lab.grid(row=self.max_row + 1, column=0)
        self.signup_al_drop.grid(row=self.max_row, column=1, sticky="ew")
        self.signup_btn = Button(self, text="Sign up", command=self.check_info)
        self.signup_btn.grid(row=self.max_row + 1, column=0)

    def check_info(self) -> None:
        username = self.check_username()
        passw = self.check_pass()
        priv = self.signup_altext.get().lower()
        emp_id = self.signup_emp_var.get()
        if username is not None and passw is not None:
            sql_cmd = """
            INSERT INTO users (user_id, employee_id, username, password, privilege) values (null, '{}', '{}', '{}', '{}')"""\
                .format(emp_id, username, passw, priv)
            self.cursor.execute(sql_cmd)
            self.mydb.commit()
            messagebox.showinfo(
                "INFO",
                "An account has been created successfully!\n"
                "Account's password is: {}".format(self.check_pass())
            )

    def check_username(self) -> str:
        usernam = self.signup_utext.get()
        sql_cmd = "SELECT * from users where username = '{}'".format(usernam)
        self.cursor.execute(sql_cmd)
        results = self.cursor.fetchall()
        if len(results) == 0:
            return usernam
        else:
            messagebox.showwarning(
                "WARNING",
                "Your username has been chosen, please choose another one."
            )

    def check_pass(self) -> str or None:
        # spec_cha = "!@#$%^&*()_+{}|'/?.,<>[];=-`"
        # passw = self.signup_ptext.get()
        # conf_pass = self.signup_confirm_text.get()
        # if passw != conf_pass:
        #     messagebox.showwarning(
        #         "Warning",
        #         "Your passwords do not match, please try again")
        #     self.signup_ptext.set("")
        #     self.signup_confirm_text.set("")
        #     return
        #
        # if len(passw) <= 8:
        #     messagebox.showwarning(
        #         "Warning",
        #         "Your password must be longer than 8 characters, "
        #         "it must not include no special characters and include at least one number")
        #     self.signup_ptext.set("")
        #     self.signup_confirm_text.set("")
        #     return
        #
        # for cha in passw:
        #     if cha in spec_cha:
        #         messagebox.showwarning(
        #             "Warning",
        #             "Your password must not include special characters: !@#$%^&*()_+{}|'/?.,<>[];=-`")
        #         self.signup_ptext.set("")
        #         self.signup_confirm_text.set("")
        #         return
        #
        # if not any(
        #         map(lambda x: x.isdigit(), passw)
        # ):
        #     messagebox.showwarning(
        #         "Warning",
        #         "Your password must have at least one number")
        #     self.signup_ptext.set("")
        #     self.signup_confirm_text.set("")
        #     return

        return "1234"


if __name__ == '__main__':
    SignUpPage().mainloop()
