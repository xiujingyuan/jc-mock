import json
import traceback
from datetime import datetime

import requests
from celery_once import QueueOnce
from flask_mail import Message
from requests.auth import HTTPBasicAuth

from app import celery, db, mail
from flask import current_app
import jenkins

from app.models.AssumptBuildTaskDb import AssumptBuildTask
from app.models.AssumptBuildTaskRunDb import AssumptBuildTaskRun
from app.models.CiAutotestDB import CiAutotestInfo
from app.models.CiEmailDB import CiEmail
from app.models.CiJobDB import CiJobInfo
from app.models.CiLogDB import CiLogInfo
from app.models.CiPipilineDB import CiPipeline
from app.models.CiSONADB import CiSonaInfo
from app.models.JenkinsJobDb import JenkinsJob
from app.tasks.run_pipeline.build_email import build_email
from app.tasks.run_pipeline.pipeline_config import *


@celery.task(base=QueueOnce, once={"graceful": True}, bind=True, ignore_result=True)
def run_pipeline(self):
    try:
        running_pipeline = CiPipeline.query.filter(
            CiPipeline.ci_pipeline_status.in_([STATUS_READY, STATUS_PROCESS])).all()
        current_app.logger.info("当前进行中的流水线，共%s条" % len(running_pipeline))
        for pipeline in running_pipeline:
            try:
                pipeline = db.session.merge(pipeline)
                job_info = CiJobInfo.query.filter(CiJobInfo.ci_job_id == pipeline.ci_pipeline_job_id).first()

                jenkins_url = job_info.ci_job_address
                server = jenkins.Jenkins(jenkins_url, username=JENKINS_USER, password=JENKINS_PASSWD)

                current_app.logger.info("当前流水线：%s, 步骤：%s，状态：%s" %
                                        (pipeline.ci_pipeline_serial_num,
                                         pipeline.ci_pipeline_step,
                                         pipeline.ci_pipeline_status))
                if pipeline.ci_pipeline_status == STATUS_READY:
                    # 创建jenkins任务，落库信息
                    create_jenkins_job(pipeline)
                    # update_assumpt_build_task(pipeline)
                elif pipeline.ci_pipeline_status in (STATUS_SUCCESS, STATUS_FAILRE):
                    # 已经成功or失败的，不处理
                    pass
                elif pipeline.ci_pipeline_status == STATUS_PROCESS:
                    # 获取jenkins 任务信息
                    build_num = pipeline.ci_pipeline_build_num
                    job_build_info = server.get_build_info(job_info.ci_job_name, int(build_num))
                    job_build_status = job_build_info["result"]
                    current_app.logger.info("当前流水线：%s, 步骤：%s, job状态：%s" %
                                            (pipeline.ci_pipeline_serial_num,
                                             pipeline.ci_pipeline_step,
                                             job_build_status))
                    # 更新日志，落库状态
                    if job_build_status == STATUS_SUCCESS:
                        update_job_log(pipeline, server, job_info)
                        update_env_ip(pipeline, server, job_info)
                        update_pipeline(pipeline, job_build_info)
                        # update_assumpt_build_task(pipeline)
                        # 任务顺序，依次是unit sona build test
                        if pipeline.ci_pipeline_step == STEP_SONA:
                            update_sona_info(pipeline)
                        elif pipeline.ci_pipeline_step == STEP_BUILD and \
                                pipeline.ci_pipeline_trigger_type == TRIGGER_TYPE_PUSH:
                            # 创建冒烟测试
                            new_pipeline = create_pipeline(pipeline, STEP_SMOKE_TEST)
                            create_jenkins_job(new_pipeline)
                        elif pipeline.ci_pipeline_step == STEP_BUILD and \
                                pipeline.ci_pipeline_trigger_type != TRIGGER_TYPE_PUSH:
                            # 创建全量测试
                            new_pipeline = create_pipeline(pipeline, STEP_AUTO_TEST)
                            create_jenkins_job(new_pipeline)
                        elif pipeline.ci_pipeline_step in (STEP_SMOKE_TEST, STEP_AUTO_TEST):
                            # 发送邮件
                            update_test_info(pipeline)
                            send_mail(pipeline)
                            pass
                        else:
                            current_app.logger.info("当前流水线：%s, 步骤：%s, 步骤不正确，无法处理" %
                                                    (pipeline.ci_pipeline_serial_num,
                                                     pipeline.ci_pipeline_step))
                    elif job_build_status in (STATUS_FAILRE, STATUS_ABORDED):
                        # 更新信息并发送邮件
                        if pipeline.ci_pipeline_step in (STEP_SMOKE_TEST, STEP_AUTO_TEST):
                            update_test_info(pipeline)
                        update_job_log(pipeline, server, job_info)
                        update_pipeline(pipeline, job_build_info)
                        # update_assumpt_build_task(pipeline)
                        send_mail(pipeline)
                        pass
                    elif job_build_status == STATUS_PROCESS:
                        # 处理中，不处理
                        pass
                    else:
                        current_app.logger.info("当前流水线：%s, 步骤：%s, job状态：%s，无法处理" %
                                                (pipeline.ci_pipeline_serial_num,
                                                 pipeline.ci_pipeline_step,
                                                 job_build_status))
                else:
                    current_app.logger.info("当前流水线：%s, 步骤：%s, 流水线状态：%s，无法处理" %
                                            (pipeline.ci_pipeline_serial_num,
                                             pipeline.ci_pipeline_step,
                                             pipeline.ci_pipeline_status))
            except Exception as e:
                current_app.logger.info(str(e))
                current_app.logger.info(traceback.format_exc())
            finally:
                current_app.logger.info("-----------------------一条流水线处理完成----------------------------")
        current_app.logger.info("所有流水线处理完成")
    except Exception as e:

        current_app.logger.info(str(e))
        current_app.logger.info(traceback.format_exc())


