import json
import random
import time

import pandas as pd
import requests

from app.api.dh.encry_data import generate_data
from app.common.random_infos import *
from app.util.dh.dh_db_function import get_individual, get_period_transaction, get_transaction
from environment.common.config import Config
from util.log.log_util import LogUtil

url = Config.ENCRY_URL
oversea_url = Config.OVERSEA_ENCRY_URL
timestamp = str(int(time.time() * 1000))
current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def request_post(url, param):
    fails = 0
    while True:
        try:
            if fails >= 20:
                break

            headers = {'content-type': 'application/json;charset=UTF-8', 'Accept': 'application/json'}
            ret = requests.post(url, json=param, headers=headers, timeout=10)

            if ret.status_code == 200:
                text = json.loads(ret.text)
            else:
                continue
        except:
            fails += 1
            print('网络连接出现问题, 正在尝试再次请求: ', fails)
        else:
            break
    return text


def request_get(url, param):
    fails = 0
    while True:
        try:
            if fails >= 20:
                break

            ret = requests.get(url=url, params=param, timeout=10)

            if ret.status_code == 200:
                text = json.loads(ret.text)
            else:
                continue
        except:
            fails += 1
            print('网络连接出现问题, 正在尝试再次请求: ', fails)
        else:
            break
    return text


def asset_bean(asset_from_app, specified_overdue_amount, overdue_amount, i):
    asset_item = time.strftime("%Y%m%d", time.localtime()) + str(int(time.time() * 1000)) + "_" + str(i + 1)
    if asset_from_app == "草莓":
        asset_from_system = "strawberry"
    if asset_from_app == "香蕉":
        asset_from_system = "banana"
    # 默认草莓
    if asset_from_app not in ("香蕉", "草莓"):
        asset_from_system = "strawberry"
    body = {
        "asset_item_number": "CN_test_" + asset_item,
        "asset_from_system": asset_from_system,
        "asset_from_app": asset_from_app,
        "asset_type": "现金贷",
        "asset_sub_type": "multiple",
        "asset_name": "CN_test_" + asset_item,
        "asset_sign_at": "2019-02-13 13:52:23",
        "asset_grant_at": "2019-02-13 13:52:23",
        "asset_due_at": "2019-05-13 00:00:00",
        "asset_channel": "Paydayloan",
        "asset_city_code": 652200,
        "asset_status": "repay",
        "asset_loan_channel": "hengfeng",
        "asset_repaid_amount": 0,
        "asset_period_type": "month",
        "asset_period_count": 3,
        "asset_period_days": 0,
        "asset_ref_order_no": "",
        "asset_ref_order_type": "game_bill",
        "asset_risk_level": "2",
        "asset_sub_order_type": "",
        "asset_product_name": "元宝钱包",
        "asset_actual_grant_at": "2019-02-13 14:23:12",
        "asset_owner": "KN",
        "asset_version": int(time.time() * 1000),
        "asset_credit_term": 0,
        "asset_repayment_app": "",
        "ref_order_loan_channel": ""
    }
    if specified_overdue_amount is True:
        amount_body = {
            "asset_interest_amount": 0,
            "asset_repaid_interest_amount": 0,
            "asset_principal_amount": overdue_amount,
            "asset_repaid_principal_amount": 0,
            "asset_penalty_amount": 0,
            "asset_repaid_penalty_amount": 0,
            "asset_decrease_penalty_amount": 0,
            "asset_fee_amount": 0,
            "asset_repaid_fee_amount": 0,

        }
    if specified_overdue_amount is False:
        amount_body = {
            "asset_interest_amount": 9999,
            "asset_repaid_interest_amount": 0,
            "asset_principal_amount": 600000,
            "asset_repaid_principal_amount": 0,
            "asset_penalty_amount": 6888,
            "asset_repaid_penalty_amount": 0,
            "asset_decrease_penalty_amount": 0,
            "asset_fee_amount": 44328,
            "asset_repaid_fee_amount": 0,

        }
    body.update(amount_body)
    return json.dumps(body, ensure_ascii=False)


def individual_bean():
    individual_name = random_name()
    param1 = [generate_data('name', individual_name)]
    res1 = request_post(url, param1)

    individual_idnum = gennerator()
    param2 = [generate_data('idnum', individual_idnum)]
    res2 = request_post(url, param2)

    individual_tel = random_tele(is_false=False)
    param3 = [generate_data('mobile', individual_tel)]
    res3 = request_post(url, param3)

    individual_work_tel = random_work_tel()
    param4 = [generate_data('mobile', individual_work_tel)]
    res4 = request_post(url, param4)

    individual_residence_tel = random_tele(is_false=False)
    param5 = [generate_data('mobile', individual_residence_tel)]
    res5 = request_post(url, param5)

    individual_mate_name = random_name()
    param6 = [generate_data('name', individual_mate_name)]
    res6 = request_post(url, param6)

    individual_mate_tel = random_tele(is_false=False)
    param7 = [generate_data('mobile', individual_mate_tel)]
    res7 = request_post(url, param7)

    individual_relative_name = random_name()
    param8 = [generate_data('name', individual_relative_name)]
    res8 = request_post(url, param8)

    individual_relative_tel = random_tele(is_false=False)
    param9 = [generate_data('mobile', individual_relative_tel)]
    res9 = request_post(url, param9)

    individual_workmate_name = random_name()
    param10 = [generate_data('name', individual_workmate_name)]
    res10 = request_post(url, param10)

    individual_workmate_tel = random_tele(is_false=False)
    param11 = [generate_data('mobile', individual_workmate_tel)]
    res11 = request_post(url, param11)

    body = {
        "enc_individual_name": res1['data'][0]['hash'],
        "enc_individual_idnum": res2['data'][0]['hash'],

        "enc_individual_tel": "enc_01_4878840_203",
        "enc_individual_work_tel": "",
        "enc_individual_residence_tel": "",
        "enc_individual_mate_name": "",
        "enc_individual_mate_tel": "",
        "enc_individual_relative_name": "enc_04_3577547027946932224_815",
        "enc_individual_relative_tel": "enc_01_3536591222989129728_887",
        "enc_individual_workmate_name": "",
        "enc_individual_workmate_tel": "",

        # "enc_individual_tel": res3['data'][0]['hash'],
        # "enc_individual_work_tel": res4['data'][0]['hash'],
        # "enc_individual_residence_tel": res5['data'][0]['hash'],
        # "enc_individual_mate_name": res6['data'][0]['hash'],
        # "enc_individual_mate_tel": res7['data'][0]['hash'],
        # "enc_individual_relative_name": res8['data'][0]['hash'],
        # "enc_individual_relative_tel": res9['data'][0]['hash'],
        # "enc_individual_workmate_name": res10['data'][0]['hash'],
        # "enc_individual_workmate_tel": res11['data'][0]['hash'],

        "individual_gender": random.choice(['f', 'm']),
        "individual_residence": random_road(),
        "individual_workplace": random_road(),
        "individual_permanent": random_road(),
        "individual_company": random_company(),
        "individual_remark": "",
        "individual_nation": random_nation(),
        "individual_email": random_tele(is_false=False) + "@qq.com",
        "individual_relative_relation": "3",

        "individual_name": "",
        "individual_idnum": "",
        "individual_tel": "",
        "individual_work_tel": "",
        "individual_residence_tel": "",
        "individual_mate_name": "",
        "individual_mate_tel": "",
        "individual_relative_name": "",
        "individual_relative_tel": "",
        "individual_workmate_name": "",
        "individual_workmate_tel": "",

        "code_individual_name": "",
        "code_individual_idnum": "",
        "code_individual_tel": "",
        "code_individual_work_tel": "",
        "code_individual_residence_tel": "",
        "code_individual_mate_name": "",
        "code_individual_mate_tel": "",
        "code_individual_relative_name": "",
        "code_individual_relative_tel": "",
        "code_individual_workmate_name": "",
        "code_individual_workmate_tel": ""
    }
    return json.dumps(body, ensure_ascii=False)


def receive_card():
    body = {
        "card_bank_code": "CCB",
        "card_bank_name": "中国建设银行",
        "card_num_encrypt": "enc_03_3538955538950260736_840"
    }
    return json.dumps(body, ensure_ascii=False)


