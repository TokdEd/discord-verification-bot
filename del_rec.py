import sqlite3
import sys

def delete_record(school_number):
    # 連接到數據庫
    conn = sqlite3.connect('members.db')  # 確保這是你的數據庫文件名
    c = conn.cursor()

    try:
        # 檢查記錄是否存在
        c.execute("SELECT * FROM members WHERE school_number = ?", (school_number,))
        if c.fetchone() is None:
            print(f"未找到學號為 {school_number} 的記錄。")
            return

        # 刪除記錄
        c.execute("DELETE FROM members WHERE school_number = ?", (school_number,))
        conn.commit()
        print(f"已成功刪除學號為 {school_number} 的記錄。")

    except sqlite3.Error as e:
        print(f"刪除記錄時發生錯誤: {e}")

    finally:
        # 關閉數據庫連接
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使用方法: python delete_record.py <school_number>")
        sys.exit(1)

    school_number = sys.argv[1]
    delete_record(school_number)