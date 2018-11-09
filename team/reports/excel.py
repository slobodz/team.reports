from openpyxl import load_workbook
import json


class ExcelFile:
    """ Load the template xlsx file which contains product_code list
    and update appropriate cells using the data from the api call
    """

    NOT_FOUND_ITEM = '<not found>'
    PRODUCT_CODE = 'product_code'

    def __init__(self, filename, sheet, target_filename=None):
        self.filename = filename
        self.target_filename = target_filename if target_filename is not None else filename
        self.wb = load_workbook(self.filename)
        self.sheet = self.wb[sheet]
        

        self.column_names_dict = {column_name.value: column_name.column
                                for column_name in self.sheet[1]} #for now assume column names are in 1st row

        if self.PRODUCT_CODE not in self.column_names_dict:
            raise KeyError("Column names not in first row")

        self.product_codes_dict = {
            product_code.value: product_code.row
            for product_code in self.sheet[self.column_names_dict[self.PRODUCT_CODE]] if product_code.row != 1
            }


    def update_line(self, product, row=None):
        _current_product_code = str(self.product_codes_dict[product[self.PRODUCT_CODE]]) if row is None \
                                else str(row)

        for item in self.column_names_dict:
            self.sheet[self.column_names_dict[item] + _current_product_code] \
             = product[item] if item in product else self.NOT_FOUND_ITEM


    def update_file(self, product_list):
        for product in product_list:
            self.update_line(product)


    def list_all_products(self):
        return [product_code for product_code in self.product_codes_dict]


    def save_file(self):
        self.wb.close()
        self.wb.save(self.target_filename)


    def update_all_products(self, product_list):
        _product_code_column = self.column_names_dict[self.PRODUCT_CODE]

        for row, product in enumerate(product_list, 2):
            self.sheet[_product_code_column + str(row)] = product[self.PRODUCT_CODE]
            self.update_line(product, row=row)




        



if __name__ == '__main__':


    with open('products.json') as f:
        all_products = json.load(f)


    a = ExcelFile('team_lista.xlsx', 'produkty')

    a.update_file(all_products)
    a.save_file()