def asset_transaction(overdue_days, specified_overdue_amount, overdue_amount):
    transactions = []
    if specified_overdue_amount is True:
        repayprincipal = {
            "asset_transaction_type": "repayprincipal",
            "asset_transaction_amount": overdue_amount,
            "asset_transaction_status": "unfinish",
            "asset_transaction_expect_finish_time": get_before_date(overdue_days, 31, 0) + " 00:00:00",
            "asset_transaction_finish_at": "",
            "asset_transaction_period": 1,
            "asset_transaction_remark": "",
            "asset_transaction_decrease_amount": 0,
            "asset_transaction_repaid_amount": 0
        }
        transactions.append(repayprincipal)
    if specified_overdue_amount is False:
        repaylateinterest = {
            "asset_transaction_type": "repaylateinterest",
            "asset_transaction_amount": 6888,
            "asset_transaction_status": "unfinish",
            "asset_transaction_expect_finish_time": get_before_date(overdue_days, 31, 0) + " 00:00:00",
            "asset_transaction_finish_at": "",
            "asset_transaction_period": 1,
            "asset_transaction_remark": "",
            "asset_transaction_decrease_amount": 0,
            "asset_transaction_repaid_amount": 0
        }
        transactions.append(repaylateinterest)
        for i in range(3):
            repayprincipal = {
                "asset_transaction_type": "repayprincipal",
                "asset_transaction_amount": 200000,
                "asset_transaction_status": "unfinish",
                "asset_transaction_expect_finish_time": get_before_date(overdue_days, 31, i) + " 00:00:00",
                "asset_transaction_finish_at": "",
                "asset_transaction_period": i + 1,
                "asset_transaction_remark": "",
                "asset_transaction_decrease_amount": 0,
                "asset_transaction_repaid_amount": 0
            }
            repayinterest = {
                "asset_transaction_type": "repayinterest",
                "asset_transaction_amount": 3333,
                "asset_transaction_status": "unfinish",
                "asset_transaction_expect_finish_time": get_before_date(overdue_days, 31, i) + " 00:00:00",
                "asset_transaction_finish_at": "",
                "asset_transaction_period": i + 1,
                "asset_transaction_remark": "",
                "asset_transaction_decrease_amount": 0,
                "asset_transaction_repaid_amount": 0
            }
            repayafter_loan_manage = {
                "asset_transaction_type": "repayafter_loan_manage",
                "asset_transaction_amount": 10000,
                "asset_transaction_status": "unfinish",
                "asset_transaction_expect_finish_time": get_before_date(overdue_days, 31, i) + " 00:00:00",
                "asset_transaction_finish_at": "",
                "asset_transaction_period": i + 1,
                "asset_transaction_remark": "",
                "asset_transaction_decrease_amount": 0,
                "asset_transaction_repaid_amount": 0
            }
            repaytechnical_service = {
                "asset_transaction_type": "repaytechnical_service",
                "asset_transaction_amount": 2888,
                "asset_transaction_status": "unfinish",
                "asset_transaction_expect_finish_time": get_before_date(overdue_days, 31, i) + " 00:00:00",
                "asset_transaction_finish_at": "",
                "asset_transaction_period": i + 1,
                "asset_transaction_remark": "",
                "asset_transaction_decrease_amount": 0,
                "asset_transaction_repaid_amount": 0
            }
            repayservice = {
                "asset_transaction_type": "repayservice",
                "asset_transaction_amount": 1888,
                "asset_transaction_status": "unfinish",
                "asset_transaction_expect_finish_time": get_before_date(overdue_days, 31, i) + " 00:00:00",
                "asset_transaction_finish_at": "",
                "asset_transaction_period": i + 1,
                "asset_transaction_remark": "",
                "asset_transaction_decrease_amount": 0,
                "asset_transaction_repaid_amount": 0
            }
            transactions.append(repayprincipal)
            transactions.append(repayinterest)
            transactions.append(repayafter_loan_manage)
            transactions.append(repaytechnical_service)
            transactions.append(repayservice)
    return json.dumps(transactions, ensure_ascii=False)


# 用户中心信息，泰国
def oversea_th_individual_bean():
    individual_full_name = random_oversea_name()
    param1 = [generate_data('name', individual_full_name)]
    res1 = request_post(oversea_url, param1)

    individual_id_card = random_oversea_gennerator()
    param2 = [generate_data('idnum', individual_id_card)]
    res2 = request_post(oversea_url, param2)

    individual_phone = random_th_tel()
    param4 = [generate_data('mobile', individual_phone)]
    res4 = request_post(oversea_url, param4)

    individual_gender = random.choice(['female', 'male'])

    home_address = random_road()
    param5 = [generate_data('address', home_address)]
    res5 = request_post(oversea_url, param5)

    individual_address = random_road()
    param6 = [generate_data('address', individual_address)]
    res6 = request_post(oversea_url, param6)

    individual_english_name = random_oversea_name()
    param7 = [generate_data('name', individual_english_name)]
    res7 = request_post(oversea_url, param7)

    email = random_email()
    param8 = [generate_data('email', email)]
    res8 = request_post(oversea_url, param8)

    public_data = {
        "individual_full_name": res1['data'][0]['plain_text'],
        "individual_full_name_encrypt": res1['data'][0]['hash'],
        "individual_birthday": "01/08/1979",
        "individual_gender": individual_gender,
        "marital_status": random_th_marital_status(),
        "province": "อบุลราชธานี",
        "city": "กง่ิอาเภอสวา่งวรีะวงศ์",
        "home_address": res5['data'][0]['plain_text'],
        "home_address_encrypt": res5['data'][0]['hash'],
        "individual_address": res6['data'][0]['plain_text'],
        "individual_address_encrypt": res6['data'][0]['hash'],
        "individual_id_card": res2['data'][0]['plain_text'],
        "individual_id_card_encrypt": res2['data'][0]['hash'],
        "individual_phone": res4['data'][0]['plain_text'],
        "individual_phone_encrypt": res4['data'][0]['hash'],
        "job_type": random_job_type(),
        "monthly_income": random_th_monthly_income(),
        "individual_english_name": res7['data'][0]['plain_text'],
        "individual_english_name_encrypt": res7['data'][0]['hash'],
        "email_encrypt": res8['data'][0]['hash'],
        "contacts": []
    }
    return public_data


# 用户中心信息，菲律宾
def oversea_php_individual_bean():
    individual_full_name = random_oversea_name()
    param1 = [generate_data('name', individual_full_name)]
    res1 = request_post(oversea_url, param1)

    id_card_type = random.randint(1, 9)
    individual_id_card = random_ph_id_card_type(id_card_type)
    param2 = [generate_data('idnum', individual_id_card)]
    res2 = request_post(oversea_url, param2)

    individual_phone = random_php_tel()
    param4 = [generate_data('mobile', individual_phone)]
    res4 = request_post(oversea_url, param4)

    individual_gender = random.choice(['female', 'male'])

    facebook = random_oversea_email()
    param5 = [generate_data('email', facebook)]
    res5 = request_post(oversea_url, param5)

    email = random_email()
    param8 = [generate_data('email', email)]
    res8 = request_post(oversea_url, param8)

    # 证件类型：
    # "1": "UMID (unified multi-purpose ID)",
    # "2": "TIN（Taxpayer Identification Number）",
    # "3": "SSS (Social Security System ID)",
    # "4": "Passport",
    # "5": "Driver's License",
    # "6": "PhiHealth",
    # "7": "Voter's ID",
    # "8": "Postal Card",
    # "9": "National ID"

    # contactable_id，可联系时段 0:未填写 1: "9:00 - 14:00", 2: "14:00 - 18:00", 3: "18:00 - 21:00", 4: "Anytime"
    public_data = {
        "fullname_encrypt": res1['data'][0]['hash'],
        "id_card_type": id_card_type,
        "id_card_no_encrypt": res2['data'][0]['hash'],
        "phone_encrypt": res4['data'][0]['hash'],
        "birthday": "20/01/2021",
        "gender": individual_gender,
        "education_level": random.randint(1, 7),
        "marital_status": random.randint(1, 4),
        "home_address": "Flora Apayao",
        "duration_of_stay": random.randint(1, 6),
        "occupation": random.randint(1, 13),
        "position_level": random.randint(1, 6),
        "company_name": "Lawyer employed Employee",
        "monthly_income": random.randint(1, 5),
        "working_years": random.randint(1, 5),
        "facebook_encrypt": res5['data'][0]['hash'],
        "email_encrypt": res8['data'][0]['hash'],
        "contactable_id": random.randint(0, 4),
        "contacts": [],
        "bank_card": [],
    }
    return public_data


# 用户中心信息，墨西哥
def oversea_mex_individual_bean():
    name1 = random_oversea_name()
    param1 = [generate_data('name', name1)]
    first_name = request_post(oversea_url, param1)

    name2 = random_oversea_name()
    param1 = [generate_data('name', name2)]
    middle_name = request_post(oversea_url, param1)

    name3 = random_oversea_name()
    param1 = [generate_data('name', name3)]
    last_name = request_post(oversea_url, param1)

    individual_id_card = random_mex_id_number()
    param2 = [generate_data('idnum', individual_id_card)]
    res2 = request_post(oversea_url, param2)

    individual_phone = random_mex_tel()
    param3 = [generate_data('mobile', individual_phone)]
    res3 = request_post(oversea_url, param3)

    company_phone = random_mex_tel()
    param4 = [generate_data('mobile', company_phone)]
    res4 = request_post(oversea_url, param4)

    individual_gender = random.choice(['female', 'male'])

    bank_reserved_phone = random_mex_tel()
    param5 = [generate_data('mobile', bank_reserved_phone)]
    res5 = request_post(oversea_url, param5)

    whatsapp_account = random_mex_tel()
    param6 = [generate_data('mobile', whatsapp_account)]
    res6 = request_post(oversea_url, param6)

    email = random_email()
    param8 = [generate_data('email', email)]
    res8 = request_post(oversea_url, param8)

    public_data = {
        "facebook": email,
        "first_name_encrypt": first_name['data'][0]['hash'],
        "middle_name_encrypt": middle_name['data'][0]['hash'],
        "last_name_encrypt": last_name['data'][0]['hash'],
        "id_card_no_encrypt": res2['data'][0]['hash'],
        "phone_encrypt": res3['data'][0]['hash'],
        "birthday": "20/01/2021",
        "gender": individual_gender,
        "marital_status": random.randint(1, 3),
        "occupation": random.randint(1, 6),
        "company_name": "Lawyer employed Employee",
        "company_phone_encrypt": res4['data'][0]['hash'],
        "working_years": random.randint(1, 5),
        "school_name": "middle school",
        "post_code": "212451",
        "bank_phone_encrypt": res5['data'][0]['hash'],
        "whatsapp_encrypt": res6['data'][0]['hash'],
        "email_encrypt": res8['data'][0]['hash'],
        "home_address": "家庭地址MAR MZ 5 LT 7 CS 4 FRACC",
        "ocr_address": "C JARDINES DEL MAR MZ 5 LT 7 CS 4 FRACC HEROES TECAMAC SECC JARDIN TECAMAC,MEX.",
        "contacts": [],
    }
    return public_data


