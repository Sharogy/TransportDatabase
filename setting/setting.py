from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import configparser
from utilities.utilities import Util
from setting.constants import COLORS, FONTS
from numpy import arange
from abc import ABC, abstractmethod


class AbstractSetting(ABC):
    def __init__(self):
        self.configparser = configparser.ConfigParser()
        self.configparser.read("config.ini")
        #self.resolutions = ("600x800", "1280x720", "1280x1024", "1360x768", "1600x900", "1920x1080")

    @abstractmethod
    def apply_setting(self):
        pass

    def save(self):
        with open("config.ini", "w+") as configfile:
            self.configparser.write(configfile)
        messagebox.showinfo(
            "INFO",
            "Changes applied successfully! \n "
            "Please restart the program for the effects to take place",
            parent=self
        )


class Statistic(AbstractSetting, Frame, Util):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        Util.__init__(self, self)
        AbstractSetting.__init__(self)
        #self.canvasframe_reso_lab = Label(self, text="Canvasframe resolution: ", width=18)
        #self.canvasframe_reso_var = StringVar()
        #self.canvasframe_reso_var.set(self.resolutions[0])
        #self.canvasframe_reso_opt = OptionMenu(self, self.canvasframe_reso_var, *self.resolutions)
        #self.canvasframe_reso_lab.grid(row=self.max_row + 1, column=0)
        #self.canvasframe_reso_opt.grid(row=self.max_row, column=1, sticky="ew")
        self.canvasframe_color_lab = Label(self, text="Canvasframe color: ", width=18)
        self.canvasframe_color_var = StringVar()
        self.canvasframe_color_var.set("light blue")
        self.canvasframe_color_opt = OptionMenu(self, self.canvasframe_color_var, *COLORS)
        self.canvasframe_color_lab.grid(row=self.max_row + 1, column=0)
        self.canvasframe_color_opt.grid(row=self.max_row, column=1)
        self.buttonframe_color_lab = Label(self, text="Buttonframe color: ", width=18)
        self.buttonframe_color_var = StringVar()
        self.buttonframe_color_var.set("light blue")
        self.buttonframe_color_opt = OptionMenu(self, self.buttonframe_color_var, *COLORS)
        self.buttonframe_color_lab.grid(row=self.max_row + 1, column=0)
        self.buttonframe_color_opt.grid(row=self.max_row, column=1, sticky="ew")
        #self.buttonframe_reso_lab = Label(self, text="Buttonframe resolution: ", width=18)
        #self.buttonframe_reso_var = StringVar()
        #self.buttonframe_reso_var.set(self.resolutions[0])
        #self.buttonframe_reso_opt = OptionMenu(self, self.canvasframe_reso_var, *self.resolutions)
        #self.buttonframe_reso_lab.grid(row=self.max_row + 1, column=0)
        #self.buttonframe_reso_opt.grid(row=self.max_row, column=1, sticky="ew")
        #self.figure_x_lab = Label(self, text="Figure width: ", width=18)
        #self.figure_x_var = StringVar()
        #self.figure_x_opt = OptionMenu(self, self.figure_x_var, *range(1, 10))
        #self.figure_x_lab.grid(row=self.max_row + 1, column=0)
        #self.figure_x_opt.grid(row=self.max_row, column=1, sticky="ew")
        #self.figure_y_lab = Label(self, text="Figure height: ", width=18)
        #self.figure_y_var = StringVar()
        #self.figure_y_opt = OptionMenu(self, self.figure_y_var, *range(1, 10))
        #self.figure_y_lab.grid(row=self.max_row + 1, column=0)
        #self.figure_y_opt.grid(row=self.max_row, column=1)
        #self.dyna_resize_lab = Label(self, text="Dynamic Resize: ", width=18)
        #self.dyna_resize_var = StringVar()
        #self.dyna_resize_var.set("False")
        #self.dyna_resize_opt = OptionMenu(self, self.dyna_resize_var, *("True", "False"))
        #self.dyna_resize_lab.grid(row=self.max_row + 1, column=0)
        #self.dyna_resize_opt.grid(row=self.max_row, column=1, sticky="ew")
        self.navi_lab = Label(self, text="Navigation toolbar: ", width=18)
        self.navi_var = StringVar()
        self.navi_opt = OptionMenu(self, self.navi_var, *("True", "False"))
        self.navi_lab.grid(row=self.max_row + 1, column=0)
        self.navi_opt.grid(row=self.max_row, column=1)
        self.apply_btn = Button(self, text="Apply", command=self.apply_setting, width=16)
        self.apply_btn.grid(row=self.max_row + 1, column=0)

    def apply_setting(self):
        #canvas_reso = self.canvasframe_reso_var.get().split('x')
        #canvas_reso_x, canvas_reso_y = canvas_reso
        #button_reso = self.buttonframe_reso_var.get().split('x')
        #button_reso_x, button_reso_y = button_reso
        #self.configparser.set("STATISTIC", "CANVASFRAME_WIDTH", canvas_reso_x)
        #self.configparser.set("STATISTIC", "CANVASFRAME_HEIGHT", canvas_reso_y)
        self.configparser.set("STATISTIC", "CANVASFRAME_COLOR", self.canvasframe_color_var.get())
        #self.configparser.set("STATISTIC", "BUTTONFRAME_WIDTH", button_reso_x)
        #self.configparser.set("STATISTIC", "BUTTONFRAME_HEIGHT", button_reso_y)
        self.configparser.set("STATISTIC", "BUTTONFRAME_COLOR", self.buttonframe_color_var.get())
        #self.configparser.set("STATISTIC", "FIGURE_SIZE_X", self.figure_x_var.get())
        #self.configparser.set("STATISTIC", "FIGURE_SIZE_Y", self.figure_y_var.get())
        #self.configparser.set("STATISTIC", "DYNAMIC_RESIZE", self.dyna_resize_var.get())
        self.configparser.set("STATISTIC", "NAVIGATION_TOOLBAR", self.navi_var.get())
        self.save()


