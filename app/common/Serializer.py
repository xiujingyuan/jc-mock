# -*- coding: utf-8 -*-
# @Title: Serializer
# @ProjectName gaea-api
# @Description: TODO
# @author fyi zhang
# @date 2019/1/6 15:53


import json

from sqlalchemy.inspection import inspect
from datetime import datetime, date, time

from flask_sqlalchemy import Model
from sqlalchemy import DateTime, Date, Numeric, Time


class BaseToDict(object):

    @classmethod
    def to_dicts(cls, models):
        return cls.change_dict(models)

    @classmethod
    def to_spec_dicts(cls, models):
        return cls.change_dict(models, spec_type=True)

    @property
    def to_dict(self):
        return self.change_dict(self)

    @property
    def to_spec_dict(self):
        return self.change_dict(self, spec_type=True)

    @staticmethod
    def get_dict_data(model, spec_type=False):
        gen = model.model_to_dict(model)
        dit = dict((g[0].replace(model.__tablename__ + '_', ''), g[1]) for g in gen) if spec_type \
            else dict((g[0], g[1]) for g in gen)
        return dit

    def change_dict(self, models=None, spec_type=False):
        models = models if models is not None else self
        if isinstance(models, list):
            if isinstance(models[0], Model):
                lst = []
                for model in models:
                    dit = model.get_dict_data(model, spec_type)
                    lst.append(dit)
                return lst
            else:
                res = self.result_to_dict(models)
                return res
        else:
            if isinstance(models, Model):
                return self.get_dict_data(models, spec_type)
            else:
                res = dict(zip(models.keys(), models))
                self.find_datetime(res)
                return res

    # 当结果为result对象列表时，result有key()方法
    @staticmethod
    def result_to_dict(results):
        res = [dict(zip(r.keys(), r)) for r in results]
        # 这里r为一个字典，对象传递直接改变字典属性
        for r in res:
            BaseToDict.find_datetime(r)
        return res

    @staticmethod
    def model_to_dict(model):  # 这段来自于参考资源
        for col in model.__table__.columns:
            if isinstance(col.type, DateTime):
                value = BaseToDict.convert_datetime(getattr(model, col.name))
            elif isinstance(col.type, Numeric):
                value = float(getattr(model, col.name))
            else:
                value = getattr(model, col.name)
            yield col.name, value

    @staticmethod
    def find_datetime(value):
        for v in value:
            if isinstance(value[v], datetime):
                value[v] = BaseToDict.convert_datetime(value[v])  # 这里原理类似，修改的字典对象，不用返回即可修改

    @staticmethod
    def convert_datetime(value):
        if value:
            if isinstance(value, (datetime, DateTime)):
                return value.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(value, (date, Date)):
                return value.strftime("%Y-%m-%d")
            elif isinstance(value, (Time, time)):
                return value.strftime("%H:%M:%S")
        else:
            return ""


class Serializer(object):

    def serialize(self, except_attr=[]):
        return {c: self.format_date(getattr(self, c)) for c in inspect(self).attrs.keys() if c not in except_attr}

    def format_date(self, value):
        # 将datetime转成时间
        if isinstance(value, datetime):
            value = value.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(value, str):
            try:
                value = json.loads(value, encoding='utf-8')
            except:
                pass
        return value

    @staticmethod
    def serialize_list(l, except_attr=[]):
        return [m.serialize() for m in l]

