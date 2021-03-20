# coding=utf-8
"""
Author: Liang Ziyi
Date: 2021/3/20
Title: Dictionary based on hash-map (immutable)
"""


class Node(object):
    def __init__(self, key=None, value=None, next=None):
        self.key = key
        self.value = value
        self.next = next


class HashMap(object):

    def __init__(self, dict=None):
        self.key_set = []
        self.size = 10
        self.data = [Node() for _ in range(10)]

        # Initialize dict
        if dict is not None:
            self.from_dict(self, dict)


# get hash value
def get_value(hash, key):
    hash_value = key % hash.size
    return hash_value


# insert key-value pairs into hash map
def add(hash, key, value) -> HashMap:
    if hash is None:
        hash = HashMap()
    hash_value = get_value(hash, key)
    if hash.data[hash_value].key is None:
        hash.data[hash_value].value = value
        hash.data[hash_value].key = key
        hash.key_set.append(key)
    else:
        temp = Node(key, value)
        hash.key_set.append(key)
        p = hash.data[hash_value]
        while p.next is not None:
            p = p.next
        p.next = temp
    return hash


# remove element in hash map by key
def remove(hash, key) -> HashMap:
    if hash is None:
        return None
    hash_value = get_value(hash, key)
    if hash.data[hash_value].value is None:
        raise Exception('No valid key value was found')
    else:
        p = hash.data[hash_value]
        if key == p.key:
            if p.next is None:
                p.key = None
                p.value = None
            else:
                temp = p.next
                p.key = temp.key
                p.value = temp.value
                p.next = temp.next
            remove_key_set(hash, key)
            return hash
        else:
            while p is not None:
                if p.key == key:
                    temp = p.next
                    p.next = temp.next
                    remove_key_set(hash, key)
                    return hash
                else:
                    p = p.next
    raise Exception('No valid key value was found')


# find element in hash map by key
def find(hash, key: int) -> object:
    if hash.key_set is None:
        return None
    i = 0
    while i < hash.size:
        if hash.data[i].key is None:
            i += 1
            continue
        else:
            p = hash.data[i]
            while p is not None:
                if p.key == key:
                    return p.value
                p = p.next
            i += 1
    return i


def remove_key_set(hash, key):
    for i, k in enumerate(hash.key_set):
        if key == k:
            arr = hash.key_set
            del arr[i]
            return hash


def from_dict(hash, dict):
    for k, v in dict.items():
        add(hash, k, v)


# transfer hash map into dict
def to_dict(hash) -> {}:
    myDict = {}
    if hash is None:
        return myDict
    else:
        i = 0
        while i < hash.size:
            if hash.data[i].value is None:
                i += 1
                continue
            else:
                p = hash.data[i]
                while p is not None:
                    myDict[p.key] = p.value
                    p = p.next
                i += 1
    return myDict


# element number in hash map
def get_size(hash) -> int:
    sum = 0
    i = 0
    while i < hash.size:
        if hash.data[i].value is None:
            i += 1
            continue
        else:
            p = hash.data[i]
            while p is not None:
                sum += 1
                p = p.next
            i += 1
    return sum


# transfer hash map into list type
def to_list(hash):
    list = []
    if hash is None:
        return list
    for i, key in enumerate(hash.key_set):
        list.append(find(hash, key))
    return list


# add element from list type
def from_list(hash, list):
    for key, value in enumerate(list):
        add(hash, key, value)


# find element with even value in hash map.
def find_iseven(hash) -> HashMap:
    list = to_list(hash)
    my_list = []
    for value in range(len(list)):
        if type(list[value]) is int or type(list[value]) is float:
            if list[value] % 2 == 0:
                my_list.append(list[value])
    return my_list


# filter element with even value in hash map.
def filter_iseven(hash):
    list = to_list(hash)
    for value in list:
        if type(value) is int or type(value) is float:
            if value % 2 == 0:
                list.remove(value)
    return list


# map element value in hash map with f
def map(hash, f) -> HashMap:
    dict = to_dict(hash)
    for key in hash.key_set:
        value = f(find(hash, key))
        add(dict, key, value)
    return dict


#  build a return value by specific functions(f)
def reduce(hash, f, initial_state):
    state = initial_state
    for key in hash.key_set:
        value = find(hash, key)
        state = f(state, value)
    return state


def mempty(hash):
    return None


def mconcat(a, b):
    if a is None:
        return b
    if b is None:
        return a
    for key in b.key_set:
        value = find(b, key)
        add(a, key, value)
    return a


# iterator
def iterator(hash):
    if hash is not None:
        res = []
        list = to_list(hash)
        for i in list:
            res.append(i)
        a = iter(res)
    else:
        a = None

    def get_next():
        if a is None:
            return False
        else:
            return next(a)

    return get_next
