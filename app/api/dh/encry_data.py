# @Time    : 2019/12/2 5:46 下午
# @Author  : yuanxiujing
# @File    : encry_data.py
# @Software: PyCharm


def generate_data(type, value):
    if type == "idnum":
        return {
            "type": 2,
            "plain": value
        }
    elif type == "mobile":
        return {
            "type": 1,
            "plain": value
        }
    elif type == "card_number":
        return {
            "type": 3,
            "plain": value
        }
    elif type == "name":
        return {
            "type": 4,
            "plain": value
        }
    elif type == "email":
        return {
            "type": 5,
            "plain": value
        }
    elif type == "address":
        return {
            "type": 6,
            "plain": value
        }
