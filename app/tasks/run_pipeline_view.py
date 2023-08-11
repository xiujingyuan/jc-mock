from flask import jsonify
from app.tasks import task_url
from app.tasks.run_pipeline.run_pipeline_task import run_pipeline, run_pipeline_send_email


@task_url.route("/run_pipeline", methods=["GET"])
def run_pipeline():
    run_pipeline.delay()
    return jsonify({"code": "success"})


@task_url.route("/run_pipeline_sendmail", methods=["GET"])
def run_pipeline_send_email():
    run_pipeline_send_email.delay()
    return jsonify({"code": "success"})


@task_url.route("/run_pipeline_create_task", methods=["GET"])
def run_pipeline_create_task():
    run_pipeline_create_task.delay()
    return jsonify({"code": "success"})
