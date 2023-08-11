import json

from sqlalchemy import and_
from app.models.CiJobDB import CiJobInfo
from app.models.CiLogDB import CiLogInfo
from app.models.CiAutotestDB import CiAutotestInfo
from app.models.CiPipilineDB import CiPipeline
from app.models.CiSONADB import CiSonaInfo
from app.tasks.run_pipeline.pipeline_config import *


def build_email(pipeline):
    pipelines = CiPipeline.query.filter(CiPipeline.ci_pipeline_serial_num == pipeline.ci_pipeline_serial_num).all()
    subject = build_subject(pipeline)
    table = build_trigger_info(pipeline)
    receiver = get_receiver(pipeline)
    for p in pipelines:
        if p.ci_pipeline_step == STEP_SONA:
            table = table + build_sona_info(pipeline)
        elif p.ci_pipeline_step == STEP_BUILD:
            table = table + build_compile_info(pipeline)
        elif p.ci_pipeline_step in (STEP_SMOKE_TEST, STEP_AUTO_TEST):
            table = table + build_test_info(pipeline, p.ci_pipeline_step)
    header = build_header(pipeline)
    html = header + '''
    <body leftmargin="8" marginwidth="0" topmargin="8" marginheight="4" offset="0">  
        <div>
        %s
        </div>
    </body>  
    </html>''' % table
    return subject, html, receiver


def get_receiver(pipeline):
    build_info = CiPipeline.query.filter(and_(CiPipeline.ci_pipeline_serial_num == pipeline.ci_pipeline_serial_num,
                                              CiPipeline.ci_pipeline_step == STEP_BUILD)).first()
    job_build_info = CiJobInfo.query.filter(CiJobInfo.ci_job_id == build_info.ci_pipeline_job_id).first()
    job_unit_info = CiJobInfo.query.filter(CiJobInfo.ci_job_git_project_id == job_build_info.ci_job_git_project_id,
                                           CiJobInfo.ci_job_type == STEP_UNIT_TEST).first()
    receiver = json.loads(job_unit_info.ci_job_mail_receiver)
    return receiver


def build_subject(pipeline):
    job_info = CiJobInfo.query.filter(CiJobInfo.ci_job_id == pipeline.ci_pipeline_job_id).first()
    if pipeline.ci_pipeline_trigger_type == TRIGGER_TYPE_DAILY:
        subject = "%s项目-日构建-持续集成报告" % job_info.ci_job_deciption
    elif pipeline.ci_pipeline_trigger_type == TRIGGER_TYPE_SUBMIT:
        subject = "%s项目-%s分支提测-持续集成报告" % (job_info.ci_job_deciption, pipeline.ci_pipeline_branch)
    elif pipeline.ci_pipeline_trigger_type == TRIGGER_TYPE_MERGE:
        subject = "%s项目-%s分支合入master-持续集成报告" % (job_info.ci_job_deciption, pipeline.ci_pipeline_source_branch)
    elif pipeline.ci_pipeline_trigger_type == TRIGGER_TYPE_PUSH:
        subject = "%s项目-%s分支代码提交-持续集成报告" % (job_info.ci_job_deciption, pipeline.ci_pipeline_branch)
    elif pipeline.ci_pipeline_trigger_type == TRIGGER_TYPE_TAG:
        subject = "%s项目-新tag:%s-持续集成报告" % (job_info.ci_job_deciption, pipeline.ci_pipeline_branch)
    else:
        subject = "%s项目-持续集成报告" % job_info.ci_job_deciption
    return subject


def build_header(pipeline):
    build_info = CiPipeline.query.filter(and_(CiPipeline.ci_pipeline_serial_num == pipeline.ci_pipeline_serial_num,
                                              CiPipeline.ci_pipeline_step == STEP_BUILD)).first()
    job_info = CiJobInfo.query.filter(CiJobInfo.ci_job_id == build_info.ci_pipeline_job_id).first()
    header = '''
        <!DOCTYPE html>  
        <html>  
        <head>  
        <meta charset="UTF-8">  
        <title>%s项目持续集成报告</title>  
        </head>
        ''' % job_info.ci_job_deciption
    return header