class FrameTab(AbstractSetting, Frame, Util):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        Util.__init__(self, self)
        AbstractSetting.__init__(self)
        self.title = "Login Setting"
        self.config(bg="light blue")
        #self.resolution_var = StringVar()
        #self.resolution_var.set(self.resolutions[0])
        #self.resolution_opt = OptionMenu(self, self.resolution_var, *self.resolutions)
        #self.resolution_lab = Label(self, text="Resolution: ", width=14)
        #self.resolution_lab.grid(row=self.max_row + 1, column=0)
        #self.resolution_opt.grid(row=self.max_row, column=1, sticky="ew")
        #self.dyna_resize_lab = Label(self, text="Dynamic Resize: ", width=14)
        #self.dyna_resize_var = StringVar()
        #self.dyna_resize_var.set("False")
        #self.dyna_resize_opt = OptionMenu(self, self.dyna_resize_var, *("True", "False"))
        #self.dyna_resize_lab.grid(row=self.max_row + 1, column=0)
        #self.dyna_resize_opt.grid(row=self.max_row, column=1, sticky="ew")
        self.dataframe_color_lab = Label(self, text="Dataframe color: ", width=14)
        self.dataframe_color_var = StringVar()
        self.dataframe_color_var.set("light blue")
        self.dataframe_color_opt = OptionMenu(self, self.dataframe_color_var, *COLORS)
        self.dataframe_color_lab.grid(row=self.max_row + 1, column=0)
        self.dataframe_color_opt.grid(row=self.max_row, column=1, sticky="ew")
        self.buttonframe_color_lab = Label(self, text="Buttonframe color: ", width=14)
        self.buttonframe_color_var = StringVar()
        self.buttonframe_color_var.set("light blue")
        self.buttonframe_color_opt = OptionMenu(self, self.buttonframe_color_var, *COLORS)
        self.buttonframe_color_lab.grid(row=self.max_row + 1, column=0)
        self.buttonframe_color_opt.grid(row=self.max_row, column=1, sticky="ew")
        self.apply_btn = Button(self, text="Apply", command=self.apply_setting, width=14)
        self.apply_btn.grid(row=self.max_row + 1, column=0)

    def apply_setting(self):
        #resolution = self.resolution_var.get().split('x')
        #resolution_w, resolution_h = resolution
        #self.configparser.set("FRAMETAB", "WIDTH", resolution_w)
        #self.configparser.set("FRAMETAB", "HEIGHT", resolution_h)
        #self.configparser.set("FRAMETAB", "DYNAMIC_RESIZE", self.dyna_resize_var.get())
        self.configparser.set("FRAMETAB", "DATAFRAME_COLOR", self.dataframe_color_var.get())
        self.configparser.set("FRAMETAB", "BUTTONFRAME_COLOR", self.buttonframe_color_var.get())
        self.save()


class Login(AbstractSetting, Frame, Util):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        Util.__init__(self, self)
        AbstractSetting.__init__(self)
        self.title = "Login Setting"
        self.config(bg="light blue")
        #self.resolution_var = StringVar()
        #self.resolution_var.set(self.resolutions[0])
        #self.resolution_opt = OptionMenu(self, self.resolution_var, *self.resolutions)
        #self.resolution_lab = Label(self, text="Resolution: ", width=10)
        #self.resolution_lab.grid(row=self.max_row + 1, column=0)
        #self.resolution_opt.grid(row=self.max_row, column=1, sticky="ew")
        self.font_var = StringVar()
        self.font_var.set("Helvetica")
        self.font_opt = OptionMenu(self, self.font_var, *FONTS)
        self.font_lab = Label(self, text="Font: ", width=10)
        self.font_lab.grid(row=self.max_row + 1, column=0)
        self.font_opt.grid(row=self.max_row, column=1)
        self.fontsize_lab = Label(self, text="Font size: ", width=10)
        self.fontsize_var = StringVar()
        self.fontsize_var.set("12")
        self.fontsize_opt = OptionMenu(self, self.fontsize_var, *list(arange(12, 24, 0.5)))
        self.fontsize_lab.grid(row=self.max_row + 1, column=0)
        self.fontsize_opt.grid(row=self.max_row, column=1, sticky="ew")
        self.apply_btn = Button(self, text="Apply", command=self.apply_setting, width=10)
        self.apply_btn.grid(row=self.max_row + 1, column=0)

    def apply_setting(self):
        #resolution = self.resolution_var.get().split('x')
        #resolution_w, resolution_h = resolution
        #self.configparser.set("LOGIN", "WIDTH", resolution_w)
        #self.configparser.set("LOGIN", "HEIGHT", resolution_h)
        self.configparser.set("LOGIN", "FONT", self.font_var.get())
        self.configparser.set("LOGIN", "FONTSIZE", self.fontsize_var.get())
        self.save()


class Setting(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.notebook = ttk.Notebook(self)
        self.notebook.add(Login(self.notebook), text="Login")
        self.notebook.add(FrameTab(self.notebook), text="Frametab")
        self.notebook.add(Statistic(self.notebook), text="Statistic")
        self.notebook.grid(row=0, column=0, sticky="nw")


if __name__ == '__main__':
    Setting().mainloop()
