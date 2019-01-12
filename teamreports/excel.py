from openpyxl import load_workbook
from openpyxl.drawing.image import Image as exImage
import json
from PIL import Image
from io import BytesIO
import os

class ExcelFile:
    """ Load the template xlsx file which contains product_code list
    and update appropriate cells using the data from the api call
    """

    NOT_FOUND_ITEM = '<not found>'
    PRODUCT_CODE = 'product_code'
    PHOTO_CODE = 'photo'
    TEMPLATE_FILE_NAME = 'template.xlsx'
    TEMPLATE_SHEET_NAME = 'products'
    TEMP_IMG_FILE_NAME = 'temp.jpeg'

    def __init__(self, filename=TEMPLATE_FILE_NAME, sheet=TEMPLATE_SHEET_NAME, target_filename=None):
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
            for product_code in self.sheet[self.column_names_dict[self.PRODUCT_CODE]]
            if product_code.row != 1 and product_code.value is not None
            }


    def update_line(self, product, row=None):
        _current_row = self.product_codes_dict[product[self.PRODUCT_CODE]] if row is None else row

        for item in self.column_names_dict:
            _current_column = self.column_names_dict[item]
            _current_cell = _current_column + str(_current_row)
            if(item == self.PHOTO_CODE and item in product):
                img = Image.open(BytesIO(product[item])) #change bytes from request into image obj
                img.save(self.TEMP_IMG_FILE_NAME) #save image on the disk
                img = exImage(self.TEMP_IMG_FILE_NAME) #locate image using openpyxl
                self.sheet.column_dimensions[_current_column].width = (img.width/7) #experimental
                self.sheet.row_dimensions[_current_row].height = (img.height *0.75) #experimental  
                self.sheet.add_image(img, _current_cell) #insert image
            else:
                self.sheet[_current_cell] = product[item] if item in product else self.NOT_FOUND_ITEM


    def update_file_with_selected_products(self, product_list):
        for product in product_list:
            self.update_line(product)


    def list_all_products(self):
        return [product_code for product_code in self.product_codes_dict]


    def save_file(self):
        self.wb.close()
        self.wb.save(self.target_filename)
        if os.path.exists(self.TEMP_IMG_FILE_NAME):
            os.remove(self.TEMP_IMG_FILE_NAME)


    def update_all_products(self, product_list):
        _product_code_column = self.column_names_dict[self.PRODUCT_CODE]

        for row, product in enumerate(product_list, 2):
            self.sheet[_product_code_column + str(row)] = product[self.PRODUCT_CODE]
            self.update_line(product, row=row)




        



# if __name__ == '__main__':


#     with open('products.json') as f:
#         all_products = json.load(f)


#     a = ExcelFile('team_lista.xlsx', 'produkty')

#     a.update_file(all_products)
#     a.save_file()
