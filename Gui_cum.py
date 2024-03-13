import tkinter as tk

root = tk.Tk()
root.title("Grid Lines Example")
total_sum_var = tk.IntVar()


def layout_control():
# Create a grid of Frame widgets with distinct background colors
    for r in range(5):  # Adjust the range based on your grid
        for c in range(4):  # Adjust the range based on your grid
            frame = tk.Frame(root, borderwidth=1, relief="solid", bg="grey")
            frame.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")

# Now, you can create your actual widgets and place them on top of the grid frames
def range_add():
    r += 1
    return r



# Example widget placement
label = tk.Label(root, text="This is a label")
label.grid(row=0, column=0)

label2 = tk.Label(root, text="Cock and balls")
label2.grid(row=1, column=0)

button = tk.Button(root, text="Range Add", command=range_add)
button.grid(row=0, column=1)

entry = tk.Entry(root)
entry.grid(row=0, column=2)
# Create a Label to display the total_sum
total_sum_label = tk.Label(root, textvariable=total_sum_var)
total_sum_label.grid(row=3, column=0, pady=5)
# Configure the column and row weights to ensure that they expand equally
for i in range(4):  # Adjust the range based on your grid
    root.grid_columnconfigure(i, weight=1)
    root.grid_rowconfigure(i, weight=1)

root.mainloop()