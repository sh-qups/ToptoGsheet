import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path

# json_file = Path(__file__).parent.parent / 'credentials/credentials2.json'


def get_authorized_client(credential_file):
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credential_file, scopes)  # access the json key you downloaded earlier
    return gspread.authorize(credentials)


def open_spreadsheet_by_filename(file, filename):
    return file.open(filename)


# client = get_authorized_client(json_file)
# sheet = open_spreadsheet_by_filename(client, 'test')


def open_spreadsheet_by_file_id(client, key):
    return client.open_by_key(key)


def open_spreadsheet_by_file_url(client, url):
    return client.open_by_url(url)


def create_spreadsheet(client, filename):
    client.create(filename)


def share_spreadsheet(client, email, permission_type, role_type, notify_option):
    # permission type user, group,domain,anyone
    # role type owner, writer,reader
    client.share(email, perm_type=permission_type, role=role_type, notify=notify_option)


def share_spreadsheet_with_details(client, email, permission_type, role_type, notify_option, email_message, with_link):
    client.share(email, perm_type=permission_type, role=role_type, notify=notify_option, email_message=email_message,
                 with_link=with_link)


def get_sheet_id(client):
    return client.id


def get_list_of_all_worksheets(gsheet):
    return gsheet.worksheets()


def select_worksheet_by_index(gsheet, index):
    return gsheet.get_worksheet(index)


def select_worksheet_by_name(gsheet, name):
    return gsheet.worksheet(name)


def create_worksheet(gsheet, title, rows, cols):
    worksheet = gsheet.add_worksheet(title=title, rows=rows, cols=cols)
    return worksheet


def delete_worksheet(gsheet, worksheet):
    gsheet.del_worksheet(worksheet)


def get_cell_value(worksheet, row_number, col_number):
    return worksheet.cell(row_number, col_number).value


def get_cell_value_A1_notation(worksheet, a1_notation):
    return worksheet.acell(a1_notation).value


def get_cell_formula(worksheet, row_number, col_number):
    return worksheet.cell(row_number, col_number, value_render_option='FORMULA').value


def get_cell_formula_a1_notation(worksheet, cell_a1_notation):
    return worksheet.acell(cell_a1_notation, value_render_option='FORMULA').value


def get_single_row_value(worksheet, row_number):
    return worksheet.row_values(row_number)


def get_single_col_value(worksheet, col_number):
    return worksheet.col_values(col_number)


def get_all_values_as_list_of_list(worksheet):
    return worksheet.get_all_values()


def get_all_values_as_list_of_dictionaries(worksheet):
    return worksheet.get_all_records()


def find_cell_by_value(worksheet, value):
    cell = worksheet.find(value)
    return cell


def find_all_matched_cells_by_value(worksheet, value):
    cell_list = worksheet.findall(value)
    return cell_list


def clear_cells(worksheet, list1):
    # list ["A1:B1", "C2:E2", "my_named_range"]
    worksheet.batch_clear(list1)


def clear_whole_sheet(worksheet):
    worksheet.clear()


def update_cell(worksheet, row_number, col_number, update_value):
    worksheet.update_cell(row_number, col_number, update_value)


def update_cell_a1_notation(worksheet, cdll_a1_notation, update_value):
    worksheet.update(cdll_a1_notation, update_value)


def update_range_values(worksheet, range1, value):
    # range 'A1:B2', [[1, 2], [3, 4]]
    worksheet.update(range1, value)


def bold_text(worksheet, range1):
    worksheet.format(range1, {'textFormat': {'bold': True}})


def change_font_size(worksheet, range1, font_size):
    worksheet.format(range1, {'textFormat': {'fontSize': font_size}})


def change_text_color(worksheet, range1, red, green, blue):
    worksheet.format(range1, {'foregroundColor': {"red": red, "green": green, "blue": blue}})


def change_background_color(worksheet, range1, red, green, blue):
    worksheet.format(range1, {"backgroundColor": {"red": red, "green": green, "blue": blue}})


def change_alignment(worksheet, range1, alignment_type, alignment_position):
    # "horizontalAlignment": "CENTER",
    # print(f'"{alignment_type}": "{alignment_position}"')
    # sheet.format(range1, {f'"{alignment_type}": "{alignment_position}"'})
    worksheet.format(range1, {"horizontalAlignment": "CENTER"})


def freeze_cells(worksheet, rows=None, cols=None):
    worksheet.freeze(rows, cols)


def write_dataframe_in_sheet(dataframe, worksheet):
    worksheet.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())


def max_col(worksheet, row_num):
    return len(worksheet.row_values(row_num))


def max_row(worksheet, col_num):
    return len(worksheet.col_values(col_num))


def max_row_with_empty_row(worksheet):
    return worksheet.row_count


def max_col_with_empty_col(worksheet):
    return worksheet.col_count


def max_row_col(worksheet):
    max_rows = len(
        worksheet.get_all_values())  # this is a list of all data and the length is equal to the number of rows including header row if it exists in data set
    max_cols = len(worksheet.get_all_values()[0])
    # print(max_rows, max_cols)
    return max_rows, max_cols


def delete_rows(worksheet, row_num):
    worksheet.delete_rows(row_num)


def delete_cols(worksheet, col_num):
    worksheet.delete_columns(col_num)


def resize_sheet(worksheet, row_num, col_num):
    worksheet.resize(row_num, col_num)


# Pandas function

def read_sheet_pandas(sheet_name):
    dataframe = pd.DataFrame(sheet_name.get_all_rocords())
    return dataframe


def read_excel_pandas(file_name):
    dataframe = pd.read_excel(file_name)
    return dataframe


def read_excel_sheet_by_index_pandas(file_name, index):
    dataframe = pd.read_excel(file_name, sheet_name=index)
    return dataframe


def read_excel_sheet_by_sheet_name_pandas(file_name, sheet_name):
    dataframe = pd.read_excel(file_name, sheet_name=sheet_name)
    return dataframe


def write_df_in_sheet(json_file, gsheet, sheet_name, dataframe):
    client = get_authorized_client(json_file)
    gsheet = open_spreadsheet_by_filename(client, gsheet)
    worksheet = select_worksheet_by_name(gsheet, sheet_name)
    worksheet.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())


def create_and_share_drive_spreadsheet_for_all_result(spreadsheet_name, json_file):
    client = get_authorized_client(json_file)
    create_spreadsheet(client, spreadsheet_name)
    spreadsheet = open_spreadsheet_by_filename(client, spreadsheet_name)
    spreadsheet.share('project.task.ax@gmail.com', perm_type='user', role='owner')
