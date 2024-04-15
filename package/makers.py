from page import init

keyAttr_makers = { "ikvision":"hik",
                   "iconDH-logo":"dahua-new",
                   "login-logo-dhtech":"dahua-old",
                   "华为":"huawei",
                   "自动实况":"unv"

}

def get_html(ip:str='127.0.0.1') ->str:
    page = init()
    page.get(f'http://{ip}')
    return page.html

def get_maker(html:str)->str:
    for key in keyAttr_makers.keys():
        if key in html:
            return keyAttr_makers[key]
    return None



if __name__ == '__main__':
    #ip = '172.16.15.120'
    #ip = '172.16.11.134'
    ip = '172.16.14.176'
    username = 'admin'
    passwd = '...'
    success = get_maker(get_html(ip,username,passwd))
    print(success)