from DrissionPage import ChromiumOptions, SessionOptions, WebPage
import traceback
import time
co = ChromiumOptions(ini_path=r'.\config\web-config.ini')
so = SessionOptions(ini_path=r'.\config\web-config.ini')
page = WebPage(chromium_options=co, session_or_options=so)
# 创建页面对象
#page = SessionPage()

"""
# 获取 id 为 one 的元素
div1 = page.ele('#one')
# 获取 name 属性为 row1 的元素
p1 = page.ele('@name=row1')
# 获取包含“第二个div”文本的元素
div2 = page.ele('第二个div')
# 获取所有div元素
div_list = page.eles('tag:div')
# 获取到一个元素div1
div1 = page.ele('#one')
# 在div1内查找所有p元素
p_list = div1.eles('tag:p')
#下载操作
ele.click.to_download(rename=f'{datetime.date.today()}',)
"""

def ntp_hik_DS2(ip:str, user:str, passwd:str, ntp:str='172.16.1.6'):
    try:
        page.get(f'http://{ip}/doc/page/config.asp')
        page.ele(locator='#username').input(user)
        page.ele(locator='#password').input(passwd)
        page.ele(locator='@type=button').click()
        time.sleep(0.2)
        page.ele(locator='时间配置').click()
        page.ele('#radioNTP').click()
        page.ele('@ng-model=oSettingTimeInfo.szNTPAddress').input(ntp)
        page.ele('@ng-model=oSettingTimeInfo.szNTPInterval').input('120')
        page.ele('保存').click()
        page.ele('@ng-model=oSettingTimeInfo.szNTPInterval').input('60')
        page.ele('保存').click()
        time.sleep(0.3)
    except:
        traceback.print_exc()
        return False
    return True
# 设备型号 DS-2CD7A47HEWD-XZS
def change_osd_hik_DS2(ip:str, user:str, passwd:str, osd3:str,osd4:str):
    try:
        page.get(f'http://{ip}/doc/page/config.asp')
        page.ele(locator='#username').input(user)
        page.ele(locator='#password').input(passwd)
        page.ele(locator='@type=button').click()
        page.ele(locator='图像').click()
        page.ele(locator='OSD设置').click()
        #selects = page.eles('tag:select')
        #selects[7].click()
        #page.ele('ng-model=oOsdParams.OSDSize').click()
        #clicks = page.eles('tag:option')
        #clicks[0].click()
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
    ip = '172.16.x.x'
    username = 'admin'
    passwd = '...'
    osd4 = "085311"
    ntp = ''
    success = ntp_hik_DS2(ip,username,passwd,ntp)
    print(success)