# 用户中心信息，巴基斯坦
def oversea_pk_individual_bean():
    name1 = random_oversea_name()
    param1 = [generate_data('name', name1)]
    borrower_name = request_post(oversea_url, param1)

    name2 = random_oversea_name()
    param1 = [generate_data('name', name2)]
    father_name = request_post(oversea_url, param1)

    individual_id_card = random_oversea_gennerator()
    param2 = [generate_data('idnum', individual_id_card)]
    res2 = request_post(oversea_url, param2)

    individual_phone = random_pk_tel()
    param3 = [generate_data('mobile', individual_phone)]
    res3 = request_post(oversea_url, param3)

    email = random_email()
    param4 = [generate_data('email', email)]
    res4 = request_post(oversea_url, param4)

    individual_gender = random.choice(['female', 'male'])

    public_data = {
        "education_level_id": random.randint(1, 4),
        "marital_status_id": random.randint(1, 3),
        "language_id": random.randint(1, 2),
        "occupation_id": random.randint(1, 4),
        "pay_period_id": random.randint(1, 4),
        "self_income_id": random.randint(1, 6),
        "family_income_id": random.randint(1, 5),
        "job_description": "工作介绍工作介绍haha",
        "company_name": "公司名称公司名称",
        "name_encrypt": borrower_name['data'][0]['hash'],
        "father_name_encrypt": father_name['data'][0]['hash'],
        "phone_encrypt": res3['data'][0]['hash'],
        "gender": individual_gender,
        "birthday": "20/01/2021",
        "id_number_encrypt": res2['data'][0]['hash'],
        "email_encrypt": res4['data'][0]['hash'],
        "contacts": [],
    }
    return public_data


# 用户中心信息，印度、印尼公共部分
def oversea_in_id_individual_bean():
    individual_full_name = random_oversea_name()
    param1 = [generate_data('name', individual_full_name)]
    res1 = request_post(oversea_url, param1)

    individual_email = random_oversea_email()
    param3 = [generate_data('email', individual_email)]
    res3 = request_post(oversea_url, param3)

    individual_phone = random_ind_tel()
    param4 = [generate_data('mobile', individual_phone)]
    res4 = request_post(oversea_url, param4)

    individual_gender = random.choice(['female', 'male'])

    home_address = random_road()
    param5 = [generate_data('address', home_address)]
    res5 = request_post(oversea_url, param5)

    company_name = random_company()

    company_address = random_road()
    param6 = [generate_data('address', company_address)]
    res6 = request_post(oversea_url, param6)

    public_data = {
        "individual_full_name": res1['data'][0]['plain_text'],
        "individual_full_name_encrypt": res1['data'][0]['hash'],
        "individual_email": res3['data'][0]['plain_text'],
        "individual_email_encrypt": res3['data'][0]['hash'],
        "individual_phone": res4['data'][0]['plain_text'],
        "individual_phone_encrypt": res4['data'][0]['hash'],
        "individual_gender": individual_gender,
        "home_address": res5['data'][0]['plain_text'],
        "home_address_encrypt": res5['data'][0]['hash'],
        "company_name": company_name,
        "company_address": res6['data'][0]['plain_text'],
        "company_address_encrypt": res6['data'][0]['hash'],
        "contacts": []
    }
    return public_data


# 用户中心信息，印度独有部分
def oversea_in_individual_bean():
    encrypt_url = Config.OVERSEA_ENCRY_URL

    individual_aadhaar = random_oversea_ind_gennerator()
    param2 = [generate_data('idnum', individual_aadhaar)]
    res2 = request_post(encrypt_url, param2)

    individual_pan = random_oversea_ind_pan_id_card()
    param3 = [generate_data('idnum', individual_pan)]
    res3 = request_post(encrypt_url, param3)

    individual_state = '借款人户籍所在省份aaa'
    individual_city = "借款人户籍所在城市bbb"
    home_state = "借款人居住地址所在省份ccc"
    home_city = "借款人居住地址所在城市ddd"

    individual_address = '借款人户籍地址eee'
    param7 = [generate_data('address', individual_address)]
    res7 = request_post(encrypt_url, param7)

    individual_pan_name = random_oversea_name()
    param1 = [generate_data('name', individual_pan_name)]
    res1 = request_post(encrypt_url, param1)

    asset_language = random.choice(
        ["English", "Urdu", "Hindi", "Oriya", "Telugu", "Bhojpuri",
         "Punjabi", "Nepali", "Gujarati", "Bengali", "Tamil",
         "Other", "Kannada", "Marathi"])

    in_individual = {
        "individual_state": individual_state,
        "individual_city": individual_city,
        "home_state": home_state,
        "home_city": home_city,
        "individual_aadhaar": res2['data'][0]['plain_text'],
        "individual_aadhaar_encrypt": res2['data'][0]['hash'],
        "individual_pan": res3['data'][0]['plain_text'],
        "individual_pan_encrypt": res3['data'][0]['hash'],
        "individual_address": res7['data'][0]['plain_text'],
        "individual_address_encrypt": res7['data'][0]['hash'],
        "individual_pan_name": res1['data'][0]['plain_text'],
        "individual_pan_name_encrypt": res1['data'][0]['hash'],
        "individual_language": [asset_language]
    }
    return in_individual


# # 用户中心信息，印尼独有部分
# def oversea_id_individual_bean():
#     url = Config.OVERSEA_ENCRY_URL
#
#     individual_id_num = random_id_gennerator()
#     param2 = [generate_data('idnum', individual_id_num)]
#     res2 = request_post(url, param2)
#     home_state = "印尼借款人居住地址所在省份ccc"
#
#     id_individual = {
#         "home_province": home_state,
#         "individual_id_num": res2['data'][0]['plain_text'],
#         "individual_id_num_encrypt": res2['data'][0]['hash'],
#         "duration_of_occupancy": random_duration_of_occupancy(),
#         "marital_status": random_marital_status(),
#         "number_of_offspring": random_number_of_offspring(),
#         "education_level": random_education_level(),
#         "job_type": random_job_type(),
#         "monthly_income": random_monthly_income()
#     }
#     return id_individual


# 用户中心信息，印度独有部分，联系人信息
def oversea_ind_contact_bean():
    contacts = []
    for i in range(6):
        encrypt_url = Config.OVERSEA_ENCRY_URL
        contact_name = random_oversea_name()
        param1 = [generate_data('name', contact_name)]
        res1 = request_post(encrypt_url, param1)

        contact_phone = random_ind_tel()
        param2 = [generate_data('mobile', contact_phone)]
        res2 = request_post(encrypt_url, param2)
        c1 = {
            "contact_name": res1['data'][0]['plain_text'],
            "contact_name_encrypt": res1['data'][0]['hash'],
            "contact_phone": res2['data'][0]['plain_text'],
            "contact_phone_encrypt": res2['data'][0]['hash'],
            "contact_relationship": i + 1
        }
        contacts.append(c1)
    return json.dumps(contacts, ensure_ascii=False)


# 用户中心信息，印度独有部分，银行卡信息
def oversea_ind_bank_bean():
    banks = []
    url = Config.OVERSEA_ENCRY_URL
    bank_card_name = random_oversea_name()
    param1 = [generate_data('name', bank_card_name)]
    res1 = request_post(url, param1)

    bank_card_no = random_card_uuid()
    param2 = [generate_data('card_number', bank_card_no)]
    res2 = request_post(url, param2)

    bank_card_account_number = random_bank_card_account_number()
    param3 = [generate_data('card_number', bank_card_account_number)]
    res3 = request_post(url, param3)
    c1 = {
        # 预留姓名
        "bank_card_name": res1['data'][0]['plain_text'],
        "bank_card_name_encrypt": res1['data'][0]['hash'],
        # 银行卡号，线上印度是空，暂时随便mock
        "bank_card_no": res2['data'][0]['plain_text'],
        "bank_card_no_encrypt": res2['data'][0]['hash'],
        # ifsc
        "bank_card_ifsc_code": "CBIN****540",
        "bank_card_ifsc_code_encrypt": "enc_03_3016264629334056960_069",
        # ifsc账户号
        "bank_card_account_number": res3['data'][0]['plain_text'],
        "bank_card_account_number_encrypt": res3['data'][0]['hash']
    }
    upi_name = random_oversea_name()
    param4 = [generate_data('name', upi_name)]
    res4 = request_post(url, param4)

    upi_account_number = random_upi_account_number()
    param5 = [generate_data('card_number', upi_account_number)]
    res5 = request_post(url, param5)
    c2 = {
        # 预留姓名
        "bank_card_name": res4['data'][0]['plain_text'],
        "bank_card_name_encrypt": res4['data'][0]['hash'],
        # UPI
        "individual_bank_card_upi": res5['data'][0]['plain_text'],
        "individual_bank_card_upi_encrypt": res5['data'][0]['hash']
    }
    banks.append(c1)
    banks.append(c2)
    return json.dumps(banks, ensure_ascii=False)


