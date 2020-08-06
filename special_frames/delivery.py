from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from frame_tab import FrameTab
import googlemaps


class Delivery(FrameTab):
    def __init__(self, parent, name: str, access_level: str):
        FrameTab.__init__(self, parent, name, access_level)
        self.recommend_btn = Button(self.btn_frame_2, text="Get recommended truck", command=self.get_recommended_truck)
        self.recommend_btn.grid(row=self.max_row + 1, column=0)

    def auto_create_widgets(self):
        self.cursor.execute("SELECT truck_id, description FROM trucks WHERE availability = 'Y';")
        available_trucks = ["{}, {}".format(i[0], i[1]) for i in self.cursor.fetchall()]
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
                year_opt.grid(row=self.max_row, column=1, sticky="ew")
                month_opt.grid(row=self.max_row, column=2, sticky="ew")
                day_opt.grid(row=self.max_row, column=3, sticky="ew")
                self.label_dic[col] = {"day": day_var,
                                       "month": month_var,
                                       "year": year_var}
            elif col == "truck_id":
                options = OptionMenu(self.btn_frame_2, str_var, *available_trucks)
                self.label_dic[col] = str_var
                options.grid(row=self.max_row, column=1,columnspan=3, sticky="ew")

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

    def get_distance(self, origin: str, destination: str) -> int:
        api_key = "AIzaSyDICNUXEXQDHtjvGpmmj24SDFuosdVKCfk"
        gmaps = googlemaps.Client(key=api_key)
        try:
            return gmaps.distance_matrix(origins=origin,
                                         destinations=destination,
                                         mode="driving")["rows"][0]["elements"][0]["distance"]["value"]
        except googlemaps.exceptions.HTTPError:
            messagebox.showerror("ERROR",
                                 "Network error occured, please try again,",
                                 parent=self)
            return 0

    def get_recommended_truck(self):
        order_id = self.label_dic["order_id"].get().split(',')[0]
        if order_id == "":
            messagebox.showwarning("WARNING",
                                   "No order_id specified",
                                   parent=self)
        self.cursor.execute("""
        SELECT destination FROM orders
        WHERE order_id = {};""".format(order_id))
        destination = self.cursor.fetchall()[0]
        self.cursor.execute("""
        SELECT trucks.truck_id, offices.office_location FROM trucks, offices
        WHERE trucks.office_id = offices.office_id
        AND trucks.availability = 'Y';""")
        data = self.cursor.fetchall()
        data = sorted(data, key=lambda i: self.get_distance(i[1], destination[0]))
        chosen = data[0][0]
        self.label_dic["truck_id"].set(chosen)
