from tkinter import *

root = Tk()

w = Frame(root, bg="red")
w.pack(side=LEFT, fill=X, expand=1)
z = Frame(root, bg="green")
z.pack(side=RIGHT, fill=X, expand=1)

mainloop()