from tkinter import *

root = Tk()
root.geometry('300x100')
root.title('Team Reports')
root.resizable(False, False)


frame = Frame(root)

email = Label(frame, text='Email')
email.grid(row=0, column=0, pady=80, padx=0)

frame.pack(side=BOTTOM)

# f2 = Frame(root)
# f2.pack(side=BOTTOM, fill='both')

# l1 = Label(f1, text="User Name", anchor=NE)
# l1.pack()

# l2 = Label(f2, text="Password")
# l2.pack(side=LEFT)

# E1 = Entry(f1, fg='red')
# E1.pack()

root.mainloop()