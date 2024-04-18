from pathlib import Path
from DrissionPage import ChromiumPage
import traceback
from package.ntp import ntp_Unv

#co = ChromiumOptions(ini_path=r'.\config\web-config.ini')
#so = SessionOptions(ini_path=r'.\config\web-config.ini')
def init():
    from DrissionPage import ChromiumOptions
    co = ChromiumOptions().set_local_port(9222)
    co = co.ignore_certificate_errors()
    page = ChromiumPage(addr_or_opts=co,timeout=5)
    return page

from package.makers import get_maker,get_html
def call_run(inputs):
    try:
        code_steps = [file for file in Path.cwd().joinpath('./steps/').iterdir() if file.is_file() and '~' not in file.name]
        page = init()
        makers = get_maker(get_html(inputs["IP地址"]))
        if "unv" in makers or len(page.eles("自动实况",timeout=3)) > 0:
            print(f"{inputs['IP地址']}为宇视设备",end='')
            status =  ntp_Unv(inputs)
            """for step in code_steps:
                with open(step,'r',encoding='utf-8') as f:
                    step = f.read()
                exec(step)
            """
        else:
            return '跳过'
        page.refresh()
    except:
        traceback.print_exc()
        return False
    return status

if __name__ == '__main__':
    pass