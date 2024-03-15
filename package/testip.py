# -*- coding: utf-8 -*-
import sys
from datetime import datetime
from ipaddress import ip_address
from pathlib import Path
from chardet import detect
from openpyxl import load_workbook
import configparser
import traceback
import subprocess
import locale

ip_list_name = "ip.txt"
result_name = "result.txt"
bad_name = "bad.txt"
ping_relative_path = r'tools\PingInfoView.exe'
name = "专网IP"
input_col = -1  # 自定义IP所在列

def listdir(path):
    directory = Path(path)
    return [file.name for file in directory.iterdir() if file.is_file()]

'''
description: 
param {*} filename
param {*} header_row
return {*}
'''
def is_sheet_empty(sheet):
    return sheet.max_row == 1 and sheet.max_column == 1


'''
description: 
param {*} filename
param {*} sheet
return {*}
'''
def get_ip_row_in_sheet(filename, sheet):
    if is_sheet_empty(sheet):
        return -1
    global name, input_col
    backnames = ['管理服务器','专网地址', '专网IP', '专网ip', '外网IP']
    # 在前四行尝试寻找表头
    max_try_times = 5
    row_generator = sheet.iter_rows(values_only=True)
    while(max_try_times > 0):
        try:
            header_row = next(row_generator)
        except StopIteration:
            return -1
        for back_name in backnames:
            try:
                col = header_row.index(back_name)
                return col
            except ValueError:
                pass
        max_try_times = max_try_times - 1

    return input_col-1


'''
description: 
param {*} files
return {*}
'''
def read_xlsx(files=None):
    data = []
    for fn in files:
        try:
            wb = load_workbook(fn, read_only=True)
        except PermissionError:
            input("文件被占用,无法读取,按任意键退出")
            sys.exit(1)

        for sheet in wb.worksheets:
            col_num = get_ip_row_in_sheet(Path(fn).name, sheet)
            if col_num <= -1:
                continue
            for row in sheet.iter_rows():
                cell_value = row[col_num].value
                if cell_value is not None:
                    try:
                        ip_address(cell_value)
                        #if ip_address(cell_value).is_private == False:
                        data.append(cell_value)
                    except ValueError:
                        pass
    data = list(set(data))  # 去重
    return data


def get_ip_list(xfile, result):
    data = read_xlsx(xfile)
    with open(result, 'w') as f:
        for item in data:
            f.write(f"{item}\n")



def count_lines(filename):
    with open(filename, 'r') as file:
        count = sum(1 for line in file if line.strip())
    return count

'''
description: 
param {*} tool_path
param {*} xfile
param {*} result
return {*}
'''
def call_ping(tool_path, xfile, result, timeout = 5000, size = 4):
    if not Path(result).exists():
        with open(result, 'w') as f:
            f.write('')
    path = Path(tool_path).resolve()
    command = f'{path} /loadfile {xfile} /stab {result} /PingTimeout {timeout} /PingSize {size}'
    print(f'超时IP数{count_lines(xfile)}.')
    process = None
    try:
        #os.system(command)
        process = subprocess.Popen(command, shell=True)
        process.communicate()
    except:
        print("调用失败.")
        traceback.print_exc()
    finally:
        if process is not None and process.poll() is None:
            process.terminate()
            process.wait()

def get_encoding(file):
    # 二进制方式读取，获取字节数据，检测类型
    if Path(file).exists():
        with open(file, 'rb') as f:
            data = f.read()
            return detect(data)['encoding']


'''
description: 
param {*} ip_list
param {*} bad_ip_list
return {*}
'''
def get_bad_ip(ip_list, bad_ip_list):
    with open(ip_list, 'r', encoding=get_encoding(ip_list)) as f:
        lines = f.readlines()
    with open(bad_ip_list, 'w') as f:
        for line in lines:
            parts = line.split()
            if parts[1] == '0':
                f.write(parts[0] + '\n')


'''
description: 
param {*} file_list
param {*} bad_ip
return {*}
'''
def write_result(file_list, ip_file, is_in, not_in):
    for fn in file_list:
        try:
            wb = load_workbook(fn)
        except PermissionError:
            input("文件被占用,无法读取,按任意键退出")
            sys.exit(1)

        for sheet in wb.worksheets:
            col_num = get_ip_row_in_sheet(Path(fn).name, sheet)
            if col_num <= -1:
                continue
            max_col = sheet.max_column
            #new_col = max_col + 1  # 增加 “是否在线” 统计结果列
            new_col = 3
            sheet.cell(row=1, column=new_col).value = datetime.now().strftime("是否在线%m%d %H:%M")

            with open(ip_file, "r") as f:
                ip_list = set(f.read().splitlines())

            for row in range(2, sheet.max_row + 1):
                cell_value = sheet.cell(row=row, column=col_num + 1).value  # sheet.cell 的 column 是从1开始
                try:
                    ip_address(cell_value)
                except ValueError:
                    continue
                #if ip_address(cell_value).is_private == False:
                if cell_value in ip_list:
                    sheet.cell(row=row, column=new_col).value = is_in
                else:
                    sheet.cell(row=row, column=new_col).value = not_in
        wb.save(fn)


def remove_txt():
    file_path = Path.cwd()
    file_ext = '.txt'
    for path in listdir(file_path):
        path_list = Path(file_path).joinpath(Path(path))
        if path_list.is_file():
            if path_list.suffix == file_ext:
                path_list.unlink()  # 删除


'''
description: 对XLSX文件列表,执行IP连通性测试,并回写结果
param {*} file_list
param {*} enter 为True时，需要手动输入按键以结束.
return {*}
'''
def ip_xlsx_test(file_list, ping_timeout, ping_size, times,enter=False):
    get_ip_list(file_list, ip_list_name)
    # 未测试时bad ip为全部ip
    with open(ip_list_name, 'r') as file1, open(bad_name, 'w') as file2:
        file2.write(file1.read())
    # ping重复操作
    print(f'ping设置:超时{ping_timeout}ms,{ping_size}字节')
    while(times > 0):
        call_ping(ping_relative_path, bad_name, result_name, ping_timeout, ping_size)
        get_bad_ip(result_name, bad_name)

        times = times - 1
        print(f'剩余{times}次,',end='')
    # 结果回写
    write_result(file_list, bad_name, "超时", "已通")
    if enter:
        input("操作完成,按任意键退出.")
    remove_txt()

def test_ip(relative_path=''):
    print(Path.cwd())
    locale.setlocale(locale.LC_ALL, 'en_US.utf8')
    config = configparser.ConfigParser()
    config.read('config/ping.ini',encoding="utf-8-sig")

    ping_timeout = config.getint('cfg', 'ping_timeout', fallback=5000)    #ping超时时间
    ping_times = config.getint('cfg', 'ping_times', fallback=15)        #ping尝试次数
    ping_size = 4

    try:
        file_list = [relative_path+f for f in listdir(relative_path) if f.endswith('.xlsx')]
        ip_xlsx_test(file_list, ping_timeout, ping_size, ping_times)
    except Exception:
        traceback.print_exc()
        input("发生异常，按任意键退出.")
        remove_txt()

if __name__ == '__main__':
    test_ip(relative_path=".\数据文件\\")
    sys.exit(0)
