import discord
from discord.ext import commands
import re
import sqlite3
import os
import asyncio
import logging
from dotenv import load_dotenv
load_dotenv()
# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 使用環境變量獲取 Token
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

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
        r"^131\d{4}$": "台南女中",
        r"^231\d{4}$": "台南一中",
        r"^310\d{3}$": "家齊中學",
        r"^312\d{3}$": "家齊職業科",
        r"^431\d{4}$": "台南二中"
    }
    
    for pattern, school in school_patterns.items():
        if re.match(pattern, school_number):
            return school
    return "未知學校"

# 創建 bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

class SchoolRegistration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def register(self, ctx, school_number: str):
        try:
            # 首先檢查學號是否已被註冊
            c.execute("SELECT * FROM members WHERE school_number = ?", (school_number,))
            if c.fetchone() is not None:
                await ctx.send(f"學號 {school_number} 已經被註冊！")
                return

            username = str(ctx.author)
            group = assign_group(school_number)
            
            if group == "未知學校":
                await ctx.send("無效的學號格式，請重新輸入。")
                return

            c.execute("INSERT INTO members (username, school_number, group_name) VALUES (?, ?, ?)",
                      (username, school_number, group))
            conn.commit()

            await ctx.send(f"用戶名 {username} 的學號 {school_number} 已分配到 {group} 組別並記錄到資料庫中。")

            role = discord.utils.get(ctx.guild.roles, name=group)
            if role:
                await ctx.author.add_roles(role)
            else:
                await ctx.send(f"未找到身份組 {group}，請聯繫管理員。")

        except Exception as e:
            logging.error(f"註冊過程中發生錯誤: {e}")
            await ctx.send("註冊過程中發生錯誤，請稍後再試或聯繫管理員。")

@bot.event
async def on_ready():
    logging.info(f'已經登入為 {bot.user}')

async def main():
    async with bot:
        await bot.add_cog(SchoolRegistration(bot))
        await bot.start(TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        conn.close()