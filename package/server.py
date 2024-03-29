from DrissionPage import ChromiumPage
from DrissionPage import ChromiumOptions, SessionOptions, WebPage
import traceback
import time
import datetime
#co = ChromiumOptions(ini_path=r'.\config\web-config.ini')
#so = SessionOptions(ini_path=r'.\config\web-config.ini')
def init():
    page = ChromiumPage()
    page.set.timeouts(page_load=20)
    page.set.retry_times(0)
    return page
# 创建页面对象
#page = SessionPage()

ip = '172.16.1.1'
username = 'admin'
passwd = ''


def get_devices(ip:str, user:str, passwd:str,count:int=0):
    try:
        page = init()
        page.clear_cache(cache=False)
        page.get(f'https://{ip}')
        inputs = page.eles('@class=el-input__inner')
        inputs[0].input(user)
        inputs[1].input(passwd)
        page.ele(locator='@type=button').click()
        page.ele(locator='视频监测').focus()
        time.sleep(0.5)
        page.ele(locator='视频监测').click()
        page.ele(locator='编码设备检测').click()
        page.run_js_loaded('')
        page.ele(locator='刷新').click()
        page.run_js_loaded('')
        page.ele(locator='导出所有').click.to_download(rename=f'编码设备在线情况{ip}',save_path='./街乡平台设备导出表/')
    except:
        traceback.print_exc()
        return False
    return True

# 监控点
def get_online(ip:str, user:str='admin', passwd:str='hik@2022'):
    try:
        page = init()
        page.clear_cache()
        page.get(f'https://{ip}')
        inputs = page.eles('@class=el-input__inner')
        inputs[0].input(user)
        inputs[1].input(passwd)
        page.ele(locator='@type=button').click()
        page._wait_loaded(2)
        time.sleep(2)
        page.get(f'https://{ip}/portal/ui/system-configuration')
        #page.eles('@class=el-submenu__title--text')[2].click()
        ele = page.ele(locator='设备管理')
        ele.click()
        ele.after('视频').click()
        #ele.after('@class=el-menu-item').click()
        page.ele(locator='监控点').click()
        page.ele('@class=el-checkbox__label').before('@class=el-checkbox__input').click()
        time.sleep(0.5)
        page.run_js_loaded('')
        page.ele('@class=h-icon-export').click()
        #ele = page.ele('@class=el-message-box__btns')
        ele = page.ele('@class=el-button el-button--default el-button--primary ')
        ele.click.to_download(rename=f'监控点{ip}',save_path='./街乡平台监控点导出表/')
    except:
        traceback.print_exc()
        return False
    return True

def community(user:str="qjsys",passwd="Cyzhsq2020"):
    try:
        page = init()
        page.get(f'https://172.16.1.168:82/#/capture-mack')
        inputs = page.eles('@class=loginText')
        if len(inputs) > 1:
            inputs[0].input(user)
            inputs[1].input(passwd)
            page.ele(locator='@type=button').click()
        clicks = page.eles(locator='数据统计')
        clicks[0].click()
        clicks = page.eles(locator='数据统计')
        clicks[1].click()
        page.ele(locator='各小区设备统计').click()
        time.sleep(0.5)
        page.run_js_loaded('')
        ele = page.ele(locator='导出')
        ele.click.to_download(rename=f'小区设备情况-{datetime.date.today()}')
        page.close()
    except:
        traceback.print_exc()
        return False
    return True

if __name__ == '__main__':
    #get_online(ip=ip)
    community()