def create_jenkins_job(pipeline):
    current_app.logger.info("当前流水线：%s，创建jenkins任务，步骤：%s" % (pipeline.ci_pipeline_serial_num, pipeline.ci_pipeline_step))
    result = check_create_job(pipeline)
    if not result:
        return
    job_info = CiJobInfo.query.filter(CiJobInfo.ci_job_id == pipeline.ci_pipeline_job_id).first()

    jenkins_url = job_info.ci_job_address
    server = jenkins.Jenkins(jenkins_url, username=JENKINS_USER, password=JENKINS_PASSWD)

    build_number = server.get_job_info(job_info.ci_job_name)['nextBuildNumber']
    build_parameters = {"Branch": pipeline.ci_pipeline_branch,
                        "branch": pipeline.ci_pipeline_branch,
                        "num": pipeline.ci_pipeline_env,
                        "env": pipeline.ci_pipeline_env,
                        "test_version": pipeline.ci_pipeline_env}
    server.build_job(job_info.ci_job_name, parameters=build_parameters)

    current_app.logger.info("当前流水线：%s，创建jenkins任务后，创建对应的log" % pipeline.ci_pipeline_serial_num)
    next_job_log = CiLogInfo()
    next_job_log.ci_log_pipeline_serial_num = pipeline.ci_pipeline_serial_num
    next_job_log.ci_log_build_number = build_number
    next_job_log.ci_log_console_address = job_info.ci_job_address + "/job/" + job_info.ci_job_name + "/" + str(
        build_number) + "/console"
    db.session.add(next_job_log)
    db.session.flush()
    log_id = next_job_log.ci_log_id

    current_app.logger.info("当前流水线：%s，创建jenkins任务后，更新流水线状态，步骤：%s，状态：%s" %
                            (pipeline.ci_pipeline_serial_num, pipeline.ci_pipeline_step, STATUS_PROCESS))
    pipeline.ci_pipeline_status = STATUS_PROCESS
    pipeline.ci_pipeline_job_log_id = log_id
    pipeline.ci_pipeline_build_num = build_number
    db.session.add(pipeline)
    db.session.flush()


