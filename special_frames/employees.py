from tkinter import messagebox
from tkinter import *
from tkinter import ttk
from frame_tab import FrameTab
import re
from dateutil import parser
from datetime import datetime
from utilities.sdebugger import Decorators
from utilities.utilities import Util


@Decorators.timecheck
class Employee(FrameTab):
    def __init__(self, parent, name: str, access_level: str):
        FrameTab.__init__(self, parent, name, access_level)
        self.after(6000, self.alert)
        self.extra_events = self.extra_y
        self.extra_event_btn = Button(self.btn_frame_2, text="More events", width=12, command=self.create_more_event)
        self.extra_event_btn.grid(row=self.max_row + 1, column=0)
        self.special_wdgs = [self.extra_event_btn]
        self.limit = 3
        # TODO: Add limit to setting

    @Util.grid_regrid
    def create_more_event(self):
        if len(self.extra_events) < self.limit:
            day_label = Label(self.btn_frame_2, text="Date")
            day_label.grid(row=self.max_row + 1, column=0)
            day_var, month_var, year_var = StringVar(), StringVar(), StringVar()
            day_var.set("Day")
            month_var.set("Month")
            year_var.set("Year")
            day_opt = ttk.Combobox(self.btn_frame_2, textvariable=day_var, values=[i for i in range(32)],
                                   width=3)
            month_opt = ttk.Combobox(self.btn_frame_2, textvariable=month_var, values=[i for i in range(1, 13)],
                                     width=6)
            year_opt = ttk.Combobox(self.btn_frame_2, textvariable=year_var, values=[i for i in range(1900, 2301)],
                                    width=6)
            year_opt.grid(row=self.max_row, column=1, sticky="ew")
            month_opt.grid(row=self.max_row, column=2, sticky="ew")
            day_opt.grid(row=self.max_row, column=3, sticky="ew")
            text_label = Label(self.btn_frame_2, text="Note")
            text_label.grid(row=self.max_row + 1, column=0)
            text_var = StringVar()
            text_entry = Entry(self.btn_frame_2, textvariable=text_var, width=12)
            text_entry.grid(row=self.max_row, column=1, sticky="ew")
            delete_btn = Button(self.btn_frame_2, text="Delete", command=lambda: self.delete(delete_btn))
            delete_btn.grid(row=self.max_row, column=2)
            self.extra_events.append((day_label, day_opt, month_opt, year_opt, text_label, text_entry, delete_btn))
        else:
            messagebox.showwarning("WARNING",
                                   "Extra events limit reached!",
                                   parent=self)

    def alert(self):
        days_to_alert = 3
        imp_events_count = 0
        current_date = parser.parse(datetime.now().date().strftime("%Y-%m-%d"))
        pattern = re.compile(r'(\d+-\d+-\d+)([A-Za-z\s]+)')
        self.cursor.execute("SELECT important_date, first_name FROM employees;")
        result = self.cursor.fetchall()
        alert_string = ""
        lst = []
        for note, name in result:
            matched = pattern.findall(note)
            new_matched = [(parser.parse(i[0].strip('\n')), i[1].strip('\n')) for i in matched]
            if len(new_matched) >= 1:
                for matched in new_matched:
                    lst.append({"name": name,
                                "time": matched[0],
                                "note": matched[1]})
        for item in lst:
            remaining_date = (item["time"] - current_date).days % 365
            if remaining_date <= days_to_alert:
                date_str = "{month}-{day}".format(month=item["time"].month, day=item["time"].day)
                date_obj = datetime.strptime(date_str, "%m-%d")
                new_date_str = datetime.strftime(date_obj, "%d %b")
                imp_events_count += 1
                alert_string += "Employee {name} on {date} has note:{note}\n ".format(
                    name=item["name"],
                    date=new_date_str,
                    note=item["note"]
                )
        if imp_events_count > 0:
            messagebox.showinfo("INFO",
                                "These employees have important events less than {} days from now:\n {}".format(
                                    days_to_alert,
                                    alert_string),
                                parent=self)
