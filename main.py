from package.driver import init
import re
import traceback
import openpyxl
from package.operation import *
from pathlib import Path

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

