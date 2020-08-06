from tkinter import *
from tkinter import messagebox
from utilities.database import Database
from utilities.utilities import Util


class NewTablePage(Toplevel, Util, Database):
    def __init__(self):
        Toplevel.__init__(self)
        Util.__init__(self, self)
        Database.__init__(self)
        self.types = ["INT", "DOUBLE", "DATE", "VARCHAR"]
        self.title = "New table"
        self.extra_col = []
        self.table_name_var = StringVar()
        self.table_name_lab = Label(self, text="Table name:")
        self.table_name_entry = Entry(self, textvariable=self.table_name_var)
        self.table_name_lab.grid(row=self.max_row + 1, column=0)
        self.table_name_entry.grid(row=self.max_row, column=1)
        self.first_col_var = StringVar()
        self.first_col_lab = Label(self, text="Column name:")
        self.first_col_entry = Entry(self, textvariable=self.first_col_var)
        self.first_col_lab.grid(row=self.max_row + 1, column=0)
        self.first_col_entry.grid(row=self.max_row, column=1)
        self.first_col_opt_var = StringVar()
        self.first_col_opt_var.set("Types")
        self.first_col_types = OptionMenu(self, self.first_col_opt_var, *self.types)
        self.first_col_types.grid(row=self.max_row, column=2, sticky="ew")
        self.xtra_col_btn = Button(self, text="More column", command=self.create_more_column)
        self.xtra_col_btn.grid(row=self.max_row + 1, column=0)
        self.create_table = Button(self, text="Create table", command=self.create_new_table)
        self.create_table.grid(row=self.max_row + 1, column=0)
        self.special_wdgs = [self.xtra_col_btn, self.create_table]

    @Util.grid_regrid
    def create_more_column(self):
        new_label = Label(self, text="Column name:")
        new_label.grid(row=self.max_row + 1, column=0)
        new_col_var = StringVar()
        new_col_entry = Entry(self, textvariable=new_col_var)
        new_col_entry.grid(row=self.max_row, column=1)
        new_col_opt_var = StringVar()
        new_col_opt_var.set("Types")
        new_col_opt = OptionMenu(self, new_col_opt_var, *self.types)
        new_col_opt.grid(row=self.max_row, column=2, sticky="ew")
        delete_btn = Button(self, text="Delete", command=lambda: self.delete(delete_btn))
        delete_btn.grid(row=self.max_row, column=3)
        self.extra_col.append({
            "label": new_label,
            "entry": new_col_entry,
            "name var": new_col_var,
            "delete": delete_btn,
            "opt": new_col_opt,
            "opt var": new_col_opt_var
        })

    def delete(self, button: Button):
        for col in self.extra_col:
            if col["delete"] is button:
                for value in col.values():
                    try:
                        value.destroy()
                    except AttributeError:
                        continue
                self.extra_col.remove(col)

    def generate_sql(self) -> str:
        self.cursor.execute("SHOW tables;")
        all_tab_names = [table[0] for table in self.cursor.fetchall()]
        col_lst = []
        table_name = self.table_name_var.get()
        if table_name in all_tab_names:
            messagebox.showerror(
                "ERROR",
                "Table name already existed.",
                parent=self
            )
            return ""
        table_id = self.table_name_var.get() + "ID"
        result = "CREATE TABLE IF NOT EXISTS {table_name} (\n" \
                 "{tableID} INT AUTO_INCREMENT," \
                 "{first_col} {col_type} NOT NULL," \
            .format(table_name=table_name,
                    tableID=table_id,
                    first_col=self.first_col_var.get(),
                    col_type=self.first_col_opt_var.get())
        col_lst.append(self.first_col_var.get())
        for col in self.extra_col:
            result += """{col_name} {col_type} NOT NULL, \n
            """.format(col_name=col["name var"].get(),
                       col_type=col["opt var"].get())
            col_lst.append(col["name var"].get())
        result += "\n PRIMARY KEY ({tableID})) ENGINE=INNODB;".format(tableID=table_id)
        if len(set(col_lst)) < len(self.extra_col) + 1:
            messagebox.showerror(
                "ERROR",
                "Duplicate or missing column detected!",
                parent=self
            )
            return ""
        return result

    def create_new_table(self):
        sql = self.generate_sql()
        if sql == "":
            return
        self.cursor.execute(sql)
        self.cursor.execute("commit;")
        messagebox.showinfo(
            "INFO",
            "Table created successfully!",
            parent=self
        )


if __name__ == '__main__':
    NewTablePage().mainloop()