def create_pipeline(pipeline, step):
    current_app.logger.info("当前流水线：%s，当前步骤：%s，创建下一步骤：%s" %
                            (pipeline.ci_pipeline_serial_num, pipeline.ci_pipeline_step, step))
    old_job = CiJobInfo.query.filter(CiJobInfo.ci_job_id == pipeline.ci_pipeline_job_id).first()
    new_job = CiJobInfo.query.filter(CiJobInfo.ci_job_system == old_job.ci_job_system,
                                     CiJobInfo.ci_job_type == step).first()
    # 创建流水线
    new_pipeline = CiPipeline()
    new_pipeline.ci_pipeline_serial_num = pipeline.ci_pipeline_serial_num
    new_pipeline.ci_pipeline_trigger_type = pipeline.ci_pipeline_trigger_type
    new_pipeline.ci_pipeline_trigger_user = pipeline.ci_pipeline_trigger_user
    new_pipeline.ci_pipeline_trigger_info = pipeline.ci_pipeline_trigger_info
    new_pipeline.ci_pipeline_branch = pipeline.ci_pipeline_branch
    new_pipeline.ci_pipeline_source_branch = pipeline.ci_pipeline_source_branch
    new_pipeline.ci_pipeline_step = step
    new_pipeline.ci_pipeline_address = ""
    new_pipeline.ci_pipeline_job_id = new_job.ci_job_id
    new_pipeline.ci_pipeline_job_log_id = 0
    new_pipeline.ci_pipeline_autotest_id = 0
    new_pipeline.ci_pipeline_sona_id = 0
    new_pipeline.ci_pipeline_build_num = 0
    new_pipeline.ci_pipeline_env = pipeline.ci_pipeline_env
    new_pipeline.ci_pipeline_status = STATUS_READY
    new_pipeline.ci_pipeline_handler_user = ""
    new_pipeline.ci_pipeline_handler_info = ""
    new_pipeline.ci_pipeline_handler_times = ""
    new_pipeline.ci_pipeline_create_time = datetime.now()
    db.session.add(new_pipeline)

    return new_pipeline


def update_job_log(pipeline, server, job_info):
    current_app.logger.info("当前流水线：%s，步骤：%s，更新日志" % (pipeline.ci_pipeline_serial_num, pipeline.ci_pipeline_step))
    log_info = CiLogInfo.query.filter(CiLogInfo.ci_log_id == pipeline.ci_pipeline_job_log_id).first()
    log_output = server.get_build_console_output(job_info.ci_job_name, pipeline.ci_pipeline_build_num)
    log_info.ci_log_console_info = log_output
    db.session.add(log_info)
    db.session.flush()


def update_env_ip(pipeline, server, job_info):
    if pipeline.ci_pipeline_step == STEP_BUILD:
        current_app.logger.info("当前流水线：%s，步骤：%s，更新环境ip" % (pipeline.ci_pipeline_serial_num, pipeline.ci_pipeline_step))
        log_output = server.get_build_console_output(job_info.ci_job_name, pipeline.ci_pipeline_build_num)
        get_pod_str = "kubectl get pod -o wide"
        if get_pod_str in log_output:
            get_pod_run_str = log_output.split(get_pod_str)[-1]
            get_pod_id_list = get_pod_run_str.split("Running")[1]
            get_pod_id_list = get_pod_id_list.strip().split(" ")
            get_pod_id_list = list(filter(lambda x: x, get_pod_id_list))
            get_pod_ip = get_pod_id_list[2]
            current_app.logger.info("当前流水线：%s，步骤：%s，环境：%s，ip：%s" %
                                    (pipeline.ci_pipeline_serial_num, pipeline.ci_pipeline_step,
                                     pipeline.ci_pipeline_env, get_pod_ip))
            get_pod_env = pipeline.ci_pipeline_env
            find_job = JenkinsJob.query.filter(JenkinsJob.jenkins_job_name == job_info.ci_job_name).first()
            if find_job is not None and find_job.change_ip:
                new_jenkins_job = json.loads(find_job.git_module)
                for env, module in new_jenkins_job.items():
                    if env == get_pod_env:
                        for module_info in module:
                            module_info["address"] = get_pod_ip
                find_job.git_module = json.dumps(new_jenkins_job)
                db.session.add(find_job)
                db.session.flush()


