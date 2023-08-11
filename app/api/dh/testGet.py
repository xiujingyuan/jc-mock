# @Time    : 2019/11/26 7:32 下午
# @Author  : yuanxiujing
# @File    : testGet.py
# @Software: PyCharm
# 导入Flask类
from flask import Flask, request
import json
# 实例化，可视为固定格式
from app.api.dh import api_dh

app = Flask(__name__)


# 只接受get方法访问
# route()方法用于设定路由
@api_dh.route("/test_1.0", methods=["GET"])
def check():
    # 默认返回内容
    return_dict = {'return_code': '200', 'return_info': '处理成功', 'result': False}
    # 判断入参是否为空
    if request.args is None:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    # 获取传入的参数
    get_data = request.args.to_dict()
    name = get_data.get('name')
    age = get_data.get('age')
    # 对参数进行操作
    return_dict['result'] = tt(name, age)

    return json.dumps(return_dict, ensure_ascii=False)


# 功能函数
def tt(name, age):
    result_str = "%s今年%s岁" % (name, age)
    return result_str


if __name__ == "__main__":
    # app.run(host, port, debug, options)
    # 默认值：host=127.0.0.1, port=5000, debug=false
    # 直接设置app的debug为true
    # app.debug = True
    # 方法2：把debug=true作为参数，传入到run方法
    app.run(debug=True)
