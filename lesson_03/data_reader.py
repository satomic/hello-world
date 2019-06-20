# coding=utf-8

import os
import common
import xlrd
import pandas as pd

def file_check(file_path):

    if not os.path.exists(file_path):
        err = "%s is not exist" % file_path
        common.print_err(err)
        raise Exception(err)

    if not os.path.isfile(file_path):
        err = "%s is not file" % file_path
        common.print_err(err)
        raise Exception(err)



def reader_text(text_path):
    file_check(text_path)

    lines = []
    with open(text_path, "r", encoding='UTF-8') as f:
        lines = f.readlines()
    return lines


def reader_excel_get_sheet(excel_path, sheet_name=None, sheet_index=None):

    file_check(excel_path)

    excel = xlrd.open_workbook(excel_path)
    sheet_names = excel.sheet_names()

    if sheet_name is not None:
        if sheet_name not in sheet_names:
            err = "%s is not in %s" % (sheet_name, sheet_names)
            common.print_err(err)
            raise Exception(err)
        return excel.sheet_by_name(sheet_name)

    if sheet_index is not None:
        if sheet_index > len(sheet_names) - 1:
            err = "%s is larger then the number of Sheets: %s" % (sheet_index, sheet_names)
            common.print_err(err)
            raise Exception(err)
        return excel.sheet_by_index(sheet_index)

    err = "you must input at least one para of sheet_name or sheet_index"
    common.print_err(err)
    raise Exception(err)


def reader_csv(csv_path):
    file_check(csv_path)
    data = pd.read_csv(csv_path)
    return data

if __name__ == "__main__":

    lines = reader_text("samples/data.txt")
    for line in lines:
        print(line.strip())

    sheet1 = reader_excel_get_sheet("samples/data.xlsx", "Sheet1")
    print(sheet1.row_values(0))
    print(sheet1.row_values(1))
    values = sheet1.row_values(1, start_colx=1, end_colx=7)

    print(reader_csv("samples/data.csv"))