# -*- coding: utf-8 -*-
import unittest
import sys
#sys.path.insert(0, '/app/db')
sys.path.insert(0, '/app/importation')
#from mysql_select_users import input_num
from impfunc import sort_list_num, sort_list_text, select_sbf

class SortListNumTest(unittest.TestCase):

    def test_insortlist_num(self):
        list_obj_num = [ 0 ,2, 12, 23, 112, 104, 10, 110, 2, 1, 20 ];
        res = sort_list_num(list_obj_num)
        self.assertEqual(res, [0, 1, 2, 10, 12, 20, 23, 104, 110, 112] )

    def test_insortlist_num_zero(self):
        res = sort_list_num([0])
        self.assertEqual(res,[0])

    def test_insortlist_num_empty(self):
        res = sort_list_num([])
        self.assertEqual(res,[])

class SortListTextTest(unittest.TestCase):

    def test_sort_list_text(self):
        list_obj_text = ['В','','аб','А','вг','Б','аВ','ав','а','АбВ','7а','77']
        res = sort_list_text(list_obj_text)
        self.assertEqual(res, ['', '77', '7А', 'А', 'Аб', 'Абв','Ав', 'Б', 'В', 'Вг'])

    def test_srt_list_text_empty(self):
        res = sort_list_text([])
        self.assertEqual(res,[])

list_obj_sbf = [{'street': 'Шевченко', 'build': (133, '0'), 'flat': (52, '0')},\
                {'street': 'Власа Волошина', 'build': (33, '0'), 'flat': (13, '0')},\
                {'street': 'Левино', 'build': (1, '0'), 'flat': (27, '0')}]
class SortListStreetBuildFlatTest(unittest.TestCase):

    def test_select_sbf(self):
        res = select_sbf(list_obj_sbf)
        self.assertEqual(res,list_obj_sbf)

    def test_select_sbf_street(self):
        res = select_sbf(list_obj_sbf,item='street')
        self.assertEqual(res,['Власа Волошина', 'Левино', 'Шевченко'])

    def test_select_sbf_build(self):
        res = select_sbf(list_obj_sbf,item='build')
        self.assertEqual(res,[(1, '0'), (33, '0'), (133, '0')])

    def test_select_sbf_flat(self):
        res = select_sbf(list_obj_sbf,item='flat')
        self.assertEqual(res,[(13, '0'), (27, '0'), (52, '0')])

    def test_select_sbf_empty(self):
        res = select_sbf()
        self.assertEqual(res,[])

    def test_select_sbf_empty2(self):
        res = select_sbf('')
        self.assertEqual(res,[])

    def test_select_sbf_empty3(self):
        res = select_sbf([])
        self.assertEqual(res,[])

    def test_select_sbf_err(self):
        res = select_sbf('as3333')
        self.assertEqual(res,[])

    def test_select_sbf_err1(self):
        res = select_sbf(['as3333','e'])
        self.assertEqual(res,[])

    def test_select_sbf_err2(self):
        res = select_sbf(('as3333','e'))
        self.assertEqual(res,[])

    def test_select_sbf_err3(self):
        res = select_sbf({'as3333','e'})
        self.assertEqual(res,[])

    def test_select_sbf_err4(self):
        res = select_sbf({'as3333':'e'})
        self.assertEqual(res,[])

    def test_select_sbf_err5(self):
        res = select_sbf({'as3333':'e'}, item='1w')
        self.assertEqual(res,[])

if __name__ == '__main__':
    unittest.main()
