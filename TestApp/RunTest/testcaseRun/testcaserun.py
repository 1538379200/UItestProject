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
import json
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
                work_book = openpyxl.load_workbook(casefile_Path)
                # sheet = work_book['Sheet1']
                sheets = work_book.sheetnames
                # print(sheets)
                for sheet_name in sheets:
                    sheet = work_book[sheet_name]
                    for value_row in sheet.values:
                        # print('用例')
                        if type(value_row[0]) is int:
                            # print('用例')
                            value_list = value_row[2].split(';')
                            Keys_list = []
                            Values_list = []
                            for valueTodict in value_list:
                                kv_list = valueTodict.split('=',1)
                                # print(kv_list)
                                Keys_list.append(kv_list[0])
                                Values_list.append(kv_list[1])
                            dict_ = dict(zip(Keys_list,Values_list))
                            getattr(wb,value_row[1])(**dict_)
                wb.quit()
                return render(request,'TestApp/testpage.html',{'message':'运行成功了'})
            except Exception as e:
                Logger.erro('程序运行出错，请检查输入的数据',e)
                wb.quit()
                return HttpResponse({'message':'运行失败，请检查数据'})
    else:
        return HttpResponse("您当前还没有用例文件,请先去上传用例")