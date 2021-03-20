# coding=utf-8
"""
Author: Liang Ziyi
Date: 2021/3/20
Title: Dictionary based on hash-map (mutable_test)
"""

import unittest
from src.Lab1.mutable import *
from hypothesis import given
import hypothesis.strategies as st


class TestMutableList(unittest.TestCase):
    def test_get_value(self):
        hash = HashMap()
        self.assertEqual(hash.get_value(5), 5)
        self.assertEqual(hash.get_value(24), 4)

    def test_add(self):
        hash = HashMap()
        hash.add(2, 6)
        self.assertEqual(hash.find(2), 6)
        self.assertEqual(hash.to_dict(), {2: 6})
        hash.add(4, 5)
        self.assertEqual(hash.find(4), 5)
        hash.add(1, 5)
        self.assertEqual(hash.find(1), 5)

    def test_remove(self):
        hash = HashMap()
        dict1 = {1: 2, 2: 4, 3: 6}
        hash.from_dict(dict1)
        hash.remove(1)
        dict2 = {2: 4, 3: 6}
        self.assertEqual(hash.to_dict(), dict2)

    def test_get(self):
        hash = HashMap()
        hash.add(1, 5)
        hash.add(2, 10)
        hash.add(4, 5)
        hash.add(5, 10)
        self.assertEqual(hash.find(1), 5)
        self.assertEqual(hash.find(2), 10)
        self.assertEqual(hash.find(4), 5)
        self.assertEqual(hash.find(5), 10)

    def test_remove_key_set(self):
        hash = HashMap()
        self.assertEqual(hash.key_set, [])
        hash.from_dict({1: 2, 2: 4, 3: 6})
        self.assertEqual(hash.key_set, [1, 2, 3])
        hash.remove_key_set(1)
        self.assertEqual(hash.key_set, [2, 3])

    def test_from_dict(self):
        hash = HashMap()
        dict = {1: 2, 2: 4, 3: 6, 4: 8}
        hash.from_dict(dict)
        self.assertEqual(hash.find(4), 8)
        self.assertEqual(hash.find(3), 6)

    def test_to_dict(self):
        hash = HashMap()
        hash.add(1, 2)
        hash.add(2, 4)
        hash.add(3, 6)
        hash.add(4, 8)
        hash.to_dict()
        self.assertEqual(hash.to_dict(), {1: 2, 2: 4, 3: 6, 4: 8})

    def test_get_size(self):
        hash = HashMap()
        self.assertEqual(hash.get_size(), 0)
        hash.add(1, 2)
        self.assertEqual(hash.get_size(), 1)
        hash.add(14, 2)
        self.assertEqual(hash.get_size(), 2)
        hash.add(1, 3)  # test for same key, new value alter the old one
        self.assertEqual(hash.get_size(), 2)

    def test_from_list(self):
        test_data = [
            [],
            ['a', 'b', 'c'],
            ['0', '11', '111'],
            [1, 2, 3],
            [None]
        ]
        for e in test_data:
            hash = HashMap()
            hash.from_list(e)
            self.assertEqual(hash.to_list(), e)

    def test_to_list(self):
        hash = HashMap()
        dict = {1: 2, 2: 4, 3: 6, 4: 8}
        hash.from_dict(dict)
        self.assertEqual(hash.to_list(), [2, 4, 6, 8])

    def test_find_iseven(self):
        hash = HashMap()
        hash.from_list(['a', 1, 2, 3.14, 'b', 4, 5, 'c', 6.0, 7, 8])
        self.assertEqual(hash.to_list(), ['a', 1, 2, 3.14, 'b', 4, 5, 'c', 6.0, 7, 8])
        self.assertEqual(hash.find_iseven(), [2, 4, 6.0, 8])

    def test_filter_iseven(self):
        hash = HashMap()
        hash.from_list(['a', 1, 2, 3.14, 'b', 4, 5, 'c', 6.0, 7, 8])
        self.assertEqual(hash.to_list(), ['a', 1, 2, 3.14, 'b', 4, 5, 'c', 6.0, 7, 8])
        self.assertEqual(hash.filter_iseven(), ['a', 1, 3.14, 'b', 5, 'c', 7])

    def test_map(self):
        dict1 = {1: 2, 2: 4}
        dict2 = {1: '2', 2: '4'}
        hash = HashMap()
        hash.from_dict(dict1)
        self.assertEqual(hash.map(str), dict2)

    def test_reduce(self):
        hash = HashMap()
        self.assertEqual(hash.reduce(lambda st, e: st + e, 0), 0)
        dict1 = {1: 2, 2: 4}
        hash1 = HashMap()
        hash1.from_dict(dict1)
        self.assertEqual(hash1.reduce(lambda st, e: st + e, 0), 6)

    def test_hash_collision(self):
        hash1 = HashMap()
        hash2 = HashMap()
        hash1.add(1, 777)
        hash2.add(11, 777)
        self.assertEqual(hash1.get_value(1), hash2.get_value(11))

    def test_iter(self):
        dict1 = {1: 2, 2: 4, 3: 6, 4: 8}
        table = HashMap()
        table.from_dict(dict1)
        tmp = {}
        for e in table:
            tmp[e.key] = e.value
        self.assertEqual(table.to_dict(), tmp)
        i = iter(HashMap())
        self.assertRaises(StopIteration, lambda: next(i))

    @given(a=st.lists(st.integers()))
    def test_monoid_identity(self, a):
        hash = HashMap()
        hash_a = HashMap()
        hash_a.from_list(a)
        self.assertEqual(hash.mconcat(hash.mempty(), hash_a), hash_a)
        self.assertEqual(hash.mconcat(hash_a, hash.mempty()), hash_a)

    @given(a=st.lists(st.integers()), b=st.lists(st.integers()), c=st.lists(st.integers()))
    def test_monoid_associativity(self, a, b, c):
        hash = HashMap()
        hash_a = HashMap()
        hash_b = HashMap()
        hash_c = HashMap()
        # add list to HashMap
        hash_a.from_list(a)
        hash_b.from_list(b)
        hash_c.from_list(c)
        # (a·b)·c
        a_b = hash.mconcat(hash_a, hash_b)
        ab_c = hash.mconcat(a_b, hash_c)
        # a·(b·c)
        b_c = hash.mconcat(hash_b, hash_c)
        a_bc = hash.mconcat(hash_a, b_c)
        self.assertEqual(ab_c, a_bc)

    @given(st.lists(st.integers()))
    def test_from_list_to_list_equality(self, a):
        hash = HashMap()
        hash.from_list(a)
        b = hash.to_list()
        self.assertEqual(a, b)

    @given(st.lists(st.integers()))
    def test_python_len_and_list_size_equality(self, a):
        hash = HashMap()
        hash.from_list(a)
        self.assertEqual(hash.get_size(), len(a))

    @given(st.lists(st.integers()))
    def test_from_list(self, a):
        hash = HashMap()
        hash.from_list(a)
        self.assertEqual(hash.to_list(), a)

if __name__ == '__main__':
    unittest.main()