import collections
import json

from flask import jsonify, request
from app import csrf
from app.api.dh import api_dh
from app.api.dh.individual import *
from app.api.dh.make_base_data import *
from app.common.random_infos import *
from app.util.dh.dh_db_function import get_asset_info_by_item_no, get_exist_asset_info_by_item_no
from config.dh.db_const import *
from environment.common.config import Config
from util.log.log_util import LogUtil


@api_dh.route('/', methods=['GET', 'POST'])
def hello_world():
    return 'Hello Dh!'


@api_dh.route('/idcard', methods=["GET"])
def contract_idcard():
    data = {"idcard": gennerator()}
    return jsonify(data)


@api_dh.route('/phone', methods=["GET"])
def contract_phone():
    data = {"phone": random_tele(is_false=False)}
    return jsonify(data)


@api_dh.route('/three', methods=["GET"])
def contract_three():
    data = {
        "name": random_name(),
        "mobile": random_tele(is_false=False),
        "identity": gennerator()
    }
    return jsonify(data)


@api_dh.route('/get/cn/intimacy/v4', methods=["GET"])
def get_intimacy():
    count = int(request.args.to_dict().get('count'))
    public_data = get_cn_contact()
    body = {
        "code": 1000,
        "message": "成功",
        "data": public_data
    }
    # for i in range(count):
    #     mydict = {"phone_num_loc": "北京",
    #               "intimacy": random.randint(600, 700),
    #               "call_cnt": "1",
    #               "name": random_name(),
    #               "phone_num": random_tele(is_false=False),
    #               "relation_ship": random.randint(1, 4),
    #               "call_len": random.randint(0, 10)}
    #     # 写法二
    #     # mydict = {}
    #     # mydict["phone_num_loc"] = "北京"
    #     # mydict["intimacy"] = random.randint(600, 700)
    #     # mydict["call_cnt"] = "1"
    #     # mydict["name"] = random_name()
    #     # mydict["phone_num"] = random_tele(is_false=False)
    #     # mydict["relation_ship"] = random.randint(1, 4)
    #     # mydict["call_len"] = random.randint(0, 10)
    #     contacts.append(mydict)
    public_data["d0"] = json.loads(get_cn_contact_bean(count))
    current_app.logger.info(body)
    return jsonify(body)


# 泰国，IVR预提醒订单查询mock，大量
@api_dh.route('/getPreRemindList', methods=["GET"])
def get_pre_remind_list():
    count = int(request.args.to_dict().get('count'))
    remind_list = []
    body = {
        "code": 0,
        "data": {
            "list": remind_list
        },
        "message": "ความสำเร็จ"
    }
    for i in range(count):
        timestamp = str(int(time.time() * 1000)) + str(i)
        asset_number = "T202208301509_" + timestamp
        remind_list.append(asset_number)
    return jsonify(body)


def GBK2312():
    head = random.randint(0xb0, 0xf7)
    body = random.randint(0xa1, 0xf9)  # 在head区号为55的那一块最后5个汉字是乱码,为了方便缩减下范围
    val = f'{head:x}{body:x}'
    str = bytes.fromhex(val).decode('gb2312')
    return str


@api_dh.route('/create_asset_sync', methods=['POST'])
@csrf.exempt
def asset_sync():
    ret = {
        "code": 0,
        "msg": "不是json格式请求"
    }
    args = request.json
    asset_from_app = random.choice(args['asset_from_app'])
    overdue_days = args['overdue_days']
    item_cust_flg = random.choice(args['item_cust_flg'])
    count = args['count']
    d3_level = random.choice(args['d3_level'])
    specified_overdue_amount = args['specified_overdue_amount']
    overdue_amount = args['overdue_amount']
    env = args['env']
    LogUtil.log_info("传入env=%s" % env)
    result = []
    # 初始化环境
    init_dh_env(env, "CN", "test")
    for i in range(count):
        asset_item_number = create_asset_sync(asset_from_app, overdue_days, item_cust_flg, d3_level,
                                              specified_overdue_amount, overdue_amount, env, i)
        ret["code"] = 0
        ret["msg"] = "资产同步请求成功"
        result.append(asset_item_number)
    ret["asset_item_number"] = result
    return jsonify(ret)


