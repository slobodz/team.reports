from tkinter import *
import tkinter as tk


root = Tk()
root.title('Team Reports')
root.resizable(False, False)


top_frame = Frame(root, height=35)
top_frame.pack(anchor=N)

login_output = Label(top_frame, text="Wrong credentials", fg='red')
# login_output.pack(fill=BOTH)

def pack_login_output(Label):
    Label.pack(anchor=W)



frame = Frame(root)
frame.pack(anchor=NW, pady=0, padx=10)

email_label = Label(frame, text='Email')
email_label.grid(row=0, column=0, pady=10, padx=5, sticky=E)

password_label = Label(frame, text='Password')
password_label.grid(row=1, column=0, pady=10, padx=5, sticky=E)

email_input = Entry(frame, width=30)
email_input.grid(row=0, column=1)

password_input = Entry(frame, width=30, show='*')
password_input.grid(row=1, column=1)


login_frame = Frame(root)
login_frame.pack(anchor=S, pady=10)
login_button = Button(login_frame, text='Log In', width=10, command=lambda: login_output.pack(fill=BOTH))
login_button.pack(anchor=CENTER)




# root.mainloop()



class LoginForm(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Team Reports")
        self.geometry("300x150")
        self.frame()

        self.name_label = tk.Label(self, text="Email")
        self.name_entry = tk.Entry(self, bg="white", fg="black", state='disabled')
        self.code_label = tk.Label(self, text="Password")
        self.code_entry = tk.Entry(self, bg="white", fg="black")
        self.empty_label = tk.Label(self, text)
        self.submit_button = tk.Button(self, text="Log In", command=print("hello"))


        self.name_label.pack(fill=tk.BOTH, expand=1)
        self.name_entry.pack(fill=tk.BOTH, expand=1)
        self.code_label.pack(fill=tk.BOTH, expand=1)
        self.code_entry.pack(fill=tk.BOTH, expand=1)
        self.empty_label.pack(fill=tk.BOTH, expand=1)
        self.submit_button.pack(fill=tk.X)


    def submit(self):
        pass



a = LoginForm()
a.mainloop()