def update_pipeline(pipeline, job_build_info):
    status = job_build_info["result"]
    duration = job_build_info["duration"]

    current_app.logger.info("当前流水线：%s，步骤：%s，更新状态：%s，执行时间：%s" %
                            (pipeline.ci_pipeline_serial_num,
                             pipeline.ci_pipeline_step, status, duration))
    if int(duration) == 0:
        raise Exception("执行时间未知，待下次轮训")
    m, s = divmod(int(duration / 1000), 60)
    pipeline.ci_pipeline_run_time = "%s分%s秒" % (m, s)
    pipeline.ci_pipeline_status = status
    db.session.add(pipeline)
    db.session.flush()


def update_assumpt_build_task(pipeline):
    try:
        if pipeline.ci_pipeline_step == STEP_BUILD and \
                pipeline.ci_pipeline_status != STATUS_READY and \
                int(pipeline.ci_pipeline_build_num) != 0:
            current_app.logger.info("更新assumpt_build_task开始，当前流水线：%s" % pipeline.ci_pipeline_serial_num)
            job_info = CiJobInfo.query.filter(CiJobInfo.ci_job_id == pipeline.ci_pipeline_job_id).first()
            log_info = CiLogInfo.query.filter(CiLogInfo.ci_log_id == pipeline.ci_pipeline_job_log_id).first()
            build_task = AssumptBuildTask.query.filter(
                AssumptBuildTask.build_branch == pipeline.ci_pipeline_branch,
                AssumptBuildTask.gitlab_program_id == job_info.ci_job_git_project_id).first()
            if build_task is None:
                current_app.logger.info("更新assumpt_build_task结束，当前流水线：%s，assumpt_build_task不存在分支：%s，项目：%s" %
                                        (pipeline.ci_pipeline_serial_num,
                                         pipeline.ci_pipeline_branch,
                                         job_info.ci_job_git_project_id))
                return
            build_task_run = AssumptBuildTaskRun.query.filter(
                AssumptBuildTaskRun.build_branch == pipeline.ci_pipeline_branch,
                AssumptBuildTaskRun.build_program_id == build_task.program_id,
                AssumptBuildTaskRun.build_task_id == build_task.id,
                AssumptBuildTaskRun.build_jenkins_task_id == pipeline.ci_pipeline_build_num).first()
            if build_task_run is None:
                build_task_run = AssumptBuildTaskRun()
                build_task_run.build_task_run_id = None
                build_task_run.build_user = 'test_platform'
                build_task_run.build_time = pipeline.ci_pipeline_create_time
                build_task_run.build_branch = pipeline.ci_pipeline_branch
                build_task_run.build_result = 0
                build_task_run.build_message = log_info.ci_log_console_address
                build_task_run.build_task_id = build_task.id
                build_task_run.build_jenkins = job_info.ci_job_name
                build_task_run.build_jenkins_task_id = pipeline.ci_pipeline_build_num
                build_task_run.build_env = build_task.last_build_env
                build_task_run.build_program_id = build_task.program_id
                build_task_run.iteration_id = build_task.iteration_id
                build_task_run.build_commit_type = build_task.build_commit_type
                db.session.add(build_task_run)
                db.session.flush()

                build_task.build_count = int(build_task.build_count) + 1
                build_task.last_build_user = 'testplatform'
                build_task.last_build_time = pipeline.ci_pipeline_create_time
                build_task.last_build_status = 3
                build_task.last_run_id = None
                db.session.add(build_task)
                db.session.flush()
                current_app.logger.info("插入assumpt_build_task成功，当前流水线：%s，assumpt_build_task_id：%s，项目：%s" %
                                        (pipeline.ci_pipeline_serial_num,
                                         build_task.id,
                                         job_info.ci_job_git_project_id))
            else:
                build_task_run.build_task_run_id = None
                build_task_run.build_result = 2 if pipeline.ci_pipeline_status == STATUS_SUCCESS else 3
                build_task_run.build_message = log_info.ci_log_console_address
                build_task_run.build_task_id = build_task.id
                build_task_run.build_jenkins = job_info.ci_job_name
                build_task_run.build_jenkins_task_id = pipeline.ci_pipeline_build_num
                build_task_run.build_env = build_task.last_build_env
                build_task_run.build_program_id = build_task.program_id
                build_task_run.iteration_id = build_task.iteration_id
                build_task_run.build_commit_type = build_task.build_commit_type
                db.session.add(build_task_run)
                db.session.flush()

                build_task.last_build_user = 'testplatform'
                build_task.last_build_status = 1 if pipeline.ci_pipeline_status == STATUS_SUCCESS else 2
                db.session.add(build_task)
                db.session.flush()
                current_app.logger.info("更新assumpt_build_task成功，当前流水线：%s，assumpt_build_task_id：%s，项目：%s" %
                                        (pipeline.ci_pipeline_serial_num,
                                         build_task.id,
                                         job_info.ci_job_git_project_id))
    except Exception as e:
        current_app.logger.info(str(e))
        current_app.logger.info(traceback.format_exc())
        current_app.logger.info("插入assumpt_build_task报错，当前流水线：%s" % pipeline.ci_pipeline_serial_num +
                                traceback.format_exc())


