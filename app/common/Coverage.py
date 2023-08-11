#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2019/11/04
 @file: Coverage.py
 @site:
 @email:
 处理覆盖率相关的公共方法
"""
import math
import traceback

from flask import current_app
import json
import gitlab

from app.tools.tools import send_tv

REPLACE_STR = "src/main/java/qsq/paysvr/payment/"


def change_lines(change_line):
    new_lines = []
    for item in change_line:
        if not item:
            continue
        if "-" not in item:
            new_lines.append(int(item) - 1)
        else:
            item_list = item.split('-')
            for i in range(int(item_list[0]) - 1, int(item_list[1])):
                new_lines.append(i)
    return new_lines


def change_content_old(content):
    new_content = [
        {
            "text": "总体覆盖率",
            "content": [
                {
                    "fileName": "total",
                    "miss_line": int(content["basicInfo"]["missing"]) if content["basicInfo"] else 0,
                    "filter_line": int(content["basicInfo"]["total"]) if content["basicInfo"] else 0,
                    "total_line": int(content["basicInfo"]["total"]) if content["basicInfo"] else 0,
                    "coverage": content["basicInfo"]["coverage"] if content["basicInfo"] else "0%",
                    "filter_coverage": content["basicInfo"]["coverage"] if content["basicInfo"] else "0%",
                },
                {
                    "fileName": "total_calc",
                    "miss_line": 0,
                    "filter_line": 0,
                    "total_line": 0,
                    "coverage": "0%",
                    "filter_coverage": "0%",
                }
            ],
            "nodes": []
        }
    ]

    new_nodes = []

    for detail in content["detailInfo"]:
        item_line = change_lines(detail["missLines"])
        add_line = change_lines(detail["addSourceLines"])
        filter_line = change_lines(detail["addFilterLines"])
        total = len(add_line)
        miss_total = len(item_line)
        filter_total = len(filter_line)
        leaf = {
            "text": detail["fileName"],
            "type": "leaf", "src": "{0}/{1}".format(detail["src"], detail["fileName"]),
            "content": {"missLines": item_line, "addLines": add_line, "filterLines": filter_line}
        }
        src_list = detail["src"].split("/")
        new_text = "{0}/.../{1}/{2}".format(src_list[0], src_list[-2], src_list[-1])
        filter_coverage = "{0:.2f}%".format((filter_total - miss_total) / filter_total * 100) if filter_total else \
            detail["sigleCoverage"]

        coverage = "{0:.2f}%".format((total - miss_total) / total * 100) if total else \
            "0%"

        node = {
            "text": new_text,
            "type": "node",
            "src": detail["src"],
            "content": [
                {
                    "fileName": "total",
                    "miss_line": miss_total,
                    "total_line": total,
                    "filter_line": filter_total,
                    "coverage": coverage,
                    "filter_coverage": detail["sigleCoverage"]
                },
                {
                    "fileName": "{0}/{1}".format(detail["src"], detail["fileName"]),
                    "miss_line": miss_total,
                    "total_line": total,
                    "filter_line": filter_total,
                    "coverage": coverage,
                    "filter_coverage": detail["sigleCoverage"]
                }
            ],
            "nodes": [leaf]
        }

        new_content[0]["content"].append({
            "fileName": "{0}/{1}".format(detail["src"], detail["fileName"]),
            "miss_line": miss_total,
            "total_line":  total,
            "filter_line": filter_total,
            "coverage": coverage,
            "filter_coverage": detail["sigleCoverage"]
        })

        new_content[0]["content"][1]["miss_line"] += miss_total
        new_content[0]["content"][1]["total_line"] += total
        new_content[0]["content"][1]["filter_line"] += filter_total
        new_content[0]["content"][1]["coverage"] = "{0:.2f}%".format((total - miss_total) / total * 100) if total \
            else "0%"
        new_content[0]["content"][1]["filter_coverage"] = "{0:.2f}%".format((filter_total - miss_total) /
                                                                            filter_total * 100) if \
            filter_total else "0%"

        if new_nodes and detail["src"] in [item["src"] for item in new_nodes]:
            for item in new_nodes:
                if item["src"] == detail["src"]:
                    item["content"].append(
                        {
                            "fileName": "{0}/{1}".format(detail["src"], detail["fileName"]),
                            "miss_line": miss_total,
                            "total_line": total,
                            "filter_line": filter_total,
                            "coverage": coverage,
                            "filter_coverage": detail["sigleCoverage"]
                        }
                    )
                    item["content"][0]["miss_line"] += miss_total
                    item["content"][0]["total_line"] += total
                    item["content"][0]["filter_line"] += filter_total
                    item["content"][0]["coverage"] = "{0:.2f}%".format(100 * float(item["content"][0]["total_line"] -
                                                                                   item["content"][0]["miss_line"]) /
                                                                       item["content"][0]["total_line"]) if \
                        total != 0 else "100%"
                    item["content"][0]["filter_coverage"] = "{0:.2f}%".format(100 * float(
                        item["content"][0]["filter_line"] -
                        item["content"][0]["miss_line"]) / item["content"][0]["total_line"]) if \
                        filter_total != 0 else "100%"
                    item["nodes"].append(leaf)
                    break
        else:
            new_nodes.append(node)

    new_content[0]["nodes"] = new_nodes
    return new_content


def change_content(content):
    new_content = [
        {
            "text": "总体覆盖率",
            "content": [
                {
                    "fileName": "total",
                    "miss_line": int(content["basicInfo"]["missing"]) if content["basicInfo"] else 0,
                    "filter_line": int(content["basicInfo"]["total"]) if content["basicInfo"] else 0,
                    "total_line": int(content["basicInfo"]["total"]) if content["basicInfo"] else 0,
                    "coverage": content["basicInfo"]["coverage"] if content["basicInfo"] else "0%",
                    "filter_coverage": content["basicInfo"]["coverage"] if content["basicInfo"] else "0%",
                },
                {
                    "fileName": "total_calc",
                    "miss_line": 0,
                    "filter_line": 0,
                    "total_line": 0,
                    "coverage": "0%",
                    "filter_coverage": "0%",
                }
            ],
            "nodes": []
        }
    ]

    new_nodes = []

    for detail in content["detailInfo"]:
        item_line = change_lines(detail["missLines"])
        add_line = change_lines(detail["addSourceLines"]) if "addSourceLines" in detail else []
        filter_line = change_lines(detail["addFilterLines"]) if "addFilterLines" in detail else []
        total = len(add_line)
        miss_total = len(item_line)
        filter_total = len(filter_line)
        leaf = {
            "text": detail["fileName"],
            "type": "leaf", "src": "{0}/{1}".format(detail["src"], detail["fileName"]),
            "content": {"missLines": item_line, "addLines": add_line, "filterLines": filter_line}
        }
        src_list = detail["src"].split("/")
        new_text = "{0}/.../{1}/{2}".format(src_list[0], src_list[-2], src_list[-1])
        filter_coverage = "{0:.2f}%".format((filter_total - miss_total) / filter_total * 100) if filter_total else \
            detail["sigleCoverage"]

        coverage = "{0:.2f}%".format((total - miss_total) / total * 100) if total else \
            "0%"

        node = {
            "text": new_text,
            "type": "node",
            "src": detail["src"],
            "content": [
                {
                    "fileName": "total",
                    "miss_line": miss_total,
                    "total_line": total,
                    "filter_line": filter_total,
                    "coverage": coverage,
                    "filter_coverage": detail["sigleCoverage"]
                },
                {
                    "fileName": "{0}/{1}".format(detail["src"], detail["fileName"]),
                    "miss_line": miss_total,
                    "total_line": total,
                    "filter_line": filter_total,
                    "coverage": coverage,
                    "filter_coverage": detail["sigleCoverage"]
                }
            ],
            "nodes": [leaf]
        }

        new_content[0]["content"].append({
            "fileName": "{0}/{1}".format(detail["src"], detail["fileName"]),
            "miss_line": miss_total,
            "total_line":  total,
            "filter_line": filter_total,
            "coverage": coverage,
            "filter_coverage": detail["sigleCoverage"]
        })

        new_content[0]["content"][1]["miss_line"] += miss_total
        new_content[0]["content"][1]["total_line"] += total
        new_content[0]["content"][1]["filter_line"] += filter_total

        new_content[0]["content"][1]["coverage"] = "{0:.2f}%".format(
            (1 - round(new_content[0]["content"][1]["miss_line"] / new_content[0]["content"][1]["total_line"],
                       4)) * 100) if new_content[0]["content"][1]["total_line"] else "0%"
        # new_content[0]["content"][1]["filter_coverage"] = "{0:.2f}%".format(
        #     (1 - round(new_content[0]["content"][1]["miss_line"] / new_content[0]["content"][1]["filter_line"],
        #                4)) * 100) if new_content[0]["content"][1]["filter_line"] else "0%"
        new_content[0]["content"][1]["filter_coverage"] = "{0:.2f}%".format(100 * float(
            new_content[0]["content"][1]["filter_line"] -
            new_content[0]["content"][1]["miss_line"]) / new_content[0]["content"][1]["filter_line"]) if \
            filter_total != 0 else "100%"
        if new_nodes and detail["src"] in [item["src"] for item in new_nodes]:
            for item in new_nodes:
                if item["src"] == detail["src"]:
                    item["content"].append(
                        {
                            "fileName": "{0}/{1}".format(detail["src"], detail["fileName"]),
                            "miss_line": miss_total,
                            "total_line": total,
                            "filter_line": filter_total,
                            "coverage": coverage,
                            "filter_coverage": detail["sigleCoverage"]
                        }
                    )
                    item["content"][0]["miss_line"] += miss_total
                    item["content"][0]["total_line"] += total
                    item["content"][0]["filter_line"] += filter_total
                    item["content"][0]["coverage"] = "{0:.2f}%".format(100 * float(item["content"][0]["total_line"] -
                                                                                   item["content"][0]["miss_line"]) /
                                                                       item["content"][0]["total_line"]) if \
                        total != 0 else "100%"
                    item["content"][0]["filter_coverage"] = "{0:.2f}%".format(100 * float(
                        item["content"][0]["filter_line"] -
                        item["content"][0]["miss_line"]) / item["content"][0]["filter_line"]) if \
                        filter_total != 0 else "100%"
                    item["nodes"].append(leaf)
                    break
        else:
            new_nodes.append(node)

    new_content[0]["nodes"] = new_nodes
    return new_content


def set_diff_coverage_redis(system, branch, env, commit_id, task_id):
    new_coverage = {
        'branch': branch,
        'system': system,
        'env': env,
        "commit_id": commit_id,
        "task_id": task_id
    }
    current_app.logger.info("new_coverage is :{0}".format(new_coverage))
    if current_app.app_redis.exists("get_diff_coverage"):
        diff_coverages = json.loads(current_app.app_redis.get("get_diff_coverage"))
        is_found = False
        for coverage in diff_coverages:
            if new_coverage["task_id"] == coverage["task_id"]:
                coverage["env"] = new_coverage["env"]
                coverage["commit_id"] = new_coverage["commit_id"]
                coverage["branch"] = new_coverage["branch"]
                is_found = True
                break
        if not is_found:
            diff_coverages.append(new_coverage)
        current_app.app_redis.set("get_diff_coverage", json.dumps(diff_coverages, ensure_ascii=False))
    else:
        diff_coverages = [new_coverage]
        current_app.app_redis.set("get_diff_coverage", json.dumps(diff_coverages, ensure_ascii=False))


def get_branch_commit(gitlab_id, branch):
    """
    根据传递的gitlab的ID和分支名，返回当前最新的commit的ID
    :param gitlab_id: 需求获取的gitlab的iD
    :param branch: 需要获取的分支名
    :param type: OA
    :return: 返回对应项目，对应分支最新的commit的ID
    """
    commit_id = 0
    current_app.logger.info("get_branch_commit begin, gitlab_id is {0}, branch is {1}".format(gitlab_id, branch))
    try:
        gl = gitlab.Gitlab('https://git.kuainiujinke.com', private_token='VgsYpQHfbEr9KBCTWJPc')
        gl.auth()
        project = gl.projects.get(gitlab_id)
        branch_commits = project.commits.list(ref_name=branch)
        commit_id = branch_commits[0].id
    except:
        send_tv(traceback.format_exc())
        current_app.logger.error(traceback.format_exc())
    finally:
        current_app.logger.info("get_branch_commit finish, gitlab_id is {0}, branch is {1}, commit is : {2}".format(
            gitlab_id,
            branch,
            commit_id))
        return commit_id


def get_tag_commit(gitlab_id):
    """
    根据传递的gitlab的ID和分支名，返回当前最新的commit的ID
    :param gitlab_id: 需求获取的gitlab的iD
    :return: 返回对应项目，对应最新tag对应的commit的ID
    """
    commit_id = 0
    current_app.logger.info("get_tag_commit begin, gitlab_id is {0}".format(gitlab_id))
    try:
        gl = gitlab.Gitlab('https://git.kuainiujinke.com', private_token='VgsYpQHfbEr9KBCTWJPc')
        gl.auth()
        project = gl.projects.get(gitlab_id)
        branch_tag = project.tags.list()
        commit_id = branch_tag[0].commit["id"]
    except:
        send_tv(traceback.format_exc())
        current_app.logger.error(traceback.format_exc())
    finally:
        current_app.logger.info("get_tag_commit finish, gitlab_id is {0}, commit is : {1}, tag is {2}".format(
            gitlab_id,
            commit_id,
            branch_tag[0].name))
        return commit_id


def get_branch_commit_all(gitlab_id, branch, env):
    commit_id = []
    current_app.logger.info("get_branch_commit begin, gitlab_id is {0}, branch is {1}".format(gitlab_id, branch))
    try:
        gl = gitlab.Gitlab('https://git.kuainiujinke.com', private_token='VgsYpQHfbEr9KBCTWJPc')
        gl.auth()
        project = gl.projects.get(gitlab_id)
        branch_commits = project.commits.list(ref_name=branch)
        for index, branch_commit in enumerate(branch_commits):
            if index > 9:
                break
            commit_id.append({"id": branch_commit.id,
                              "author": branch_commit.author_name,
                              "time": branch_commit.committed_date,
                              "name": branch_commit.title,
                              "gitlab_id": gitlab_id,
                              "branch": branch,
                              "env": env})
    except:
        send_tv(traceback.format_exc())
        current_app.logger.error(traceback.format_exc())
        commit_id = []
    finally:
        current_app.logger.info("get_branch_commit finish, gitlab_id is {0}, branch is {1}".format(
            gitlab_id,
            branch))
        return commit_id
