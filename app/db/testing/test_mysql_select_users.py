# -*- coding: utf-8 -*-
import unittest
import sys
sys.path.insert(0, '/app/db')
from dbfunc import str_build_num

class InputNumTest(unittest.TestCase):

    def test_str_build_num_None(self):
        res = str_build_num()
        self.assertEqual(res,( 0,'0'))

    def test_str_build_num_empty(self):
        res = str_build_num('')
        self.assertEqual(res,( 0,'0'))

    def test_str_build_num_space(self):
        res = str_build_num(' ')
        self.assertEqual(res,( 0, ' '))

    def test_str_build_num_str(self):
        res = str_build_num('a')
        self.assertEqual(res,( 0, 'a'))

    def test_str_build_num_str2(self):
        res = str_build_num('aa')
        self.assertEqual(res,( 0, 'aa'))

    def test_str_build_num_str3(self):
        res = str_build_num('abc')
        self.assertEqual(res,( 0, 'abc'))

    def test_str_build_num_int(self):
        res = str_build_num('123')
        self.assertEqual(res,( 123,'0'))

    def test_str_build_num_str_int(self):
        res = str_build_num('a1')
        self.assertEqual(res,( 0, 'a1'))

    def test_str_build_num_int_str(self):
        res = str_build_num('2a')
        self.assertEqual(res,( 2, 'a'))

    def test_str_build_num_int2_str(self):
        res = str_build_num('12a')
        self.assertEqual(res,( 12, 'a'))

    def test_str_build_num_int3_str(self):
        res = str_build_num('123a')
        self.assertEqual(res,( 123, 'a'))

    def test_str_build_num_int3_str2(self):
        res = str_build_num('123ab')
        self.assertEqual(res,( 123, 'ab'))

    def test_str_build_num_zero2(self):
        res = str_build_num('00')
        self.assertEqual(res,( 0,'0'))

    def test_str_build_num_zero001(self):
        res = str_build_num('001')
        self.assertEqual(res,( 1,'0'))


if __name__ == '__main__':
        unittest.main()
