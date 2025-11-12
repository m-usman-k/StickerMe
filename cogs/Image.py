# ----- Modules -----
# Discord
import discord
from discord.ext import commands
from discord import app_commands


class Image(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        
        
        
async def setup(bot: commands.Bot):
    await bot.add_cog(Image(bot=bot))