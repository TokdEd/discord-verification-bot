import os
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands
import re
import sqlite3
import logging
import asyncio
# 載入 .env 檔案
load_dotenv()

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 獲取 Token
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# 檢查 Token
if not TOKEN:
    raise ValueError("無效的 Discord Bot Token。請確保 .env 檔案中已正確設置 'DISCORD_BOT_TOKEN'。")

# 創建數據庫連接
def create_connection():
    conn = sqlite3.connect('members.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            school_number TEXT NOT NULL UNIQUE,
            group_name TEXT NOT NULL
        )
    ''')
    conn.commit()
    return conn, c

conn, c = create_connection()

# 分配身份組函數
def assign_group(school_number):
    school_patterns = {
        "a": ("台南女中",  [(311001, 311637), (312001, 312025)]),
        "b": ("台南一中", 310001, 310675),
        "c": ("家齊中學", [(390001, 390069), (310001, 310298), (312001, 312103),(311001, 311107)]),
        "d": ("台南二中", [(311001, 311636), (313001, 313023)])
    }
    
    if len(school_number) < 2:
        return "未知學校"

    prefix = school_number[0].lower()
    try:
        num = int(school_number[1:])
        if prefix in school_patterns:
            school_info = school_patterns[prefix]
            school_name = school_info[0]
            if isinstance(school_info[1], list):  # 多個範圍
                for start, end in school_info[1:][0]:
                    if start <= num <= end:
                        return school_name
            else:  # 單一範圍
                start, end = school_info[1], school_info[2]
                if start <= num <= end:
                    return school_name
    except ValueError:
        pass  # 如果轉換為整數失敗，直接返回未知學校
    
    return "未知學校"
# 創建 bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

class SchoolRegistration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="register", description="登記學號")
    async def register(self, interaction: discord.Interaction, school_number: str):
        try:
        # 檢查學號格式
            if len(school_number) < 2 or school_number[0].lower() not in ['a', 'b', 'c', 'd']:
                await interaction.response.send_message("無效的學號格式。請使用正確的前綴（a/b/c/d）加上學號。")
                return

        # 首先檢查學號是否已被註冊
            c.execute("SELECT * FROM members WHERE school_number = ?", (school_number,))
            if c.fetchone() is not None:
                await interaction.response.send_message(f"學號 {school_number} 已經被註冊！")
                return

            username = str(interaction.user)
            group = assign_group(school_number)
        
            if group == "未知學校":
                await interaction.response.send_message("無效的學號格式或學號範圍，請確保輸入正確的學號。")
                return

            c.execute("INSERT INTO members (username, school_number, group_name) VALUES (?, ?, ?)",
                        (username, school_number, group))
            conn.commit()

            await interaction.response.send_message(f"用戶名 {username} 的學號 {school_number} 已分配到 {group} 組別並記錄到資料庫中。")

            role = discord.utils.get(interaction.guild.roles, name=group)
            if role:
                await interaction.user.add_roles(role)
            else:
                await interaction.followup.send(f"未找到身份組 {group}，請聯繫管理員。")

        except Exception as e:
            logger.error(f"註冊過程中發生錯誤: {e}")
            await interaction.response.send_message("註冊過程中發生錯誤，請稍後再試或聯繫管理員。")

    @app_commands.command(name="check", description="檢查學號組別")
    async def check(self, interaction: discord.Interaction, school_number: str):
        try:
            c.execute("SELECT group_name FROM members WHERE school_number = ?", (school_number,))
            result = c.fetchone()
            if result:
                await interaction.response.send_message(f"{school_number} 属于 {result[0]} 组别。")
            else:
                await interaction.response.send_message(f"學號 {school_number} 未注册。")
        except Exception as e:
            logger.error(f"檢查過程中發生錯誤: {e}")
            await interaction.response.send_message("檢查過程中發生錯誤，請稍後再試或聯繫管理員。")

@bot.event
async def on_ready():
    logger.info(f'已經登入為 {bot.user}')
    try:
        synced = await bot.tree.sync()
        logger.info(f"同步了 {len(synced)} 個指令")
    except Exception as e:
        logger.error(f"同步指令時發生錯誤: {e}")

async def main():
    async with bot:
        await bot.add_cog(SchoolRegistration(bot))
        await bot.start(TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("程序被用戶中斷")
    except Exception as e:
        logger.error(f"程序發生異常: {e}")
    finally:
        logger.info("正在關閉數據庫連接...")
        conn.close()
        logger.info("程序已完全關閉")