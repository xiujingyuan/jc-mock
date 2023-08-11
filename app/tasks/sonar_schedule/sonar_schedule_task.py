import os
import traceback
from datetime import date, datetime, timedelta
from celery_once import QueueOnce
from app import celery, db
from flask import current_app
import jenkins

from app.models.AssumptBuildTaskDb import AssumptBuildTask
from app.models.SonarScheduleDB import SonarSchedule
from app.models.SonarScheduleLogDB import SonarScheduleLog
from app.tasks.run_pipeline.pipeline_config import STATUS_PROCESS, STATUS_READY
from app.tools.tools import send_tv


@celery.task(base=QueueOnce, once={"graceful": True}, bind=True, ignore_result=True)
def sonar_schedule_create(self):
    try:
        sonar_schedule = SonarSchedule.query.filter(SonarSchedule.sonar_schedule_status == STATUS_PROCESS.lower()).first()
        if sonar_schedule is not None:
            return
        sonar_schedule = SonarSchedule.query.filter(SonarSchedule.sonar_schedule_last_date < date.today()).first()
        if sonar_schedule is not None:
            username = current_app.config["JENKINS_DICT"]["https://k8s-test-jenkins.kuainiujinke.com/"]["USER_ID"]
            password = current_app.config["JENKINS_DICT"]["https://k8s-test-jenkins.kuainiujinke.com/"]["USER_PWD"]
            server = jenkins.Jenkins("https://k8s-test-jenkins.kuainiujinke.com/", username=username, password=password)

            build_param = {"git_url": sonar_schedule.sonar_schedule_git_url,
                           "branch": sonar_schedule.sonar_schedule_branch,
                           "project_key": sonar_schedule.sonar_schedule_project_key,
                           "project_name": sonar_schedule.sonar_schedule_project_name,
                           "sonar_sources": sonar_schedule.sonar_schedule_project_key,
                           "sonar_exclusion": sonar_schedule.sonar_exclusion,
                           "sonar_language": sonar_schedule.sonar_language,
                           "maven_version": sonar_schedule.sonar_schedule_maven_version,
                           "maven_extend": sonar_schedule.sonar_schedule_maven_extend}
            queue_id = server.build_job("sonar_analysis", parameters=build_param)
            sonar_schedule_log = SonarScheduleLog()
            sonar_schedule_log.sonar_schedule_log_id = sonar_schedule.id
            sonar_schedule_log.sonar_schedule_log_project_key = sonar_schedule.sonar_schedule_project_key
            sonar_schedule_log.sonar_schedule_log_queue_id = queue_id
            sonar_schedule_log.sonar_schedule_log_status = STATUS_READY.lower()
            db.session.add(sonar_schedule_log)
            db.session.flush()

            sonar_schedule.sonar_schedule_status = STATUS_PROCESS.lower()
            sonar_schedule.sonar_schedule_last_date = date.today()
            db.session.add(sonar_schedule)
            db.session.flush()
    except Exception as e:
        send_tv(str(e))
        current_app.logger.info(traceback.format_exc())


@celery.task(base=QueueOnce, once={"graceful": True}, bind=True, ignore_result=True)
def sonar_schedule_query(self):
    try:
        sonar_schedule_log_list = \
            SonarScheduleLog.query.filter(SonarScheduleLog.sonar_schedule_log_status.in_([STATUS_READY.lower(),
                                                                                         STATUS_PROCESS.lower()])).all()
        username = current_app.config["JENKINS_DICT"]["https://k8s-test-jenkins.kuainiujinke.com/"]["USER_ID"]
        password = current_app.config["JENKINS_DICT"]["https://k8s-test-jenkins.kuainiujinke.com/"]["USER_PWD"]
        server = jenkins.Jenkins("https://k8s-test-jenkins.kuainiujinke.com/", username=username, password=password)

        for sonar_schedule_log in sonar_schedule_log_list:
            if sonar_schedule_log.sonar_schedule_log_status == STATUS_READY.lower():
                # 先查询排队信息
                queue_info = None
                try:
                    queue_info = server.get_queue_item(int(sonar_schedule_log.sonar_schedule_log_queue_id))
                except:
                    pass
                # 如果已经在构建中了，则更新build_num
                if queue_info and \
                        queue_info["blocked"] is False and \
                        "executable" in queue_info.keys() and \
                        queue_info["executable"] is not None and \
                        queue_info["task"]["name"] == "sonar_analysis":
                    sonar_schedule_log.sonar_schedule_log_build_num = queue_info["executable"]["number"]
                    sonar_schedule_log.sonar_schedule_log_status = STATUS_PROCESS.lower()
                    db.session.add(sonar_schedule_log)
                    db.session.flush()
                # 如果还是在排队中，则下次轮训再查
                elif queue_info and queue_info["blocked"] is True:
                    continue
                else:
                    pass
            if sonar_schedule_log.sonar_schedule_log_status == STATUS_PROCESS.lower():
                next_build_num = sonar_schedule_log.sonar_schedule_log_build_num
                # 获取构建信息，并更新状态，这里如果报错，则认为构建任务不存在
                try:
                    build_info = server.get_build_info("sonar_analysis", int(next_build_num))
                except:
                    continue
                sonar_schedule = SonarSchedule.query.filter(SonarSchedule.id == sonar_schedule_log.sonar_schedule_log_id).first()
                job_build_status = build_info["result"]
                if job_build_status is None:
                    job_build_status = STATUS_PROCESS.lower()
                sonar_schedule.sonar_schedule_status = job_build_status.lower()
                sonar_schedule.sonar_schedule_last_date = date.today()
                db.session.add(sonar_schedule)
                db.session.flush()
                sonar_schedule_log.sonar_schedule_log_status = job_build_status.lower()
                sonar_schedule_log.sonar_schedule_log_console = os.path.join(build_info["url"], "console")
                db.session.add(sonar_schedule_log)
                db.session.flush()
    except Exception as e:
        send_tv(str(e))
        current_app.logger.info(traceback.format_exc())