def build_trigger_info(pipeline):
    build_info = CiPipeline.query.filter(and_(CiPipeline.ci_pipeline_serial_num == pipeline.ci_pipeline_serial_num,
                                              CiPipeline.ci_pipeline_step == STEP_BUILD)).first()
    job_info = CiJobInfo.query.filter(CiJobInfo.ci_job_id == build_info.ci_pipeline_job_id).first()
    from_system = job_info.ci_job_deciption
    trigger_user = build_info.ci_pipeline_trigger_user
    trigger_type = TRIGGER_MSG_MAP[build_info.ci_pipeline_trigger_type]
    trigger_time = build_info.ci_pipeline_create_time.strftime("%Y-%m-%d %H:%M:%S")
    branch = build_info.ci_pipeline_branch
    serial_num = build_info.ci_pipeline_serial_num

    trigger_info = '''
    <p style="text-align:left;font-size:22px">
    一、构建信息：
    </p>
    <div> 
    <table>
        <tbody>
            <tr>
                <td width="200" valign="top" style="word-break:break-all;text-align:center;font-size:18px">
                    所属系统：
                </td>
                <td width="200" valign="top" style="word-break:break-all;font-size:18px">
                    %s
                </td>
                <td width="200" valign="top" style="word-break:break-all;text-align:center;font-size:18px">
                    分支：：
                </td>
                <td width="200" valign="top" style="word-break:break-all;font-size:18px">
                    %s
                </td>
            </tr>
            <tr>
                <td width="200" valign="top" style="word-break:break-all;text-align:center;font-size:18px">
                    触发人员：
                </td>
                <td width="200" valign="top" style="word-break:break-all;font-size:18px">
                    %s
                </td>
                <td width="200" valign="top" style="word-break:break-all;text-align:center;font-size:18px">
                    触发类型：
                </td>
                <td width="200" valign="top" style="word-break:break-all;font-size:18px">
                    %s
                </td>
            </tr>
            <tr>
                <td width="200" valign="top" style="word-break:break-all;text-align:center;font-size:18px">
                    开始时间：
                </td>
                <td width="200" valign="top" style="word-break:break-all;font-size:18px">
                    %s
                </td>
                <td width="200" valign="top" style="word-break:break-all;text-align:center;font-size:18px">
                    流水线id：
                </td>
                <td width="200" valign="top" style="word-break:break-all;font-size:18px">
                    %s
                </td>
            </tr>
        </tbody>
    </table>
    </div>
    ''' % (from_system, branch, trigger_user, trigger_type, trigger_time, serial_num)
    return trigger_info


def build_sona_info(pipeline):
    build_info = CiPipeline.query.filter(and_(CiPipeline.ci_pipeline_serial_num == pipeline.ci_pipeline_serial_num,
                                              CiPipeline.ci_pipeline_step == STEP_SONA)).first()
    job_info = CiJobInfo.query.filter(CiJobInfo.ci_job_id == build_info.ci_pipeline_job_id).first()
    log_info = CiLogInfo.query.filter(CiLogInfo.ci_log_id == build_info.ci_pipeline_job_log_id).first()
    sona_info = CiSonaInfo.query.filter(CiSonaInfo.ci_sona_id == build_info.ci_pipeline_sona_id).first()
    sonar_base_url = "http://sonar.kuainiujinke.com"
    sonar_url = sonar_base_url + "/dashboard?id=%s" % job_info.ci_job_system
    build_trigger_info = '''
    <p style="text-align:left;font-size:22px">
    二、SONA扫描详情
    </p>
    <p style="text-align:left">
        <span style="color:#3f4a56;font-size:18px">&nbsp; &nbsp; 1、构建信息<br style="text-align:left"></span>
	</p>
    <table>
        <tbody>
            <tr>
                <td width="200" valign="top" style="word-break:break-all;text-align:center;font-size:18px">
                    执行时间：
                </td>
                <td width="200" valign="top" style="word-break:break-all;font-size:18px">
                    %s
                </td>
                <td width="200" valign="top" style="word-break:break-all;text-align:center;font-size:18px">
                    扫描状态：
                </td>
                <td width="200" valign="top" style="word-break:break-all;font-size:18px">
                    %s
                </td>
            </tr>
            <tr>
                <td width="200" valign="top" style="word-break:break-all;text-align:center;font-size:18px">
                    扫描日志：
                </td>
                <td width="200" valign="top" style="word-break:break-all;font-size:18px">
                    <a href="%s" style="white-space:normal" target="_blank" >点击查看</a>
                </td>
                <td width="200" valign="top" style="word-break:break-all;text-align:center;font-size:18px">
                    扫描结果：
                </td>
                <td width="200" valign="top" style="word-break:break-all;font-size:18px">
                    <a href="%s" style="white-space:normal" target="_blank" >点击查看</a>
                </td>
            </tr>
        </tbody>
    </table>
    ''' % (build_info.ci_pipeline_run_time, build_info.ci_pipeline_status, log_info.ci_log_console_address, sonar_url)
    build_quality = '''
    <p style="text-align:left">
        <span style="color:#3f4a56;font-size:18px">&nbsp; &nbsp; 2、代码质量<br style="text-align:left"></span>
	</p>
    <table>
    <tbody>
        <tr>
            <td width="147" valign="top" style="word-break:break-all;text-align:center">
                 <span style="font-size:30px;color:#f85e5e"><strong><span style="font-size:30px;font-family:微软雅黑,&quot;Microsoft YaHei&quot;">%s</span></strong>
            </span></td>
            <td width="147" valign="top" style="word-break:break-all;text-align:center">
                 <span style="font-size:30px;color:#f85e5e"><strong><span style="font-size:30px;font-family:微软雅黑,&quot;Microsoft YaHei&quot;">%s</span></strong>
            </span></td>
            <td width="147" valign="top" style="word-break:break-all;text-align:center">
                 <span style="font-size:30px;color:#8091a5"><strong><span style="font-size:30px;font-family:微软雅黑,&quot;Microsoft YaHei&quot;">%s</span></strong>
            </span></td>
            <td width="147" valign="top" style="word-break:break-all;text-align:center">
                <span style="font-size:30px"><strong><span style="font-size:30px;font-family:微软雅黑,&quot;Microsoft YaHei&quot;">%s%%</span></strong></span>
            </td>
            <td width="147" valign="top" style="word-break:break-all;text-align:center">
                 <span style="font-size:30px"><strong><span style="font-size:30px;font-family:微软雅黑,&quot;Microsoft YaHei&quot;">%s%%</span></strong>
            </span></td>
            <td width="147" valign="top" style="word-break:break-all;text-align:center">
                 <span style="font-size:30px"><strong><span style="font-size:30px;font-family:微软雅黑,&quot;Microsoft YaHei&quot;">%s</span></strong>
            </span></td>
        </tr>
        <tr>
            <td width="147" valign="top" style="word-break:break-all;color:#8091a5;text-align:center">
                Bug
            </td>
            <td width="147" valign="top" style="word-break:break-all;color:#8091a5;text-align:center">
                漏洞
            </td>
            <td width="147" valign="top" style="word-break:break-all;color:#8091a5;text-align:center">
                坏味道
            </td>
            <td width="147" valign="top" style="word-break:break-all;color:#8091a5;text-align:center">
                覆盖率
            </td>
            <td width="147" valign="top" style="word-break:break-all;color:#8091a5;text-align:center">
                重复度
            </td>
            <td width="147" valign="top" style="word-break:break-all;color:#8091a5;text-align:center">
                重复块
            </td>
        </tr>
    </tbody>
    </table>
    ''' % (sona_info.ci_sona_bugs, sona_info.ci_sona_vulnerabilities, sona_info.ci_sona_code_smells,
           sona_info.ci_sona_coverage, sona_info.ci_sona_duplicateds, sona_info.ci_sona_duplicated_blocks)
    return build_trigger_info + build_quality


