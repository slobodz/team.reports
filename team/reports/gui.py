from tkinter import *
import tkinter as tk


# root = Tk()
# root.title('Team Reports')
# root.resizable(False, False)


# top_frame = Frame(root, height=35)
# top_frame.pack(anchor=N)

# login_output = Label(top_frame, text="Wrong credentials", fg='red')
# # login_output.pack(fill=BOTH)

# def pack_login_output(Label):
#     Label.pack(anchor=W)



# frame = Frame(root)
# frame.pack(anchor=NW, pady=0, padx=10)

# email_label = Label(frame, text='Email')
# email_label.grid(row=0, column=0, pady=10, padx=5, sticky=E)

# password_label = Label(frame, text='Password')
# password_label.grid(row=1, column=0, pady=10, padx=5, sticky=E)

# email_input = Entry(frame, width=30)
# email_input.grid(row=0, column=1)

# password_input = Entry(frame, width=30, show='*')
# password_input.grid(row=1, column=1)


# login_frame = Frame(root)
# login_frame.pack(anchor=S, pady=10)
# login_button = Button(login_frame, text='Log In', width=10, command=lambda: login_output.pack(fill=BOTH))
# login_button.pack(anchor=CENTER)




# root.mainloop()



class LoginForm(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Team Reports")
        self.geometry("300x150")
        self.frame()

        self.email_label = tk.Label(self, text="Email")
        self.email_entry = tk.Entry(self, bg="white", fg="black")
        self.password_label = tk.Label(self, text="Password")
        self.password_entry = tk.Entry(self, bg="white", fg="black", show='*')
        self.empty_label = tk.Label(self, text="")
        self.submit_button = tk.Button(self, text="Log In", command=self.submit)


        self.email_label.pack(fill=tk.BOTH, expand=1)
        self.email_entry.pack(fill=tk.BOTH, expand=1)
        self.password_label.pack(fill=tk.BOTH, expand=1)
        self.password_entry.pack(fill=tk.BOTH, expand=1)
        self.empty_label.pack(fill=tk.BOTH, expand=1)
        self.submit_button.pack(fill=tk.X)


    def submit(self):
        self.email_entry.config(state='disable')
        self.password_entry.config(state='disable')   
        self.email = self.email_entry.get()
        self.password = self.password_entry.get()

        # here send post request to api and get the token if correct or 500 if invalid

        if self.email == "a":
            self.empty_label.config(text="Correct!")

            self.destroy()

            GenerateReportForm().mainloop()




        else:
            self.empty_label.config(text="Invalid credentials", fg='red')
            self.email_entry.config(state='normal')
            self.password_entry.config(state='normal')




class GenerateReportForm(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Team Reports")
        self.geometry("300x150")
        self.frame()

        self.product_label = tk.Label(self, text="")
        self.product_button = tk.Button(self, text="Generate report for selected products")
        self.full_refresh_label = tk.Label(self, text="")
        self.full_refresh_button = tk.Button(self, text="Generate report for all products")


        self.product_label.pack(fill=BOTH, expand=1)
        self.product_button.pack(fill=BOTH, expand=1)
        self.full_refresh_label.pack(fill=BOTH, expand=1)
        self.full_refresh_button.pack(fill=BOTH, expand=1)


a = LoginForm()
a.mainloop()
