import traceback
from datetime import datetime

from app.api.ci import ci_url
from app.models.AssumptBuildTaskDb import AssumptBuildTask
from app.models.CiPipilineDB import CiPipeline
from app.models.CiJobDB import CiJobInfo
from flask import request, jsonify, current_app
from app import db, csrf
from pprint import pformat
import json

from app.tasks.run_pipeline.pipeline_config import *
from app.tools.tools import send_tv


@ci_url.route("/ci/hook_api", methods=["POST"])
@csrf.exempt
def load_info():
    try:
        req_data = request.json
        current_app.logger.info("收到请求：%s" % pformat(request.headers))
        current_app.logger.info("收到请求：%s" % pformat(req_data))
        # 收到请求后，解析相关数据
        git_id = req_data["project"]["id"]
        trigger_type = request.headers["X-Gitlab-Event"]
        trigger_user = ""
        branch = ""
        source_branch = ""

        # 提测请求
        if trigger_type == TRIGGER_TYPE_SUBMIT:
            branch = req_data['ref']
            trigger_user = req_data["user_name"]
        # 分支提测后，代码提交
        # elif trigger_type == TRIGGER_TYPE_PUSH:
        #     # push的请求，不对master进行处理
        #     branch = req_data['ref'].split("/")[2]
        #     trigger_user = req_data["user_name"]
        #     if branch == "master":
        #         raise Exception("push类型的master分支，不进行处理")
        # 分支测试完成后合入master，需要判断merge请求，是创建更新还是最终merged
        elif trigger_type == TRIGGER_TYPE_MERGE:
            if req_data["object_attributes"]["state"] == "merged":
                branch = req_data["object_attributes"]["target_branch"]
                source_branch = req_data["object_attributes"]["source_branch"]
                trigger_user = req_data["user"]["name"]
            else:
                raise Exception("merge提交操作，不进行处理")
        # 上线前新tag创建
        elif trigger_type == TRIGGER_TYPE_TAG:
            branch = req_data['ref'].split("/")[2]
            trigger_user = req_data["user_name"]
        # 日构建请求
        elif trigger_type == TRIGGER_TYPE_DAILY:
            branch = req_data['ref']
            trigger_user = req_data["user_name"]
        else:
            raise Exception("无需处理的请求")
        if branch == "not found":
            raise Exception("无需处理的分支")
        current_app.logger.info("流水线解析完成，分支：%s" % branch)

        job_info = CiJobInfo.query.filter(CiJobInfo.ci_job_git_project_id == git_id,
                                          CiJobInfo.ci_job_type == STEP_BUILD).first()
        default_env = job_info.ci_job_default_env
        # 如果是master，则选取固定环境
        if branch == "master":
            env = default_env
        # 如果不是master，切此分支已经提测，且部署过的环境存在，使用之前的环境，否则使用默认环境
        else:
            build_task = AssumptBuildTask.query.filter(AssumptBuildTask.build_branch == branch,
                                                       AssumptBuildTask.gitlab_program_id == git_id).first()
            if build_task is None:
                current_app.logger.info("未提测分支：%s" % branch)
                raise Exception("未提测分支")
            elif build_task.last_build_env is not None and \
                    build_task.run_pipeline is not None and \
                    int(build_task.run_pipeline) == 1:
                env = build_task.last_build_env
            else:
                env = default_env
        current_app.logger.info("流水线解析完成，环境：%s" % env)
        # 创建流水线，这里只是插入数据，流水线由异步task执行
        pipeline_serial_num = str(datetime.now().timestamp()).replace('.', '')
        # job_sonar_info = CiJobInfo.query.filter(CiJobInfo.ci_job_git_project_id == git_id,
        #                                         CiJobInfo.ci_job_type == STEP_SONA).first()
        # pipeline_sonar = CiPipeline()
        # pipeline_sonar.ci_pipeline_serial_num = pipeline_serial_num
        # pipeline_sonar.ci_pipeline_trigger_type = trigger_type
        # pipeline_sonar.ci_pipeline_trigger_user = trigger_user
        # pipeline_sonar.ci_pipeline_trigger_info = json.dumps(req_data, ensure_ascii=False)
        # pipeline_sonar.ci_pipeline_branch = branch
        # pipeline_sonar.ci_pipeline_source_branch = source_branch
        # pipeline_sonar.ci_pipeline_step = STEP_SONA
        # pipeline_sonar.ci_pipeline_address = ""
        # pipeline_sonar.ci_pipeline_job_id = job_sonar_info.ci_job_id
        # pipeline_sonar.ci_pipeline_job_log_id = 0
        # pipeline_sonar.ci_pipeline_autotest_id = 0
        # pipeline_sonar.ci_pipeline_sona_id = 0
        # pipeline_sonar.ci_pipeline_build_num = 0
        # pipeline_sonar.ci_pipeline_env = env
        # pipeline_sonar.ci_pipeline_status = STATUS_READY
        # pipeline_sonar.ci_pipeline_handler_user = ""
        # pipeline_sonar.ci_pipeline_handler_info = ""
        # pipeline_sonar.ci_pipeline_handler_times = ""
        # pipeline_sonar.ci_pipeline_create_time = datetime.now()
        # db.session.add(pipeline_sonar)
        # db.session.flush()

        job_build_info = CiJobInfo.query.filter(CiJobInfo.ci_job_git_project_id == git_id,
                                                CiJobInfo.ci_job_type == STEP_BUILD).first()
        pipeline_build = CiPipeline()
        pipeline_build.ci_pipeline_serial_num = pipeline_serial_num
        pipeline_build.ci_pipeline_trigger_type = trigger_type
        pipeline_build.ci_pipeline_trigger_user = trigger_user
        pipeline_build.ci_pipeline_trigger_info = json.dumps(req_data, ensure_ascii=False)
        pipeline_build.ci_pipeline_branch = branch
        pipeline_build.ci_pipeline_source_branch = source_branch
        pipeline_build.ci_pipeline_step = STEP_BUILD
        pipeline_build.ci_pipeline_address = ""
        pipeline_build.ci_pipeline_job_id = job_build_info.ci_job_id
        pipeline_build.ci_pipeline_job_log_id = 0
        pipeline_build.ci_pipeline_autotest_id = 0
        pipeline_build.ci_pipeline_sona_id = 0
        pipeline_build.ci_pipeline_build_num = 0
        pipeline_build.ci_pipeline_env = env
        pipeline_build.ci_pipeline_status = STATUS_READY
        pipeline_build.ci_pipeline_handler_user = ""
        pipeline_build.ci_pipeline_handler_info = ""
        pipeline_build.ci_pipeline_handler_times = ""
        pipeline_build.ci_pipeline_create_time = datetime.now()
        db.session.add(pipeline_build)
        db.session.flush()
        pass
    except Exception as e:
        current_app.logger.info(str(e))
        current_app.logger.info(traceback.format_exc())
        send_tv("流水线触发失败" + traceback.format_exc())
        return jsonify({"msg": str(traceback.format_exc())})
    else:
        return jsonify({"msg": str(traceback.format_exc())})
