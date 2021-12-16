import chunk
import os.path
from pathlib import Path
from django.forms import models
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from TestApp import models
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.http import StreamingHttpResponse   #文件流形式读取文件
import json
from django.core.paginator import Paginator   #使用django自带分页进行表格分页操作处理数据
# Create your views here.
from django.http import JsonResponse
from luckylog.luckylog import Logger
from luckylog import luckylog
luckylog.path = Path(__file__).resolve().parents[1]/'logfile'/'systemRun.log'
luckylog.module = 'success,erro,worning,tip'

#注册账号界面
def sightPage(request):
    return render(request,'TestApp/sightin_page.html')

@csrf_exempt
#登录界面
def loginpage(request):
    return render(request,'TestApp/login_page.html')

#退出登录
def loginOut(request):
    logout(request)
    return redirect('loginpage')

#实际进行注册的方法
@csrf_exempt
def insertUser(request):
    if request.method == 'POST':
        user = request.POST['username']
        pwd = request.POST['pwd']
        email = request.POST['email']
        User.objects.create_user(username=user,password=pwd,email=email)
        Logger.success(user,'进行注册成功','邮箱',email)
        return render(request,'TestApp/login_page.html',{'mes':'注册成功，请登录'})

@login_required(login_url='/loginpage')
#正式进行界面自动化测试界面
def UItestIndex(request):
    return render(request,'TestApp/startUItest.html')


@csrf_exempt
def loginUser(request):
    username = request.POST.get('user')
    pwd = request.POST.get('pwd')
    print(username,pwd)
    user = authenticate(request,username=username,password=pwd)
    if user is not None:
        print('进入登录')
        login(request,user)
        Logger.success('***用户',username,'登录***')
        request.session['username']=username    #获取request的session，传递给此用户名
        request.session.set_expiry(0)    #设置关闭session在关闭浏览器之后
        return JsonResponse({'st':0,'ms':'登录成功,点击确定跳转首页'})
    else:
        return JsonResponse({'st':4,'ms':'登录失败，请检查账号密码'})


#首页
@login_required(login_url='/loginpage')
def Indexpage(request):
    return render(request, 'TestApp/index.html')

#功能测试首页
@login_required(login_url='/loginpage')
def UiTestPage(request):
    return render(request,'TestApp/uploadpage.html')

#上传文件并写入数据库
@csrf_exempt
def upload_testcase(request):
    # u_id = User.objects.filter(username='hzz').values('id')
    current_userID = request.user.id   #获取登录用户ID，关联上传的文件
    print(current_userID)
    if request.method == 'POST':
        file = request.FILES['file']
        # print(file.name)
        database_files = models.case_file.objects.filter(f_num_id=current_userID, title=file.name)
        print(bool(database_files))
        if database_files:
            return JsonResponse({'st':2,'info1':'您已上传过此文件，请直接使用'})
        else:
            try:
                with open(os.path.join('media',file.name),'wb+') as f:
                    for chunk in file.chunks():
                        f.write(chunk)
                models.case_file.objects.create(title=file.name,file=file,f_num_id=current_userID)
                current_file = Path(__file__).resolve().parent.parent/'media'/file.name
                current_file.unlink()
                Logger.success('用户',request.user.username,'成功上传用例文件：',file.name)
                return JsonResponse({'st':1,'info1':'上传成功！！'})
            except:
                Logger.erro('用户：',request.user.username,'上传用例文件失败')
                return JsonResponse({'st':3,'info1':'上传失败，请检查文件'})
    else:
        return render(request,'TestApp/uploadpage.html')

#定义删除数据库数据和文件方法,应用于表格文件删除
@csrf_exempt
def deleta_data(request):
    user_id = request.user.id
    file_name = request.POST.get('filename')
    data = models.case_file.objects.filter(f_num_id=user_id,title=file_name)
    print('data是：',data)
    files_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'media/')
    for del_file in data:
        file = files_path+'{}'.format(del_file.file)
        print(file)
        os.remove(file)
        data.delete()
    Logger.success('用户',request.user.username,'删除文件：',file_name)
    return JsonResponse({'info_del':'文件数据已删除'})

#定义下载model测试模板的方法
def download_model(request):
    father_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(father_dir,'case_model','2.xlsx')
    def send_file(file,chunk_size=512):
        with open(file_path,'rb') as f:
            while True:
                a = f.read(chunk_size)
                if a:
                    yield a
                else:
                    break
    response = StreamingHttpResponse(send_file(file_path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachement;filename={}'.format('2.xlsx')
    return response

#我的用例界面及操作
def testcasePage(request):
    return render(request,'TestApp/myTastCase.html')

def myTestCase(request):
    current_user = request.user.id
    files = models.case_file.objects.filter(f_num_id=current_user)   #获取数据库所有文件数据
    data_list = []
    for file in files:
        data = dict()
        data['id'] = file.id
        data['filename'] = file.title
        data['update'] = file.upload_time.strftime("%Y-%m-%d %H:%M:%S")
        data_list.append(data)
    # data_list1={"code":0,"msg":"","count":1,"data":[{"id":1,"filename":"12.csv","update":"2021 10"}]}
    #layui会默认传来page和limit数据，直接获取就好
    page_index = request.GET.get('page')   #获取前端传来的页数
    page_limit = request.GET.get('limit')     #获取前端限制的数据显示
    # page_index = 1
    # page_limit = 10
    if page_limit and page_index:
        paginator = Paginator(data_list,page_limit)       #使用分页器进行数据分配
        data_page = paginator.page(page_index)      #前端传来的页数数据
        files_info = [x for x in data_page]     #将数据放在一个列表进行返回
        # print(files_info)
        send_files = {"code":0,"msg":"","count":files.count(),"data":files_info}
        return JsonResponse(send_files)
#检查用例的界面
def casecheck_page(request):
    return render(request,'TestApp/casecheck.html')

#获取所有的用例文件名，返回给前端
def return_casefiles(request):
    current_user = request.user.id
    print(current_user)
    case_files = models.case_file.objects.filter(f_num_id=current_user)
    casefiles_list = []
    for file in case_files:
        casefiles_list.append(file.title)
    return JsonResponse({'casefiles':casefiles_list})

#等待loading界面
def loading(request):
    return render(request,'TestApp/LoadingPage.html')