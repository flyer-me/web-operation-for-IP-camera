import traceback
import time

def init():
    from DrissionPage import ChromiumOptions,ChromiumPage
    co = ChromiumOptions().set_local_port(9222)
    co = co.ignore_certificate_errors()
    page = ChromiumPage(addr_or_opts=co,timeout=5)
    return page
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
def ntp_hik_DS2(ip:str, user:str, passwd:str, time=1000):
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

def ntp_Unv(inputs):
    page = init()
    try:
        page.ele("#password").input(inputs['密码'])
        page.ele("@class=login-button").click()
        page._wait_loaded(10)
        page.ele("配置").click('js')
        page._wait_loaded()

        if len(page.eles("#Com_timeCfgLink",timeout=0.6)) > 0:
            page.ele("#Com_timeCfgLink").click()
        else:
            page.ele("#systemCfgLink").click()
            page.ele("#timeCfgTab").click()

        page._wait_loaded()
        if page.ele("#SyncType").attr('defaultvalue') not in "3":
            page.ele("#SyncType").click()
            page.eles("同步NTP服务器时间")[-1].click()
        page.ele("#NTPIPAddr").input(inputs['NTP'])
        page.ele("#NTPSyncInterval").input(inputs['NTP间隔'])
        page.ele("@class=submit_btn").click()
        import time
        time.sleep(1)
    except:
        traceback.print_exc()
        return False
    return True

def ntp_dahua(ip:str, user:str='admin', passwd:str='', time=1200):
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

if __name__ == '__main__':
    ip = '172.16.1.1'
    username = 'admin'
    passwd = '...'
    success = ntp_dahua(ip,username,passwd)
    print(success)
