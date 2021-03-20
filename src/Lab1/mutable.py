# coding=utf-8
"""
Author: Liang Ziyi
Date: 2021/3/20
Title: Dictionary based on hash-map (mutable)
"""


class Node(object):
    def __init__(self, key, value, next=None):
        self.key = key
        self.value = value
        self.next = next


class HashMap(object):

    empty = object()

    def __init__(self, dict=None):
        self.key_set = []
        self.size = 10
        self.data = [self.empty for _ in range(10)]

        # Initialize dict
        if dict is not None:
            self.from_dict(self, dict)

        self.len = 0
        self.index = 0

    # get hash value
    def get_value(self, key):
        hash_value = key % self.size
        return hash_value

    # insert key-value pairs into hash map
    def add(self, key, value):
        hash_value = self.get_value(key)
        kv_entry = Node(key, value)

        if self.data[hash_value] == self.empty:
            self.data[hash_value] = kv_entry
            self.key_set.append(key)
            self.len = self.len + 1
        else:  # collision resolution: separate chaining
            f = self.data[hash_value]
            while f.next is not None:
                if f.key is key:
                    f.value = value
                    return
                f = f.next
            if f.key is key:
                f.value = value
                return
            f.next = kv_entry
            self.key_set.append(key)
            self.len = self.len + 1

    # remove element in hash map by key
    def remove(self, key):
        hash_value = self.get_value(key)
        if self.data[hash_value] is self.empty:
            return False
        elif self.data[hash_value].key is key:
            self.data[hash_value] = self.data[hash_value].next
            self.remove_key_set(key)
            return True
        p = self.data[hash_value]
        q = self.data[hash_value].next
        while q.next is not None:
            if q.key is key:
                p.next = q.next
                self.remove_key_set(key)
                return True
            p = q
            q = q.next
        if q.key is key:
            p.next = None
            self.remove_key_set(key)
            return True
        return False

    # find element in hash map by key
    def find(self, key):
        myDict = self.to_dict()
        value = myDict[key]
        return value

    def remove_key_set(self, key):
        self.key_set.remove(key)
        self.len = self.len - 1

    def from_dict(self, dict):
        for k, v in dict.items():
            self.add(k, v)

    # transfer hash map into dict
    def to_dict(self):
        myDict = {}
        if self.len == 0:
            return myDict
        else:
            i = 0
            while i < self.size:
                if self.data[i] is self.empty:
                    i += 1
                    continue
                else:
                    p = self.data[i]
                    while p is not None:
                        myDict[p.key] = p.value
                        p = p.next
                    i += 1
        return myDict

    # element number in hash map
    def get_size(self):
        size = len(self.key_set)
        return size

    # transfer hash map into list type
    def to_list(self):
        list = []
        for key in self.key_set:
            list.append(self.find(key))
        return list

    # add element from list type
    def from_list(self, list):
        for key, value in enumerate(list):
            self.add(key, value)

    # find element with even value in hash map.
    def find_iseven(self):
        list = self.to_list()
        my_list = []
        for value in list:
            if type(value) is int or type(value) is float:
                if value % 2 == 0:
                    my_list.append(value)
        return my_list

    # filter element with even value in hash map.
    def filter_iseven(self):
        list = self.to_list()
        for value in list:
            if type(value) is int or type(value) is float:
                if value % 2 == 0:
                    list.remove(value)
        return list

    # list to store all node in hash map by key&value
    def to_kv_entry_list(self):
        list = []
        for key in self.key_set:
            list.append(Node(key, self.find(key)))
        return list

    # map element value in hash map with f
    def map(self, f):
        dict = {}
        for key in self.key_set:
            value = f(self.find(key))
            dict[key] = value
        return dict

    #  build a return value by specific functions(f)
    def reduce(self, f, initial_state):
        state = initial_state
        for key in self.key_set:
            value = self.find(key)
            state = f(state, value)
        return state

    def mempty(self):
        return None

    def mconcat(self, a, b):
        if a is None:
            return b
        if b is None:
            return a
        for key in b.key_set:
            value = b.find(key)
            a.add(key, value)
        return a

    def __iter__(self):
        return iter(self.to_kv_entry_list())

    def __next__(self):
        if self.index >= self.len:
            raise StopIteration("end")
        else:
            self.index += 1
            val = self.find(self.key_set[self.index - 1])
            return val
