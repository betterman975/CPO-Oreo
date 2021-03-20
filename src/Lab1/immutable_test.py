# coding=utf-8
"""
Author: Liang Ziyi
Date: 2021/3/20
Title: Dictionary based on hash-map (immutable_test)
"""

import unittest
from src.Lab1.immutable import *
from hypothesis import given
import hypothesis.strategies as st


class TestImmutableList(unittest.TestCase):
    def test_get_value(self):
        hash = HashMap()
        self.assertEqual(get_value(hash, 5), 5)
        self.assertEqual(get_value(hash, 24), 4)

    def test_add(self):
        hash = HashMap()
        add(hash, 2, 6)
        self.assertEqual(find(hash, 2), 6)
        self.assertEqual(to_dict(hash), {2: 6})
        add(hash, 4, 5)
        self.assertEqual(find(hash, 4), 5)
        add(hash, 1, 5)
        self.assertEqual(find(hash, 1), 5)

    def test_remove(self):
        hash = HashMap()
        dict1 = {1: 2, 2: 4, 3: 6}
        from_dict(hash, dict1)
        remove(hash, 1)
        dict2 = {2: 4, 3: 6}
        self.assertEqual(to_dict(hash), dict2)

    def test_get(self):
        hash = HashMap()
        add(hash, 1, 5)
        add(hash, 2, 10)
        add(hash, 4, 5)
        add(hash, 5, 10)
        self.assertEqual(find(hash, 1), 5)
        self.assertEqual(find(hash, 2), 10)
        self.assertEqual(find(hash, 4), 5)
        self.assertEqual(find(hash, 5), 10)

    def test_remove_key_set(self):
        hash = HashMap()
        self.assertEqual(hash.key_set, [])
        from_dict(hash, {1: 2, 2: 4, 3: 6})
        self.assertEqual(hash.key_set, [1, 2, 3])
        remove_key_set(hash, 1)
        self.assertEqual(hash.key_set, [2, 3])

    def test_from_dict(self):
        hash = HashMap()
        dict = {1: 2, 2: 4, 3: 6, 4: 8}
        from_dict(hash, dict)
        self.assertEqual(find(hash, 4), 8)
        self.assertEqual(find(hash, 3), 6)

    def test_to_dict(self):
        hash = HashMap()
        add(hash, 1, 2)
        add(hash, 2, 4)
        add(hash, 3, 6)
        add(hash, 4, 8)
        to_dict(hash)
        self.assertEqual(to_dict(hash), {1: 2, 2: 4, 3: 6, 4: 8})

    def test_get_size(self):
        hash = HashMap()
        self.assertEqual(get_size(hash), 0)
        add(hash, 1, 2)
        self.assertEqual(get_size(hash), 1)
        add(hash, 14, 2)
        self.assertEqual(get_size(hash), 2)

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
            from_list(hash, e)
            self.assertEqual(to_list(hash), e)

    def test_to_list(self):
        hash = HashMap()
        dict = {1: 2, 2: 4, 3: 6, 4: 8}
        from_dict(hash, dict)
        self.assertEqual(to_list(hash), [2, 4, 6, 8])

    def test_find_iseven(self):
        hash = HashMap()
        from_list(hash, ['a', 1, 2, 3.14, 'b', 4, 5, 'c', 6.0, 7, 8])
        self.assertEqual(to_list(hash), ['a', 1, 2, 3.14, 'b', 4, 5, 'c', 6.0, 7, 8])
        self.assertEqual(find_iseven(hash), [2, 4, 6.0, 8])

    def test_filter_iseven(self):
        hash = HashMap()
        from_list(hash, ['a', 1, 2, 3.14, 'b', 4, 5, 'c', 6.0, 7, 8])
        self.assertEqual(to_list(hash), ['a', 1, 2, 3.14, 'b', 4, 5, 'c', 6.0, 7, 8])
        self.assertEqual(filter_iseven(hash), ['a', 1, 3.14, 'b', 5, 'c', 7])

    def test_map(self):
        dict1 = {1: 2, 2: 4}
        dict2 = {1: '2', 2: '4'}
        hash = HashMap()
        from_dict(hash, dict1)
        self.assertEqual(map(hash, str), dict2)

    def test_reduce(self):
        hash = HashMap()
        self.assertEqual(reduce(hash, lambda st, e: st + e, 0), 0)
        dict1 = {1: 2, 2: 4}
        hash1 = HashMap()
        from_dict(hash1, dict1)
        self.assertEqual(reduce(hash1, lambda st, e: st + e, 0), 6)

    def test_hash_collision(self):
        hash1 = HashMap()
        hash2 = HashMap()
        add(hash1, 1, 777)
        add(hash2, 11, 777)
        self.assertEqual(get_value(hash1, 1), get_value(hash2, 11))

    def test_iter(self):
        dict1 = {1: 2, 2: 4, 3: 6, 4: 8}
        table = HashMap()
        from_dict(table, dict1)
        tmp = {}
        for e in table:
            tmp[e.key] = e.value
        self.assertEqual(to_dict(table), tmp)
        i = iter(HashMap())
        self.assertRaises(StopIteration, lambda: next(i))

    @given(a=st.lists(st.integers()))
    def test_monoid_identity(self, a):
        hash = HashMap()
        hash_a = HashMap()
        from_list(hash_a, a)
        self.assertEqual(mconcat(mempty(hash), hash_a), hash_a)
        self.assertEqual(mconcat(hash_a, mempty(hash)), hash_a)

    @given(a=st.lists(st.integers()), b=st.lists(st.integers()), c=st.lists(st.integers()))
    def test_monoid_associativity(self, a, b, c):
        hash = HashMap()
        hash_a = HashMap()
        hash_b = HashMap()
        hash_c = HashMap()
        # add list to HashMap
        from_list(hash_a, a)
        from_list(hash_b, b)
        from_list(hash_c, c)
        # (a·b)·c
        a_b = mconcat(hash_a, hash_b)
        ab_c = mconcat(a_b, hash_c)
        # a·(b·c)
        b_c = mconcat(hash_b, hash_c)
        a_bc = mconcat(hash_a, b_c)
        self.assertEqual(ab_c, a_bc)

    @given(st.lists(st.integers()))
    def test_from_list_to_list_equality(self, a):
        hash = HashMap()
        from_list(hash, a)
        b = to_list(hash)
        self.assertEqual(a, b)

    @given(st.lists(st.integers()))
    def test_python_len_and_list_size_equality(self, a):
        hash = HashMap()
        from_list(hash, a)
        self.assertEqual(get_size(hash), len(a))

    @given(st.lists(st.integers()))
    def test_from_list(self, a):
        hash = HashMap()
        from_list(hash, a)
        self.assertEqual(to_list(hash), a)

    def test_iter(self):
        x = [1, 2, 3]
        hash = HashMap()
        from_list(hash, x)
        tmp = []
        try:
            get_next = iterator(hash)
            while True:
                tmp.append(get_next())
        except StopIteration:
            pass
        self.assertEqual(x, tmp)
        self.assertEqual(to_list(hash), tmp)

        get_next = iterator(None)
        self.assertEqual(get_next(), False)


if __name__ == '__main__':
    unittest.main()