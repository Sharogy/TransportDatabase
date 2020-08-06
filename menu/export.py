from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from utilities.utilities import Util
from typing import List, Tuple
import pandas as pd
import os
from utilities.database import Database


class Export(Toplevel, Util, Database):
    def __init__(self, tables: Tuple):
        Toplevel.__init__(self)
        Util.__init__(self, self)
        Database.__init__(self)
        self.tables = tables
        self.current_path = os.getcwd() + "\\exports"
        self.first_tab_lab = Label(self, text="Table: ", width=10, borderwidth=2)
        self.first_tab_lab.grid(row=self.max_row + 1, column=0)
        self.first_tab_var = StringVar()
        self.first_tab_var.set(tables[0])
        self.first_tab_opt = OptionMenu(self, self.first_tab_var, *tables)
        self.first_tab_opt.grid(row=self.max_row, column=1, sticky="ew")
        # self.other_tab_button = Button(self, text="More table", width=10, borderwidth=2,
        #                                command=lambda: self.create_more_y(tables, Widget.OPTION, "Table: "))
        # self.other_tab_button.grid(row=self.max_row + 1, column=0)
        self.file_loc_button = Button(self, text="Export as", width=10, borderwidth=2, command=self.export_as)
        self.file_loc_button.grid(row=self.max_row + 1, column=0)
        self.file_loc_var = StringVar()
        self.file_loc_var.set(self.current_path)
        self.file_loc_ent = Entry(self, textvariable=self.file_loc_var, width=20, borderwidth=2)
        self.file_loc_ent.grid(row=self.max_row, column=1)
        self.export_btn = Button(self, text="Export", width=10, borderwidth=2)
        self.export_btn.grid(row=self.max_row + 1, column=0)
        # self.special_wdgs = [self.formats_lab, self.export_btn]

    def export_as(self):
        filename = filedialog.asksaveasfilename(initialdir=self.current_path,
                                                title="Export file",
                                                defaultextension=".xlsx",
                                                filetypes=(("excel files", "*.xlxs"),
                                                           ("csv files", "*.csv"),
                                                           ("json files", "*.json")))
        self.cursor.execute("SELECT * FROM {};".format(self.first_tab_var.get()))
        rows = self.cursor.fetchall()
        columns = self.cursor.column_names
        df = pd.DataFrame(rows, columns=columns)
        df.set_index(columns[0], inplace=True)
        if filename.endswith(".xlsx"):
            df.to_excel(filename, sheet_name=self.first_tab_var.get())
        elif filename.endswith(".csv"):
            df.to_csv(filename)
        else:
            df.to_json(filename)
        messagebox.showinfo(
            "INFO",
            "Table {} exported successfully!".format(self.first_tab_var.get().upper())
        )


if __name__ == '__main__':
    Export(("assigns", "customers")).mainloop()
