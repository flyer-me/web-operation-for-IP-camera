from package.driver import By, Keys, _click, _get_attribute_of_element, init
import re
import time
import traceback
import openpyxl
from pathlib import Path


# 适用于华为人卡 车卡
def login_type_hw(driver,url,user,passwd):
    driver.get(url)
    """inputs = driver.find_elements(by=By.TAG_NAME,value="input")
    user_input = inputs[0]
    passwd_input = inputs[1]"""
    user_input = driver.find_element(by=By.CSS_SELECTOR,value="#loginUserName")
    passwd_input = driver.find_element(by=By.CSS_SELECTOR,value="#loginPwd")
    user_input.send_keys(user)  
    passwd_input.send_keys(passwd)
    _click(driver,"//*[text()='登录']")
    return driver
# 华为人卡
def get_type_hw_r(driver):
    try:
        _click(driver,"button",by=By.TAG_NAME)
    except:
        try:
            _click(driver,"//*[text()='确定']")
        except:
            print("不需要跳过 或跳过失败.")

    try:
        _click(driver,"#menu_setting > a",by=By.CSS_SELECTOR)
    except:
        _click(driver,"#setting > a > i",by=By.CSS_SELECTOR)
    _click(driver,"//*[text()='音视图']")
    _click(driver,"//*[text()='OSD参数']")
    osd = ""
    '''if _get_attribute(driver,"osd_item_content_id0").find("北京") !=-1:
        osd = _get_attribute(driver,"osd_item_content_id0")
    elif _get_attribute(driver,"osd_item_content_id1").find("北京") !=-1:
        osd = _get_attribute(driver,"osd_item_content_id1")
    elif _get_attribute(driver,"osd_item_content_id2").find("北京") !=-1:
        osd = _get_attribute(driver,"osd_item_content_id2")
    elif _get_attribute(driver,"osd_item_content_id3").find("北京") !=-1:
        osd = _get_attribute(driver,"osd_item_content_id3")'''
    element = driver.find_element(By.XPATH,"//div[contains(text(),'人')]")
    osd = _get_attribute_of_element(element)
    return osd
# 华为车卡
def get_type_hw_c(driver):
    #_click(driver,"skipBtnID",by=By.ID)
    try:
        _click(driver,"button",by=By.TAG_NAME)
    except:
        try:
            _click(driver,"//*[text()='确定']")
        except:
            print("不需要跳过 或跳过失败.")
    try:
        _click(driver,"#menu_setting > a",by=By.CSS_SELECTOR)
    except:
        _click(driver,"#setting > a > i",by=By.CSS_SELECTOR)
    
    _click(driver,"//*[text()='音视图']")
    time.sleep(0.8)
    _click(driver,"//*[text()='OSD参数']")
    osd = ""
    element = driver.find_element(By.XPATH,"//div[contains(text(),'车')]")
    osd = _get_attribute_of_element(element)
    '''elements = driver.find_elements(By.CLASS_NAME,"anyway-table-textdisplay")
    for element in elements:
        if _get_attribute_of_element(element).find("车") !=-1:
            osd = _get_attribute_of_element(element)'''
    return osd
# 适用于宇视人卡 车卡
def login_type_unv(driver,url,user,passwd):
    driver.get(url)
    driver.switch_to.frame(driver.find_element(by=By.ID,value="banner"))
    passwd_input = driver.find_element(by=By.CSS_SELECTOR,value="#password")
    passwd_input.send_keys(passwd)
    _click(driver,"//*[text()='登录']")
    return driver
# 宇视人卡
def get_type_unv_r(driver):
    _click(driver,"//*[text()='配置']")
    try:
        _click(driver,"//*[text()='OSD']")
    except:
        _click(driver,"//*[text()='常用']")
        _click(driver,"//*[text()='OSD']")
    #osd2 = _get_attribute(driver,"osdInfoLabel5")
    element = driver.find_element(By.XPATH,"//div[contains(text(),'人')]")
    osd2 = _get_attribute_of_element(element)
    return osd2
# 宇视车卡
def get_type_unv_c(driver):
    _click(driver,"//*[text()='配置']")
    _click(driver,"//*[text()='OSD']")
    #element = driver.find_element(By.XPATH,"//div[contains(text(),'车')]")
    element = driver.find_element(By.ID,"osdInfoLabel4")
    osd2 = _get_attribute_of_element(element)
    return osd2

