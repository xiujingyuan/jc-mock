TASK_RESULT = {
    "code": 0,
    "msg": "success",
    "data": {
        "status": "",
        "state": "",
        "message": ""
    }
}

UPDATE_TASK = {
    "message": "",
    "build_number": 0,
    "result": "ABORTED",
    "url": "",
    "env": 1,
    "build_type": 1
}


# 最后构建状态 0:空闲，1:成功，2:失败 3:构建中 4:已取消 5:等待中 6:排队中'
TASK_BUILD_RESULT_FREE = 0
TASK_BUILD_RESULT_SUCCESS = 1
TASK_BUILD_RESULT_FAILED = 2
TASK_BUILD_RESULT_BUILDING = 3
TASK_BUILD_RESULT_CANCEL = 4
TASK_BUILD_RESULT_PENDING = 5
TASK_BUILD_RESULT_QUEUE = 6