def create_asset_sync(asset_from_app, overdue_days, item_cust_flg, d3_level, specified_overdue_amount, overdue_amount, env, i):
    cn_url = Config.CN_ASSET_SYNC_URL.format(env)
    key = str(int(time.time() * 1000))
    data1 = asset_bean(asset_from_app, specified_overdue_amount, overdue_amount, i)
    data2 = individual_bean()
    data3 = asset_transaction(overdue_days, specified_overdue_amount, overdue_amount)
    date4 = receive_card()
    data = {
        "asset": json.loads(data1),
        "receive_card": json.loads(date4),
        "borrower": json.loads(data2),
        "repayer": json.loads(data2),
        "asset_transactions": json.loads(data3)
    }
    body = {
        "type": "AssetImport",
        "key": key,
        "from_system": "qianshengqian",
        "data": data
    }
    resp = request_post(cn_url, body)
    if resp['code'] == 0:
        time.sleep(2)
    LogUtil.log_info("资产同步请求发送成功")
    asset_item_number = body.get("data").get("asset")["asset_item_number"]
    # 创建用户类型信息，asset_quality
    create_asset_quality(asset_item_number, item_cust_flg)
    # 创建C卡数据，c_card
    create_c_card(asset_item_number, item_cust_flg, d3_level)
    return asset_item_number


# def create_c_card(asset_item_number, item_cust_flg, d3_level):
#     c_card = CCard()
#     if d3_level != "" and item_cust_flg in ("新用户", "老用户"):
#         if item_cust_flg == "新用户":
#             c_card.customer_type = "new"
#         if item_cust_flg == "老用户":
#             c_card.customer_type = "old"
#         c_card.asset_item_number = asset_item_number
#         c_card.d3_score = random.randint(500, 600)
#         c_card.d3_level = d3_level
#         c_card.m1_score = random.randint(300, 400)
#         c_card.m1_level = random.randint(1, 10)
#         c_card.create_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#         c_card.m1plus_score = "0.345125"
#         c_card.m1plus_level = random.randint(1, 10)
#         c_card.self_healing = 0
#         db.session.add(c_card)
#         db.session.flush()
#         current_app.logger.info("create_c_card成功")
#
#
# def create_asset_quality(asset_item_number, item_cust_flg):
#     asset_quality = AssetQuality()
#     current_app.logger.info("item_cust_flg:" + item_cust_flg)
#     if item_cust_flg != "新用户" and item_cust_flg != "老用户":
#         return
#     if item_cust_flg == "新用户":
#         asset_quality.apply_user_type = "1"
#     if item_cust_flg == "老用户":
#         asset_quality.apply_user_type = "2"
#     asset_quality.item_sn = random.randint(1, 9999)
#     asset_quality.statistical_date = time.strftime("%Y-%m-%d 00:00:00", time.localtime())
#     asset_quality.asset_item_number = asset_item_number
#     asset_quality.product_cnt = 3
#     asset_quality.product_time_type = "3期*月"
#     asset_quality.item_cust_flg = item_cust_flg
#     asset_quality.create_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#     db.session.add(asset_quality)
#     db.session.flush()
#     current_app.logger.info("asset_quality.item_cust_flg:" + asset_quality.item_cust_flg)
#
#     current_app.logger.info("create_asset_quality成功")


# 泰国用户中心mock
@api_dh.route('/th/individual', methods=['GET', 'POST'])
def get_th_individual():
    public_data = oversea_th_individual_bean()
    # ind_individual = oversea_in_individual_bean()
    # public_data.update(ind_individual)
    body = {
        "msg": "success",
        "data": public_data
    }
    public_data["contacts"] = json.loads(oversea_th_contact_bean())
    public_data["banks"] = json.loads(oversea_th_bank_bean())
    current_app.logger.info(body)
    return jsonify(body)


# 海外资产同步
@api_dh.route('/overseas/sync', methods=['POST'])
@csrf.exempt
def overseas_asset_sync():
    ret = {
        "code": 0,
        "msg": "不是json格式请求"
    }
    args = request.json
    asset_from_app = random.choice(args['asset_from_app'])
    region = args['region']
    overdue_days = args['overdue_days']
    period_count = args['period_count']
    period_days = args['period_days']
    specified_overdue_amount = args['specified_overdue_amount']
    overdue_amount = args['overdue_amount']
    item_cust_flg = random.choice(args['item_cust_flg'])
    d3_level = random.choice(args['d3_level'])
    a_card_level = random.choice(args['a_card_level'])
    # 资产语言，默认泰国：ภาษาไทย，菲律宾、巴基斯坦：english，墨西哥：spanish
    specified_asset_language = args['specified_asset_language']
    asset_language = random.choice(args['asset_language'])
    count = args['count']
    result = []
    # 初始化环境
    init_dh_env("", region, "test")
    for i in range(count):
        r = create_overseas_asset_sync(asset_from_app, region, overdue_days, item_cust_flg, d3_level, specified_overdue_amount, overdue_amount,
                                       specified_asset_language, asset_language, a_card_level, i, period_count, period_days)
        ret["code"] = 0
        ret["msg"] = "海外资产同步请求成功"
        result.append(r)
    ret["asset_item_number"] = result
    return jsonify(ret)