def update_sona_info(pipeline):
    current_app.logger.info("当前流水线：%s，步骤：%s，更新sona信息" % (pipeline.ci_pipeline_serial_num, pipeline.ci_pipeline_step))
    pipeline_sonar = CiPipeline.query.filter(CiPipeline.ci_pipeline_serial_num == pipeline.ci_pipeline_serial_num,
                                             CiPipeline.ci_pipeline_step == STEP_SONA).first()
    if pipeline_sonar is None:
        return False

    sona_info = CiSonaInfo.query.filter(CiSonaInfo.ci_sona_id == pipeline_sonar.ci_pipeline_sona_id).first()
    if sona_info is None:
        sona_info = CiSonaInfo()

        job_info = CiJobInfo.query.filter(CiJobInfo.ci_job_id == pipeline_sonar.ci_pipeline_job_id).first()
        jenkins_url = job_info.ci_job_address
        server = jenkins.Jenkins(jenkins_url, username=JENKINS_USER, password=JENKINS_PASSWD)
        log_output = server.get_build_console_output(job_info.ci_job_name, pipeline_sonar.ci_pipeline_build_num)
        log_output_list = log_output.split("\n")
        ce_task_id = None
        for item in log_output_list[-15:-1]:
            if "More about the report processing" in item:
                ce_task_id = item.split("id=")[1]
                break
        sona_info.ci_sona_ce_task_id = ce_task_id
        sona_info.ci_sona_pipeline_serial_num = pipeline_sonar.ci_pipeline_serial_num

    return_result = False
    if sona_info is not None and sona_info.ci_sona_ce_task_id is not None:
        sonar_base_url = "https://sonar.kuainiujinke.com"
        auth = "b551aa46a348f2f57ef3f7a91916bdbe942b8ca5", ""
        sona_result_url = sonar_base_url + "/api/ce/task?id=" + sona_info.ci_sona_ce_task_id
        sona_result = requests.get(sona_result_url, auth=auth).json()
        if sona_info.ci_sona_ce_task_id is not None and sona_result["task"]["status"] == "SUCCESS":
            sona_result_url = sonar_base_url + "/api/measures/component?" \
                                               "additionalFields=metrics,periods&component=%s&metricKeys=bugs," \
                                               "new_bugs,code_smells,new_code_smells,coverage,new_coverage," \
                                               "vulnerabilities,new_vulnerabilities,duplicated_lines_density," \
                                               "new_duplicated_lines_density,duplicated_blocks" % \
                              sona_result["task"]["componentKey"]
            sona_result = requests.get(sona_result_url, auth=auth).json()
            for mersure in sona_result["component"]["measures"]:
                if mersure["metric"] == "bugs":
                    sona_info.ci_sona_bugs = mersure["value"]
                elif mersure["metric"] == "vulnerabilities":
                    sona_info.ci_sona_vulnerabilities = mersure["value"]
                elif mersure["metric"] == "":
                    sona_info.ci_sona_debt = mersure["value"]
                elif mersure["metric"] == "code_smells":
                    sona_info.ci_sona_code_smells = mersure["value"]
                elif mersure["metric"] == "coverage":
                    sona_info.ci_sona_coverage = mersure["value"]
                elif mersure["metric"] == "duplicated_lines_density":
                    sona_info.ci_sona_duplicateds = mersure["value"]
                elif mersure["metric"] == "duplicated_blocks":
                    sona_info.ci_sona_duplicated_blocks = mersure["value"]
            return_result = True
        if sona_info.ci_sona_ce_task_id is None:
            return_result = True
        db.session.add(sona_info)
        db.session.flush()
        sona_id = sona_info.ci_sona_id

        pipeline_sonar.ci_pipeline_sona_id = sona_id
        db.session.add(pipeline_sonar)
        db.session.flush()
    return return_result