def build_compile_info(pipeline):
    build_info = CiPipeline.query.filter(and_(CiPipeline.ci_pipeline_serial_num == pipeline.ci_pipeline_serial_num,
                                              CiPipeline.ci_pipeline_step == STEP_BUILD)).first()
    if build_info is None:
        return ""
    log_info = CiLogInfo.query.filter(CiLogInfo.ci_log_id == build_info.ci_pipeline_job_log_id).first()

    build_compile_info = '''
    <p style="text-align:left;font-size:22px">
    三、项目编译详情
    </p>
    <p style="text-align:left">
        <span style="color:#3f4a56;font-size:18px">&nbsp; &nbsp; 1、构建信息<br style="text-align:left"></span>
    </p>
    <table>
        <tbody>
            <tr>
                <td width="200" valign="top" style="word-break:break-all;text-align:center;font-size:18px">
                    执行时间：
                </td>
                <td width="200" valign="top" style="word-break:break-all;font-size:18px">
                    %s
                </td>
                <td width="200" valign="top" style="word-break:break-all;text-align:center;font-size:18px">
                    构建状态：
                </td>
                <td width="200" valign="top" style="word-break:break-all;font-size:18px">
                    %s
                </td>
            </tr>
            <tr>
                <td width="200" valign="top" style="word-break:break-all;text-align:center;font-size:18px">
                    构建日志：
                </td>
                <td width="200" valign="top" style="word-break:break-all;font-size:18px">
                    <a href="%s" style="white-space:normal" target="_blank" >点击查看</a>
                </td>
            </tr>
        </tbody>
    </table>
    ''' % (build_info.ci_pipeline_run_time, build_info.ci_pipeline_status, log_info.ci_log_console_address)
    return build_compile_info