# 印度资产语言mock
@api_dh.route('/in/language', methods=["GET"])
def get_language():
    language_info = {}
    body = json.loads(json.dumps(language_info))
    asset_number = request.args.to_dict().get('asset_number')
    first_language = request.args.to_dict().get('first_language')
    language_data = {
        "asset_number": asset_number,
        "second_language": "0",
        "first_language": first_language,
        "third_language": "0"
    }

    body["message"] = "成功"
    body["code"] = 1000
    body["data"] = language_data

    language = json.dumps(body, ensure_ascii=False)
    return json.loads(language)


def create_overseas_asset_sync(asset_from_app, region, overdue_days, item_cust_flg, d3_level, specified_overdue_amount, overdue_amount,
                               specified_asset_language, asset_language, a_card_level, i, period_count, period_days):
    if region == 'TH':
        overseas_url = Config.OVERSEA_ASSET_SYNC_URL.format("th")
    if region == 'PH':
        overseas_url = Config.OVERSEA_ASSET_SYNC_URL.format("ph")
    if region == 'MX':
        overseas_url = Config.OVERSEA_ASSET_SYNC_URL.format("mx")
    if region == 'PK':
        overseas_url = Config.OVERSEA_ASSET_SYNC_URL.format("pk")
    if region == 'IN':
        overseas_url = Config.OVERSEA_ASSET_SYNC_URL.format("ind")
    # 不指定资产语言，取默认语言
    if specified_asset_language is False:
        if region == 'TH':
            final_language = "ภาษาไทย"
        if region == 'PH':
            final_language = "english"
        if region == 'MX':
            final_language = "spanish"
        if region == 'IN':
            final_language = asset_language
        if region == 'PK':
            final_language = "english"
    if specified_asset_language is True:
        final_language = asset_language
    key = str(int(time.time() * 1000))
    data1 = overseas_asset_bean(region, overdue_days, specified_overdue_amount, overdue_amount, asset_from_app, i, period_count, period_days)
    data2 = borrower_bean()
    principal_amount = json.loads(data1)["asset_principal_amount"]
    interest_amount = json.loads(data1)["asset_interest_amount"]
    penalty_amount = json.loads(data1)["asset_penalty_amount"]
    data3 = overseas_asset_transaction(overdue_days, principal_amount, interest_amount, penalty_amount, period_count, period_days)
    data = {
        "asset": json.loads(data1),
        "borrower": json.loads(data2),
        "asset_transactions": json.loads(data3)
    }
    body = {
        "type": "AssetImport",
        "key": key,
        "from_system": "Rbiz",
        "data": data
    }
    resp = request_post(overseas_url, body)
    if resp['code'] == 0:
        time.sleep(1)
    asset_item_number = body.get("data").get("asset")["asset_item_number"]
    LogUtil.log_info("海外资产同步请求发送成功")
    # 创建用户类型信息，asset_quality
    create_asset_quality(asset_item_number, item_cust_flg)
    # 创建C卡数据，c_card
    create_c_card(asset_item_number, item_cust_flg, d3_level)
    # 创建资产语言，asset_language。印度的资产语言由用户中心传入
    creat_asset_language(asset_item_number, final_language)
    # 创建A卡数据，a_card
    create_a_card(asset_item_number, a_card_level)
    return asset_item_number


@api_dh.route('/getThreeElement', methods=["GET"])
def get_three_element():
    url = Config.ENCRY_URL
    user_name = random_name()
    param1 = [generate_data('name', user_name)]
    data1 = request_post(url, param1)

    id_number = gennerator()
    param2 = [generate_data('idnum', id_number)]
    data2 = request_post(url, param2)

    mobile = random_tele(is_false=False)
    param3 = [generate_data('mobile', mobile)]
    data3 = request_post(url, param3)

    body = collections.OrderedDict()
    body["user_name"] = user_name
    body["enc_user_name"] = data1['data'][0]['hash']
    body["code_user_name"] = data1['data'][0]['plain_text']
    body["id_number"] = id_number
    body["enc_id_number"] = data2['data'][0]['hash']
    body["code_id_number"] = data2['data'][0]['plain_text']
    body["mobile"] = mobile
    body["enc_mobile"] = data3['data'][0]['hash']
    body["code_mobile"] = data3['data'][0]['plain_text']

    return jsonify(body)