def update_test_info(pipeline):
    current_app.logger.info("当前流水线：%s，步骤：%s，更新自动化信息" % (pipeline.ci_pipeline_serial_num, pipeline.ci_pipeline_step))
    job_info = CiJobInfo.query.filter(CiJobInfo.ci_job_id == pipeline.ci_pipeline_job_id).first()
    test_url = job_info.ci_job_address + "/view/Auto_test/job/" + job_info.ci_job_name + "/" + str(
        pipeline.ci_pipeline_build_num) + "/allure"
    test_result_url = test_url + "/widgets/summary.json"
    try:
        rest_result = requests.get(test_result_url, auth=HTTPBasicAuth(JENKINS_USER, JENKINS_PASSWD)).json()
    except Exception as e:
        rest_result = None
        current_app.logger.info(e)
    test_info = CiAutotestInfo()
    test_info.ci_autotest_pipeline_serial_num = pipeline.ci_pipeline_serial_num
    test_info.ci_autotest_report_address = test_url
    if rest_result is not None:
        if int(rest_result["statistic"]["total"]) != 0:
            m, s = divmod(int(int(rest_result["time"]["sumDuration"]) / 1000), 60)
        else:
            m, s = 0, 0
        test_info.ci_autotest_total_num = rest_result["statistic"]["total"]
        test_info.ci_autotest_success_num = rest_result["statistic"]["passed"]
        test_info.ci_autotest_fail_num = rest_result["statistic"]["failed"] + \
            rest_result["statistic"]["broken"] + rest_result["statistic"]["unknown"]
        test_info.ci_autotest_success_rate = 0 if int(rest_result["statistic"]["total"]) == 0 else \
            round((rest_result["statistic"]["passed"] / rest_result["statistic"]["total"]) * 100, 2)
        test_info.ci_autotest_running_time = "%s分%s秒" % (m, s)
    else:
        test_info.ci_autotest_total_num = 0
        test_info.ci_autotest_success_num = 0
        test_info.ci_autotest_fail_num = 0
        test_info.ci_autotest_success_rate = 0
        test_info.ci_autotest_running_time = "0分0秒"
    db.session.add(test_info)
    db.session.flush()
    test_id = test_info.ci_autotest_id

    pipeline.ci_pipeline_autotest_id = test_id
    db.session.add(pipeline)
    db.session.flush()


