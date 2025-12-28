import discord
from discord.ext import commands, tasks
import os
import sqlite3
from dotenv import load_dotenv
import itertools

load_dotenv()

class BitBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)
        
        self.conn = sqlite3.connect('data.db')
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS terms (user_id INTEGER PRIMARY KEY, agreed INTEGER)")
        self.conn.commit()

        self.status_cycle = None

    async def setup_hook(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
        await self.tree.sync()

    async def on_ready(self):
        print(f'{self.user.name} 로그인 완료!')
        server_count = len(self.guilds)
        user_count = sum(guild.member_count for guild in self.guilds)
        
        self.status_cycle = itertools.cycle([
            f"현재 {server_count}개의 서버에서 일하는중..",
            f"{user_count}명에게 정보를 전달하는중.."
        ])
        
        if not self.change_status.is_running():
            self.change_status.start()

    @tasks.loop(seconds=10)
    async def change_status(self):
        if self.status_cycle:
            current_status = next(self.status_cycle)
            await self.change_presence(activity=discord.Game(name=current_status))

bot = BitBot()
bot.run(os.getenv('DISCORD_TOKEN'))