@api_dh.route('/overseas/getThreeElement', methods=["GET"])
def get_overseas_three_element():
    region = request.args.to_dict().get('region')
    url = Config.OVERSEA_ENCRY_URL
    user_name = random_oversea_name()
    param1 = [generate_data('name', user_name)]
    data1 = request_post(url, param1)

    if region == 'TH':
        mobile = random_th_tel()
        id_number = random_oversea_gennerator()
    if region == 'PH':
        mobile = random_php_tel()
        id_number = random_oversea_gennerator()
    if region == 'MX':
        mobile = random_mex_tel()
        id_number = random_mex_id_number()
    param2 = [generate_data('idnum', id_number)]
    data2 = request_post(url, param2)
    param3 = [generate_data('mobile', mobile)]
    data3 = request_post(url, param3)

    body = collections.OrderedDict()
    body["user_name"] = user_name
    body["enc_user_name"] = data1['data'][0]['hash']
    body["code_user_name"] = data1['data'][0]['plain_text']
    body["id_number"] = id_number
    body["enc_id_number"] = data2['data'][0]['hash']
    body["code_id_number"] = data2['data'][0]['plain_text']
    body["mobile"] = mobile
    body["enc_mobile"] = data3['data'][0]['hash']
    body["code_mobile"] = data3['data'][0]['plain_text']

    return jsonify(body)


# 菲律宾，用户中心mock
@api_dh.route('/ph/individual', methods=['GET', 'POST'])
def get_php_individual():
    individual_data = oversea_php_individual_bean()
    body = {
        "code": 0,
        "msg": "success",
        "data": individual_data
    }
    individual_data["contacts"] = json.loads(oversea_ph_contact_bean())
    individual_data["bank_card"] = json.loads(oversea_ph_bank_bean())
    current_app.logger.info(body)
    return jsonify(body)


# 墨西哥，用户中心mock
@api_dh.route('/mx/individual', methods=['GET', 'POST'])
def get_mex_individual():
    individual_data = oversea_mex_individual_bean()
    body = {
        "code": 0,
        "msg": "success",
        "data": individual_data
    }
    individual_data["contacts"] = json.loads(oversea_mex_contact_bean())
    current_app.logger.info(body)
    return jsonify(body)


# 巴基斯坦，用户中心mock
@api_dh.route('/pk/individual', methods=['GET', 'POST'])
def get_pk_individual():
    individual_data = oversea_pk_individual_bean()
    body = {
        "code": 0,
        "msg": "success",
        "data": individual_data
    }
    individual_data["contacts"] = json.loads(oversea_pk_contact_bean())
    current_app.logger.info(body)
    return jsonify(body)


# 印度用户中心mock
@api_dh.route('/in/individual', methods=['GET', 'POST'])
def get_ind_individual():
    public_data = oversea_in_id_individual_bean()
    ind_individual = oversea_in_individual_bean()
    public_data.update(ind_individual)
    body = {
        "msg": "success",
        "data": public_data
    }
    public_data["contacts"] = json.loads(oversea_ind_contact_bean())
    public_data["banks"] = json.loads(oversea_ind_bank_bean())
    current_app.logger.info(body)
    return jsonify(body)


@api_dh.route('/get/overseas/intimacy', methods=["GET"])
def get_overseas_intimacy():
    count = int(request.args.to_dict().get('count'))
    region = request.args.to_dict().get('region')
    source = request.args.to_dict().get('source')
    public_data = get_overseas_contact()
    body = {
        "code": 1000,
        "message": "成功",
        "data": public_data
    }
    public_data["contacts"] = json.loads(get_overseas_contact_bean(count, region, source))
    current_app.logger.info(body)
    return jsonify(body)


@api_dh.route('/get/overseas/repay/list', methods=["POST"])
def get_overseas_repay_list():
    args = request.json
    start_date = args['start_date']
    end_date = args['end_date']
    page_size = args['page_size']
    page_index = args['page_index']

    public_data = get_overseas_repay_list_public(page_index, page_size)
    ret = {
        "code": 0,
        "message": "查询成功",
        "data": public_data
    }
    current_app.logger.info(public_data)
    public_data["data_list"] = json.loads(get_overseas_repay_list_data(page_index, page_size,
                                                                       public_data["total_count"],
                                                                       public_data["total_pages"],
                                                                       start_date))
    return jsonify(ret)


