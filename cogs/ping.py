import discord
from discord import app_commands
from discord.ext import commands
import sqlite3

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def check_membership(self, interaction: discord.Interaction):
        db = sqlite3.connect('data.db')
        cur = db.cursor()
        cur.execute("SELECT agreed FROM terms WHERE user_id = ?", (interaction.user.id,))
        result = cur.fetchone()
        db.close()
        
        if not result or result[0] != 1:
            embed = discord.Embed(
                title="⛔ 권한 없음",
                description="비트의 명령어를 사용하려면 먼저 `/서비스가입`을 완료해야 합니다.",
                color=0xFF0000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return False
        return True

    @app_commands.command(name="핑", description="봇의 응답 속도를 확인합니다.")
    async def ping(self, interaction: discord.Interaction):
        # 1. 가입 여부 체크
        if not await self.check_membership(interaction):
            return

        latency = round(self.bot.latency * 1000) 
        
        embed = discord.Embed(
            title="🏓 퐁! (Pong!)",
            description=f"현재 비트의 응답 속도는 **{latency}ms** 입니다.",
            color=0x2ecc71
        )
        embed.set_footer(text=f"요청자: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Ping(bot))