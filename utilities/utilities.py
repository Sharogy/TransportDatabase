from tkinter import *
from functools import wraps
from enum import Enum
from .sdebugger import Decorators


class Widget(Enum):
    ENTRY = 1
    OPTION = 2
    BUTTON = 3


@Decorators.timecheck
class Util:
    def __init__(self, widget):
        self.widget = widget
        self.extra_y = []

    @property
    def max_row(self) -> int:
        m = 0
        for child in self.widget.winfo_children():
            try:
                if child.grid_info()["row"] > m:
                    m = child.grid_info()["row"]
            except KeyError:
                continue
        return m

    @staticmethod
    def grid_regrid(func: callable):
        @wraps(func)
        def decorate(*args):
            try:
                for wdgt in args[0].special_wdgs:
                    wdgt.grid_forget()
                f = func(*args)
                for wdgt in args[0].special_wdgs:
                    if type(wdgt) in (OptionMenu, Entry):
                        wdgt.grid(row=args[0].max_row, column=1)
                    else:
                        wdgt.grid(row=args[0].max_row + 1, column=0)
            except NameError:
                raise NameError("Variable 'special_wdgs' not found")
            return f
        return decorate

    def create_more_y(self, extra_lst, extra_widget_type: Widget, label_name: str):
        for wdgt in self.special_wdgs:
            wdgt.grid_forget()
        new_label = Label(self.widget, text=label_name)
        new_label.grid(row=self.max_row + 1, column=0)
        if extra_widget_type is Widget.ENTRY:
            new_y_var = StringVar()
            new_y_entry = Entry(self.widget, textvariable=new_y_var)
            new_y_entry.grid(row=self.max_row, column=1)
            delete_btn = Button(self.widget, text="Delete", command=lambda: self.delete(delete_btn))
            delete_btn.grid(row=self.max_row, column=2)
            self.extra_y.append((new_label, new_y_entry, delete_btn))
        elif extra_widget_type is Widget.OPTION:
            new_y_opt_var = StringVar()
            new_y_opt_var.set(extra_lst[0])
            new_y_opt = OptionMenu(self.widget, new_y_opt_var, *extra_lst)
            new_y_opt.grid(row=self.max_row, column=1, sticky="ew")
            delete_btn = Button(self.widget, text="Delete", command=lambda: self.delete(delete_btn))
            delete_btn.grid(row=self.max_row, column=2)
            self.extra_y.append((new_label, new_y_opt, delete_btn))
        for wdgt in self.special_wdgs:
            if type(wdgt) is OptionMenu:
                wdgt.grid(row=self.max_row, column=1)
            else:
                wdgt.grid(row=self.max_row + 1, column=0)

    def delete(self, button: Button):
        for y in self.extra_y:
            if y[-1] is button:
                for value in y:
                    try:
                        value.destroy()
                    except AttributeError:
                        continue
                self.extra_y.remove(y)
