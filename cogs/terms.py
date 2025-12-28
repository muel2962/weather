import discord
from discord import app_commands
from discord.ext import commands
import sqlite3

class AgreementView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(label="이용약관 보기", url="http://예시입니다.com")) 

    @discord.ui.button(label="동의하고 가입하기", style=discord.ButtonStyle.green, custom_id="agree_button")
    async def agree(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = sqlite3.connect('data.db')
        cur = db.cursor()
        
        cur.execute("SELECT agreed FROM terms WHERE user_id = ?", (interaction.user.id,))
        if cur.fetchone():
            db.close()
            return await interaction.response.send_message("이미 서비스에 가입되어 있습니다!", ephemeral=True)

        cur.execute("INSERT INTO terms (user_id, agreed) VALUES (?, ?)", (interaction.user.id, 1))
        db.commit()
        db.close()

        embed = discord.Embed(
            title="✅ 서비스 가입 완료",
            description=f"{interaction.user.mention}님, 환영합니다! 이제 모든 기능을 사용하실 수 있습니다.",
            color=0x00ff00
        )
        await interaction.response.edit_message(embed=embed, view=None)

class Terms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="서비스가입", description="서비스 가입 및 약관 동의")
    async def join_service(self, interaction: discord.Interaction):
        db = sqlite3.connect('data.db')
        cur = db.cursor()
        cur.execute("SELECT agreed FROM terms WHERE user_id = ?", (interaction.user.id,))
        
        if cur.fetchone():
            db.close()
            return await interaction.response.send_message("이미 가입된 상태입니다. 즐겁게 이용해주세요!", ephemeral=True)

        embed = discord.Embed(
            title="📜 서비스 가입",
            description="서비스를 이용하시려면 아래 약관을 확인 후 버튼을 눌러주세요.",
            color=0x5865F2
        )
        await interaction.response.send_message(embed=embed, view=AgreementView())

async def setup(bot):
    await bot.add_cog(Terms(bot))