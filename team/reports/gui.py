#from tkinter import *
import tkinter as tk
from team.reports.excel import ExcelFile
import json

class LoginForm(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Team Reports")


        self.login_frame = tk.Frame(self, bd=5)
        self.main_frame = tk.Frame(self, bd=5)
        self.empty_frame = tk.Frame(self, width=15, bd=5)



        self.email_label = tk.Label(self.login_frame, text="Email", width=25)
        self.email_entry = tk.Entry(self.login_frame, bg="white", fg="black", width=25)
        self.password_label = tk.Label(self.login_frame, text="Password", width=25)
        self.password_entry = tk.Entry(self.login_frame, bg="white", fg="black", show='*', width=25)
        self.empty_label = tk.Label(self.login_frame, text="", width=25)
        self.submit_button = tk.Button(self.login_frame, text="Log In", command=self.submit, width=25)

        self.product_label = tk.Label(self.main_frame, text="")
        self.product_button = tk.Button(self.main_frame, text="Generate report for\nselected products", width=25, state='disabled', command=self.generate_selected_products)
        self.full_refresh_label = tk.Label(self.main_frame, text="")
        self.full_refresh_button = tk.Button(self.main_frame, text="Generate report for\nall products", width=25, state='disabled')



        self.login_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.empty_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)        
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)


        self.email_label.pack(fill=tk.BOTH, expand=1)
        self.email_entry.pack(fill=tk.BOTH, expand=1)
        self.password_label.pack(fill=tk.BOTH, expand=1)
        self.password_entry.pack(fill=tk.BOTH, expand=1)
        self.empty_label.pack(fill=tk.BOTH, expand=1)
        self.submit_button.pack(fill=tk.BOTH, expand=1)



        self.product_label.pack(fill=tk.BOTH, expand=1)
        self.product_button.pack(fill=tk.BOTH, expand=1)
        self.full_refresh_label.pack(fill=tk.BOTH, expand=1)
        self.full_refresh_button.pack(fill=tk.BOTH, expand=1)






    def submit(self):
        self.email_entry.config(state='disable')
        self.password_entry.config(state='disable')
        self.email = self.email_entry.get()
        self.password = self.password_entry.get()

        # here send post request to api and get the token if correct or 500 if invalid

        if self.email == "a":
            self.email_entry.config(state='normal')
            self.password_entry.config(state='normal')
            self.product_button.config(state='normal')
            self.full_refresh_button.config(state='normal')

            #GenerateReportForm().mainloop()

        else:
            self.empty_label.config(text="Invalid credentials", fg='red')
            self.email_entry.config(state='normal')
            self.password_entry.config(state='normal')


    def generate_selected_products(self):
        self.product_label.config(text="Loading...")
        with open('products.json') as f:
            all_products = json.load(f)


        a = ExcelFile('team_lista.xlsx', 'produkty')

        a.update_file(all_products)
        a.save_file()


    def generate_all_products(self):
        pass





a = LoginForm()
a.mainloop()
