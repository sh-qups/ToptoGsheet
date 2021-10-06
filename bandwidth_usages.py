# import openpyxl
import os
# import pygsheets
import pandas as pd

command = 'sudo -S iftop -t -s10 -L15 >log1.txt'
os.system(command)
# time.sleep(3)

sudoPassword = 'asdfgh'
command = 'mount -t vboxsf myfolder /home/myuser/myfolder'
p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))


myfile = open('log1.txt')
readcontent = myfile.readlines()

res = []
for i in range(len(readcontent)):
        text = readcontent[i]
        # print(text)
        if 'Total send rate:' in text or 'Total receive rate:' in text:
                res.append((text.split(':')[-1]).split('    ')[-3])

print(res)

# myfile = open('log1.txt')
# readcontent = myfile.readlines()
#
# # res = []
# # for i in range(10, 12):
# #         text = readcontent[i]
# #         print(text)
# #         res.append((text.split(':')[-1]).split('    ')[-3])

#print(len(res), res)
# wb = openpyxl.Workbook()
#
# sheet = wb.active
#
# c1 = sheet.cell(row=1, column=1)
# #writing values to cells
# c1.value = 'Input'
#
# c2 = sheet.cell(row=1, column=2)
# c2.value = 'Output'
#
# c3 = sheet.cell(row=2, column=1)
# c3.value = res[1]
#
# c4 = sheet.cell(row=2, column=2)
# #writing values to cells
# c4.value = res[0]


# wb.save('/home/project/PycharmProjects/ReadData/saveddata.xlsx')

# #authorization
# gc = pygsheets.authorize(service_file='/home/project/Downloads/credentials.json')
#
# # Create empty dataframe
# df = pd.DataFrame()
#
# # Create a column
# df['name'] = ['John', 'Steve', 'Sarah']
#
# #open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
# sh = gc.open('ParsedData')
#
# #select the first sheet
# wks = sh[0]
#
# #update the first sheet with df, starting at cell B2.
# wks.set_dataframe(df,(1,1))



# import pygsheets
# import pandas as pd
# #authorization
# gc = pygsheets.authorize(service_file='/home/project/PycharmProjects/ReadData/credentials/cred.json')
# new_sheet = gc.sheet.create('PassedData3')
# sh = gc.open('PassedData3')
# sh.share('reza.qups@gmail.com', role='writer')
#
#
# # Create empty dataframe
# df = pd.DataFrame()
#
# # Create a column
# df['name'] = ['John']
#
# #select the first sheet
# wks = sh[0]
# #update the first sheet with df, starting at cell B2.
# wks.set_dataframe(df, (1, 1))