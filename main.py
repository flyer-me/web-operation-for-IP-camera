import traceback
import openpyxl
from package.ping import *
from pathlib import Path

if __name__ == '__main__':
    user = "admin"
    current_dir = Path.cwd()
    files = [file for file in current_dir.joinpath('./数据文件/').iterdir() if file.is_file()]
    xlsx_file = files[0]
    #test_ip()
    try:
        wb = openpyxl.load_workbook(xlsx_file)
        ws = wb.active
        from operations import *
        for row in range(2, ws.max_row + 1):
            '''
            ip = ws.cell(row=row, column=17).value   # Q列IP
            user = ws.cell(row=row, column=18).value   #user
            passwd = ws.cell(row=row, column=19).value   #passwd
            ipc_type = ws.cell(row=row, column=8).value   #摄像机品牌
            name = ws.cell(row=row, column=4).value   #设备名称
            osd = ws.cell(row=row, column=8).value  #OSD
            '''
            
            if ws.cell(row=row, column=10).value == "不通" or ws.cell(row=row, column=11).value:
                continue
            ip = ws.cell(row=row, column=1).value
            passwd = ws.cell(row=row, column=5).value[:-1]+"..."
            success = change_ntp_dahua(ip=ip,passwd=passwd)
            #success = ntp_hik_DS2(ip,passwd=passwd)
            ws.cell(row=row, column=11).value = success
            print(f'{ip}:{success}')
            wb.save(xlsx_file)
        wb.save(xlsx_file)
        wb.close()
    except:
        traceback.print_exc()
        input("操作失败,按键退出")

    print("全部完成")