# 用户中心信息，泰国独有部分，联系人信息
def oversea_th_contact_bean():
    contacts = []
    for i in range(6):
        contact_name = random_oversea_name()
        param1 = [generate_data('name', contact_name)]
        res1 = request_post(oversea_url, param1)

        contact_phone = random_th_tel()
        param2 = [generate_data('mobile', contact_phone)]
        res2 = request_post(oversea_url, param2)
        c1 = {
            "contact_name": res1['data'][0]['plain_text'],
            "contact_name_encrypt": res1['data'][0]['hash'],
            "contact_phone": res2['data'][0]['plain_text'],
            "contact_phone_encrypt": res2['data'][0]['hash'],
            "contact_relationship": i + 1
        }
        contacts.append(c1)
    return json.dumps(contacts, ensure_ascii=False)


# 用户中心信息，菲律宾，联系人信息
def oversea_ph_contact_bean():
    contacts = []
    for i in range(5):
        contact_name = random_oversea_name()
        param1 = [generate_data('name', contact_name)]
        res1 = request_post(oversea_url, param1)

        contact_phone = random_php_tel()
        param2 = [generate_data('mobile', contact_phone)]
        res2 = request_post(oversea_url, param2)
        c1 = {
            "contact_name": res1['data'][0]['plain_text'],
            "contact_name_encrypt": res1['data'][0]['hash'],
            "contact_phone": res2['data'][0]['plain_text'],
            "contact_phone_encrypt": res2['data'][0]['hash'],
            "contact_relationship": i + 1
        }
        contacts.append(c1)
    return json.dumps(contacts, ensure_ascii=False)


# 泰国，用户中心信息，银行卡信息
def oversea_th_bank_bean():
    banks = []
    bank_card_account_number = random_bank_card_account_number()
    param3 = [generate_data('card_number', bank_card_account_number)]
    res3 = request_post(oversea_url, param3)
    c1 = {
        # 银行名称
        "bank_name": random_bank_name(),
        # 账户号
        "bank_account": res3['data'][0]['plain_text'],
        "bank_account_encrypt": res3['data'][0]['hash']
    }
    banks.append(c1)
    return json.dumps(banks, ensure_ascii=False)


# 菲律宾，用户中心信息，银行卡信息
def oversea_ph_bank_bean():
    banks = []
    for i in range(3):
        bank_card_account_number = random_bank_card_account_number()
        card_number = [generate_data('card_number', bank_card_account_number)]
        res3 = request_post(oversea_url, card_number)
        c1 = {
            # 卡号来源，1银行，2电子钱包，3线下
            "bank_card_method": random.randint(1, 3),
            # 银行卡号
            "bank_card_account_number_encrypt": res3['data'][0]['hash']
        }
        banks.append(c1)
    return json.dumps(banks, ensure_ascii=False)


# 海外资产头部
def overseas_asset_bean(region, overdue_days, specified_overdue_amount, overdue_amount, asset_from_app="", i=1, period_count=3, period_days=0):
    if region == 'TH':
        app_name = random.choice(["cherry", "mango"])
    if region == 'PH':
        app_name = random.choice(["rose"])
    if region == 'MX':
        app_name = random.choice(["ginkgo", "mexico"])
    if region == 'PK':
        app_name = random.choice(["pk", "pakistan"])
    if region == 'IN':
        app_name = random.choice(["ind002", "ind003", "ind004", "ind005", "ind007"])

    if asset_from_app != "":
        app_name = asset_from_app

    if int(overdue_days) < 1:
        asset_item = region + "_Negative_" + time.strftime("%Y%m%d", time.localtime()) + str(int(time.time() * 1000)) + "_" + str(i + 1)
        asset_penalty_amount = 0
    else:
        asset_item = region + "_" + time.strftime("%Y%m%d", time.localtime()) + str(int(time.time() * 1000)) + "_" + str(i + 1)
        asset_penalty_amount = 6888

    if period_days == 0:
        asset_period_type = "month"
    else:
        asset_period_type = "day"

    body = {
        "asset_item_number": asset_item,
        "asset_from_system": region,
        "asset_from_app": app_name,
        "asset_type": "paydayloan",
        "asset_sub_type": "multiple",
        "asset_name": asset_item,
        "asset_sign_at": get_before_date(overdue_days, period_days, -period_count) + " 16:00:00",
        "asset_grant_at": get_before_date(overdue_days, period_days, -period_count) + " 16:00:00",
        "asset_due_at": get_before_date(overdue_days, period_days, period_count-1) + " 00:00:00",
        "asset_channel": "nbfc_sino",
        "asset_city_code": "",
        "asset_status": "repay",
        "asset_loan_channel": "tha_picocapital_plus",
        "asset_repaid_amount": 0,
        "asset_period_type": asset_period_type,
        "asset_period_count": period_count,
        "asset_period_days": period_days,
        "asset_ref_order_no": "ref_" + asset_item,
        "asset_ref_order_type": "game_bill",
        "asset_risk_level": "2",
        "asset_sub_order_type": "",
        "asset_product_name": "NBFC",
        "asset_actual_grant_at": get_before_date(overdue_days, period_days, -period_count) + " 16:00:00",
        "asset_owner": region,
        "asset_version": int(time.time() * 1000),
        "asset_credit_term": 0,
        "asset_repayment_app": ""
    }

    if specified_overdue_amount is True:
        principal_amount = int((overdue_amount - asset_penalty_amount) * 0.9)
        interest_amount = overdue_amount - asset_penalty_amount - principal_amount
        amount_body = {
            "asset_interest_amount": interest_amount,
            "asset_repaid_interest_amount": 0,
            "asset_principal_amount": principal_amount,
            "asset_repaid_principal_amount": 0,
            "asset_penalty_amount": asset_penalty_amount,
            "asset_repaid_penalty_amount": 0,
            "asset_decrease_penalty_amount": 0,
            "asset_fee_amount": 0,
            "asset_repaid_fee_amount": 0,
        }
    if specified_overdue_amount is False:
        amount_body = {
            "asset_interest_amount": 3333 * period_count,
            "asset_repaid_interest_amount": 0,
            "asset_principal_amount": 200000 * period_count,
            "asset_repaid_principal_amount": 0,
            "asset_penalty_amount": asset_penalty_amount,
            "asset_repaid_penalty_amount": 0,
            "asset_decrease_penalty_amount": 0,
            "asset_fee_amount": 0,
            "asset_repaid_fee_amount": 0,
        }
    body.update(amount_body)
    return json.dumps(body, ensure_ascii=False)


# 海外借款人，只需要用到参数borrower_uuid
def borrower_bean():
    body = {
        "borrower_uuid": timestamp,
        "borrower_card_uuid": random_card_uuid(),
        "individual_uuid": "2440806398317",
        "individual_id_num": "enc_02_2972218610539825152_880",
        "individual_tel": "enc_01_2970130348065163264_569"
    }
    return json.dumps(body, ensure_ascii=False)


# 海外还款计划，费用类型有区别
def overseas_asset_transaction(overdue_days, principal_amount, interest_amount, penalty_amount, period_count, period_days):
    transactions = []
    lateinterest = {
        "asset_transaction_type": "lateinterest",
        "asset_transaction_amount": penalty_amount,
        "asset_transaction_status": "unfinish",
        "asset_transaction_expect_finish_time": get_before_date(overdue_days, period_days, 0) + " 00:00:00",
        "asset_transaction_finish_at": "",
        "asset_transaction_period": 1,
        "asset_transaction_remark": "",
        "asset_transaction_decrease_amount": 0,
        "asset_transaction_repaid_amount": 0
    }
    if overdue_days > 0:
        transactions.append(lateinterest)

    principal_integer = int(principal_amount / period_count)
    principal_reminder = principal_amount % period_count
    interest_integer = int(interest_amount / period_count)
    interest_reminder = interest_amount % period_count

    for i in range(period_count):
        # 末期取剩余
        if i == period_count - 1:
            principal_amount = principal_integer + principal_reminder
            interest_amount = interest_integer + interest_reminder
        else:
            principal_amount = principal_integer
            interest_amount = interest_integer
        repayprincipal = {
            "asset_transaction_type": "repayprincipal",
            "asset_transaction_amount": principal_amount,
            "asset_transaction_status": "unfinish",
            "asset_transaction_expect_finish_time": get_before_date(overdue_days, period_days, i) + " 00:00:00",
            "asset_transaction_finish_at": "",
            "asset_transaction_period": i + 1,
            "asset_transaction_remark": "",
            "asset_transaction_decrease_amount": 0,
            "asset_transaction_repaid_amount": 0
        }
        repayinterest = {
            "asset_transaction_type": "repayinterest",
            "asset_transaction_amount": interest_amount,
            "asset_transaction_status": "unfinish",
            "asset_transaction_expect_finish_time": get_before_date(overdue_days, period_days, i) + " 00:00:00",
            "asset_transaction_finish_at": "",
            "asset_transaction_period": i + 1,
            "asset_transaction_remark": "",
            "asset_transaction_decrease_amount": 0,
            "asset_transaction_repaid_amount": 0
        }
        transactions.append(repayprincipal)
        transactions.append(repayinterest)
    return json.dumps(transactions, ensure_ascii=False)


def get_cn_contact():
    public_data = {
        "asset_item_number": time.strftime("%Y%m%d", time.localtime()) + str(int(time.time() * 1000)),
        "d0": []
    }
    return public_data


