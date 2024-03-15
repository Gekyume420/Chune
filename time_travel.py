from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext


"""
todays_date1 = datetime.now()
yesterdays_date = todays_date1 - timedelta(days=1)
todays_date = yesterdays_date.strftime("%Y-%m-%d") # time travel mode
"""


class DateNavigator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Date Navigator")
        self.geometry("200x100")

        self.current_date = datetime.now()
        self.create_widgets()

    def create_widgets(self):
        self.date_label = ttk.Label(self, text=self.format_date(self.current_date))
        self.date_label.pack(pady=20)

        left_arrow_button = ttk.Button(self, text="<", command=self.decrement_date)
        left_arrow_button.pack(side="left", padx=10)

        right_arrow_button = ttk.Button(self, text=">", command=self.increment_date)
        right_arrow_button.pack(side="right", padx=10)

    def format_date(self, date):
        return date.strftime("%Y-%m-%d")

    def update_label(self):
        self.date_label.config(text=self.format_date(self.current_date))

    def decrement_date(self):
        self.current_date -= timedelta(days=1)
        self.update_label()

    def increment_date(self):
        self.current_date += timedelta(days=1)
        self.update_label()

if __name__ == "__main__":
    app = DateNavigator()
    #print(app)
    app.mainloop()

    