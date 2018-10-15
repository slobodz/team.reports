import unittest
import os
from team.reports.excel import ExcelFile



class TestExcel(unittest.TestCase):
    
    def setUp(self):
        os.chdir(os.path.dirname(__file__))

    def test_init(self):
        a = ExcelFile('sample_excel.xlsx', 'Arkusz1', 'test')
        self.assertEqual(a.column_names_dict, {'a': 'A', 'b': 'B', 'product_code': 'C', 'd': 'D', 'e': 'E'})




if __name__ == '__main__':
    unittest.main()

