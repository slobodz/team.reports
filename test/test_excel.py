import unittest
import os
from teamreports.excel import ExcelFile



class TestExcel(unittest.TestCase):
    
    def setUp(self):
        os.chdir(os.path.dirname(__file__))

    def test_column_names_dict(self):
        a = ExcelFile('test_column_names_dict.xlsx', 'Arkusz1')
        self.assertEqual(a.column_names_dict, {'col1': 'A', 'col2': 'B', 'col3': 'C', 'product_code': 'D'})


    def test_no_product_code_column(self):
        self.assertRaises(KeyError, ExcelFile, 'test_no_product_code_column.xlsx', 'Arkusz1')


    def test_product_codes_dict(self):
        a = ExcelFile('test_product_codes_dict.xlsx', 'Arkusz1')
        self.assertEqual(a.product_codes_dict, {'prod1':2, 'prod2':3, 'prod3':4})


    def test_list_all_product_codes(self):
        a = ExcelFile('test_product_codes_dict.xlsx', 'Arkusz1')
        self.assertEqual(a.list_all_products(), ['prod1', 'prod2', 'prod3'])


    def test_update_single_product(self):
        a = ExcelFile('test_update_single_product.xlsx', 'Arkusz1')
        product = {
            'a':10,
            'b':20,
            'c':30,
            'product_code':'prod3'
        }
        a.update_line(product)

        b = ExcelFile('test_update_single_product.xlsx', 'Arkusz2')

        a_values = list(a.sheet.values)
        b_values = list(b.sheet.values)

        self.assertEqual(a_values, b_values)


if __name__ == '__main__':
    unittest.main()