@api_dh.route('/get/overseas/repay/detail', methods=["GET"])
def get_overseas_repay_detail():
    item_no = request.args.to_dict().get('item_no')
    repay_date = request.args.to_dict().get('repay_date')
    public_data = get_overseas_repay_detail_public(item_no, repay_date)
    body = {
        "code": 0,
        "message": "查询成功",
        "data": public_data
    }
    current_app.logger.info(body)
    return jsonify(body)


# 结清资产的逾期期次，组装资产信息并导入到资产同步
#
# 1、根据资产编号+国家，判断资产状态是否是payoff，如果payoff，返回”该资产已结清，无需处理。“；如果repay，继续；
# 2、根据资产编号查询asset表，收集并组装asset；
# 3、根据资产编号查询debtor_asset表、individual表，收集并组装borrower；
# 4、根据资产编号查询asset_transaction表，收集并组装asset_transactions，只结清逾期期次；
# 海外结清前必须在fox页面修改字典：QueryBorrowerUrl
@api_dh.route('/payoffAsset', methods=["POST"])
def payoff_asset():
    ret = {
        "code": 0,
        "msg": "不是json格式请求"
    }
    args = request.json
    asset_item_number = args['asset_item_number']
    country = args['country']
    env = args["env"]

    # 初始化环境、资产同步请求地址
    if country == "CN":
        init_dh_env("1", country, env)
        sync_url = Config.CN_ASSET_SYNC_URL.format(1)
    if country in ("TH", "PH", "MX", "IN", "PK"):
        init_dh_env("", country, env)
        if country == 'TH':
            sync_url = Config.OVERSEA_TH_ASSET_SYNC_URL
        if country == 'PH':
            sync_url = Config.OVERSEA_PH_ASSET_SYNC_URL
        if country == 'MX':
            sync_url = Config.OVERSEA_MX_ASSET_SYNC_URL
        if country == 'PK':
            sync_url = Config.OVERSEA_PK_ASSET_SYNC_URL
        if country == 'IN':
            sync_url = Config.OVERSEA_IN_ASSET_SYNC_URL
    LogUtil.log_info("#### 请求参数-资产编号：%s，国家：%s；请求地址：%s" % (asset_item_number, country, sync_url))
    asset = get_asset_info_by_item_no(asset_item_number)
    if not asset:
        ret["code"] = 1
        ret["msg"] = "资产{0}不存在，请确认！".format(asset_item_number)
        return jsonify(ret)
    if asset:
        asset_info = get_exist_asset_info_by_item_no(asset_item_number)

    if not asset_info:
        ret["code"] = 1
        ret["msg"] = "资产{0}已结清，无需处理。".format(asset_item_number)
        return jsonify(ret)
    if asset_info:
        data_asset_info = get_payoff_asset_detail(country, asset_item_number, asset_info)
        borrower_cn = get_payoff_borrower_detail(asset_item_number)
        borrower_overseas = {
            "borrower_uuid": "272233274917519360",
            "borrower_card_uuid": "6621122700001777106",
            "individual_uuid": "272233274917519360",
            "individual_id_num": "enc_02_3735598582729296896_617",
            "individual_tel": "enc_01_3855502888206359552_785"
        }
        asset_transaction_info = get_payoff_transactions_detail(country, asset_item_number)
        data = {
            "asset": json.loads(data_asset_info),
            "asset_transactions": json.loads(asset_transaction_info)
        }
        if country == "CN":
            data["receive_card"] = json.loads(receive_card())
            data["borrower"] = json.loads(borrower_cn)
            data["repayer"] = json.loads(borrower_cn)
        if country in ("TH", "PH", "MX", "IN", "PK"):
            data["borrower"] = borrower_overseas
        body = {
            "type": "AssetImport",
            "key": str(int(time.time() * 1000)),
            "from_system": "Rbiz",
            "data": data
        }
        LogUtil.log_info("#### body=%s" % body)
        request_post(sync_url, body)
        ret["msg"] = "环境：%s，资产%s结清发起成功，仅结清逾期中的期次。" % (country, asset_item_number)

    return jsonify(ret)


# 指定期次还款，组装还款通知
#
# 1、根据资产编号+国家，判断是否资产不存在、指定期次的还款计划不存在，资产存在则继续；
# 2、根据资产编号查询asset表，收集并组装asset；
# 3、根据资产编号查询asset_transaction表，收集并组装：国内dtransactions、fees、tran_logs，海外trans、tran_logs
# 指定期次、还款时间

