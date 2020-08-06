from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
from typing import List, Tuple
import mysql.connector
from configparser import ConfigParser
from features.statistic import Stat
from utilities.sdebugger import Decorators
from utilities.utilities import Util
from utilities.database import Database
from cryptography.fernet import Fernet


@Decorators.timecheck
class FrameTab(Frame, Util, Database):
    def __init__(self, parent: Tk, name: str, access_level: str):
        Frame.__init__(self, parent)
        try:
            Database.__init__(self, name)
        except mysql.connector.errors.ProgrammingError:
            messagebox.showerror("ERROR",
                                 "Too many connections to database!")
            self.destroy()
            parent.destroy()
        self.config_parser = ConfigParser()
        self.config_parser.read("setting/config.ini")
        self.config_frame = self.config_parser["FRAMETAB"]
        self.access_lvl = access_level
        self.cursor.execute("SELECT * from {};".format(name))
        #print("cursorexecute", self.cursor.execute)
        rows = self.cursor.fetchall()
        #print("rows",rows)           
        self.col_names = self.cursor.column_names
        self.name = name
        self.latest_action = ""
        self.added_data = None
        self.editted_data = None
        self.deleted_data = None
        self.reverse_add = []
        self.reverse_edit = []
        self.reverse_delete = []
        self.commit_actions = []
        self.label_dic = {}
        self.prime_var_dic = {}
        self.pressed = False
        self.prime_ind = self.prime_index()
        self.height = int(self.config_frame["HEIGHT"])
        self.width = int(self.config_frame["WIDTH"])
        
        #self.resizable(0, 0)

        self.rows = rows
        self.main_id = self.get_max_id()
        self.foreign_keys_opts = self.all_foreign_keys_selection()

        self.base_frame = Frame(self, borderwidth=1,
                                height=self.height,
                                width=self.width,
                                relief="solid")
        self.dbs_frame = Frame(self.base_frame,
                               bg=self.config_frame["DATAFRAME_COLOR"],
                               borderwidth=5,
                               height=self.height,
                               width=self.width / 4 * 3)
        self.btn_frame = Frame(self.base_frame,
                               bg=self.config_frame["BUTTONFRAME_COLOR"],
                               borderwidth=5,
                               height=self.height,
                               width=self.width / 4)
        self.foreign_dict = self.foreign_keys()
        self.prime_keys = self.primary_keys(True)
        # frame packing
        self.base_frame.pack(expand=True, fill="both")
        self.dbs_frame.pack(side="left", fill="both", expand=True)
        self.btn_frame.pack(side="left", expand=True, fill="both")
        self.btn_frame_1 = Frame(self.btn_frame, borderwidth=1, width=self.width / 4)
        self.btn_frame_1_1 = Frame(self.btn_frame_1, borderwidth=1, width=self.width / 8)
        self.btn_frame_1_2 = Frame(self.btn_frame_1, borderwidth=1, width=self.width / 8)
        self.btn_frame_2 = Frame(self.btn_frame, borderwidth=3, width=self.width / 4, relief="ridge")
        Util.__init__(self, self.btn_frame_2)
        # self.btn_frame_3 = Frame(self.btn_frame, borderwidth=1, width=self.width/8)
        self.btn_frame_3_1 = Frame(self.btn_frame, borderwidth=1, width=self.width / 8)
        self.btn_frame_3_2 = Frame(self.btn_frame, borderwidth=1, width=self.width / 8)
        self.btn_frame_3_3 = Frame(self.btn_frame, borderwidth=1, width=self.width / 8)
        self.dbs_frame.pack_propagate(0)
        self.btn_frame.pack_propagate(0)

        self.tree_dbs = ttk.Treeview(self.dbs_frame)
        self.vertical_scroll = ttk.Scrollbar(self.dbs_frame, orient="vertical", command=self.tree_dbs.yview)
        self.horizontal_scroll = ttk.Scrollbar(self.dbs_frame, orient="horizontal", command=self.tree_dbs.xview)

        self.tree_dbs["columns"] = self.col_names
        self.exclusionlist=["pass_word"]
        self.displaycolumns=[]
        for col in self.tree_dbs["columns"]:
            if not "%s"%col in self.exclusionlist:
                self.displaycolumns.append(col)
        self.tree_dbs["displaycolumns"]=self.displaycolumns
        
        self.tree_dbs["show"] = "headings"
        self.tree_dbs.bind("<Double-1>", self.edit)
        self.tree_dbs.bind("<Button-1>", self.get_selected_row_data)
        for col in self.col_names:
            self.tree_dbs.heading(col, text=col)
        index = iid = 0
        for row in rows:
            self.tree_dbs.insert("", index, iid, values=row)
            index = iid = index + 1
        self.tree_id = index

        # browser packing
        self.vertical_scroll.pack(side="right", fill="y")
        self.horizontal_scroll.pack(side="bottom", fill="x")
        self.tree_dbs.pack(expand=True, fill="both")
        self.tree_dbs.pack_propagate(0)

        self.modify_btn = Button(self.btn_frame_1_1, text="Modify data", width=12, bg="white", command=self.modify_data,
                                 borderwidth=2)
        self.stat_btn = Button(self.btn_frame_1_2, text="Graph mode", width=12,
                               command=lambda: Stat(table=self.return_table(),
                                                    table_name=self.name, col_names=self.col_names).mainloop(),
                               borderwidth=2)

        self.add_btn = Button(self.btn_frame_3_1, text="Add data", width=12, bg="white", command=self.add_data,
                              borderwidth=2)
        self.refr_btn = Button(self.btn_frame_3_1, text="Refresh", width=12, command=self.refresh, borderwidth=2)

        self.edit_btn = Button(self.btn_frame_3_1, text="Edit data", width=12, bg="white", command=self.edit_data,
                               borderwidth=2)
        self.delete_btn = Button(self.btn_frame_3_1, text="Delete data", width=12, bg="white", command=self.delete_data,
                                 borderwidth=2)

        self.commit_btn = Button(self.btn_frame_3_2, text="Commit", width=12, command=self.commit_to_dbs, borderwidth=2)
        self.rollback_btn = Button(self.btn_frame_3_2, text="Rollback", width=12, command=self.rollback, borderwidth=2)

        self.btn_frame_1.pack(pady=(25, 25))
        self.btn_frame_2.pack()
        # self.btn_frame_3.pack(pady=(25,25))
        self.btn_frame_1_1.pack(side=LEFT)
        self.btn_frame_1_2.pack(side=LEFT)
        self.btn_frame_3_1.pack(pady=(25, 5))
        self.btn_frame_3_2.pack()
        self.auto_create_widgets()

        self.modify_btn.pack()
        self.modify_btn.config(relief=RAISED)
        self.stat_btn.pack()

        self.refr_btn.pack(side=RIGHT)
        self.add_btn.pack(side=RIGHT)

        # self.delete_btn.grid(row=0, column=2)
        self.commit_btn.pack(side=LEFT)

        self.hide_btn()

    def encrypt(self, message: bytes, key: bytes) -> bytes:
        return Fernet(key).encrypt(message)

    def decrypt(self, token: bytes, key: bytes) -> bytes:
        return Fernet(key).decrypt(token)

    def auto_create_widgets(self):
        count = 0
        for col in self.col_names:
            label = Label(self.btn_frame_2, text=col, width=12, borderwidth=1)
            label.grid(row=self.max_row + 1, column=0, padx=3, pady=3)
            str_var = StringVar()
            if "date" in col:
                day_var, month_var, year_var = StringVar(), StringVar(), StringVar()
                day_var.set("Day")
                month_var.set("Month")
                year_var.set("Year")
                day_opt = ttk.Combobox(self.btn_frame_2, textvariable=day_var, values=[i for i in range(32)],width=6)
                month_opt = ttk.Combobox(self.btn_frame_2, textvariable=month_var, values=[i for i in range(1, 13)],width=6)
                year_opt = ttk.Combobox(self.btn_frame_2, textvariable=year_var, values=[i for i in range(1900, 2301)],width=6)
                year_opt.grid(row=self.max_row, column=1)
                month_opt.grid(row=self.max_row, column=2)
                day_opt.grid(row=self.max_row, column=3)
                self.label_dic[col] = {"day": day_var,
                                       "month": month_var,
                                       "year": year_var}

            elif col in self.foreign_dict.keys() and col not in self.prime_keys:
                all_opts = self.foreign_keys_opts[col]
                options = OptionMenu(self.btn_frame_2, str_var, *all_opts )
                self.label_dic[col] = str_var
                options.grid(row=self.max_row, column=1, sticky="ew", columnspan=3)
            elif col not in self.prime_keys:
                entry = Entry(self.btn_frame_2, textvariable=str_var, borderwidth=1)
                entry.grid(row=self.max_row, column=1, columnspan=3, sticky="ew")
                self.label_dic[col] = str_var
            else:
                self.id_change(1)
                str_var.set(self.main_id[count])
                entry = Entry(self.btn_frame_2, textvariable=str_var, borderwidth=1)
                entry.grid(row=self.max_row, column=1,  columnspan=3)
                self.label_dic[col] = str_var
                self.prime_var_dic[col] = (str_var, count)
                entry.configure(state="readonly")
                count += 1

    def return_table(self) -> List[Tuple]:
        return [tuple(self.tree_dbs.item(child)["values"]) for child in self.tree_dbs.get_children()]

    def hide_btn(self):
        allowed_tables = {
            "human resource": ["employees", "office_emp","drivers","users"],
            "finance": ["salaries","customers","orders"],
            "logistics": ["assignment", "delivery", "trucks", "offices"],
        }
        if self.access_lvl == "manager":
            pass
        elif self.name not in allowed_tables[self.access_lvl]:
            self.btn_frame.pack_forget()
       #else:
            #self.cursor.execute("SELECT * from {};".format(name))
            #rows = self.cursor.fetchall()
            #self.col_names = self.cursor.column_names
            #self.tree_dbs["columns"] = self.col_names
            #self.tree_dbs["show"] = "headings"
            #self.tree_dbs.bind("<Double-1>", self.edit)
            #self.tree_dbs.bind("<Button-1>", self.get_selected_row_data)
            #for col in self.col_names:
            #    self.tree_dbs.heading(col, text=col)
            #index = iid = 0
            #for row in rows:
            #    self.tree_dbs.insert("", index, iid, values=row)
            #    index = iid = index + 1
            #self.tree_id = index
            
    def refresh(self):
        self.mydb.reconnect()
        children = self.tree_dbs.get_children()
        for i in children:
            self.tree_dbs.delete(i)
        self.cursor.execute(
            "SELECT * from {}".format(self.name)
        )
        rows = self.cursor.fetchall()
        for i in range(len(rows)):
            self.tree_dbs.insert("", i, i, values=rows[i])

    def add_rollback(self) -> None:
        self.rollback_btn.pack(side=LEFT)

    def id_change(self, change: int = 1):
        for i in range(len(self.main_id)):
            self.main_id[i] += change

    def prime_var_change(self, change: int = 1):
        for v in self.prime_var_dic.values():
            v.set(int(v.get()) + change)

    def get_selected(self):
        item = self.tree_dbs.selection()[0]
        row = self.tree_dbs.item(self.tree_dbs.focus())
        return item, row

    def rollback(self):
        str_msg = "Rollbacks:\n"
        for item1 in self.reverse_add:
            try:
                self.tree_dbs.delete(item1)
                self.tree_id -= 1
                self.prime_var_change(-1)
                self.id_change(-1)
                str_msg += "Deleted item with index: {}\n".format(item1)
            except TclError:
                continue
        for item2 in self.reverse_delete:
            try:
                self.tree_dbs.insert("", item2["values"][0], values=tuple(item2["values"]))
                self.id_change(1)
                self.tree_id += 1
                self.prime_var_change(1)
                str_msg += "Added item with values: {}\n".format(str(tuple(item2["values"])))
            except TclError:
                continue
        for item3 in self.reverse_edit:
            try:
                if type(item3["value"]) is list:
                    self.tree_dbs.item(item3["item"], text="", values=tuple(item3["value"]))
                    for i1, i2 in zip(self.editted_data["new value"], item3["value"]):
                        str_msg += "Change '{}' to '{}'".format(i2, i1)
                else:
                    self.tree_dbs.set(item=item3["item"], column=item3["column"], value=item3["value"])
                    str_msg += "Changed '{}' to '{}'".format(self.editted_data["new value"], item3["value"])
            except TclError:
                continue
        self.reverse_add = []
        self.reverse_delete = []
        self.reverse_edit = []
        self.commit_actions = []
        messagebox.showinfo(
            "INFO",
            str_msg
        )
        self.rollback_btn.pack_forget()

    def sort_tree(self, event: EventType):
        chosen_column = self.tree_dbs.identify_column(event.x)[1]
        self.cursor.execute("SELECT * FROM {table_name} ORDER BY {col_num};".format(table_name=self.table_name,
                                                                                    col_num=chosen_column))
        sorted_rows = self.cursor.fetchall()
        children = self.tree_dbs.get_children()
        for child, row in zip(children, sorted_rows):
            self.tree_dbs.item(child, text="", values=row)

    def edit(self, event: EventType) -> None:
        region = self.tree_dbs.identify("region", event.x, event.y)
        if region == "heading":
            self.sort_tree(event)
        elif region == "cell":
            if not self.pressed:
                item, row = self.get_selected()
                col = int(self.tree_dbs.identify_column(event.x)[-1]) - 1
                col_name = self.col_names[col]
                row_id = row["values"][0]
                cell_val = row["values"][col]
                answer = simpledialog.askstring(
                    "INPUT",
                    "Change {} into: ".format(cell_val),
                    parent=self.dbs_frame
                )
                if answer == "":
                    messagebox.showwarning(
                        "WARNING",
                        "Please enter the new value !"
                    )
                    return
                elif answer is not None:
                    self.latest_action = "edit"
                    try:
                        args = [row["values"][index] for index in self.prime_ind]
                        cmd = self.multi_update([col_name], [answer], *args)
                        self.cursor.execute(cmd)
                        self.editted_data = {
                            "column": col_name,
                            "new value": answer,
                            "id": row_id
                        }
                        self.tree_dbs.set(item, column=col, value=answer)
                        self.cursor.execute("rollback;")
                        self.commit_actions.append(cmd)
                        self.reverse_edit.append(
                            {"item": item,
                             "column": col,
                             "value": cell_val}
                        )
                        self.add_rollback()
                    except (mysql.connector.DataError, mysql.connector.DatabaseError, mysql.connector.ProgrammingError):
                        er_msg = sys.exc_info()
                        messagebox.showerror(
                            "ERROR",
                            er_msg
                        )

    def delete_data(self) -> None:
        item, row = self.get_selected()
        self.deleted_data = item
        self.latest_action = "delete"
        try:
            args = [row["values"][index] for index in self.prime_ind]
            cmd = self.multi_delete(*args)
            print(cmd)
            self.cursor.execute(cmd)
            self.cursor.execute("rollback;")
            self.tree_dbs.delete(item)
            self.reverse_delete.append(row)
            self.commit_actions.append(cmd)
            self.id_change(-1)
            self.tree_id -= 1
            self.prime_var_change(-1)
            self.add_rollback()
        except (mysql.connector.DataError, mysql.connector.DatabaseError, mysql.connector.ProgrammingError):
            er_msg = sys.exc_info()[1]
            messagebox.showwarning(
                "ERROR",
                er_msg
            )

    def get_selected_row_data(self, event: EventType):
        if self.pressed:
            region = self.tree_dbs.identify("region", event.x, event.y)
            if region == "cell":
                try:
                    item, row = self.get_selected()
                except IndexError:
                    return
                for i1, i2 in zip(row["values"], self.label_dic.keys()):
                    if "date" in i2 and len(i1.split("-")) == 3:
                        year, month, day = i1.split("-")
                        self.label_dic[i2]["year"].set(year)
                        self.label_dic[i2]["month"].set(month)
                        self.label_dic[i2]["day"].set(day)
                    else:
                        self.label_dic[i2].set(i1)

    def modify_data(self) -> None:
        if not self.pressed:
            self.pressed = True
            self.modify_btn.config(relief=SUNKEN)
            self.add_btn.pack_forget()
            self.delete_btn.pack(side=RIGHT)
            self.edit_btn.pack(side=RIGHT)
        else:
            self.pressed = False
            self.modify_btn.config(relief=RAISED)
            self.delete_btn.pack_forget()
            self.edit_btn.pack_forget()
            self.add_btn.pack(side=RIGHT)
            for key, val in self.prime_var_dic.items():
                print(val[1])
                val[0].set(self.main_id[val[1]])

    def edit_data(self) -> None:
        try:
            item, row = self.get_selected()
            row_id = row["values"][0]
        except IndexError:
            return
        data_lst = []
        for col in self.label_dic.keys():
            if "date" not in col:
                content = self.label_dic[col].get()
            else:
                content = "{year}-{month}-{day}".format(year=self.label_dic[col]["year"].get(),
                                                        month=self.label_dic[col]["month"].get(),
                                                        day=self.label_dic[col]["day"].get())
            if len(str(content)) > 0:
                data_lst.append(content.split(',')[0])
            else:
                continue
        if len(data_lst) < len(self.label_dic.keys()):
            messagebox.showerror(
                "ERROR",
                "Please input the necessary data !"
            )
            return
        else:
            self.latest_action = "edit"
            try:
                args = [row["values"][index] for index in self.prime_ind]
                cmd = self.multi_update(self.col_names, data_lst, *args)
                print(cmd)
                self.cursor.execute(cmd)
                self.editted_data = {
                    "column": self.col_names,
                    "new value": data_lst,
                    "id": row_id
                }
                self.tree_dbs.item(item, text="", values=tuple(data_lst))
                self.cursor.execute("rollback;")
                self.commit_actions.append(cmd)
                self.reverse_edit.append(
                    {"item": item,
                     "value": row["values"]}
                )
                self.add_rollback()
            except (mysql.connector.DataError, mysql.connector.DatabaseError, mysql.connector.ProgrammingError):
                er_msg = sys.exc_info()
                messagebox.showerror(
                    "ERROR",
                    er_msg
                )

    def add_data(self) -> None:
        data_lst = []
        # data_lst.extend(self.main_id)
        for col in self.label_dic.keys():
            if "date" not in col:
                content = self.label_dic[col].get()
            else:
                content = "{year}-{month}-{day}".format(year=self.label_dic[col]["year"].get(),
                                                        month=self.label_dic[col]["month"].get(),
                                                        day=self.label_dic[col]["day"].get())
            if len(str(content)) > 0:
                data_lst.append(content.split(',')[0])
            else:
                continue
        if len(data_lst) < len(self.label_dic.keys()):
            messagebox.showerror(
                "ERROR",
                "Please input the necessary data !"
            )
            return
        else:
            # self.id_change(1)
            # data_lst[0:len(self.main_id)] = self.main_id
            self.added_data = tuple(data_lst)
            try:
                cmd = "INSERT INTO {table_name} VALUES {values_tup};".format(
                    table_name=self.name,
                    values_tup=self.added_data
                )
                self.cursor.execute(cmd)
                self.cursor.execute("rollback;")
                self.tree_dbs.insert("", self.tree_id, self.tree_id, values=data_lst)
                self.latest_action = "add"
                self.reverse_add.append(self.tree_id)
                self.commit_actions.append(cmd)
                self.tree_id += 1
                self.id_change(1)
                self.prime_var_change(1)
                self.add_rollback()
            except (mysql.connector.DataError, mysql.connector.DatabaseError):
                er_msg = sys.exc_info()[1]
                messagebox.showwarning(
                    "ERROR",
                    er_msg
                )
                self.id_change(-1)
                self.tree_id -= 1

    def commit_to_dbs(self) -> None:
        if len(self.commit_actions) == 0:
            messagebox.showinfo(
                "INFO",
                "No changes to commit"
            )
            return
        else:
            yes = messagebox.askyesno(
                "ATTENTION",
                "Do you want to commit the changes to database ?")
            if yes:
                for cmd in self.commit_actions:
                    self.cursor.execute(cmd)
                self.cursor.execute("commit;")
                messagebox.showinfo(
                    "INFO",
                    "Changes committed successfully !"
                )
                self.commit_actions = []
                self.reverse_edit, self.reverse_delete, self.reverse_add = [], [], []
                self.rollback_btn.grid_forget()
