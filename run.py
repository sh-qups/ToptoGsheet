import subprocess
import os
from utils.gspread_utils import *
from datetime import datetime
from pathlib import Path
import pandas as pd
from time import sleep

json_file = Path(__file__).parent / 'credentials/credentials.json'


def read_date_time_underscore_format1():
    return str(datetime.now().strftime('%d-%m_%H:%M:%S'))


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
for k in range(1, 3):
    count = count + 1
    try:
        result = []
        for i in range(0, 3):
            print('started collecting')
            # subprocess.run(["./top.sh"], shell=True)
            # subprocess.call(["./top.sh"])
            command = './top.sh'
            os.system(command)
            print('executed top command')
            file1 = open(f'top{i}.txt', 'r')
            Lines = file1.readlines()
            print('read file')
            # if i == 0:
            #     for l in range(3, 5):
            #         # print(Lines[l])
            #         result.append([Lines[l][:-2], '', '', '', '', '', '', '', '', '', '', '', ''])
            #     result.append(['PID', 'USER', 'PR', 'NI', 'VIRT', 'RES', 'SHR', 'S', '%CPU', '%MEM', 'TIME+', 'COMMAND', 'TIMESTAMP'])
            # else:
            print('extract result')
            for j in range(7, len(Lines)):
                result_list = (Lines[j].split('\n'))[0].split(' ')
                result_list = list(filter(lambda a: a != '', result_list))
                result.append(result_list)
                # result.append(read_date_time_underscore_format1())
        print(*result, sep='\n')
        # print(len(result))
        df = pd.DataFrame(result, columns=['PID', 'USER', 'PR', 'NI', 'VIRT', 'RES', 'SHR', 'S', '%CPU', '%MEM', 'TIME+', 'COMMAND'])
        # df = pd.DataFrame(result, columns=['', '', '', '', '', '', '', '', '', '', '', '', ''])
        print('collecting done')
        # print(df)
        # if count == 100:
        #     gsheet_name = create_gsheet()
        #     count = 0
        # print('creating worksheet')
        sheetname = hour_min_time_underscore_format()
        create_worksheet(json_file, gsheet_name, f'S{k}_{sheetname}', 10, 15)
        # print('writing data to gsheet')
        write_df_in_sheet(json_file, gsheet_name, f'S{k}_{sheetname}', df)
        print('report_num:', k)
    except:
        continue
    sleep(5)
