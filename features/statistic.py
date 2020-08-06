from tkinter import *
from tkinter import messagebox
from typing import List, Tuple
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from utilities.sdebugger import Decorators
from utilities.utilities import Util, Widget
from configparser import ConfigParser


@Decorators.timecheck
class Stat(Toplevel, Util):
    def __init__(self, table: List[Tuple], table_name: str, col_names: List[str]):
        Toplevel.__init__(self)
        self.col_names = col_names
        self.extra_y_cols = []
        # self.mainframe.pack_propagate(0)
        self.table = table
        self.current_row = -1
        self.selected_opt = []
        self.available = []
        self.configparser = ConfigParser()
        self.configparser.read("setting/config.ini")
        self.config_stat = self.configparser["STATISTIC"]
        self.df = pd.DataFrame(table, columns=col_names)
        self.df.set_index(col_names[0], inplace=True)
        self.fig = Figure(
            figsize=(
                int(self.config_stat["FIGURE_SIZE_X"]),
                int(self.config_stat["FIGURE_SIZE_y"])),
            dpi=100,
            frameon=False)
        self.ax = self.fig.add_subplot(111)
        self.canvas_frame = Frame(self,
                                  bg=self.config_stat["CANVASFRAME_COLOR"],
                                  width=int(self.config_stat["CANVASFRAME_WIDTH"]),
                                  height=int(self.config_stat["CANVASFRAME_HEIGHT"]),
                                  borderwidth=10)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side='left', fill='both', expand=True)
        if bool(self.config_stat["NAVIGATION_TOOLBAR"]):
            self.toolbar = NavigationToolbar2Tk(self.canvas, self.canvas_frame)
            self.toolbar.update()
        self.canvas_frame.pack(side="left", expand=True, fill="both")
        self.btn_frame = Frame(self,
                               bg=self.config_stat["BUTTONFRAME_COLOR"],
                               width=int(self.config_stat["BUTTONFRAME_WIDTH"]),
                               height=int(self.config_stat["BUTTONFRAME_HEIGHT"]),
                               borderwidth=10)
        Util.__init__(self, self.btn_frame)
        self.btn_frame.pack(side="right", expand=True, fill="both")
        self.canvas_frame.pack_propagate(0)
        self.btn_frame.pack_propagate(0)
        self.table_name_lab = Label(self.btn_frame, text=table_name, borderwidth=3)
        self.table_name_lab.grid(row=self.max_row, column=0)
        self.x_column = Label(self.btn_frame, text="X column", width=10, borderwidth=2)
        self.x_column.grid(row=self.max_row + 1, column=0)
        self.x_column_var = StringVar()
        self.x_column_opt = OptionMenu(self.btn_frame, self.x_column_var, *col_names)
        self.x_column_opt.grid(row=1, column=1, sticky="ew")
        self.y_column = Label(self.btn_frame, text="Y columns", width=10, borderwidth=2)
        self.y_column.grid(row=self.max_row + 1, column=0)
        self.y_column_var = StringVar()
        self.y_column_opt = OptionMenu(self.btn_frame, self.y_column_var, *col_names)
        self.y_column_opt.grid(row=self.max_row, column=1, sticky="ew")
        self.extra_y_col_btn = Button(self.btn_frame, text="+1 Y column", width=10, borderwidth=2,
                                      command=lambda: self.create_more_y(col_names, Widget.OPTION, "Y column"))
        self.extra_y_col_btn.grid(row=self.max_row + 1, column=0)
        self.graph_var = StringVar()
        self.graph_opt_lab = Label(self.btn_frame, text="Graph options", width=10, borderwidth=2)
        self.graph_opt = OptionMenu(self.btn_frame, self.graph_var, *["Bar",
                                                                      "Histogram",
                                                                      "Boxplot",
                                                                      "Scatter"])
        self.graph_opt_lab.grid(row=self.max_row + 1, column=0)
        self.graph_opt.grid(row=self.max_row, column=1, sticky="ew")
        self.graph_btn = Button(self.btn_frame, text="Graph", width=10, borderwidth=2, command=self.graph)
        self.graph_btn.grid(row=self.max_row + 1, column=0)
        self.clear_graph_btn = Button(self.btn_frame, text="Clear Graph", width=10, borderwidth=2,
                                      command=self.clear_graph)
        self.clear_graph_btn.grid(row=self.max_row + 1, column=0)
        self.special_wdgs = [self.extra_y_col_btn, self.graph_opt_lab,
                             self.graph_opt, self.graph_btn, self.clear_graph_btn]

    def clear_graph(self):
        self.ax.clear()
        self.canvas.draw()

    def graph(self):
        graph_dic = {"Bar": "bar",
                     "Histogram": "hist",
                     "Boxplot": "box",
                     "Scatter": "scatter",
                     "": "line"}
        graph_kind = graph_dic[self.graph_var.get()]
        y_cols_var = [y_col["var"].get() for y_col in self.extra_y_cols]
        y_cols_var.append(self.y_column_var.get())
        try:
            self.df.plot(x=self.x_column_var.get(), y=y_cols_var, grid=True, ax=self.ax, legend=True, kind=graph_kind)
            self.ax.set_xlabel(self.x_column_var.get())
            if len(y_cols_var) == 1:
                self.ax.set_ylabel(y_cols_var[0])
        except KeyError:
            messagebox.showerror("ERROR",
                                 "You can not have the same column for X and Y variables.",
                                 parent=self)
        except TypeError:
            messagebox.showerror("ERROR",
                                 "Invalid plot type for the selected data.",
                                 parent=self)
        self.canvas.draw()

    # @Util.grid_regrid
    # def add_new_column(self):
    #     if len(self.extra_y_cols) + 1 < len(self.col_names) - 1:
    #         new_lb = Label(self.btn_frame, text="Y columns", width=10, borderwidth=2)
    #         new_lb.grid(row=self.max_row + 1, column=0)
    #         delete_btn = Button(self.btn_frame, text="Delete", width=10, borderwidth=2,
    #                             command=lambda arg: self.delete_extra_col(delete_btn))
    #         delete_btn.grid(row=self.max_row, column=2)
    #         new_y_column_var = StringVar()
    #         new_y_column_opt = OptionMenu(self.btn_frame, new_y_column_var, *self.col_names)
    #         new_y_column_opt.grid(row=self.max_row, column=1, sticky="ew")
    #         self.extra_y_cols.append({"add": new_lb,
    #                                   "var": new_y_column_var,
    #                                   "delete": delete_btn,
    #                                   "option": new_y_column_opt})
    #     else:
    #         self.extra_y_col_btn.grid_forget()

    def delete_extra_col(self, button: Button):
        # if len(self.extra_y_cols) < len(self.col_names):
        #     self.extra_y_col_btn.grid(row=self.max_row - 1, column=0)
        for y_col in self.extra_y_cols:
            if y_col["delete"] is button:
                for value in y_col.values():
                    try:
                        value.destroy()
                    except AttributeError:
                        continue
                self.extra_y_cols.remove(y_col)
