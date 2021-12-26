from django.db import models
import time

# Create your models here.

class case_file(models.Model):
    title = models.CharField(max_length=100,verbose_name='文件名')
    file = models.FileField(verbose_name='文件地址')
    upload_time = models.DateTimeField(auto_now_add=True,verbose_name='上传时间')
    f_num = models.ForeignKey(to='auth.User',on_delete=models.CASCADE)
    class Meta():
        # db_table=''
        verbose_name='用户上传用例文件'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.title

class report(models.Model):
    report = models.CharField(max_length=200,verbose_name='报告名')
    userid = models.ForeignKey(to='auth.User',on_delete=models.CASCADE)
    class Meta():
        db_table = 'report'
        verbose_name = '生成的报告文件'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.report

class personcase(models.Model):
    user = models.ForeignKey(to='auth.User',on_delete=models.CASCADE)
    reportname = models.CharField(max_length=200,verbose_name='报告名')
    systemName = models.CharField(max_length=200,verbose_name='测试系统')
    modelName = models.CharField(max_length=200,verbose_name='模块名称')
    caseName = models.CharField(max_length=200,verbose_name='用例名称')
    status = models.CharField(max_length=10,verbose_name='运行结果')
    runTime = models.DecimalField(max_digits=20,decimal_places=2)
    caseFile = models.CharField(max_length=200,verbose_name='文件名')
    descript = models.CharField(max_length=200,verbose_name='用例描述')
    class Meta():
        db_table = 'personCase'
        verbose_name = '用例运行结果'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.user,self.reportname,self.status,self.caseName,self.status