def get_cn_contact_bean(count):
    contacts_list = []
    for i in range(count):
        contact_name = random_name()
        param1 = [generate_data('name', contact_name)]
        res1 = request_post(url, param1)

        contact_phone = random_tele(is_false=False)
        param2 = [generate_data('mobile', contact_phone)]
        res2 = request_post(url, param2)
        c1 = {"phone_num_loc": "北京",
              "intimacy": random.randint(600, 700),
              "call_cnt": "1",
              "name": res1['data'][0]['hash'],
              "phone_num": res2['data'][0]['hash'],
              "relation_ship": random.randint(1, 4),
              "label": "1",
              "call_len": random.randint(0, 10),
              "is_emergency": ""
              }
        contacts_list.append(c1)
    return json.dumps(contacts_list, ensure_ascii=False)


def get_cn_long_contact_bean():
    long_contacts = []
    contact_name = random_name()
    param1 = [generate_data('name', contact_name)]
    res1 = request_post(url, param1)

    contact_phone = random_tele(is_false=False)
    param2 = [generate_data('mobile', contact_phone)]
    res2 = request_post(url, param2)
    c1 = {"phone_num_loc": "北京",
          "intimacy": random.randint(600, 700),
          "call_cnt": "1",
          "name": res1['data'][0]['hash'],
          "phone_num": res2['data'][0]['hash'],
          "relation_ship": random.randint(1, 4),
          "call_len": random.randint(0, 10)}
    long_contacts.append(c1)
    return json.dumps(long_contacts, ensure_ascii=False)


# 用户中心信息，墨西哥，联系人信息，1父母、2丈夫、3儿子、4朋友/同事
def oversea_mex_contact_bean():
    contacts = []
    for i in range(4):
        contact_name = random_oversea_name()
        param1 = [generate_data('name', contact_name)]
        res1 = request_post(oversea_url, param1)

        contact_phone = random_mex_tel()
        param2 = [generate_data('mobile', contact_phone)]
        res2 = request_post(oversea_url, param2)
        c1 = {
            "contact_name": res1['data'][0]['plain_text'],
            "contact_name_encrypt": res1['data'][0]['hash'],
            "contact_phone": res2['data'][0]['plain_text'],
            "contact_phone_encrypt": res2['data'][0]['hash'],
            "contact_relationship": i + 1
        }
        contacts.append(c1)
    return json.dumps(contacts, ensure_ascii=False)


# 用户中心信息，巴基斯坦，联系人信息，1:Father/Mother 2:Spouse 3:Brother/Sister 4:Colleague/Friend
def oversea_pk_contact_bean():
    contacts = []
    for i in range(4):
        contact_name = random_oversea_name()
        param1 = [generate_data('name', contact_name)]
        res1 = request_post(oversea_url, param1)

        contact_phone = random_pk_tel()
        param2 = [generate_data('mobile', contact_phone)]
        res2 = request_post(oversea_url, param2)
        c1 = {
            "contact_name_encrypt": res1['data'][0]['hash'],
            "contact_phone_encrypt": res2['data'][0]['hash'],
            "contact_relationship": i + 1
        }
        contacts.append(c1)
    return json.dumps(contacts, ensure_ascii=False)


def get_overseas_contact():
    public_data = {
        "asset_number": "php_test_20210427_000001",
        "contacts": [],
        "long_contacts": []
    }
    return public_data


def get_overseas_contact_bean(count, region, source):
    contacts_list = []

    for i in range(count):
        if region == "TH":
            contact_phone = random_th_tel()
        if region == "PH":
            contact_phone = random_php_tel()
        if region == "MX":
            contact_phone = random_mex_tel()
        if region == "PK":
            contact_phone = random_pk_tel()
        if region == "IN":
            contact_phone = random_ind_tel()

        contact_name = random_oversea_name()
        param1 = [generate_data('name', contact_name)]
        res1 = request_post(oversea_url, param1)

        param2 = [generate_data('mobile', contact_phone)]
        res2 = request_post(oversea_url, param2)
        c1 = {"phone_num_loc": "",
              "intimacy": random.randint(1, 700),
              "call_cnt": "",
              "phone_num_enc": res2['data'][0]['hash'],
              "relation_ship": random.randint(1, 4),
              "call_len": random.randint(0, 10),
              "name_enc": res1['data'][0]['hash']
              }
        if source == "sms":
            c1.update({"source": "sms"})
        contacts_list.append(c1)
    return json.dumps(contacts_list, ensure_ascii=False)


def get_overseas_repay_list_public(page_index, page_size):
    # total_pages = random.randint(1, 20)
    total_pages = 300
    total_count = page_size * (total_pages - 1) + 2
    public_data = {
        "page_index": page_index,
        "page_size": page_size,
        "total_count": total_count,
        "total_pages": 1,
        "data_list": []
    }
    return public_data


def get_overseas_repay_list_data(page_index, page_size, total_count, total_pages, start_date):
    data_list = []
    count = 0
    num_start = page_size * (page_index - 1)
    if page_index < total_pages:
        count = page_index * page_size
    # 最后一页
    if page_index == total_pages:
        count = total_count

    # 分页返回
    # for i in range(num_start, count):

    # 一次性返回所有的回款
    for i in range(total_count):
        item_no = "Test_reconcile_" + time.strftime("%Y%m%d", time.localtime()) + timestamp + "_" + str(i + 1)
        repay_amount = random.randint(-504000, -10000)
        repay_period = random.randint(1, 3)

        c1 = {
            "item_no": item_no,
            "repay_date": start_date,
            "repay_amount": repay_amount,
            "repay_period": repay_period
        }
        data_list.append(c1)
    return json.dumps(data_list, ensure_ascii=False)


