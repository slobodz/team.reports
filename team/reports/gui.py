from tkinter import *
import tkinter as tk


class LoginForm(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Team Reports")
        #self.geometry("300x150")

        self.login_frame = tk.Frame(self, bd=5)
        self.main_frame = tk.Frame(self, bd=5)
        self.empty_frame = tk.Frame(self, width=200, bd=5)


        self.email_label = tk.Label(self.login_frame, text="Email")
        self.email_entry = tk.Entry(self.login_frame, bg="white", fg="black")
        self.password_label = tk.Label(self.login_frame, text="Password")
        self.password_entry = tk.Entry(self.login_frame, bg="white", fg="black", show='*')
        self.empty_label = tk.Label(self.login_frame, text="")
        self.submit_button = tk.Button(self.login_frame, text="Log In", command=self.submit)
        self.test_label = tk.Label(self.empty_frame, text="test")

        self.product_label = tk.Label(self.main_frame, text="")
        self.product_button = tk.Button(self.main_frame, text="Generate report for\nselected products")
        self.full_refresh_label = tk.Label(self.main_frame, text="")
        self.full_refresh_button = tk.Button(self.main_frame, text="Generate report for\nall products")



        self.login_frame.pack(side=LEFT, fill=BOTH, expand=False)
        self.empty_frame.pack(side=LEFT, fill=BOTH, expand=False)        
        self.main_frame.pack(side=RIGHT, fill=BOTH, expand=1)

        self.email_label.pack(fill=tk.BOTH, expand=False)
        self.email_entry.pack(fill=tk.BOTH, expand=False)
        self.password_label.pack(fill=tk.BOTH, expand=False)
        self.password_entry.pack(fill=tk.BOTH, expand=False)
        self.empty_label.pack(fill=tk.BOTH, expand=False)
        self.submit_button.pack(fill=tk.BOTH, expand=False)
        self.test_label.pack(fill=tk.BOTH, expand=False)


        self.product_label.pack(fill=BOTH, expand=1)
        self.product_button.pack(fill=BOTH, expand=1)
        self.full_refresh_label.pack(fill=BOTH, expand=1)
        self.full_refresh_button.pack(fill=BOTH, expand=1)








    def submit(self):
        self.email_entry.config(state='disable')
        self.password_entry.config(state='disable')   
        self.email = self.email_entry.get()
        self.password = self.password_entry.get()

        # here send post request to api and get the token if correct or 500 if invalid

        if self.email == "a":
            self.empty_label.config(text="Correct!")

            self.destroy()

            #GenerateReportForm().mainloop()




        else:
            self.empty_label.config(text="Invalid credentials", fg='red')
            self.email_entry.config(state='normal')
            self.password_entry.config(state='normal')





# class GenerateReportForm(tk.Tk):
#     def __init__(self):
#         super().__init__()

#         self.title("Team Reports")
#         self.geometry("300x150")
#         self.frame()

#         self.product_label = tk.Label(self, text="")
#         self.product_button = tk.Button(self, text="Generate report for selected products")
#         self.full_refresh_label = tk.Label(self, text="")
#         self.full_refresh_button = tk.Button(self, text="Generate report for all products")


#         self.product_label.pack(fill=BOTH, expand=1)
#         self.product_button.pack(fill=BOTH, expand=1)
#         self.full_refresh_label.pack(fill=BOTH, expand=1)
#         self.full_refresh_button.pack(fill=BOTH, expand=1)


a = LoginForm()
a.mainloop()
