"""UItestProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from TestApp import views
from django.conf import settings
from django.conf.urls.static import static
from TestApp.RunTest.modelCheck import modelCheck
from TestApp.RunTest.testcaseRun import testcaserun
from TestApp.RunTest.testcaseRun import testview
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Indexpage,name='index'),  #首页
    path('Uitest',views.UiTestPage,name='UiTestName'),  #功能测试首页
    path('uploadfile',views.upload_testcase,name='upload_files'),#上传文件接口，无页面
    path('sightinpage',views.sightPage,name='sightinpage'),    #注册页面
    path('sightin',views.insertUser,name = 'sight'),     #注册验证实现接口，无界面
    path('loginpage',views.loginpage,name = 'loginpage'),   #登录界面
    path('login',views.loginUser,name = 'logincheck'),    #登录验证接口，无界面
    path('loginout',views.loginOut,name='loginout'),      #退出登录接口，无界面
    path('deletaData',views.deleta_data,name='deletafile'),  #删除文件的接口，无界面
    path('ui-test',views.UItestIndex,name='uitest'),     #ui正式进行测试的界面
    path('downloadmodel',views.download_model,name='downloadmodel'), #定义下载文件的方法路径
    path('mycasefile',views.testcasePage,name='testcasepage'),  #定义用例显示页面（界面）
    path('getTestcase',views.myTestCase,name="gettestcase"),   #定义获取用例的方法路径
    path('casecheckapi',modelCheck.case_Check,name = 'casecheck'),
    path('casefilereturnapi',views.return_casefiles,name='casefilereturn'), #返回用例文件接口
    path('casecheckpage',views.casecheck_page,name='casecheckpage'), #用例检查页面
    path('setcaseapi',modelCheck.case_set,name='caseset'),
    path('runtest',testcaserun.runTest,name='runTest'), #定义进行测试的方法api
    path('LOADING',views.loading,name='loading'), #定义的loading界面
    # path('report/<filename>',testcaserun.redirect_report_page,name='report')
    # path('report',testcaserun.report_ajax,name='report')
    # #测试接口
    # path('test',testview.test,name='test1'),
    # path('test2/<file>',testview.test2,name='test2'),
]+static(settings.STATIC_URL,document_root = settings.MEDIA_ROOT)