def get_overseas_repay_detail_public(item_no, repay_date):
    public_data = {
        "from_system": "Rbiz",
        "key": "ab1798362b1843b189cb6d26ca19e4fa",
        "type": "AssetChangeNotify",
        "data": {
            "asset": {
                "type": "paydayloan",
                "status": "repay",
                "decreaseAmount": 125,
                "version": timestamp,
                "asset_item_no": item_no,
                "asset_owner": "TAILAND",
                "sub_type": "multiple",
                "period_type": "day",
                "period_count": 4,
                "product_category": "7",
                "cmdb_product_number": "tha_picocapital_plus_4_7d_20210827",
                "grant_at": "2022-10-18 05:18:25",
                "effect_at": "2022-10-18 05:18:25",
                "actual_grant_at": "2022-10-18 05:18:25",
                "due_at": "2022-11-15 00:00:00",
                "payoff_at": "2022-11-24 00:00:00",
                "from_system": "tha",
                "principal_amount": 500000,
                "granted_principal_amount": 500000,
                "loan_channel": "tha_picocapital_plus",
                "alias_name": "",
                "interest_amount": 14000,
                "fee_amount": 0,
                "balance_amount": 385500,
                "repaid_amount": 128625,
                "total_amount": 514250,
                "interest_rate": "6.500",
                "charge_type": 0,
                "ref_order_no": "",
                "ref_order_type": "mileVIPstore_bill",
                "withholding_amount": "",
                "sub_order_type": "",
                "actual_payoff_at": "1000-01-01 00:00:00",
                "ref_item_no": "",
                "product_name": "",
                "from_system_name": "null",
                "order_to_asset": False,
                "late_amount": 125,
                "repaid_late_amount": 125,
                "repaid_fee_amount": 0,
                "decrease_interest_amount": 0,
                "decrease_fee_amount": 0,
                "decrease_late_amount": 125,
                "from_app": "mango",
                "decrease_principal_amount": 0,
                "repaid_principal_amount": 125000,
                "repaid_interest_amount": 0
            },
            "trans": [
                {
                    "type": "lateinterest",
                    "description": "罚息",
                    "amount": 125,
                    "status": "finish",
                    "period": 1,
                    "remark": "",
                    "category": "late",
                    "asset_item_no": item_no,
                    "decrease_amount": 125,
                    "repaid_amount": 125,
                    "total_amount": 250,
                    "balance_amount": 0,
                    "due_at": repay_date + " 00:00:00",
                    "finish_at": repay_date + " 05:18:38",
                    "late_status": "normal",
                    "repay_priority": 3,
                    "trade_at": repay_date + " 05:18:38",
                    "create_at": repay_date + " 05:18:31",
                    "update_at": repay_date + " 05:18:39"
                },
                {
                    "type": "repayinterest",
                    "description": "利息",
                    "amount": 3500,
                    "status": "finish",
                    "period": 1,
                    "remark": "",
                    "category": "interest",
                    "asset_item_no": item_no,
                    "decrease_amount": 0,
                    "repaid_amount": 3500,
                    "total_amount": 3500,
                    "balance_amount": 0,
                    "due_at": "2022-10-25 00:00:00",
                    "finish_at": repay_date + " 05:18:38",
                    "late_status": "late",
                    "repay_priority": 80,
                    "trade_at": repay_date + " 05:18:38",
                    "create_at": repay_date + " 05:18:25",
                    "update_at": repay_date + " 05:18:39"
                },
                {
                    "type": "repayprincipal",
                    "description": "本金",
                    "amount": 125000,
                    "status": "finish",
                    "period": 1,
                    "remark": "",
                    "category": "principal",
                    "asset_item_no": item_no,
                    "decrease_amount": 0,
                    "repaid_amount": 125000,
                    "total_amount": 125000,
                    "balance_amount": 0,
                    "due_at": "2022-10-25 00:00:00",
                    "finish_at": repay_date + " 05:18:38",
                    "late_status": "late",
                    "repay_priority": 90,
                    "trade_at": repay_date + " 05:18:38",
                    "create_at": repay_date + " 05:18:25",
                    "update_at": repay_date + " 05:18:40"
                },
                {
                    "type": "repayinterest",
                    "description": "利息",
                    "amount": 3500,
                    "status": "nofinish",
                    "period": 2,
                    "remark": "",
                    "category": "interest",
                    "asset_item_no": item_no,
                    "decrease_amount": 0,
                    "repaid_amount": 0,
                    "total_amount": 3500,
                    "balance_amount": 3500,
                    "due_at": "2022-11-01 00:00:00",
                    "finish_at": "1000-01-01 00:00:00",
                    "late_status": "normal",
                    "repay_priority": 80,
                    "trade_at": repay_date + " 05:18:25",
                    "create_at": repay_date + " 05:18:25",
                    "update_at": repay_date + " 05:18:35"
                },
                {
                    "type": "repayprincipal",
                    "description": "本金",
                    "amount": 125000,
                    "status": "nofinish",
                    "period": 2,
                    "remark": "",
                    "category": "principal",
                    "asset_item_no": item_no,
                    "decrease_amount": 0,
                    "repaid_amount": 0,
                    "total_amount": 125000,
                    "balance_amount": 125000,
                    "due_at": "2022-11-01 00:00:00",
                    "finish_at": "1000-01-01 00:00:00",
                    "late_status": "normal",
                    "repay_priority": 90,
                    "trade_at": repay_date + " 05:18:25",
                    "create_at": repay_date + " 05:18:25",
                    "update_at": repay_date + " 05:18:35"
                },
                {
                    "type": "repayinterest",
                    "description": "利息",
                    "amount": 3500,
                    "status": "nofinish",
                    "period": 3,
                    "remark": "",
                    "category": "interest",
                    "asset_item_no": item_no,
                    "decrease_amount": 0,
                    "repaid_amount": 0,
                    "total_amount": 3500,
                    "balance_amount": 3500,
                    "due_at": "2022-11-08 00:00:00",
                    "finish_at": "1000-01-01 00:00:00",
                    "late_status": "normal",
                    "repay_priority": 80,
                    "trade_at": repay_date + " 05:18:25",
                    "create_at": repay_date + " 05:18:25",
                    "update_at": repay_date + " 05:18:35"
                },
                {
                    "type": "repayprincipal",
                    "description": "本金",
                    "amount": 125000,
                    "status": "nofinish",
                    "period": 3,
                    "remark": "",
                    "category": "principal",
                    "asset_item_no": item_no,
                    "decrease_amount": 0,
                    "repaid_amount": 0,
                    "total_amount": 125000,
                    "balance_amount": 125000,
                    "due_at": "2022-11-08 00:00:00",
                    "finish_at": "1000-01-01 00:00:00",
                    "late_status": "normal",
                    "repay_priority": 90,
                    "trade_at": repay_date + " 05:18:25",
                    "create_at": repay_date + " 05:18:25",
                    "update_at": repay_date + " 05:18:35"
                },
                {
                    "type": "repayinterest",
                    "description": "利息",
                    "amount": 3500,
                    "status": "nofinish",
                    "period": 4,
                    "remark": "",
                    "category": "interest",
                    "asset_item_no": item_no,
                    "decrease_amount": 0,
                    "repaid_amount": 0,
                    "total_amount": 3500,
                    "balance_amount": 3500,
                    "due_at": "2022-11-15 00:00:00",
                    "finish_at": "1000-01-01 00:00:00",
                    "late_status": "normal",
                    "repay_priority": 80,
                    "trade_at": repay_date + " 05:18:25",
                    "create_at": repay_date + " 05:18:25",
                    "update_at": repay_date + " 05:18:35"
                },
                {
                    "type": "repayprincipal",
                    "description": "本金",
                    "amount": 125000,
                    "status": "nofinish",
                    "period": 4,
                    "remark": "",
                    "category": "principal",
                    "asset_item_no": item_no,
                    "decrease_amount": 0,
                    "repaid_amount": 0,
                    "total_amount": 125000,
                    "balance_amount": 125000,
                    "due_at": "2022-11-15 00:00:00",
                    "finish_at": "1000-01-01 00:00:00",
                    "late_status": "normal",
                    "repay_priority": 90,
                    "trade_at": repay_date + " 05:18:25",
                    "create_at": repay_date + " 05:18:25",
                    "update_at": repay_date + " 05:18:35"
                }
            ],
            "action": "null",
            "type": "null",
            "tran_logs": [
                {
                    "id": 293634,
                    "asset_item_no": item_no,
                    "asset_tran_no": "10353558",
                    "operate_type": "withhold_repay",
                    "amount": -125,
                    "operate_flag": "normal",
                    "comment": "代扣还款",
                    "from_system": "rbiz",
                    "ref_no": "10109429",
                    "operator_id": 0,
                    "operator_name": "",
                    "create_at": repay_date + " 05:18:39",
                    "update_at": repay_date + " 05:18:39",
                    "tran_type": "lateinterest",
                    "period": 1,
                    "withhold_finish_at": repay_date + " 05:18:38"
                },
                {
                    "id": 293635,
                    "asset_item_no": item_no,
                    "asset_tran_no": "10353550",
                    "operate_type": "withhold_repay",
                    "amount": -3500,
                    "operate_flag": "normal",
                    "comment": "代扣还款",
                    "from_system": "rbiz",
                    "ref_no": "10109430",
                    "operator_id": 0,
                    "operator_name": "",
                    "create_at": repay_date + " 05:18:39",
                    "update_at": repay_date + " 05:18:39",
                    "tran_type": "repayinterest",
                    "period": 1,
                    "withhold_finish_at": repay_date + " 05:18:38"
                },
                {
                    "id": 293636,
                    "asset_item_no": item_no,
                    "asset_tran_no": "10353546",
                    "operate_type": "withhold_repay",
                    "amount": -125000,
                    "operate_flag": "normal",
                    "comment": "代扣还款",
                    "from_system": "rbiz",
                    "ref_no": "10109431",
                    "operator_id": 0,
                    "operator_name": "",
                    "create_at": repay_date + " 05:18:40",
                    "update_at": repay_date + " 05:18:40",
                    "tran_type": "repayprincipal",
                    "period": 1,
                    "withhold_finish_at": repay_date + " 05:18:38"
                }
            ],
            "delay_infos": "null"
        },
        "sync_datetime": "null",
        "busi_key": "null"
    }
    return public_data


# 拼接结清资产的asset节点
def get_payoff_asset_detail(country, asset_item_number, asset_info):
    # 已还
    asset_repaid_interest_amount = asset_info[0]["asset_repaid_interest_amount"] + (
            asset_info[0]["overdue_interest_amount"] - asset_info[0]["recovery_interest_amount"])
    asset_repaid_principal_amount = asset_info[0]["asset_repaid_principal_amount"] + (
            asset_info[0]["overdue_principal_amount"] - asset_info[0]["recovery_principal_amount"])
    asset_repaid_fee_amount = asset_info[0]["asset_repaid_fee_amount"] + (asset_info[0]["overdue_fee_amount"] - asset_info[0]["recovery_fee_amount"])
    asset_repaid_penalty_amount = asset_info[0]["asset_repaid_penalty_amount"] + (
            asset_info[0]["overdue_penalty_amount"] - asset_info[0]["recovery_penalty_amount"])
    asset_repaid_amount = asset_repaid_principal_amount + asset_repaid_interest_amount + asset_repaid_fee_amount + asset_repaid_penalty_amount

    # 应还
    asset_interest_amount = asset_info[0]["asset_interest_amount"]
    asset_principal_amount = asset_info[0]["asset_principal_amount"]
    asset_fee_amount = asset_info[0]["asset_fee_amount"]
    asset_penalty_amount = asset_info[0]["asset_penalty_amount"]
    asset_total_amount = asset_principal_amount + asset_interest_amount + asset_fee_amount + asset_penalty_amount

    if asset_repaid_amount == asset_total_amount:
        asset_status = 'payoff'
    if asset_repaid_amount != asset_total_amount:
        asset_status = 'repay'
    if country == "CN":
        asset_type = "现金贷"
    if country in ("TH", "PH", "MX", "IN", "PK"):
        asset_type = "paydayloan"

    asset_body = {
        "asset_item_number": asset_item_number,
        "asset_from_system": asset_info[0]["asset_from_system"],
        "asset_from_app": asset_info[0]["asset_from_app"],
        "asset_type": asset_type,
        "asset_sub_type": "multiple",
        "asset_name": asset_item_number,
        "asset_sign_at": asset_info[0]["asset_sign_at"],
        "asset_grant_at": asset_info[0]["asset_grant_at"],
        "asset_due_at": asset_info[0]["asset_due_at"],
        "asset_channel": asset_info[0]["asset_channel"],
        "asset_city_code": asset_info[0]["asset_city_code"],
        "asset_status": asset_status,
        "asset_loan_channel": asset_info[0]["asset_loan_channel"],
        "asset_repaid_amount": asset_repaid_amount,
        "asset_period_type": asset_info[0]["asset_period_type"],
        "asset_period_count": asset_info[0]["asset_period_count"],
        "asset_period_days": asset_info[0]["asset_period_days"],
        "asset_ref_order_no": asset_info[0]["asset_ref_order_no"],
        "asset_ref_order_type": asset_info[0]["asset_ref_order_type"],
        "asset_risk_level": "2",
        "asset_sub_order_type": "null",
        "asset_product_name": asset_info[0]["asset_product_name"],
        "asset_actual_grant_at": asset_info[0]["asset_actual_grant_at"],
        "asset_owner": asset_info[0]["asset_owner"],
        "asset_version": int(time.time() * 1000),
        "asset_credit_term": asset_info[0]["asset_credit_term"],
        "asset_repayment_app": "",
        "asset_interest_amount": asset_interest_amount,
        "asset_repaid_interest_amount": asset_repaid_interest_amount,
        "asset_principal_amount": asset_principal_amount,
        "asset_repaid_principal_amount": asset_repaid_principal_amount,
        "asset_penalty_amount": asset_penalty_amount,
        "asset_repaid_penalty_amount": asset_repaid_penalty_amount,
        "asset_decrease_penalty_amount": asset_info[0]["asset_decrease_penalty_amount"],
        "asset_fee_amount": asset_fee_amount,
        "asset_repaid_fee_amount": asset_repaid_fee_amount
    }
    return json.dumps(asset_body, ensure_ascii=False)