def send_mail(pipeline):
    current_app.logger.info("当前流水线：%s，处理完成，发送邮件" % pipeline.ci_pipeline_serial_num)
    email = CiEmail.query.filter(CiEmail.ci_email_serial_num == pipeline.ci_pipeline_serial_num).first()
    if email is None:
        email = CiEmail()
    email.ci_email_serial_num = pipeline.ci_pipeline_serial_num
    email.ci_email_status = STATUS_READY
    db.session.add(email)
    db.session.flush()


def check_create_job(pipeline):
    current_app.logger.info("当前流水线：%s，步骤：%s，检查是否可以创建jenkins任务" %
                            (pipeline.ci_pipeline_serial_num, pipeline.ci_pipeline_step))
    job_info = CiJobInfo.query.filter(CiJobInfo.ci_job_id == pipeline.ci_pipeline_job_id).first()
    # 一个项目，只能有一条流水线运行
    running_pipeline = CiPipeline.query.join(CiJobInfo, CiJobInfo.ci_job_id == CiPipeline.ci_pipeline_job_id).filter(
        CiPipeline.ci_pipeline_status == STATUS_PROCESS,
        CiJobInfo.ci_job_git_project_id == job_info.ci_job_git_project_id,
        CiPipeline.ci_pipeline_serial_num != pipeline.ci_pipeline_serial_num).first()
    if running_pipeline is not None:
        current_app.logger.info("当前流水线：%s，步骤：%s，有正在运行的流水线：%s，环境：%s，任务阻塞" %
                                (pipeline.ci_pipeline_serial_num,
                                 pipeline.ci_pipeline_step,
                                 running_pipeline.ci_pipeline_serial_num,
                                 running_pipeline.ci_pipeline_env))
        return False
    return True


@celery.task(base=QueueOnce, once={"graceful": True}, bind=True, ignore_result=True)
def run_pipeline_send_email(self):
    try:
        emails = CiEmail.query.filter(CiEmail.ci_email_status == STATUS_READY).all()
        current_app.logger.info("开始发送邮件，需要发送邮件流水线共计%s" % len(emails))
        for email in emails:
            try:
                email = db.session.merge(email)
                pipeline = CiPipeline.query.filter(CiPipeline.ci_pipeline_serial_num == email.ci_email_serial_num,
                                                   CiPipeline.ci_pipeline_step == STEP_BUILD).first()
                # result = update_sona_info(pipeline)
                # if result:
                #     # 如果sona结果没更新，则先不发送邮件
                send_mail_sync(pipeline, email)
            except Exception as e:

                current_app.logger.info(str(e))
                current_app.logger.info(traceback.format_exc())
    except Exception as e:

        current_app.logger.info(str(e))
        current_app.logger.info(traceback.format_exc())


def send_mail_sync(pipeline, email):
    current_app.logger.info("开始发送邮件，流水线编号:%s" % pipeline.ci_pipeline_serial_num)
    subject, html, receiver = build_email(pipeline)
    msg = Message()
    msg.sender = "持续集成<{0}>".format(current_app.config["MAIL_USERNAME"])
    msg.recipients = receiver
    msg.subject = subject
    msg.html = html

    current_app.logger.info("开始发送邮件，邮件发送完成，流水线编号:%s" % pipeline.ci_pipeline_serial_num)
    email.ci_email_recipients = str(msg.recipients)
    email.ci_email_subject = str(msg.subject)
    email.ci_email_status = str(STATUS_SUCCESS)
    email.ci_email_html = str(msg.html)
    db.session.add(email)
    db.session.flush()

    app = current_app._get_current_object()
    with app.app_context():
        mail.send(msg)


@celery.task(base=QueueOnce, once={"graceful": True}, bind=True, ignore_result=True)
def run_pipeline_create_task(self, branch, git_id):
    url = "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/jc-mock/ci/hook_api"
    body = {"ref": branch,
            "user_name": "test_platform",
            "project": {"id": git_id}}
    header = {"X-Gitlab-Event": "Daily Hook", "Content-Type": "application/json"}
    requests.post(url=url, json=body, headers=header)
