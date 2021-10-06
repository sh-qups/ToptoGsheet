import os
from utils.gspread_utils import *
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
from time import sleep

json_file = Path(__file__).parent / 'credentials/credentials.json'


def read_date_time_underscore_format1():
    return str(datetime.now().strftime('%H:%M:%S'))


def read_date_time_underscore_format1_plus_6_hours():
    # return str(datetime.now().strftime('%H:%M:%S'))
    return str((datetime.now() + timedelta(hours=6)).strftime('%H:%M:%S'))


def read_date_time_underscore_format():
    return str(datetime.now().strftime('%d-%m-%y_%H-%M-%S'))


def hour_min_time_underscore_format():
    return str(datetime.now().strftime('%H-%M'))


def create_gsheet():
    gsheet_name = f'LR_MCR_{read_date_time_underscore_format()}'
    create_and_share_drive_spreadsheet_for_all_result(gsheet_name, json_file)
    return gsheet_name

# script = os.path.abspath(Path(__file__).parent / 'top.sh')
# subprocess.call(script)

count = 0
gsheet_name = create_gsheet()
for k in range(1, 1000):
    try:
        res = []
        result = []
        command = './top.sh'
        os.system(command)
        command = 'sudo -S iftop -t -s10 -L15 >log1.txt'
        os.system(command)
        myfile = open('log1.txt')
        readcontent = myfile.readlines()
        # bandwidth
        for i in range(len(readcontent)):
            text = readcontent[i]
            if 'Total send rate:' in text or 'Total receive rate:' in text:
                res.append((text.split(':')[-1]).split('    ')[-3])
        # CPU & memory usages
        for i in range(0, 4):
            file1 = open(f'top{i}.txt', 'r')
            Lines = file1.readlines()
            # print('read file')
            if i == 0:
                for li in range(3, 5):
                    # print(Lines[l])
                    result.append([Lines[li][:-2], '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
                result.append(['PID', 'USER', 'PR', 'NI', 'VIRT', 'RES', 'SHR', 'S', '%CPU', '%MEM', 'TIME+', 'COMMAND', 'TIMESTAMP','Input','Output'])
            else:
                # print('extract result')
                for j in range(7, len(Lines)):
                    result_list = (Lines[j].split('\n'))[0].split(' ')
                    result_list = list(filter(lambda a: a != '', result_list))
                    result_list.append(read_date_time_underscore_format1_plus_6_hours())
                    result_list.append(res[1])
                    result_list.append(res[0])
                    result.append(result_list)

        # print(*result, sep='\n')
        # print(len(result))
        # df = pd.DataFrame(result, columns=['PID', 'USER', 'PR', 'NI', 'VIRT', 'RES', 'SHR', 'S', '%CPU', '%MEM', 'TIME+', 'COMMAND'])
        df = pd.DataFrame(result, columns=['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
        # print('collecting done')
        # print(df)
        count = count + 1
        if count >= 100:
            gsheet_name = create_gsheet()
            count = 0
            print('creating worksheet')
        sheetname = hour_min_time_underscore_format()
        create_worksheet(json_file, gsheet_name, f'S{k}_{sheetname}', 10, 15)
        # print('writing data to gsheet')
        write_df_in_sheet(json_file, gsheet_name, f'S{k}_{sheetname}', df)
        print('report_num:', k)
    except:
        continue
    sleep(5)