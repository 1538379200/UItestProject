import json

import pytest
import allure
import os
import random
import string
from pathlib import Path
import time
def get_random():
    A1 = ''.join(random.sample(string.ascii_lowercase+string.digits,8))
    A2 = ''.join(random.sample(string.ascii_lowercase+string.digits,4))
    A3 = ''.join(random.sample(string.ascii_lowercase+string.digits,4))
    A4 = ''.join(random.sample(string.ascii_lowercase+string.digits,4))
    A5 = ''.join(random.sample(string.ascii_lowercase+string.digits,12))
    result_name = A1+'-'+A2+'-'+A3+'-'+A4+'-'+A5
    return result_name


def creat_result_file(testFeature,testStory,resultDir,resultName,caseStatus,startTime,endTime):
    result_content = {
        "name": resultName,
        "status": caseStatus,
        "steps": [{
            "name": '运行结果',
            "status": caseStatus,
            "start": startTime,
            "stop": endTime}],
        "start": startTime,
        "stop": endTime,
        "uuid": get_random(),
        "historyId": get_random(),
        "testCaseId": get_random(),
        "fullName": "测码自动化",
        "labels": [
            {
                "name": "story", "value": testStory
            },
            {
                "name": "feature", "value": testFeature
            },
            {
                "name": "suite",
                "value": "测码自动化测试套件"},
            {
                "name": "subSuite",
                "value": "测码自动化测试用例"},
            {
                "name": "host",
                "value": "DESKTOP"},
            {"name": "framework",
             "value": "pytest"},
            {
                "name": "language",
                "value": "cpython3"},
            {
                "name": "package",
                "value": "测码自动化测试"}
        ]
    }
    mypath = resultDir
    has_dir=os.path.exists(mypath)
    if not has_dir:
        os.makedirs(mypath)
    report_name = get_random()+' -result.json'
    report_dir = mypath / report_name
    with open(report_dir,'w',encoding='utf-8') as f:
        f.write(json.dumps(result_content))
        f.close()
