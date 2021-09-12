import os
from utils.gspread_utils import *
from datetime import datetime
from pathlib import Path

json_file = Path(__file__).parent / 'Test/credentials/credentials.json'


def read_date_time_underscore_format():
    return str(datetime.now().strftime('%d-%m_%H-%M-%S'))


# command = 'top -b -n 1 > top.txt'
# os.system(command)

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
gsheet_name = f'Top_{read_date_time_underscore_format()}'
create_and_share_drive_spreadsheet_for_all_result(gsheet_name, json_file)
write_df_in_sheet(json_file, gsheet_name, 'Sheet1', df)
