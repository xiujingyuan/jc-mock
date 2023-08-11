from celery_once import QueueOnce
from app import celery, db
from app.models.ApiLogDb import ApiLog
import json


@celery.task(base=QueueOnce, once={"graceful": True}, bind=True, ignore_result=True)
def calc_count_task(self, ip, request_json, request_method, current_user, response_json):
    new_api_log = ApiLog()
    new_api_log.api_log_ip = ip
    new_api_log.api_log_method = request_method
    new_api_log.api_log_request_body = request_json["common_tools_placeholder"]
    new_api_log.api_log_user = current_user
    new_api_log.api_log_url = request_json["common_tools_address"]
    new_api_log.api_log_response_body = json.dumps(response_json, ensure_ascii=False)
    new_api_log.api_log_is_success = 1 if response_json["code"] == 0 else 0
    db.session.add(new_api_log)
    db.session.flush()
