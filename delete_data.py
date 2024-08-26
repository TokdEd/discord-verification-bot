import sqlite3

def delete_data(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # 删除所有数据
    c.execute("DELETE FROM members")
    conn.commit()

    conn.close()
    print("数据已成功删除。")

if __name__ == "__main__":
    db_path = 'members.db'  # 你的数据库路径
    delete_data(db_path)
