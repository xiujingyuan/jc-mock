import time
import random
from flask import current_app
import config.dh.db_const as dc
from util.log.log_util import LogUtil

create_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def create_c_card(asset_item_number, item_cust_flg, d3_level):
    if d3_level not in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10) or d3_level == "":
        return
    if d3_level != "":
        if item_cust_flg == "新用户":
            customer_type = "new"
        if item_cust_flg == "老用户":
            customer_type = "old"
        if item_cust_flg == "":
            customer_type = random.choice(["new", "old"])
        d3_score = random.randint(500, 600)
        m1_score = random.randint(300, 400)
        m1_level = random.randint(1, 10)
        m1plus_score = "0.345125"
        m1plus_level = random.randint(1, 10)
        self_healing = 0
        sql = "INSERT INTO `c_card` (`asset_item_number`, `customer_type`, `d3_score`, `d3_level`, " \
              "`d7_score`, `d7_level`, `m1_score`, `m1_level`, " \
              "`special_risk`, `create_at`, `m1plus_score`, `m1plus_level`, `self_healing`) " \
              "VALUES ('%s', '%s', '%s', '%s', NULL, NULL, '%s', '%s', NULL, '%s', '%s', '%s', '%s')" \
              % (asset_item_number, customer_type, d3_score, d3_level,
                 m1_score, m1_level, create_at, m1plus_score, m1plus_level, self_healing)
        dc.DH_DB.insert(sql)
        LogUtil.log_info("资产编号：%s,C卡等级:%s 创建成功" % (asset_item_number, d3_level))


def create_asset_quality(asset_item_number, item_cust_flg):
    if item_cust_flg != "新用户" and item_cust_flg != "老用户":
        return
    if item_cust_flg == "新用户":
        apply_user_type = "1"
    if item_cust_flg == "老用户":
        apply_user_type = "2"
    item_sn = random.randint(1, 9999)
    statistical_date = time.strftime("%Y-%m-%d 00:00:00", time.localtime())
    product_cnt = 3
    product_time_type = "3期*月"
    sql = "INSERT INTO `asset_quality` (`item_sn`, `statistical_date`, `asset_item_number`, `product_cnt`, `product_time_type`, " \
          "`item_cust_flg`, `create_at`, `update_at`, `apply_user_type`) " \
          "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', NULL, '%s')" \
          % (item_sn, statistical_date, asset_item_number, product_cnt, product_time_type,
             item_cust_flg, create_at, apply_user_type)
    dc.DH_DB.insert(sql)
    LogUtil.log_info("资产编号：%s,用户类型：%s 创建成功" % (asset_item_number, item_cust_flg))


def creat_asset_language(asset_item_number, final_language):
    query_sql = "select first_language from asset_language where asset_item_number = '%s'" \
                % asset_item_number
    system_language_info = dc.DH_DB.query(query_sql)
    # 印度的语言由用户中心mock产生，如果mock的语言与同步mock传入的语言不一致，最终更新为传入的语言
    # 非印度国家，语言由同步mock传入
    if not system_language_info:
        LogUtil.log_info("asset_language表不存在资产：%s 的语言，开始创建" % asset_item_number)
        sql = "INSERT INTO `asset_language` (`asset_item_number`, `pincode`, `state_name`, `state`, " \
              "`first_language`, `second_language`, `third_language`, " \
              "`create_at`, `update_at`) " \
              "VALUES ('%s', NULL, NULL, NULL, '%s', '0', '0', '%s', '%s')" \
              % (asset_item_number, final_language, create_at, create_at)
        dc.DH_DB.insert(sql)
        LogUtil.log_info("资产编号：%s,资产语言：%s 创建成功" % (asset_item_number, final_language))
    if system_language_info:
        system_language = system_language_info[0]["first_language"]
        if system_language != final_language:
            update_sql = "update asset_language set first_language = '%s' where asset_item_number = '%s'" \
                         % (final_language, asset_item_number)
            dc.DH_DB.update(update_sql)
            LogUtil.log_info("资产编号：%s,传入的资产语言：%s，库中已存在的语言：%s, 更新成功"
                             % (asset_item_number, final_language, system_language))


def create_a_card(asset_item_number, a_card_level):
    if a_card_level not in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10) or a_card_level == 0:
        return
    else:
        yf_score = random.randint(1, 10)
        sql = "INSERT INTO `a_card` (`asset_item_number`, `yf_score`, `level`, `user_type`, `create_at`, `update_at`) " \
              "VALUES ('%s', '%s', '%s', NULL, '%s', '%s')" \
              % (asset_item_number, yf_score, a_card_level, create_at, create_at)
        dc.DH_DB.insert(sql)
        LogUtil.log_info("资产编号：%s,A卡等级:%s 创建成功" % (asset_item_number, a_card_level))
