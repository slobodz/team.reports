import tkinter as tk
import api
from excel import ExcelFile
import json
import requests as r


URL = 'https://team-services-uat.herokuapp.com/'

class LoginForm(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Team Reports")


        self.login_frame = tk.Frame(self, bd=5)
        self.main_frame = tk.Frame(self, bd=5)
        self.empty_frame = tk.Frame(self, width=15, bd=5)



        self.logging_info_text = LabelString()
        self.product_text = LabelString()
        self.full_refresh_text = LabelString()


        self.email_label = tk.Label(self.login_frame, text="Email", width=25)
        self.email_entry = tk.Entry(self.login_frame, bg="white", fg="black", width=25)
        self.password_label = tk.Label(self.login_frame, text="Password", width=25)
        self.password_entry = tk.Entry(self.login_frame, bg="white", fg="black", show='*', width=25)
        self.logging_info_label = tk.Label(self.login_frame, textvariable=self.logging_info_text, width=25)
        self.submit_button = tk.Button(self.login_frame, text="Log In", command=self.submit, width=25)


        self.product_label = tk.Label(self.main_frame, textvariable=self.product_text)
        self.product_button = tk.Button(self.main_frame, text="Generate report for\nselected products",
                                        width=25, state='disabled', command=self.generate_selected_products)
        self.full_refresh_label = tk.Label(self.main_frame, textvariable=self.full_refresh_text)
        self.full_refresh_button = tk.Button(self.main_frame, text="Generate report for\nall products",
                                        width=25, state='disabled', command=self.generate_all_products)



        self.login_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.empty_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)        
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)


        self.email_label.pack(fill=tk.BOTH, expand=1)
        self.email_entry.pack(fill=tk.BOTH, expand=1)
        self.password_label.pack(fill=tk.BOTH, expand=1)
        self.password_entry.pack(fill=tk.BOTH, expand=1)
        self.logging_info_label.pack(fill=tk.BOTH, expand=1)
        self.submit_button.pack(fill=tk.BOTH, expand=1)



        self.product_label.pack(fill=tk.BOTH, expand=1)
        self.product_button.pack(fill=tk.BOTH, expand=1)
        self.full_refresh_label.pack(fill=tk.BOTH, expand=1)
        self.full_refresh_button.pack(fill=tk.BOTH, expand=1)






    def submit(self):
        """Send post request with credentials"""
        LabelString.clear_text()      
        self.email_entry.config(state='disable')
        self.password_entry.config(state='disable')
        self.email = self.email_entry.get()
        self.password = self.password_entry.get()
        self.submit_button.update_idletasks()

        self.token_call = api.post_token(email=self.email, password=self.password)


        if(self.token_call.ok):
            self.logging_info_text.set("Logged in")
            self.token = self.token_call.json()['token']
            self.logging_info_label.config(fg='green')
            self.email_entry.config(state='normal')
            self.password_entry.config(state='normal')
            self.product_button.config(state='normal')
            self.full_refresh_button.config(state='normal')
            self.empty_frame.focus()


        else:
            self.logging_info_text.set("Invalid credentials")
            self.logging_info_label.config(fg='red')
            self.email_entry.config(state='normal')
            self.password_entry.config(state='normal')
            self.product_button.config(state='disable')
            self.full_refresh_button.config(state='disable')


    def generate_selected_products(self):
        """Fill the excel file with data for specified products"""
        LabelString.clear_text()
        self.product_text.set("Loading...")
        self.product_button.config(state='disable')
        self.full_refresh_button.config(state='disable')
        self.product_label.update_idletasks()

        # update the excel file here
        with open('products.json') as f:
            all_products = json.load(f)


        a = ExcelFile('team_lista.xlsx', 'produkty')

        current_products_list = a.list_all_products()
        #tutaj jak sie wyciagnie obecne produkty to strzal do api z nimi
        
        current_products = []

        for product in all_products:
            if product['product_code'] in current_products_list:
                current_products.append(product)

        a.update_file(current_products)
        
        try:
            a.save_file()
            self.product_text.set("Done!")
        except PermissionError:
            self.product_text.set("Please close the file!")
        self.product_button.config(state='normal')
        self.full_refresh_button.config(state='normal')


    def generate_all_products(self):
        """Fill the excel file with data for all products"""
        LabelString.clear_text()             
        self.full_refresh_text.set("Loading...")
        self.product_button.config(state='disable')
        self.full_refresh_button.config(state='disable')
        self.full_refresh_label.update_idletasks()


        try:
            a = ExcelFile('team_lista.xlsx', 'produkty')
            a.save_file() # check if file is accessable before processing

            self.data_products = api.get_products(token=self.token)

            a.update_all_products(self.data_products)

            self.full_refresh_text.set("Done!")
            self.product_button.config(state='normal')
            self.full_refresh_button.config(state='normal')
            a.save_file()
        except PermissionError:
            self.full_refresh_text.set("Please close the file!")


        # update the excel file here
        # with open('products.json') as f:
        #     all_products = json.load(f)




class LabelString(tk.StringVar):
    """String creator for tk objects"""
    objs = []

    def __init__(self):
        super().__init__()
        LabelString.objs.append(self)

    @classmethod
    def clear_text(cls):
        """Reset to empty string all instances"""
        for obj in cls.objs:
            obj.set("")



# if __name__ == '__main__':
#     a = LoginForm()
#     a.mainloop()

a = LoginForm()
a.mainloop()
