from TestApp.RunTest.basefile.base import Base
import openpyxl
from pathlib import Path
from luckylog.luckylog import Logger
# from django.contrib.auth.models import User
from django.shortcuts import redirect,render,HttpResponse,reverse
from selenium import webdriver
from TestApp import models
from django.views.decorators.csrf import csrf_exempt
from selenium.webdriver.chrome.options import Options
from django.http import JsonResponse
import json
import time
from TestApp.RunTest.testcaseRun.CreatRresult import creat_result_file
import os
import shutil    #此包用来移动/复制文件
# casefile_Path = Path(__file__).resolve().parents[3]/'media'/'11.xlsx'
# work_book = openpyxl.load_workbook(casefile_Path)
# # sheet = work_book['Sheet1']
# sheets = work_book.sheetnames
# # print(sheets)

@csrf_exempt
def runTest(request):
    current_user = request.user.id
    request_body = json.loads(request.body)
    file = request_body.get('file')
    file_list = models.case_file.objects.filter(title=file,f_num_id=current_user)
    print(file_list)
    option = Options()
    option.headless = True
    if file_list:
        for case_file in file_list:
            # print(case_file.file)
            wb = Base(webdriver.Chrome())
            try:
                casefile_Path = Path(__file__).resolve().parents[3] / 'media' / '{}'.format(case_file.file)
                resultDir = Path(__file__).resolve().parents[1] / 'RunedFiles' / 'RunningResult' / '{}_{}'.format(current_user,file)
                reportDir = Path(__file__).resolve().parents[1] / 'RunedFiles' / 'RunningReport' / '{}_{}'.format(current_user,file)
                work_book = openpyxl.load_workbook(casefile_Path)
                print(resultDir,reportDir)
                # sheet = work_book['Sheet1']
                sheets = work_book.sheetnames
                # print(sheets)
                for sheet_name in sheets:
                    sheet = work_book[sheet_name]
                    testFeature = sheet['A1'].value  # 表格的第一个为测试的系统
                    for value_row in sheet.values:
                        # print('用例')
                        if type(value_row[0]) is int:
                            # print('用例')
                            value_list = value_row[2].split(';')
                            Keys_list = []
                            Values_list = []
                            caseName = value_row[3]
                            testStory = value_row[4]    #表格用例的最后一个作为报告的功能点
                            for valueTodict in value_list:
                                kv_list = valueTodict.split('=',1)
                                # print(kv_list)
                                Keys_list.append(kv_list[0])
                                Values_list.append(kv_list[1])
                            # dict_ = dict(zip(Keys_list,Values_list))  #将两个列表合并成一个字典形式
                            dict_ = dict(zip(Keys_list,Values_list))
                            start_time = int(round(time.time()*1000))
                            runStatus = getattr(wb,value_row[1])(**dict_)
                            if runStatus:
                                caseStatus = "passed"
                            else:
                                caseStatus = "failed"
                            end_time = int(round(time.time()*1000))
                            creat_result_file(testFeature=testFeature,testStory=testStory,resultDir=resultDir,resultName=caseName,caseStatus=caseStatus,startTime=start_time,endTime=end_time)
                wb.quit()
                os.system('allure generate {0} -o {1} --clean'.format(resultDir,reportDir))
                os.system('allure open -h 127.0.0.1 -p 8083 {}'.format(reportDir))
                time.sleep(20)
                try:
                    os.system('taskkill -F -PID 8083')
                    print('关闭端口')
                except:
                    print('未能关闭')
                return JsonResponse({'stu':1})
                # return redirect(reverse('report',kwargs={'filename':file}))
            except Exception as e:
                Logger.erro('程序运行出错，请检查输入的数据',e)
                wb.quit()
                return JsonResponse({'stu':2,'mes':'程序运行出错，请检查数据'})
    else:
        return JsonResponse({'stu':3,'mes':'您还没有用例，请上传用例'})



def redirect_report_page(request,filename):
    currentid = request.user.id
    reportDir = str(currentid)+'_'+filename
    html_file = reportDir+'/index.html'
    return render(request,html_file)
