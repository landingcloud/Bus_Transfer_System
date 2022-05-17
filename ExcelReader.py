import re
import threading
import openpyxl
ExcelCols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def load_excel(excel_name):
    AllSite = []    #存储所有站点的列表
    wb = openpyxl.load_workbook(excel_name)
    ws = wb["Sheet1"]
    for col in ExcelCols:
        col_content = ws[col]
        if col_content == None:
            break
        for content in col_content:
            content_value = content.value
            if content_value == None:
                break
            matchobj = re.match('([0-9]+)路', content_value)
            if matchobj:
                AllSite.append('*' + content_value)
            else:
                AllSite.append(content_value)
    wb.close()
    return AllSite

if __name__ == "__main__":
    print(load_excel("./公交.xlsx"))
