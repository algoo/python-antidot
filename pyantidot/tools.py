# -*- coding: utf-8 -*-
from bunch import Bunch as BaseBunch


class Bunch(BaseBunch):
    def __getattr__(self, k):
        value = super(Bunch, self).__getattr__(k)
        if type(value) is dict:
            return Bunch(value)
        if type(value) is list:
            for key, list_item in enumerate(value):
                if type(list_item) is dict:
                    value[key] = Bunch(list_item)
        return value