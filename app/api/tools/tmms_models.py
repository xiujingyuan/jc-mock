#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/05/07
 @file: tmms_models.py
 @site:
 @email:
"""


class ClsData(object):
    def __init__(self):
        self.__name__ = ""
        self.__identity__ = ""
        self.__loan_limit__ = 0

    @property
    def loan_limit(self):
        return self.__loan_limit__

    @loan_limit.setter
    def loan_limit(self, value):
        if isinstance(value, int):
            self.__loan_limit__ = value
        else:
            raise TypeError("need int, but {0} found".format(type(value)))

    @property
    def identity(self):
        return self.__identity__

    @identity.setter
    def identity(self, value):
        if isinstance(value, str):
            self.__identity__ = value
        else:
            raise TypeError("need str, but {0} found".format(type(value)))

    @property
    def name(self):
        return self.__name__

    @name.setter
    def name(self, value):
        if isinstance(value, str):
            self.__name__ = value
        else:
            raise TypeError("need str, but {0} found".format(type(value)))


class ClsPushData(ClsData):
    def __init__(self):
        self.__finish_time__ = ""

    @property
    def finish_time(self):
        return self.__finish_time__

    @finish_time.setter
    def finish_time(self, value):
        if isinstance(value, str):
            self.__finish_time__ = value
        else:
            raise TypeError("need str, but {0} found".format(type(value)))


class ClsUpdateData(ClsData):
    def __init__(self):
        self.__loan_amount__ = 0

    @property
    def loan_amount(self):
        return self.__loan_amount__

    @loan_amount.setter
    def loan_amount(self, value):
        if isinstance(value, int):
            self.__loan_amount__ = value
        else:
            raise TypeError("need int, but {0} found".format(type(value)))


class UserUpdateInfo(object):
    def __init__(self):
        self.__phone__ = ""
        self.__type__ = 0
        self.__step__ = 0
        self.__from_system__ = ""
        self.__data__ = {}

    def change_json(self, except_attr=None):
        ret = {}
        for attr in self.__dict__:
            value = self.__getattribute__(attr)
            ret[attr[2:-2]] = value
            if isinstance(value, ClsUpdateData):
                value_dict = {}
                for data_attr in value.__dict__:
                    value_dict[data_attr[2:-2]] = value.__getattribute__(data_attr)
                ret[attr[2:-2]] = value_dict

        if except_attr is not None:
            if except_attr in ret.keys():
                ret.pop(except_attr)
            elif except_attr in ret["data"].keys():
                ret["data"].pop(except_attr)
        return ret

    def print_attr(self):
        for attr in self.__dict__:
            value = self.__getattribute__(attr)
            if isinstance(value, ClsData):
                for data_attr in value.__dict__:
                    print(attr[2:-2], data_attr[2:-2], value.__getattribute__(data_attr))
            else:
                print(attr[2:-2], value)

    @property
    def step(self):
        return self.__step__

    @step.setter
    def step(self, value):
        if isinstance(value, (str, int)):
            self.__step__ = value
        else:
            raise TypeError("need int, but {0} found".format(type(value)))

    @property
    def data(self):
        return self.__data__

    @data.setter
    def data(self, value):
        self.__data__ = value

    @property
    def from_system(self):
        return self.__from_system__

    @from_system.setter
    def from_system(self, value):
        if isinstance(value, (int, str)):
            self.__from_system__ = value
        else:
            raise TypeError("need str, but {0} found".format(type(value)))

    @property
    def type(self):
        return self.__type__

    @type.setter
    def type(self, value):
        if isinstance(value, (str, int)):
            self.__type__ = value
        else:
            raise TypeError("need int, but {0} found".format(type(value)))

    @property
    def phone(self):
        return self.__phone__

    @phone.setter
    def phone(self, value):
        if isinstance(value, (str, int)):
            self.__phone__ = value
        else:
            raise TypeError("need str, but {0} found".format(type(value)))


class UserInfo(object):
    def __init__(self):
        self.__phone__ = ""
        self.__type__ = 0
        self.__step__ = 0
        self.__valid_time__ = ""
        self.__click_time__ = ""
        self.__from_system__ = ""
        self.__customer_channel__ = ""
        self.__customer_os__ = ""
        self.__customer_app__ = ""
        self.__data__ = {}

    def change_json(self, except_attr=None):
        ret = {}
        for attr in self.__dict__:
            value = self.__getattribute__(attr)
            ret[attr[2:-2]] = value
            if isinstance(value, ClsPushData) or isinstance(value, ClsUpdateData):
                value_dict = {}
                for data_attr in value.__dict__:
                    value_dict[data_attr[2:-2]] = value.__getattribute__(data_attr)
                ret[attr[2:-2]] = value_dict

        if except_attr is not None:
            if except_attr in ret.keys():
                ret.pop(except_attr)
            elif except_attr in ret["data"].keys():
                ret["data"].pop(except_attr)
        return ret

    def print_attr(self):
        for attr in self.__dict__:
            value = self.__getattribute__(attr)
            if isinstance(value, ClsData):
                for data_attr in value.__dict__:
                    print(attr[2:-2], data_attr[2:-2], value.__getattribute__(data_attr))
            else:
                print(attr[2:-2], value)

    @property
    def customer_channel(self):
        return self.__customer_channel__

    @customer_channel.setter
    def customer_channel(self, value):
        if isinstance(value, (str, int)):
            self.__customer_channel__ = value
        else:
            raise TypeError("need int, but {0} found".format(type(value)))

    # self.__customer_os__ = ""
    # self.__customer_app_ = ""

    @property
    def customer_os(self):
        return self.__customer_os__

    @customer_os.setter
    def customer_os(self, value):
        if isinstance(value, (str, int, list)):
            self.__customer_os__ = value
        else:
            raise TypeError("need int, but {0} found".format(type(value)))

    @property
    def customer_app(self):
        return self.__customer_app_

    @customer_app.setter
    def customer_app(self, value):
        if isinstance(value, (str, int, list)):
            self.__customer_app__ = value
        else:
            raise TypeError("need int, but {0} found".format(type(value)))

    @property
    def step(self):
        return self.__step__

    @step.setter
    def step(self, value):
        if isinstance(value, (str, int)):
            self.__step__ = value
        else:
            raise TypeError("need int, but {0} found".format(type(value)))

    @property
    def data(self):
        return self.__data__

    @data.setter
    def data(self, value):
        self.__data__ = value

    @property
    def from_system(self):
        return self.__from_system__

    @from_system.setter
    def from_system(self, value):
        if isinstance(value, (int, str)):
            self.__from_system__ = value
        else:
            raise TypeError("need str, but {0} found".format(type(value)))

    @property
    def click_time(self):
        return self.__click_time__

    @click_time.setter
    def click_time(self, value):
        if isinstance(value, (int, str)):
            self.__click_time__ = value
        else:
            raise TypeError("need datetime, but {0} found".format(type(value)))

    @property
    def valid_time(self):
        return self.__valid_time__

    @valid_time.setter
    def valid_time(self, value):
        if isinstance(value, (int, str)):
            self.__valid_time__ = value
        else:
            raise TypeError("need datetime, but {0} found".format(type(value)))

    @property
    def type(self):
        return self.__type__

    @type.setter
    def type(self, value):
        if isinstance(value, (str, int)):
            self.__type__ = value
        else:
            raise TypeError("need int, but {0} found".format(type(value)))

    @property
    def phone(self):
        return self.__phone__

    @phone.setter
    def phone(self, value):
        if isinstance(value, (str, int)):
            self.__phone__ = value
        else:
            raise TypeError("need str, but {0} found".format(type(value)))
