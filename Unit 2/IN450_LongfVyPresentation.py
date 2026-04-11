# Unit 2
#Presentation layer
# Long Vy


"""
GeeksforGeeks. (2026, January 23). Python tkinter. https://www.geeksforgeeks.org/python/python-gui-tkinter/ 
"""

import tkinter as tk
from IN450_LongVyBusinessLayer_Unit2 import Business_Layer

def row_count():
    count = b1.get_row_count_450a()
    resultLabel.config(text=f"Row count in IN450A: {count}")

def show_names():
    names = b1.get_450b()
    text.delete(1.0, tk.END)
    for first, last in names:
        text.insert(tk.END, f"{first.strip()} {last.strip()}\n")

#initialize business layer

b1 = Business_Layer()


#GUI

root = tk.Tk()
root.title("450 Database App")
root.geometry("500x400")

count = tk.Button(root, text="Get Row Count (IN450A)", command=row_count)
count.pack(pady=10)

resultLabel = tk.Label(root, text="")
resultLabel.pack()

names = tk.Button(root, text="Get Names (IN450B)", command=show_names)
names.pack(pady=10)

text = tk.Text(root, height=15, width=50)
text.pack(pady=10)


root.mainloop()
b1.close_connection()