# 国内，拼接结清资产的borrower节点
def get_payoff_borrower_detail(asset_item_number):
    borrower_info = get_individual(asset_item_number)
    borrower_body = {
        "enc_individual_name": borrower_info[0]["enc_individual_name"],
        "enc_individual_idnum": borrower_info[0]["enc_individual_idnum"],
        "enc_individual_tel": borrower_info[0]["enc_individual_tel"],
        "enc_individual_work_tel": borrower_info[0]["enc_individual_work_tel"],
        "enc_individual_residence_tel": borrower_info[0]["enc_individual_residence_tel"],
        "enc_individual_mate_name": borrower_info[0]["enc_individual_mate_name"],
        "enc_individual_mate_tel": borrower_info[0]["enc_individual_mate_tel"],
        "enc_individual_relative_name": borrower_info[0]["enc_individual_relative_name"],
        "enc_individual_relative_tel": borrower_info[0]["enc_individual_relative_tel"],
        "enc_individual_workmate_name": borrower_info[0]["enc_individual_workmate_name"],
        "enc_individual_workmate_tel": borrower_info[0]["enc_individual_workmate_tel"],
        "individual_gender": borrower_info[0]["individual_gender"],
        "individual_residence": borrower_info[0]["individual_residence"],
        "individual_workplace": borrower_info[0]["individual_workplace"],
        "individual_permanent": borrower_info[0]["individual_permanent"],
        "individual_company": borrower_info[0]["individual_company"],
        "individual_remark": borrower_info[0]["individual_remark"],
        "individual_nation": borrower_info[0]["individual_nation"],
        "individual_email": "18690532146@qq.com",
        "individual_relative_relation": borrower_info[0]["individual_relative_relation"],
        "individual_name": "",
        "individual_idnum": "",
        "individual_tel": "",
        "individual_work_tel": "",
        "individual_residence_tel": "",
        "individual_mate_name": "",
        "individual_mate_tel": "",
        "individual_relative_name": "",
        "individual_relative_tel": "",
        "individual_workmate_name": "",
        "individual_workmate_tel": "",
        "code_individual_name": "",
        "code_individual_idnum": "",
        "code_individual_tel": "",
        "code_individual_work_tel": "",
        "code_individual_residence_tel": "",
        "code_individual_mate_name": "",
        "code_individual_mate_tel": "",
        "code_individual_relative_name": "",
        "code_individual_relative_tel": "",
        "code_individual_workmate_name": "",
        "code_individual_workmate_tel": ""
    }
    return json.dumps(borrower_body, ensure_ascii=False)


