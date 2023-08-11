import config.dh.db_const as dc


# 获取资产信息
def get_asset_info_by_item_no(asset_item_number):
    sql = "select * from asset where asset_item_number='%s' " % asset_item_number
    asset_info = dc.DH_DB.query(sql)
    return asset_info


# 获取逾期中、未被清除的资产信息
def get_exist_asset_info_by_item_no(asset_item_number):
    query_sql2 = "select * from asset where asset_item_number='%s' " \
                 "and asset_status='repay' " \
                 "and asset_due_at<> '1970-01-01 00:00:00'" % asset_item_number
    exist_asset_info = dc.DH_DB.query(query_sql2)
    return exist_asset_info


# 获取借款人信息
def get_individual(asset_item_number):
    query_sql = "select " \
                "`enc_individual_name`, `code_individual_name`, " \
                "`enc_individual_idnum`, `code_individual_idnum`, " \
                "`individual_gender`, `individual_nation`, " \
                "`individual_residence`, `individual_workplace`, " \
                "`individual_permanent`, `individual_company`, " \
                "`enc_individual_tel`, `code_individual_tel`, " \
                "`enc_individual_work_tel`, `code_individual_work_tel`, " \
                "`enc_individual_residence_tel`, `code_individual_residence_tel`, " \
                "`enc_individual_mate_name`, `code_individual_mate_name`, " \
                "`enc_individual_mate_tel`, `code_individual_mate_tel`, " \
                "`enc_individual_relative_name`, `code_individual_relative_name`, " \
                "`individual_relative_relation`, " \
                "`enc_individual_relative_tel`, `code_individual_relative_tel`, " \
                "`enc_individual_workmate_name`, `code_individual_workmate_name`, " \
                "`enc_individual_workmate_tel`, `code_individual_workmate_tel`, `individual_remark` " \
                "from debtor_asset da " \
                "left join individual i on da.enc_debtor_idnum = i.enc_individual_idnum " \
                "where da.asset_item_number = '%s'" % asset_item_number
    borrower_info = dc.DH_DB.query(query_sql)
    return borrower_info


# 获取还款计划
def get_transaction(asset_item_number):
    query_sql = "select atr.* from asset_transaction atr " \
                "left join asset a on atr.asset_transaction_asset_id = a.asset_id " \
                "where a.asset_item_number = '%s'" % asset_item_number
    atr_info = dc.DH_DB.query(query_sql)
    return atr_info


# 获取指定期次的还款计划
def get_period_transaction(asset_item_number, period, transaction_status):
    query_sql = "select atr.* from asset_transaction atr " \
                "left join asset a on atr.asset_transaction_asset_id = a.asset_id " \
                "where a.asset_item_number = '%s'" % asset_item_number
    if period != 0 and transaction_status is None:
        query_sql = query_sql + " and atr.asset_transaction_period ={0}".format(period)
    if period != 0 and transaction_status is not None:
        query_sql = query_sql + " and atr.asset_transaction_period ={0}".format(period) \
                    + " and atr.asset_transaction_status='{0}'".format(transaction_status)
    atr_info = dc.DH_DB.query(query_sql)
    return atr_info
