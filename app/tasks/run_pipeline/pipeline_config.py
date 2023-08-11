JENKINS_USER = "testplatform"
JENKINS_PASSWD = "test1234"

STEP_SONA = "sona"
STEP_BUILD = "build"
STEP_UNIT_TEST = "unit_test"
STEP_AUTO_TEST = "auto_test"
STEP_SMOKE_TEST = "smoke_test"

STATUS_READY = "READY"
STATUS_PROCESS = "PROCESS"
STATUS_SUCCESS = "SUCCESS"
STATUS_ABORDED = "ABORTED"
STATUS_FAILRE = "FAILURE"

TRIGGER_TYPE_PUSH = "Push Hook"
TRIGGER_TYPE_SUBMIT = "Submit Hook"
TRIGGER_TYPE_TAG = "Tag Push Hook"
TRIGGER_TYPE_MERGE = "Merge Request Hook"
TRIGGER_TYPE_DAILY = "Daily Hook"

TRIGGER_MSG_MAP = {
    "Push Hook": "已提测分支代码提交",
    "Submit Hook": "分支提测",
    "Tag Push Hook": "新tag",
    "Merge Request Hook": "分支merge到master",
    "Daily Hook": "日构建"}

# import jenkins
# from pprint import pprint
# jenkins_url = "https://jenkins-test.kuainiujinke.com/jenkins"
# server = jenkins.Jenkins(jenkins_url, username=JENKINS_USER, password=JENKINS_PASSWD)
# job_build_info = server.get_build_info("Auto_Test_Global_Repay", 180)
# pprint(job_build_info)
# duration = job_build_info["duration"]
# m, s = divmod(int(duration / 1000), 60)
# print(m, s)