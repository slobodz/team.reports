import tkinter as tk
import time

class SampleApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.main_frame = tk.Frame(self, bd=5)

        self.product_label = tk.Label(self.main_frame, text="")
        self.product_button = tk.Button(self.main_frame, text="Generate report for\nselected products", width=25, state='disabled', command=self.generate_selected_products)
        self.full_refresh_label = tk.Label(self.main_frame, text="")
        self.full_refresh_button = tk.Button(self.main_frame, text="Generate report for\nall products", width=25, state='disabled', command=self.generate_all_products)



class Parent():
    def test_text(self):
        return('this is test')

class Child(Parent):
    pass





def main():
    app = SampleApp()
    app.mainloop()  
    return 0

if __name__ == '__main__':
    main()