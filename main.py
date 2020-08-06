from tkinter import *
from tkinter import ttk
from frame_tab import FrameTab
from menu.new_table import NewTablePage
from menu.sign_up import SignUpPage
from menu.change_pass import ChangepassPage
from menu.export import Export
from utilities.sdebugger import Decorators
from setting.setting import Setting
from configparser import ConfigParser
from utilities.database import Database
from special_frames.delivery import Delivery
from special_frames.employees import Employee
from tkinter import messagebox


@Decorators.timecheck
class Main(Toplevel, Database):
    def __init__(self, parent: Tk, access_level: str):
        Toplevel.__init__(self)
        Database.__init__(self)
        self.config_parser = ConfigParser()
        self.parent = parent
        self.config_parser.read("setting/config.ini")
        self.config_frame = self.config_parser["FRAMETAB"]
        self.height = int(self.config_frame["HEIGHT"])
        self.width = int(self.config_frame["WIDTH"])
        # self.geometry("{}x{}".format(self.width, self.height)) 
        self.cursor = self.mydb.cursor()
        self.cursor.execute("SHOW tables;")        
        self.access_level = access_level
        self.exclusions = ("")
        if self.access_level == "manager":
            self.exclusions=("")
        elif self.access_level =="human resource":
            self.exclusions=("assignment","customers","delivery","orders","trucks")
        elif self.access_level =="finance":
            self.exclusions=("drivers","employees","office_emp","users")
        elif self.access_level =="logistics":
            self.exclusions=("customers","employees","office_emp","salaries","users")   
        tabs = tuple([table[0] for table in self.cursor.fetchall() if table[0] not in self.exclusions])
        self.menubar = Menu(self)
        self.new_menu = Menu(self.menubar, tearoff=0)
        self.file_menu = Menu(self.menubar, tearoff=0)
        self.acc_menu = Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Export", command=lambda: Export(tabs).mainloop())
        #self.file_menu.add_command(label="Import")
        self.file_menu.add_command(label="Settings", command=lambda: Setting().mainloop()) 
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.acc_menu.add_command(label="Change password", command=lambda: ChangepassPage().mainloop())
        self.acc_menu.add_command(label="Log Out", command=lambda: self.Logout())
        self.menubar.add_cascade(label="Myacc", menu=self.acc_menu)
        
        if self.access_level == "manager":
            self.new_menu.add_command(label="Account", command=lambda: SignUpPage().mainloop())
            #how does someone delete a table then???
            self.new_menu.add_command(label="Table", command=lambda: NewTablePage().mainloop())
            self.menubar.add_cascade(label="New", menu=self.new_menu)
        elif self.access_level == "human resource":
            self.new_menu.add_command(label="Account", command=lambda: SignUpPage().mainloop())
            self.menubar.add_cascade(label="New", menu=self.new_menu)
        self.config(menu=self.menubar)
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill="both")
        for name in tabs:
            if name == "delivery":
                frame = Delivery(notebook, name, self.access_level)
            elif name == "employees":
                frame = Employee(notebook, name, self.access_level)
            else:
                frame = FrameTab(notebook, name, self.access_level)
            notebook.add(frame, text=name)
        parent.withdraw()
        notebook.enable_traversal()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.cursor.close()

    def Logout(self):
        if messagebox.askokcancel("Quit", "Do you want to logout?", parent=self):
            from login_page import LoginPage 
            self.parent.destroy()
            LoginPage().mainloop()

    def on_closing(self):
        if messagebox.askokcancel("Quit",
                                  "Do you want to quit?",
                                  parent=self):
            self.parent.destroy()
