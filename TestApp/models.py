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

