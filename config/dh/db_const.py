import pytest

from util.db.db_util import DataBase
from util.log.log_util import LogUtil

DB = {
    "CN": {
        'fox': 'qsq_fox{0}'
    },
    "TH": {
        'fox': 'arcticfox-thailand'
    },
    "PH": {
        'fox': 'arcticfox-philippines'
    },
    "MX": {
        'fox': 'arcticfox-mexico'
    },
    "IN": {
        'fox': 'arcticfox-india'
    },
    "PK": {
        'fox': 'arcticfox-pakistan'
    }
}

DEFAULT_OPT = {
    "--env": 1,
    "--country": 'CN',
    "--environment": 'test'
}


def get_sysconfig(option):
    return pytest.config.getoption(option) if hasattr(pytest, 'config') else DEFAULT_OPT[option]


ENV = get_sysconfig('--env')
COUNTRY = get_sysconfig('--country')
ENVIRONMENT = get_sysconfig('--environment')


DH_DB = DataBase(DB[COUNTRY]['fox'].format(ENV), ENVIRONMENT) if COUNTRY == 'CN' \
    else DataBase(DB[COUNTRY]['fox'], ENVIRONMENT)


def init_dh_env(env, country, environment):
    global DH_DB
    # CN中国、TH泰国、PH菲律宾、MX墨西哥、PK巴基斯坦、IN印度
    LogUtil.log_info("传入国家：%s，environment=%s" % (country, environment))
    DH_DB = DataBase(DB[country]['fox'].format(env), environment) if country == 'CN' \
        else DataBase(DB[country]['fox'], environment)


def init_env(env, country, environment):
    # 工具环境初始化
    init_dh_env(env, country, environment)


# pytest环境初始化
init_env(env=get_sysconfig('--env'), country=get_sysconfig('--country'), environment=get_sysconfig('--environment'))