def build_test_info(pipeline, step):
    build_info = CiPipeline.query.filter(and_(CiPipeline.ci_pipeline_serial_num == pipeline.ci_pipeline_serial_num,
                                              CiPipeline.ci_pipeline_step == step)).first()
    if build_info is None:
        return ""
    log_info = CiLogInfo.query.filter(CiLogInfo.ci_log_id == build_info.ci_pipeline_job_log_id).first()
    test_info = CiAutotestInfo.query.filter(CiAutotestInfo.ci_autotest_id == build_info.ci_pipeline_autotest_id).first()

    test_trigger_info = '''
    <p style="text-align:left;font-size:22px">
    四、自动化测试详情
    </p>
    <p style="text-align:left">
        <span style="color:#3f4a56;font-size:18px">&nbsp; &nbsp; 1、构建信息<br style="text-align:left"></span>
    </p>
    <table>
        <tbody>
            <tr>
                <td width="200" valign="top" style="word-break:break-all;text-align:center;font-size:18px">
                    执行时间：
                </td>
                <td width="200" valign="top" style="word-break:break-all;font-size:18px">
                    %s
                </td>
                <td width="200" valign="top" style="word-break:break-all;text-align:center;font-size:18px">
                    构建状态：
                </td>
                <td width="200" valign="top" style="word-break:break-all;font-size:18px">
                    %s
                </td>
            </tr>
            <tr>
                <td width="200" valign="top" style="word-break:break-all;text-align:center;font-size:18px">
                    构建日志：
                </td>
                <td width="200" valign="top" style="word-break:break-all;font-size:18px">
                    <a href="%s" style="white-space:normal" target="_blank" >点击查看</a>
                </td>
                <td width="200" valign="top" style="word-break:break-all;text-align:center;font-size:18px">
                    自动化测试报告：
                </td>
                <td width="200" valign="top" style="word-break:break-all;font-size:18px">
                    <a href="%s" style="white-space:normal" target="_blank" >点击查看</a>
                </td>
            </tr>
        </tbody>
    </table>
        ''' % (build_info.ci_pipeline_run_time, build_info.ci_pipeline_status,
               log_info.ci_log_console_address, test_info.ci_autotest_report_address)
    test_quality = '''
    <p style="text-align:left">
    <span style="color:#3f4a56;font-size:18px">&nbsp; &nbsp; 2、自动化测试<br style="text-align:left"></span>
	</p>
    <table>
    <tbody>
        <tr>
            <td width="147" valign="top" style="word-break:break-all;text-align:center">
                <span style="font-size:30px"><strong><span style="font-size:30px;font-family:微软雅黑,&quot;Microsoft YaHei&quot;">%s</span></strong></span>
            </td>
            <td width="147" valign="top" style="word-break:break-all;text-align:center">
                 <span style="font-size:30px;color:#93c46b"><strong><span style="font-size:30px;font-family:微软雅黑,&quot;Microsoft YaHei&quot;">%s</span></strong>
            </span></td>
            <td width="147" valign="top" style="word-break:break-all;text-align:center">
                 <span style="font-size:30px;color:#f85e5e"><strong><span style="font-size:30px;font-family:微软雅黑,&quot;Microsoft YaHei&quot;">%s</span></strong>
            </span></td>
            <td width="147" valign="top" style="word-break:break-all;text-align:center">
                 <span style="font-size:30px;color:#8091a5"><strong><span style="font-size:30px;font-family:微软雅黑,&quot;Microsoft YaHei&quot;">%s</span></strong>
            </span></td>
            <td width="147" valign="top" style="word-break:break-all;text-align:center">
                 <span style="font-size:30px"><strong><span style="font-size:30px;font-family:微软雅黑,&quot;Microsoft YaHei&quot;">%s%%</span></strong>
            </span></td>
            <td width="147" valign="top" style="word-break:break-all;text-align:center">
                 <span style="font-size:30px"><strong><span style="font-size:30px;font-family:微软雅黑,&quot;Microsoft YaHei&quot;">%s</span></strong>
            </span></td>
        </tr>
        <tr>
            <td width="147" valign="top" style="word-break:break-all;color:#8091a5;text-align:center">
                用例总数
            </td>
            <td width="147" valign="top" style="word-break:break-all;color:#8091a5;text-align:center">
                通过
            </td>
            <td width="147" valign="top" style="word-break:break-all;color:#8091a5;text-align:center">
                失败
            </td>
            <td width="147" valign="top" style="word-break:break-all;color:#8091a5;text-align:center">
                错误
            </td>
            <td width="147" valign="top" style="word-break:break-all;color:#8091a5;text-align:center">
                通过率
            </td>
            <td width="147" valign="top" style="word-break:break-all;color:#8091a5;text-align:center">
                执行用时
            </td>
        </tr>
    </tbody>
    </table>''' % (test_info.ci_autotest_total_num, test_info.ci_autotest_success_num,
                   test_info.ci_autotest_fail_num, 0, test_info.ci_autotest_success_rate,
                   test_info.ci_autotest_running_time,)
    return test_trigger_info + test_quality
