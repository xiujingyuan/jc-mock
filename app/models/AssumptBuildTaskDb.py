# coding: utf-8
from datetime import datetime, date, time

from flask_sqlalchemy import Model
from sqlalchemy import Column, DateTime, String, text, Text, Date, Numeric, Time
from sqlalchemy.dialects.mysql import INTEGER, FLOAT
from app import db
from app.common.Serializer import Serializer, BaseToDict


class AssumptBuildTask(db.Model, BaseToDict, Serializer):
    __tablename__ = 'assumpt_build_task'

    id = Column(INTEGER(11), primary_key=True, comment='自增id')
    create_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='任务创建时间')
    update_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
                       comment='任务更新时间')
    publish_time = Column(DateTime, comment='发布时间')
    build_count = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='构建次数')
    last_build_user = Column(String(30, 'utf8_bin'), comment='最后构建人')
    last_build_time = Column(DateTime, comment='最后构建时间')
    program_id = Column(INTEGER(11), comment='项目id')
    program_name = Column(String(30, 'utf8_bin'), comment='项目名称')
    build_branch = Column(String(255, 'utf8_bin'), comment='构建分支')
    last_build_status = Column(INTEGER(11), comment='最后构建状态0:空闲，1:成功，2:失败3:构建中')
    last_run_id = Column(String(255, 'utf8_bin'), comment='最后执行id')
    last_build_env = Column(String(50, 'utf8_bin'), comment='最后构建环境')
    email_id = Column(String(11, 'utf8_bin'), comment='触发的邮件id', default='999999')
    build_task_status = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='构建任务状态。0:空闲；1:测试中')
    gitlab_program_id = Column(INTEGER(11), nullable=False, default=0)
    build_jenkins_jobs = Column(Text, nullable=False, default="")
    filter_file_value = Column(Text, nullable=False, default="", comment="覆盖率过滤文件配置")
    mail_receive_time = Column(DateTime, nullable=False, comment='提测邮件接收时间')
    case_name = Column(String(255, 'utf8_bin'), comment='用例名称')
    story_name = Column(String(255, 'utf8_bin'), comment='需求名称')
    story_url = Column(String(255, 'utf8_bin'), comment='需求地址')
    master_commit_id = Column(String(255, 'utf8_bin'), comment='该任务第一次构建时master的commit_id')
    story_id = Column(String(255, 'utf8_bin'), comment='关联需求id')
    story_full_id = Column(String(255, 'utf8_bin'), comment='关联需求的完整版id')
    work_id = Column(String(30, 'utf8_bin'), comment='关联需求所在的项目id(tapd)')
    gitlab_program_name = Column(String(30, 'utf8_bin'), comment='git项目名称')
    auto_queue_id = Column(INTEGER(10), default=0, comment='自动化任务的id')
    auto_url = Column(String(255, 'utf8_bin'), default="", comment='自动化构建地址')
    build_commit_type = Column(INTEGER(1), nullable=False, default=2,
                               comment='对比commit类型；1:构建时的commit_id;2:最新master的commit_id;3.最新的tag的commit_id')
    iteration_id = db.Column(db.String(100), nullable=False)
    last_coverage = Column(FLOAT, default=0.0)
    run_pipeline = Column(INTEGER(10), comment='是否运行流水线 1:是 0:否')
