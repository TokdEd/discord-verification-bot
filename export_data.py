import sqlite3
import pandas as pd

def export_data_to_excel(db_path, output_excel):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # 查询所有数据
    c.execute("SELECT username, school_number, group_name FROM members")
    rows = c.fetchall()

    # 创建 Pandas DataFrame
    df = pd.DataFrame(rows, columns=["Username", "School Number", "School"])

    # 将 DataFrame 保存为 Excel 文件
    df.to_excel(output_excel, index=False)

    conn.close()
    print(f"数据已成功导出到 {output_excel}")

if __name__ == "__main__":
    db_path = 'members.db'  # 你的数据库路径
    output_excel = 'members_export.xlsx'  # 导出的 Excel 文件路径
    export_data_to_excel(db_path, output_excel)