@api_dh.route('/periodRecovery', methods=["POST"])
def period_recovery():
    res = {
        "code": 0,
        "msg": "不是json格式请求"
    }
    args = request.json
    asset_item_number = args['asset_item_number']
    country = args['country']
    repay_period = args['repay_period']
    repay_date = args['repay_date']
    env = args["env"]
    # 初始化环境、还款同步请求地址
    if country == "CN":
        init_dh_env("1", country, env)
        recovery_url = Config.CN_RECOVERY_URL.format(1)
    if country in ("TH", "PH", "MX", "IN", "PK"):
        init_dh_env("", country, env)
        if country == 'TH':
            recovery_url = Config.OVERSEA_RECOVERY_URL.format("th")
        if country == 'PH':
            recovery_url = Config.OVERSEA_RECOVERY_URL.format("ph")
        if country == 'MX':
            recovery_url = Config.OVERSEA_RECOVERY_URL.format("mx")
        if country == 'PK':
            recovery_url = Config.OVERSEA_RECOVERY_URL.format("pk")
        if country == 'IN':
            recovery_url = Config.OVERSEA_RECOVERY_URL.format("ind")

    repay_detail_asset_info = get_asset_info_by_item_no(asset_item_number)
    if not repay_detail_asset_info:
        res["code"] = 1
        res["msg"] = "资产{0}不存在，请确认！".format(asset_item_number)
        return jsonify(res)

    trans = get_period_transaction(asset_item_number, repay_period, None)
    if not trans:
        res["code"] = 1
        res["msg"] = "资产{0}的还款计划不存在期次{1}，请确认！".format(asset_item_number, repay_period)
        return jsonify(res)

    if repay_detail_asset_info:
        # asset节点
        data_info_asset = get_repay_period_asset_detail(country, asset_item_number, repay_detail_asset_info, repay_period)
        # tran_logs节点
        tran_logs = get_repay_notify_tran_logs(asset_item_number, repay_period, repay_date, country)

        if country == "CN":
            dtr_info = get_repay_trans(asset_item_number, "dtransactions", repay_period, repay_date, country)
            fee_info = get_repay_trans(asset_item_number, "fees", repay_period, repay_date, country)
            data = {
                "rbizPushFox": True,
                "action": "tran_repay",
                "type": "assetAccountSync",
                "asset": json.loads(data_info_asset),
                "dtransactions": json.loads(dtr_info),
                "fees": json.loads(fee_info)
            }

        if country in ("TH", "PH", "MX", "IN", "PK"):
            trans_info = get_repay_trans(asset_item_number, "trans", repay_period, repay_date, country)
            data = {
                "rbizPushFox": True,
                "action": "tran_repay",
                "type": "assetAccountSync",
                "asset": json.loads(data_info_asset),
                "trans": json.loads(trans_info)
            }
        LogUtil.log_info("#### 请求参数-资产编号：%s，国家：%s；回款请求地址：%s" % (asset_item_number, country, recovery_url))

        data["tran_logs"] = tran_logs
        body = {
            "type": "AssetChangeNotify",
            "key": str(int(time.time() * 1000)),
            "from_system": "Rbiz",
            "data": data
        }
        LogUtil.log_info("#### 回款通知body=%s" % json.dumps(body))
        request_post(recovery_url, body)
        res["msg"] = "环境：%s，资产%s，期次%s，回款通知成功。" % (country, asset_item_number, repay_period)

    return jsonify(res)


if __name__ == '__main__':
    country = "CN"
    asset_item_number = "20221115114335896187"
    init_dh_env("1", "CN", "dev")


# # 印尼用户中心mock
# @api_dh.route('/id/individual', methods=["GET"])
# def get_idn_individual():
#     public_data = oversea_in_id_individual_bean()
#     idn_individual = oversea_id_individual_bean()
#     public_data.update(idn_individual)
#     body = {
#         "msg": "success",
#         "data": public_data
#     }
#     public_data["contacts"] = json.loads(oversea_ind_contact_bean())
#     current_app.logger.info(body)
#     return jsonify(body)


#
# # -*- coding: UTF-8 -*-
# from urllib import request
#
# if __name__ == "__main__":
#     req = request.Request("https://zhengzhou.gouhaowang.com/m/shoujihaoduan/search")
#     response = request.urlopen(req)
#     html = response.read()
#     html = html.decode("utf-8")
#     print(html)
