import openpyxl



wb = openpyxl.load_workbook("D://ab.xlsx")
print(wb)
wa = wb.active
wa.append([11,22,44,"ttu"])
wb.save("D://ab.xlsx")
wb.close()


