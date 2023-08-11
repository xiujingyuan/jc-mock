from flask import jsonify
from app.tasks import task_url
from app.tasks.sonar_schedule.sonar_schedule_task import sonar_schedule_create, sonar_schedule_query


@task_url.route("/sonar_schedule_create", methods=["GET"])
def sonar_schedule_create():
    sonar_schedule_create.delay()
    return jsonify({"code": "success"})


@task_url.route("/sonar_schedule_query", methods=["GET"])
def sonar_schedule_query():
    sonar_schedule_query.delay()
    return jsonify({"code": "success"})
