from DrissionPage import ChromiumOptions, SessionOptions, WebPage
import traceback
import time

def init():
    co = ChromiumOptions(ini_path=r'.\config\web-config.ini')
    so = SessionOptions(ini_path=r'.\config\web-config.ini')
    return WebPage(chromium_options=co, session_or_options=so)
# 创建页面对象
#page = SessionPage()

"""
#下载操作
ele.click.to_download(rename=f'{datetime.date.today()}',)
"""

# ntp设置
def ntp_hik_DS2(ip:str, user:str='admin', passwd:str=''):
    ntp:str='172.16.1.6'
    page = init()
    try:
        page.get(f'http://{ip}/doc/page/config.asp')
        page.ele(locator='#username').input(user)
        page.ele(locator='#password').input(passwd)
        page.ele(locator='@type=button').click()
        time.sleep(0.2)
        page.ele(locator='时间配置').click()
        page.ele('#radioNTP').click()
        page.ele('@ng-model=oSettingTimeInfo.szNTPAddress').input(ntp)
        page.ele('@ng-model=oSettingTimeInfo.szNTPInterval').input(120)
        page.ele('保存').click()
        page.ele('@ng-model=oSettingTimeInfo.szNTPInterval').input(100)
        try:
            page.ele('@ng-bind=oLan.save').parent().click()
        except:
            pass
        page.ele('保存').click()
        page.refresh()
        page.ele('时间配置').click()
        input('确认完成?')
    except:
        traceback.print_exc()
        if input('是否手动调整完成 输入1/0:\t') =='0':
            return False
        else:
            return True
    return True

# 设备型号 DS-2CD7A47HEWD-XZS
def change_ntp_hik_DS2(ip:str, user:str, passwd:str, time=1000):
    page = init()
    try:
        page.get(f'http://{ip}/doc/page/config.asp')
        page.ele(locator='#username').input(user)
        page.ele(locator='#password').input(passwd)
        page.ele(locator='@type=button').click()
        page.ele(locator='时间配置').click()
        page.ele('@ng-model=oSettingTimeInfo.szNTPInterval').input(time)
        page.ele('@class=btn btn-primary btn-save').click()
        input('确定?')
    except:
        return False
    return True

def change_ntp_unv(ip:str, user:str='admin', passwd:str='12345678a_', time=3600):
    page = init()
    try:
        page.get(f'http://{ip}')
        #page.ele(locator='#userName').input(user)
        page.ele(locator='#password').input(passwd)
        page.ele(locator='@type=button').click()
        page.ele('配置').click()
        page.ele('#Com_timeCfgLink').click()
        page.ele('#SyncType').click()
        page.ele('同步NTP服务器时间').click()
        page.ele('#NTPIPAddr').input('172.16.1.6')
        page.ele('#NTPSyncInterval').input(time)
        page.ele('@class=submit_btn').click()
        input('确定?')
    except:
        traceback.print_exc()
        return False
    return True

def change_ntp_dahua(ip:str, user:str='admin', passwd:str='', time=1200):
    page = init()
    print(ip,passwd)
    try:
        page.get(f'http://{ip}')
        eles = page.eles('tag:input')
        eles[0].input(user)
        eles[1].input(passwd)
        page.ele('@type=submit').click()
        page.ele('@class=anticon myicon-set myicon ').click()
        page.ele('系统管理').click()
        page.ele('日期设置').click()
        page.ele('@value=NTP').click()
        page.ele('#normal_login_Server').input('172.16.1.6')
        page.eles('@step=1')[1].input(time)
        page.ele('手动更新').click()
        page.ele('@class=ant-btn _submitButton ant-btn-primary').click()
        time.sleep(1)
        input('确定?')
    except:
        if input('是否手动调整完成 输入1/0:\t') =='0':
            return False
        else:
            return True
    return True

# 设备型号 DS-2CD7A47HEWD-XZS
def change_osd_hik_DS2(ip:str, user:str, passwd:str, osd3:str,osd4:str):
    try:
        page = init()
        page.get(f'http://{ip}/doc/page/config.asp')
        page.ele(locator='#username').input(user)
        page.ele(locator='#password').input(passwd)
        page.ele(locator='@type=button').click()
        page.ele(locator='图像').click()
        page.ele(locator='OSD设置').click()
        time.sleep(1)
        page.run_js_loaded("""document.querySelector('select[ng-model="oOsdParams.dateFormat"]').value = 0; """,timeout=3)
        time.sleep(1)
        page.run_js_loaded("""document.querySelector('select[ng-model="oOsdParams.OSDSize"]').value = 4; """,timeout=3)
        time.sleep(1)
        page.run_js_loaded("""document.querySelector('select[ng-model="oOsdParams.OSDColorMode"]').value = 0; """,timeout=3)
        try:
            page.run_js_loaded("""var selectElement = document.querySelector("select[ng-model='oOsdParams.szAlignment']");
                                selectElement.value = "5";
                                selectElement.dispatchEvent(new Event('change'));""")
        except:
            page.run_js_loaded("""var selectElement = document.querySelector("select[ng-model='oOsdParams.szAlignment']");
                                selectElement.value = "3";
                                selectElement.dispatchEvent(new Event('change'));""")
        #page.ele('@ng-model=oOsdParams.szAlignment').click()
        inputs = page.eles('tag:input')

        inputs[11].check()
        inputs[12].input('北京')
        inputs[13].check()
        inputs[14].input('朝阳')
        inputs[15].check()
        inputs[16].input(osd3)
        inputs[17].check()
        inputs[18].input(osd4)
        inputs[23].check()
        page.ele('保存').click()
    except:
        return False
    return True

if __name__ == '__main__':
    ip = '172.16.1.1'
    username = 'admin'
    passwd = '...'
    success = change_ntp_dahua(ip,username,passwd)
    print(success)
