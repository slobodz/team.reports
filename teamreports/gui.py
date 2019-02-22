import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from threading import Timer
import json
import requests as r
import time
from teamreports.api import ApiClient
from teamreports import app_config
from teamreports.excel import ExcelFile


URL = app_config.URL

class LoginForm(tk.Tk):
    def __init__(self):
        """Create an app window with login gui"""
        super().__init__()

        self.title("Team Reports")

        #select environment to connect
        self.environment_list = ('PRD', 'UAT')

        #types of images to download from teamservices
        self.image_types_list = ('wbc', 'undefined', 'offer', 'boxoffer', 'arr', 'iwbc', 'ico', 'fnk', 'threedbox', 'threedprod',
                                'threedpallet', 'threedmix', 'mix', 'png', 'fbk', 'real', 'baner', 'sqr')
        #languages for lexicons
        self.languages_list = ('pl-PL', 'en-EN', 'de-DE', 'fr-FR')



        self.logging_info_text = LabelString()
        self.product_text = LabelString()
        self.full_refresh_text = LabelString()

        self.image_type_value = tk.StringVar()
        self.language_value = tk.StringVar()
        self.environment_value = tk.StringVar()


        #level 1
        self.top_frame = tk.Frame(self, bd=5)
        #level 2
        self.login_frame = tk.Frame(self.top_frame, bd=5)
        #level 3
        self.email_label = tk.Label(self.login_frame, text="Email", width=25)
        self.email_entry = tk.Entry(self.login_frame, bg="white", fg="black", width=25)
        self.password_label = tk.Label(self.login_frame, text="Password", width=25)
        self.password_entry = tk.Entry(self.login_frame, bg="white", fg="black", show='*', width=25)
        self.logging_info_label = tk.Label(self.login_frame, textvariable=self.logging_info_text, width=25)
        self.submit_button = tk.Button(self.login_frame, text="Log In", command=self.submit, width=25)

        #level 2
        self.empty_frame = tk.Frame(self.top_frame, width=15, bd=5)
        self.main_frame = tk.Frame(self.top_frame, bd=5)
        #level 3
        self.product_label = tk.Label(self.main_frame, textvariable=self.product_text)
        self.product_button = tk.Button(self.main_frame, text="Generate report for\nselected products",
                                        width=25, state='disabled', command=self.generate_selected_products)
        self.full_refresh_label = tk.Label(self.main_frame, textvariable=self.full_refresh_text)
        self.full_refresh_button = tk.Button(self.main_frame, text="Generate report for\nall products",
                                        width=25, state='disabled', command=self.generate_all_products)        


        #level 1
        self.bottom_frame = tk.Frame(self, bd=5)
        #level 2
        self.options_separator = tk.Frame(self.bottom_frame, height=2, bg='grey')
        self.options_label = tk.Label(self.bottom_frame, text="Options")        
        self.options_dropdown1_frame = tk.Frame(self.bottom_frame, bd=5)
        #level 3
        self.image_types_dd = ttk.Combobox(self.options_dropdown1_frame, textvariable=self.image_type_value,
                                        values=self.image_types_list, state='readonly')
        self.image_types_dd.current(0)
        self.image_types_label = tk.Label(self.options_dropdown1_frame, text="Image type:", width=10, anchor='e')

        #level 2
        self.options_dropdown2_frame = tk.Frame(self.bottom_frame, bd=5)
        #level 3
        self.languages_dd = ttk.Combobox(self.options_dropdown2_frame, textvariable=self.language_value,
                                        values=self.languages_list, state='readonly')
        self.languages_dd.current(0)
        self.languages_label = tk.Label(self.options_dropdown2_frame, text="Languages:", width=10, anchor='e')

        #level 2
        self.options_dropdown3_frame = tk.Frame(self.bottom_frame, bd=5)
        #level 3
        self.environment_dd = ttk.Combobox(self.options_dropdown3_frame, textvariable=self.environment_value,
                                        values=self.environment_list, state='readonly')
        self.environment_dd.current(0)
        self.environment_label = tk.Label(self.options_dropdown3_frame, text="Environment:", width=10, anchor='e')


        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)        

        self.login_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.empty_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)        
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

        self.options_separator.pack(side=tk.TOP, fill=tk.BOTH, expand=0)
        self.options_label.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.options_dropdown3_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1) #environments
        self.options_dropdown1_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1) #img types
        self.options_dropdown2_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1) #languages


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

        self.environment_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=0)
        self.environment_dd.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)        
        self.image_types_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=0)
        self.image_types_dd.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
        self.languages_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=0)
        self.languages_dd.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

    def close_session(self):
        """Disable generate buttons so have to login again.
        This is triggered after 30 mins"""
        self.product_button.config(state='disabled')
        self.full_refresh_button.config(state='disabled')
        self.logging_info_text.set("Please log in again")
        self.logging_info_label.config(fg='black')

    def submit(self):
        """Send post request with credentials"""
        LabelString.clear_text()
        self.email_entry.config(state='disable')
        self.password_entry.config(state='disable')
        self.email = self.email_entry.get()
        self.password = self.password_entry.get()
        self.submit_button.update_idletasks()


        #init ApiClient instance to work with
        self.api_client = ApiClient(email=self.email, password=self.password)

        if(self.api_client.token_call.ok):
            self.t = Timer(1800, self.close_session)
            self.t.start()

            self.logging_info_text.set("Logged in")
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
        self.image_types_dd.config(state='disable')
        self.languages_dd.config(state='disable')
        self.environment_dd.config(state='disable')
        self.product_label.update_idletasks()

        try:
            a = ExcelFile(target_filename='report_' + time.strftime('%Y%m%d_%H%M%S') + '.xlsx')
            a.save_file(skip_delete=True) # check if file is accessable before processing

            selected_products = a.list_all_products()

            #send requests for each product
            data_products = self.api_client.get_selected_products(product_code_list=selected_products,
                                        img_type=self.image_types_dd.get(), language=self.languages_dd.get())

            a.update_file_with_selected_products(data_products)

            self.product_text.set("Done!")
            self.product_button.config(state='normal')
            self.full_refresh_button.config(state='normal')
            self.image_types_dd.config(state='readonly')
            self.languages_dd.config(state='readonly')
            self.environment_dd.config(state='readonly')
            a.save_file()
        except PermissionError:
            self.product_text.set("Please close the file!")
            self.product_button.config(state='normal')
            self.full_refresh_button.config(state='normal')
        except Exception as e:
            self.product_text.set("Error, try again")
            self.product_button.config(state='normal')
            self.full_refresh_button.config(state='normal')
            self.f = open('log.txt', 'w')
            self.f.write(e)
            self.f.close()


    def generate_all_products(self):
        """Fill the excel file with data for all products"""
        LabelString.clear_text()             
        self.full_refresh_text.set("Loading...")
        self.product_button.config(state='disable')
        self.full_refresh_button.config(state='disable')
        self.image_types_dd.config(state='disable')
        self.languages_dd.config(state='disable')
        self.environment_dd.config(state='disable')
        self.full_refresh_label.update_idletasks()


        try:
            a = ExcelFile(target_filename='report_' + time.strftime('%Y%m%d_%H%M%S') + '.xlsx')
            a.save_file() # check if file is accessable before processing

            data_products = self.api_client.get_all_products(img_type=self.image_types_dd.get(), language=self.languages_dd.get())

            #populate file with all possible products available for current user(token)
            a.update_all_products(data_products)

            self.full_refresh_text.set("Done!")
            self.product_button.config(state='normal')
            self.full_refresh_button.config(state='normal')
            self.image_types_dd.config(state='readonly')
            self.languages_dd.config(state='readonly')
            self.environment_dd.config(state='readonly')                       
            a.save_file()
        except PermissionError:
            self.full_refresh_text.set("Please close the file!")
            self.product_button.config(state='normal')
            self.full_refresh_button.config(state='normal')
        except Exception as e:
            self.full_refresh_text.set("Error, try again")
            self.product_button.config(state='normal')
            self.full_refresh_button.config(state='normal')
            print(e)
            self.f = open('log.txt', 'w')
            self.f.write(str(e))
            self.f.close()

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

