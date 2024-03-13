import traceback
import openpyxl
from ipc_hik import *
from pathlib import Path

if __name__ == '__main__':
    user = "admin"
    current_dir = Path.cwd()
    files = [file for file in current_dir.joinpath('./数据文件/').iterdir() if file.is_file()]
    xlsx_file = files[0]
    try:
        wb = openpyxl.load_workbook(xlsx_file)
        ws = wb.active
        for row in range(1, ws.max_row + 1):
            '''
            ip = ws.cell(row=row, column=17).value   # Q列IP
            user = ws.cell(row=row, column=18).value   #user
            passwd = ws.cell(row=row, column=19).value   #passwd
            ipc_type = ws.cell(row=row, column=8).value   #摄像机品牌
            name = ws.cell(row=row, column=4).value   #设备名称
            osd = ws.cell(row=row, column=8).value  #OSD
            '''
            ip = ws.cell(row=row, column=2).value   # Q列IP
            osd4 = ws.cell(row=row, column=1).value  #OSD
            osd3 = ws.cell(row=row, column=3).value  #OSD
            if ws.cell(row=row, column=4).value:
                print(f"{ip}已完成,跳过")
                continue
            #osd = re.sub(r'^\D*?(\d.*)',r'\1',osd2)
            print(osd3,osd4)
            success = change_osd_hik_DS2(ip,'admin','CYpjy123...',osd3,osd4)
            input(f'success={success}按键继续.')
            ws.cell(row=row, column=4).value = success
            #print(ip,"错误计数：",fail_count)
            wb.save(xlsx_file)
        wb.save(xlsx_file)
        wb.close()
    except:
        traceback.print_exc()
        input("操作失败,按键退出")

    print("全部完成")

