from openpyxl import load_workbook


class ExcelFile:
    """ Load the template xlsx file which contains product_code list
    and update appropriate cells using the data from the api call
    """

    NOT_FOUND_ITEM = '<not found>'

    def __init__(self, filename, sheet, target_filename):
        self.filename = filename
        self.target_filename = target_filename
        self.wb = load_workbook(self.filename)
        self.sheet = self.wb[sheet]

        self.column_names_dict = {column_name.value: column_name.column
                                for column_name in self.sheet[1]} #for now assume column names are in 1st row

        self.product_codes_dict = {
            product_code.value: product_code.row
            for product_code in self.sheet[self.column_names_dict['product_code']]
            }


    def update_line(self, product):
        _current_product_code = str(self.product_codes_dict[product['product_code']])

        for item in self.column_names_dict:
            self.sheet[self.column_names_dict[item] + _current_product_code] \
             = product[item] if item in product else self.NOT_FOUND_ITEM

    def save_file(self):
        self.wb.save(self.target_filename)
            


odp = {
    'product_code':'prod2',
    'colour':'red',
    'feature':'nice',
    'price':10,
    'nowy':0
}



a = ExcelFile('test.xlsx', 'test', 'final.xlsx')


a.update_line(odp)

a.save_file()