# 拼接结清资产的asset_transactions节点
def get_payoff_transactions_detail(country, asset_item_number):
    atr_info = get_period_transaction(asset_item_number, 0, None)
    asset_transactions = []
    for i in range(len(atr_info)):
        transaction = {
            "asset_transaction_type": atr_info[i]["asset_transaction_type"],
            "asset_transaction_amount": atr_info[i]["asset_transaction_amount"],
            "asset_transaction_expect_finish_time": atr_info[i]["asset_transaction_expect_finish_time"],
            "asset_transaction_period": atr_info[i]["asset_transaction_period"],
            "asset_transaction_remark": "",
            "asset_transaction_decrease_amount": atr_info[i]["asset_transaction_decrease_amount"],
        }
        asset_transaction_expect_finish_time = datetime.datetime.strptime(atr_info[i]["asset_transaction_expect_finish_time"], "%Y-%m-%d %H:%M:%S")
        current_date = datetime.datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")
        diff_date = (current_date - asset_transaction_expect_finish_time).days
        LogUtil.log_info("#### 结清资产=%s，预期完成时间=%s，当前日期=%s，日期差=%s" % (asset_item_number, asset_transaction_expect_finish_time, current_date, diff_date))
        if country == "CN":
            if diff_date > 0:
                transaction["asset_transaction_status"] = "finish"
                transaction["asset_transaction_finish_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                transaction["asset_transaction_repaid_amount"] = atr_info[i]["asset_transaction_amount"]
            if diff_date < 0:
                transaction["asset_transaction_status"] = "unfinish"
                transaction["asset_transaction_finish_at"] = ""
                transaction["asset_transaction_repaid_amount"] = 0
            asset_transactions.append(transaction)
        # 海外有预提醒，目前最早D-2开始催收
        if country in ("TH", "PH", "MX", "IN", "PK"):
            if diff_date >= -2:
                transaction["asset_transaction_status"] = "finish"
                transaction["asset_transaction_finish_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                transaction["asset_transaction_repaid_amount"] = atr_info[i]["asset_transaction_amount"]
            if diff_date < -2:
                transaction["asset_transaction_status"] = "unfinish"
                transaction["asset_transaction_finish_at"] = ""
                transaction["asset_transaction_repaid_amount"] = 0
            asset_transactions.append(transaction)
    return json.dumps(asset_transactions, ensure_ascii=False)


# 拼接回款的asset节点，金额改从还款计划里取。
def get_repay_period_asset_detail(country, asset_item_number, asset_info, repay_period):
    # 获取还款计划
    trans_info = get_transaction(asset_item_number)
    asset_repaid_principal_amount = asset_repaid_interest_amount = asset_repaid_fee_amount = asset_repaid_penalty_amount = 0
    asset_principal_amount = asset_interest_amount = asset_fee_amount = asset_penalty_amount = asset_decrease_penalty_amount = 0
    repaid_principal_amount = repaid_interest_amount = repaid_fee_amount = repaid_penalty_amount = asset_repaid_amount = 0
    for i in range(len(trans_info)):
        if trans_info[i]["asset_transaction_type"] == "repayprincipal":
            # 应还本金总额
            asset_principal_amount = int(trans_info[i]["asset_transaction_amount"])
            if trans_info[i]["asset_transaction_period"] == repay_period:
                repaid_principal_amount = trans_info[i]["asset_transaction_amount"]
            if trans_info[i]["asset_transaction_period"] != repay_period and trans_info[i]["asset_transaction_status"] == "finish":
                repaid_principal_amount = trans_info[i]["asset_transaction_repaid_amount"]
            # 已还本金总额
            asset_repaid_principal_amount = int(repaid_principal_amount)

        if trans_info[i]["asset_transaction_type"] == "repayinterest":
            # 应还利息总额
            asset_interest_amount = int(trans_info[i]["asset_transaction_amount"])
            if trans_info[i]["asset_transaction_period"] == repay_period:
                repaid_interest_amount = trans_info[i]["asset_transaction_amount"]
            if trans_info[i]["asset_transaction_period"] != repay_period and trans_info[i]["asset_transaction_status"] == "finish":
                repaid_interest_amount = trans_info[i]["asset_transaction_repaid_amount"]
            # 已还利息总额
            asset_repaid_interest_amount = int(repaid_interest_amount)

        if trans_info[i]["asset_transaction_type"] not in ("repayprincipal", "repayinterest", "repaylateinterest", "lateinterest"):
            # 应还费用总额
            asset_fee_amount = int(trans_info[i]["asset_transaction_amount"])
            if trans_info[i]["asset_transaction_period"] == repay_period:
                repaid_fee_amount = trans_info[i]["asset_transaction_amount"]
            if trans_info[i]["asset_transaction_period"] != repay_period and trans_info[i]["asset_transaction_status"] == "finish":
                repaid_fee_amount = trans_info[i]["asset_transaction_repaid_amount"]
            # 已还费用总额
            asset_repaid_fee_amount = int(repaid_fee_amount)

        if trans_info[i]["asset_transaction_type"] in ("repaylateinterest", "lateinterest"):
            # 应还罚息总额
            asset_penalty_amount = int(trans_info[i]["asset_transaction_amount"])
            # 已减免罚息总额
            asset_decrease_penalty_amount = int(trans_info[i]["asset_transaction_decrease_amount"])
            if trans_info[i]["asset_transaction_period"] == repay_period:
                repaid_penalty_amount = trans_info[i]["asset_transaction_amount"]
            if trans_info[i]["asset_transaction_period"] != repay_period and trans_info[i]["asset_transaction_status"] == "finish":
                repaid_penalty_amount = trans_info[i]["asset_transaction_repaid_amount"]
            # 已还罚息总额
            asset_repaid_penalty_amount = int(repaid_penalty_amount)
        # 已还总额
        asset_repaid_amount = asset_repaid_principal_amount + asset_repaid_interest_amount + asset_repaid_fee_amount + asset_repaid_penalty_amount

    # 应还总额
    asset_total_amount = asset_principal_amount + asset_interest_amount + asset_fee_amount + asset_penalty_amount + asset_decrease_penalty_amount
    # 未还总额
    balance_amount = asset_total_amount - asset_repaid_amount - asset_decrease_penalty_amount
    if asset_repaid_amount == (asset_total_amount - asset_decrease_penalty_amount):
        asset_status = 'payoff'
    if asset_repaid_amount != (asset_total_amount - asset_decrease_penalty_amount):
        asset_status = 'repay'
    if country == "CN" and asset_info[0]["asset_loan_channel"] == "noloan":
        asset_type = "comboOrder"
    else:
        asset_type = "paydayloan"
    order_to_asset = eval("True") if asset_info[0]["asset_loan_channel"] == "noloan" else eval("False")

    asset_public_body = {
        "type": asset_type,
        "status": asset_status,
        "decreaseAmount": asset_decrease_penalty_amount,
        "version": int(time.time() * 1000),
        "asset_item_no": asset_item_number,
        "asset_owner": asset_info[0]["asset_owner"],
        "sub_type": "multiple",
        "period_type": asset_info[0]["asset_period_type"],
        "period_count": asset_info[0]["asset_period_count"],
        "product_category": "7",
        "cmdb_product_number": "mangguo_postservice54%_rate1‰_late5%",
        "grant_at": asset_info[0]["asset_grant_at"],
        "effect_at": asset_info[0]["asset_grant_at"],
        "actual_grant_at": asset_info[0]["asset_actual_grant_at"],
        "due_at": asset_info[0]["asset_due_at"],
        "payoff_at": asset_info[0]["asset_due_at"],
        "from_system": asset_info[0]["asset_from_system"],
        "principal_amount": asset_principal_amount,
        "granted_principal_amount": asset_principal_amount,
        "loan_channel": asset_info[0]["asset_loan_channel"],
        "alias_name": "",
        "interest_amount": asset_interest_amount,
        "fee_amount": asset_fee_amount,
        "balance_amount": balance_amount,
        "repaid_amount": asset_repaid_amount,
        "total_amount": asset_total_amount,
        "interest_rate": "0.360",
        "charge_type": 0,
        "ref_order_no": asset_info[0]["asset_ref_order_no"],
        "ref_order_type": asset_info[0]["asset_ref_order_type"],
        "withholding_amount": "",
        "sub_order_type": "",
        "actual_payoff_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") if asset_status == "payoff" else "",
        "ref_item_no": "",
        "product_name": "",
        "order_to_asset": order_to_asset,
        "late_amount": asset_penalty_amount,
        "repaid_late_amount": asset_repaid_penalty_amount,
        "repaid_fee_amount": asset_repaid_fee_amount,
        "decrease_fee_amount": 0,
        "decrease_late_amount": asset_decrease_penalty_amount,
        "from_app": asset_info[0]["asset_from_app"]
    }
    if country == "CN":
        unique_body = {
            "asset_repayment_app": "",
            "product_code": ""
        }
    if country in ("TH", "PH", "MX", "IN", "PK"):
        unique_body = {
            "decrease_interest_amount": 0,
            "decrease_principal_amount": 0,
            "repaid_principal_amount": asset_repaid_principal_amount,
            "repaid_interest_amount": asset_repaid_interest_amount
        }
    asset_public_body.update(unique_body)
    return json.dumps(asset_public_body, ensure_ascii=False)


# 拼接回款的还款计划，海外：trans，国内：dtransactions、fees
def get_repay_trans(asset_item_number, transaction_type, repay_period, repay_date, country):
    trans_info = get_transaction(asset_item_number)
    final_body = []
    for i in range(len(trans_info)):
        due_at_date = datetime.datetime.strptime(trans_info[i]["asset_transaction_expect_finish_time"], "%Y-%m-%d %H:%M:%S")
        current_date = datetime.datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")
        # 非指定的还款期次 且 已完成状态，回款完成时间取还款计划中的实际完成时间
        if trans_info[i]["asset_transaction_status"] == "finish" and trans_info[i]["asset_transaction_period"] != repay_period:
            finish_at = trans_info[i]["asset_transaction_finish_at"]
            status = "finish"
            repaid_amount = trans_info[i]["asset_transaction_amount"]
            finish_date = datetime.datetime.strptime(finish_at, "%Y-%m-%d %H:%M:%S")
        # 非指定的还款期次 且 未完成状态，回款完成时间使用 1000-01-01 00:00:00
        if trans_info[i]["asset_transaction_status"] == "unfinish" and trans_info[i]["asset_transaction_period"] != repay_period:
            finish_at = "1000-01-01 00:00:00"
            status = "nofinish"
            repaid_amount = trans_info[i]["asset_transaction_repaid_amount"]
            finish_date = current_date
        # 指定的还款期次，无论是否完成，回款完成时间取传入的回款时间
        if trans_info[i]["asset_transaction_period"] == repay_period:
            finish_at = repay_date
            status = "finish"
            repaid_amount = trans_info[i]["asset_transaction_amount"]
            finish_date = datetime.datetime.strptime(finish_at, "%Y-%m-%d %H:%M:%S")
        # 计算逾期天数
        date_diff = (finish_date - due_at_date).days
        # 逾期天数大于0 或 费用类型late开头--------逾期
        if date_diff > 0 or trans_info[i]["asset_transaction_type"].startswith("late") \
                or trans_info[i]["asset_transaction_type"].startswith("repaylate"):
            late_status = "late"
        else:
            late_status = "normal"

        trade_at = finish_at
        if trans_info[i]["asset_transaction_type"] in ("repayprincipal", "repayinterest"):
            tran_type = trans_info[i]["asset_transaction_type"]
        if trans_info[i]["asset_transaction_type"] not in ("repayprincipal", "repayinterest"):
            if country == "CN":
                tran_type = trans_info[i]["asset_transaction_type"].replace("repay", "")
            if country in ("TH", "PH", "MX", "IN", "PK"):
                tran_type = trans_info[i]["asset_transaction_type"]
        pre_body = {
                "type": tran_type,
                "description": "",
                "amount": trans_info[i]["asset_transaction_amount"],
                "status": status,
                "period": trans_info[i]["asset_transaction_period"],
                "remark": "",
                "category": "",
                "asset_item_no": asset_item_number,
                "decrease_amount": trans_info[i]["asset_transaction_decrease_amount"],
                "repaid_amount": repaid_amount,
                "total_amount": trans_info[i]["asset_transaction_amount"],
                "balance_amount": 0,
                "due_at": trans_info[i]["asset_transaction_expect_finish_time"],
                "finish_at": finish_at,
                "late_status": late_status,
                "repay_priority": 10,
                "trade_at": trade_at,
                "create_at": current_time,
                "update_at": current_time
            }
        principal_body = interest_body = fee_body = late_body = {}
        if trans_info[i]["asset_transaction_type"] == "repayprincipal":
            description = "偿还本金"
            category = "principal"
            pre_body["description"] = description
            pre_body["category"] = category
            principal_body = pre_body
        if trans_info[i]["asset_transaction_type"] == "repayinterest":
            description = "偿还利息"
            category = "interest"
            pre_body["description"] = description
            pre_body["category"] = category
            interest_body = pre_body
        if trans_info[i]["asset_transaction_type"] not in ("repayprincipal", "repayinterest", "lateinterest", "repaylateinterest"):
            description = "服务费"
            category = "fee"
            pre_body["description"] = description
            pre_body["category"] = category
            fee_body = pre_body
        if trans_info[i]["asset_transaction_type"] in ("lateinterest", "repaylateinterest"):
            description = "逾期利息"
            category = "late"
            pre_body["description"] = description
            pre_body["category"] = category
            late_body = pre_body

        if transaction_type == "trans":
            if principal_body:
                final_body.append(principal_body)
            if interest_body:
                final_body.append(interest_body)
            if fee_body:
                final_body.append(fee_body)
            if late_body:
                final_body.append(late_body)
        if transaction_type == "dtransactions":
            if principal_body:
                final_body.append(principal_body)
            if interest_body:
                final_body.append(interest_body)
        if transaction_type == "fees":
            if fee_body:
                final_body.append(fee_body)
            if late_body:
                final_body.append(late_body)
    return json.dumps(final_body, ensure_ascii=False)


# 拼接回款的tran_logs
# 国内tran_logs：只有类型repayprincipal、repayinterest是repay开头；asset_transaction表，类型全部是repay开头
# 海外tran_logs、asset_transaction表：只有类型repayprincipal、repayinterest是repay开头
def get_repay_notify_tran_logs(asset_item_number, repay_period, repay_date, country):
    trans_info = get_transaction(asset_item_number)

    random_int = random.randint(1000, 99999999)
    tran_logs = []
    for i in range(len(trans_info)):
        # 指定的还款期次作为tran_logs节点
        if trans_info[i]["asset_transaction_period"] == repay_period:
            if country in ("TH", "PH", "MX", "IN", "PK"):
                tran_type = trans_info[i]["asset_transaction_type"]
            if country == "CN":
                if trans_info[i]["asset_transaction_type"] in ("repayprincipal", "repayinterest"):
                    tran_type = trans_info[i]["asset_transaction_type"]
                else:
                    tran_type = trans_info[i]["asset_transaction_type"].replace("repay", "")

            pre_body = {
                "id": random_int + i,
                "asset_item_no": asset_item_number,
                "asset_tran_no": 318842140 + i,
                "operate_type": "withhold_repay",
                "amount": -trans_info[i]["asset_transaction_amount"],
                "operate_flag": "normal",
                "comment": "代扣还款",
                "from_system": "rbiz",
                "ref_no": 163287000 + i,
                "operator_id": 0,
                "operator_name": "",
                "create_at": current_time,
                "update_at": current_time,
                "tran_type": tran_type,
                "period": trans_info[i]["asset_transaction_period"],
                "withhold_finish_at": repay_date
            }
            tran_logs.append(pre_body)
    return tran_logs
