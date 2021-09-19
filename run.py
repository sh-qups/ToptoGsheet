import subprocess
import os
from utils.gspread_utils import *
from datetime import datetime
from pathlib import Path
import pandas as pd
from time import sleep

json_file = Path(__file__).parent / 'credentials/credentials.json'


def read_date_time_underscore_format():
    return str(datetime.now().strftime('%d-%m-%y_%H-%M-%S'))


def hour_min_time_underscore_format():
    return str(datetime.now().strftime('%H-%M'))


def create_gsheet():
    gsheet_name = f'LR_MCR_{read_date_time_underscore_format()}'
    create_and_share_drive_spreadsheet_for_all_result(gsheet_name, json_file)
    return gsheet_name


script = os.path.abspath(Path(__file__).parent / 'top.sh')
subprocess.call(script)

gsheet_name = ''
for k in range(1, 5000):
    result = []
    for i in range(0, 5):
        file1 = open(f'top{i}.txt', 'r')
        Lines = file1.readlines()
        if i == 0:
            for l in range(3, 5):
                # print(Lines[l])
                result.append([Lines[l][:-2], '', '', '', '', '', '', '', '', '', '', ''])
            result.append(['PID', 'USER', 'PR', 'NI', 'VIRT', 'RES', 'SHR', 'S', '%CPU', '%MEM', 'TIME+', 'COMMAND'])
        else:

            for j in range(7, len(Lines)):
                result_list = (Lines[j].split('\n'))[0].split(' ')
                result_list = list(filter(lambda a: a != '', result_list))
                result.append(result_list)
    # print(*result, sep='\n')
    # print(len(result))
    # df = pd.DataFrame(result, columns=['PID', 'USER', 'PR', 'NI', 'VIRT', 'RES', 'SHR', 'S', '%CPU', '%MEM', 'TIME+', 'COMMAND'])
    df = pd.DataFrame(result, columns=['', '', '', '', '', '', '', '', '', '', '', ''])
    # print(df)
    if k == 1:
        gsheet_name = create_gsheet()
    create_worksheet(json_file, gsheet_name, f'S{k}_{hour_min_time_underscore_format()}', 1000, 26)
    write_df_in_sheet(json_file, gsheet_name, f'S{k}_{hour_min_time_underscore_format()}', df)
    print('report_num:', k)
    sleep(5)
