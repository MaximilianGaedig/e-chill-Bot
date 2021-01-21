from discord.ext import commands, tasks
import yaml


class Count(commands.Cog, name='count'):
    def __init__(self, bot):
        self.bot = bot
        self.count.start()

    @tasks.loop(seconds=30)
    async def count(self):
        """
        Changes a channel name so it
        """
        config = yaml.safe_load(open("config.yml", encoding='utf-8'))
        channel = self.bot.get_channel(config["channels"]["voice"]["count"])
        await channel.edit(name=f"♡ ﹕{channel.guild.member_count} members")


def setup(bot):
    bot.add_cog(Count(bot))
    Count(bot)
