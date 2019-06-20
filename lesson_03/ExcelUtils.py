# coding=utf-8

import os
import xlrd
import xlwt
from datetime import date,datetime
import traceback
from xlutils.copy import copy


"""
operations on sheet:

sheet.name  

sheet.nrows # number of rows
sheet.ncols # number of columns

sheet.row_values(row_index)
sheet.col_values(col_index)

# get cell value and decode it
sheet.cell(1, 0).value.encode('utf-8')
sheet.cell_value(1, 0).encode('utf-8')
sheet.row(1)[0].value.encode('utf-8')

# get datatype of one cell
sheet.cell(1, 0).ctype

"""


class Excel(object):

    def __init__(self, excel_file):
        self.excel = xlrd.open_workbook(excel_file)
        self.sheet_names = self.excel.sheet_names()

    def get_sheet(self, sheet_name):
        """
        :param sheet_name: identify a sheet by a index/name
        :return: sheet object
        """
        try:
            if isinstance(sheet_name, int):
                return self.excel.sheet_by_index(sheet_name)
            if isinstance(sheet_name, str):
                if sheet_name in self.sheet_names:
                    return self.excel.sheet_by_name(sheet_name)
                else:
                    print("sheet name: %s does not exist in excel file" % (sheet_name))
        except Exception as e:
            print(traceback.format_exc(e))
            return None

def find_left_index(iter, value):
    for i in range(len(iter)-1):
        if iter[i] <= value and iter[i+1] > value:
            # print iter[i], iter[i+1]
            return i
    return -1

def find_all_index(iter, value, cursor=0):
    ret = []
    for i in range(len(iter)):
        if iter[i] == value:
            ret.append(i + cursor)
    return ret

def get_intersection(l1, l2):
    if l1 == -1 or l2 == -1:
        return -1
    difference = list(set(l1).intersection(set(l2)))
    if len(difference) == 0:
        return -1
    elif len(difference) == 1:
        return difference[0]
    else:
        raise Exception("multi row indexs are got, this is illegal")


class Sheet(object):

    def __init__(self, excel, sheet_name):
        if isinstance(excel, str):
            if os.path.exists(excel):
                excel = Excel(excel)
            else:
                raise Exception("excel file: %s is not exists" % excel)
        self.sheet = excel.get_sheet(sheet_name)

    def row_values(self, index):
        return self.sheet.row_values(index)

    def col_values(self, index):
        return self.sheet.col_values(index)

    def get_col_index_by_value(self, value, key_row_index=0, cursor=4):
        row_values = self.sheet.row_values(key_row_index)[cursor:]
        return find_left_index(row_values, value) + cursor
        # if value not in row_values:
        #     return -1
        #     raise Exception("value: %s does not in the key row" % value)
        # return row_values.index(value)

    def get_row_index_by_value(self, value, key_col_index=0, cursor=3):
        col_values =  self.sheet.col_values(key_col_index)[cursor:]

        # print len(col_values),col_values
        # print value

        if value not in col_values:
            return -1
            raise Exception("value: %s does not in the key col" % value)
        # return col_values.index(value) + cursor
        return find_all_index(col_values, value, cursor)


    # def write_cell(self, row, col, value):
    #     xlwt.


class Updater(object):

    def __init__(self, excel_file):
        wb = xlrd.open_workbook(excel_file)
        self.excel = copy(wb)
        self.sheet = None

    def set_sheet(self, sheet_index):
        self.sheet = self.excel.get_sheet(sheet_index)

    def update(self, row, col, value):
        self.sheet.write(row, col, value)

    def save(self, file_name):
        self.excel.save(r"%s.xls" % file_name)



if __name__ == "__main__":

    original_excel = r"TIbacklog20180713.xlsx"
    final_sheet_tamplate_file = r"final_sheet_tamplate.xls"

    # load original data
    original_sheet = Sheet(original_excel, 1)
    material = original_sheet.col_values(6)
    open_qty = original_sheet.col_values(12)
    esd = original_sheet.col_values(14)
    # esd = ["%s/%02d/%02d" % xlrd.xldate_as_tuple(t, 0)[0:3] if not isinstance(t, basestring) else t for t in esd]
    esd = ["%s/%02d/%02d" % xlrd.xldate_as_tuple(t, 0)[0:3] if not isinstance(t, str) else t for t in esd]
    sloc = original_sheet.col_values(20)
    original_datas = zip(material, open_qty, esd, sloc)

    # config target sheet
    csv_content = "good,material,open_qty,esd,sloc\n"
    bad_counter = 0
    counter = 1
    qty_map = {}
    middle_sheet = Sheet(final_sheet_tamplate_file, 1)
    for data in original_datas[1:]:

        col = middle_sheet.get_col_index_by_value(data[2],key_row_index=0)
        rows_material = middle_sheet.get_row_index_by_value(data[0], key_col_index=2, cursor=3)
        rows_sloc = middle_sheet.get_row_index_by_value(data[3], key_col_index=1, cursor=3)
        # row = middle_sheet.get_row_index_by_value(data[0],key_col_index=2)
        # print rows_material, rows_sloc, col
        row = get_intersection(rows_material, rows_sloc)


        if row == -1:
            print("%s, %s, %s, can not find suitable cell in tamplate" % (data[0], data[3], data[2]))
            csv_content += "%s,%s,%s,%s,%s\n" % ("false",data[0],data[1],data[2],data[3])
            bad_counter += 1
            continue

        # print data,"\t",col,row
        key = (row, col)
        if key in qty_map:
            qty_map[key] += data[1]
        else:
            qty_map[key] = data[1]
        print("%s, %s, %s, %s, info added"  % (data[0], data[3], data[2], data[1]))
        csv_content += "%s,%s,%s,%s,%s\n" % ("true", data[0], data[1], data[2], data[3])
        counter += 1

    # save to a tamplate file
    updater = Updater(final_sheet_tamplate_file)
    updater.set_sheet(1)
    for key,value in qty_map.items():
        print(key, value)
        updater.update(key[0], key[1], value)

    import datetime
    nowTime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    updater.save("result_%s" % nowTime)

    with open("log_%s.csv" % nowTime, "w") as f:
        f.write(csv_content)

    print("%s bad info, %s good info" % (bad_counter, counter))

