import os
from utils.gspread_utils import *
from datetime import datetime
from pathlib import Path
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


gsheet_name = ''
for j in range(1, 5):
    command = 'top -b -n 1 > top.txt'
    os.system(command)
    # txt to df
    file1 = open('top.txt', 'r')
    Lines = file1.readlines()
    result = []
    for i in range(7, len(Lines)):
        result_list = (Lines[i].split('\n'))[0].split(' ')
        result_list = list(filter(lambda a: a != '', result_list))
        result.append(result_list)
    df = pd.DataFrame(result, columns=['PID', 'USER', 'PR', 'NI', 'VIRT', 'RES', 'SHR', 'S', '%CPU', '%MEM', 'TIME+', 'COMMAND'])
    # upload to g_sheet
    if j == 1:
        gsheet_name = create_gsheet()
    create_worksheet(json_file, gsheet_name, f'S{j}_{hour_min_time_underscore_format()}', 1000, 26)
    write_df_in_sheet(json_file, gsheet_name, f'S{j}_{hour_min_time_underscore_format()}', df)
    print('report_num:', j)
    # sleep(3000)
