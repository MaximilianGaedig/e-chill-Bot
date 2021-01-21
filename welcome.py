from discord.ext import commands
from main import bot


class Utils(commands.Cog, name='Utils'):
    def __init__(self, bot):
        self.bot = bot




def setup(bot):
    bot.add_cog(Utils(bot))
