from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from luckylog.luckylog import Logger,logger
from luckylog import luckylog
from pathlib import Path
from selenium.webdriver.support.select import Select

luckylog.path = Path(__file__).resolve().parents[1]/'AppRunningLog'/'TestRunningLog.log'
luckylog.module = 'erro'
luckylog.debug_file = Path(__file__).resolve().parents[1]/'AppRunningLog'/'ERRO.log'
luckylog.Debug = True

result_list = []

class Base:

    '''运行自动开启浏览器driver'''
    def __init__(self,dr):
        self.dr = dr
        self.dr.implicitly_wait(10)

    '''定义打开网址方法'''
    # @logger(success='成功打开网址',fail='打开网址失败')
    def open(self,url):
        try:
            self.dr.get(url)
            # Logger.success('成功进入网页',url)
        except Exception as e:
            Logger.erro('进入网址',url,'失败','\n',e)

    '''放入定位元素的方法'''
    def locate(self,name,value):
        return self.dr.find_element(name,value)

    '''定义点击方法'''
    # @logger(success='点击元素成功',fail='点击元素失败')
    def click(self,name,value):
        try:
            self.locate(name, value).click()
            Logger.success('进行点击事件成功')
        except Exception as e:
            Logger.erro('进行点击事件失败','\n',e)

    '''定义输入方法'''
    # @logger('元素输入成功','元素输入失败')
    def input(self,name,value,txt):
        try:
            self.locate(name, value).send_keys(txt)
            Logger.success('输入元素',txt,'成功')
        except Exception as e:
            Logger.erro('输入元素',txt,'失败','\n',e)

    '''定义等待方法'''
    # @logger('等待','进行等待失败')
    def wait(self,time_):
        try:
            time.sleep(int(time_))
            Logger.success('等待了',time_,'秒')
        except Exception as e:
            Logger.erro('等待失败','\n',e)

    # @logger('显性等待成功','显性等待失败')
    def wait_for(self,name,value):
        try:
            loc = self.locate(name, value)
            WebDriverWait(self.dr,10,0.5).until(EC.visibility_of_element_located(loc))
            Logger.success('显性等待已成功定位元素')
        except Exception as e:
            Logger.erro('显性等待失败','\n',e)

    # @logger('成功切换select','切换select失败')
    def select(self,name,value,type_,txt):
        try:
            loc = Select(self.locate(name, value))
            if 'value' in type_:
                loc.select_by_value(txt)
            elif 'index' in type_:
                loc.select_by_index(txt)
            elif 'text' in type_:
                loc.select_by_visible_text(txt)
            Logger.success('使用',type_,'定位选择成功')
        except Exception as e:
            Logger.erro('使用',type_,'定位选择失败','\n',e)

    # @logger('成功切换iframe','切换iframe失败')
    def iframe(self,name,value):
        try:
            loc = self.locate(name, value)
            self.dr.switch_to.frame(loc)
            Logger.success('切换iframe成功')
        except Exception as e:
            Logger.erro('切换iframe失败','\n',e)

    # @logger('成功切换handle','切换handle失败')
    def window(self,txt):
        try:
            handles = self.dr.window_handles
            self.dr.switch_to.window(handles[txt])
            Logger.success('切换handle成功')
        except Exception as e:
            Logger.erro('切换handle失败','\n',e)

    def js(self,txt):
        js = '''{}'''.format(txt)
        self.dr.execute_script(js)

    def quit(self):
        self.dr.quit()




