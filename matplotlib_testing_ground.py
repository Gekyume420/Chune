import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Your data
categories = ['Gym', 'Chores', 'Class']
values = [45, 74, 299]

# Calculate the remainder of the total as 'Others'
total = 1440
used_total = sum(values)
others = total - used_total
categories.append('Others')
values.append(others)

# Setting up the Tkinter window
root = tk.Tk()
root.title("Quantities Pie Chart")

# Create a figure for the pie chart
fig = Figure(figsize=(6, 6), dpi=100)
pie_chart = fig.add_subplot(111)

# Plot the pie chart
pie_chart.pie(values, labels=categories, autopct='%1.1f%%', startangle=140)
pie_chart.set_title('Quantities by Category')

# Create a canvas and add the pie chart to the Tkinter window
canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Tkinter event loop
tk.mainloop()