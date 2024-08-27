import sqlite3
import xlwt

def db_to_xls(db_file, xls_file):
    # 連接到 SQLite 資料庫
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # 查詢資料庫中的所有表格
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # 創建 .xls 文件
    workbook = xlwt.Workbook()

    for table_name in tables:
        table_name = table_name[0]
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        # 取得欄位名稱
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [column[1] for column in cursor.fetchall()]

        # 在 .xls 文件中創建一個新的工作表
        sheet = workbook.add_sheet(table_name)

        # 寫入欄位名稱
        for col_idx, column_name in enumerate(columns):
            sheet.write(0, col_idx, column_name)

        # 寫入資料
        for row_idx, row in enumerate(rows, start=1):
            for col_idx, cell_value in enumerate(row):
                sheet.write(row_idx, col_idx, cell_value)

    # 保存 .xls 文件
    workbook.save(xls_file)

    # 關閉資料庫連接
    conn.close()

# 使用範例
db_file = 'members.db'  # SQLite 資料庫檔案
xls_file = 'output.xls'  # 輸出的 .xls 檔案
db_to_xls(db_file, xls_file)