# 适用于海康人卡 车卡
def login_type_hk(driver,url,user,passwd):
    driver.get(url)
    inputs = driver.find_elements(by=By.TAG_NAME,value="input")
    user_input = inputs[0]
    passwd_input = driver.find_element(by=By.CSS_SELECTOR,value="#password")
    user_input.send_keys(user)
    passwd_input.send_keys(passwd)
    passwd_input.send_keys(Keys.ENTER)
    return driver
# 海康车卡 人卡
def get_type_hk_(driver):
    #_click(driver,"//*[text()='配  置']")
    _click(driver,"//*[text()='图像']")
    try:
        _click(driver,"//*[text()='显示设置']")
        time.sleep(6)
        _click(driver,"//*[text()='OSD设置']")
        elements = driver.find_elements(By.XPATH,"/html/body/div[4]/div[1]/div/div/div[2]/div/div[1]/div[3]/span[3]/div[16]/div/span[2]/input")
    except:
        _click(driver,"//*[text()='显示设置']")
        time.sleep(5)
        _click(driver,"//*[text()='OSD设置']")
        elements = driver.find_elements(By.XPATH,"/html/body/div[4]/div[1]/div/div/div[2]/div/div[1]/div[3]/span[3]/div[16]/div/span[2]/input")
    element = elements[-1]
    osd2 = _get_attribute_of_element(element,"value")
    return osd2

def get_OSD(type_ipc,user,passwd):
    osd2 = None
    if type_ipc == "华为人卡":
        driver = login_type_hw(driver,f"https://{ip}/",user,passwd)
        osd2 = get_type_hw_r(driver)
    elif type_ipc == "华为车卡":
        driver = login_type_hw(driver,f"https://{ip}/",user,passwd)
        osd2 = get_type_hw_c(driver)
    elif type_ipc == "宇视人卡":
        driver = login_type_unv(driver,f"http://{ip}/",user,passwd)
        osd2 = get_type_unv_r(driver)
    elif type_ipc == "宇视车卡":
        driver = login_type_unv(driver,f"http://{ip}/",user,passwd)
        osd2 = get_type_unv_c(driver)
    elif type_ipc =="海康车卡" or type_ipc =="海康人卡":
        driver = login_type_hk(driver,f"http://{ip}/doc/page/config.asp",user,passwd)
        osd2 = get_type_hk_(driver)
    else:
        pass
    return osd2
if __name__ == '__main__':
    user = "admin"
    current_dir = Path.cwd()
    files = [file.name for file in current_dir.iterdir() if file.is_file()]
    try:
        xlsx_file = [file for file in files if file.endswith(".xlsx")][0]
        wb = openpyxl.load_workbook(xlsx_file)
        ws = wb.active
        for row in range(2, ws.max_row + 1):
            try:
                ip = ws.cell(row=row, column=2).value   # B列IP
                type1 = ws.cell(row=row, column=4).value   #卡口类型
                type2 = ws.cell(row=row, column=5).value   #厂商
                passwd = ws.cell(row=row, column=6).value   #密码
                osd = ws.cell(row=row, column=8).value  #OSD
                if ws.cell(row=row, column=8).value is not None or str(ws.cell(row=row, column=7).value) == "1":
                    print("跳过")
                    continue
                if ws.cell(row=row, column=9).value == 0 :
                    continue
                fail_count = 0
                driver = init()
                type_ipc = str(type2) + str(type1)
                print(f"{type_ipc} {user},{passwd} http://{ip}/")
                osd2 = get_OSD(type_ipc,user,passwd)
                driver.quit()
                osd = re.sub(r'^\D*?(\d.*)',r'\1',osd2)
                print("OSD叠加最后一行:\n",osd)
                ws.cell(row=row, column=8).value = osd
                ws.cell(row=row, column=9).value = fail_count #F列
            except:
                print("操作失败")
                traceback.print_exc()
                fail_count = -1
                ws.cell(row=row, column=9).value = fail_count #F列
            #print(ip,"错误计数：",fail_count)
            wb.save(xlsx_file)
        wb.save(xlsx_file)
        wb.close()
    except:
        traceback.print_exc()
        input("操作失败,按键退出")

    print("全部完成")

