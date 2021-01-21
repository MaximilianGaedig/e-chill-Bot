import discord
import asyncio
import random
from discord.ext import commands
from discord.ext.commands import command
import re
import yaml
import time


class Utils(commands.Cog, name='Utils'):
    def __init__(self, client):
        self.bot = client

    @command()
    async def move(self, ctx, user_id, channel_id: int):
        if not re.search('<@!?(\d+)>', user_id):
            user_id = int(ctx.message.author.id)
        else:
            user_id = int(user_id.replace('<@!', '').replace('>', ''))
        user = ctx.guild.get_member(user_id)
        channel = self.bot.get_channel(channel_id)
        try:
            await user.edit(voice_channel=channel)
        except discord.errors.HTTPException:
            pass

    @command()
    async def move_spam(self, ctx, user_id, channel_id=0, role_id=0):
        try:
            user_id = int(user_id.replace('<@!', '').replace('>', ''))
        except ValueError:
            pass
        user = ctx.guild.get_member(user_id)
        if channel_id != 0:
            channel = self.bot.get_channel(channel_id)
        else:
            channel = None
        aborted = False
        msg = await ctx.send(content=f"Spam moving {user} to {channel}")
        i = 0
        removed_role = False
        while not aborted:
            try:
                if user.voice.channel != channel:
                    i += 1
                    try:
                        await msg.edit(content=f"Spam moving {user} to {channel} (already tried {i} times)")
                        if role_id != 0:
                            if role_id in [y.id for y in user.roles]:
                                await user.remove_roles(role_id)
                                removed_role = True
                    except discord.NotFound:
                        aborted = True
                    try:
                        await user.edit(voice_channel=channel)
                    except discord.errors.HTTPException:
                        await ctx.send(content=f"{user} left")
                        if removed_role:
                            await user.add_roles(role_id)
                await asyncio.sleep(1)
            except AttributeError:
                aborted = True
                await ctx.send(content=f"{user} left")

    @command()
    async def nickall(self, ctx, option="reset", *, nick=""):
        """Renames everyone to one nickname, use the argument "random" to select a random name"""
        owner_role = discord.utils.get(ctx.guild.roles, name="Owner")
        if nick == "random":
            random_user = ctx.guild.members[random.randint(1, len(ctx.guild.members))]
            nick = random_user.name
        if "<@" in nick and ">" in nick:
            if "&" in nick:
                nick = discord.utils.get(ctx.guild.roles, id=int(nick.replace('<@', '')
                                                                 .replace('>', '')
                                                                 .replace('!', '')
                                                                 .replace('&', ''))).name
            else:
                nick = discord.utils.get(ctx.guild.members, id=int(nick.replace('<@', '')
                                                                   .replace('>', '')
                                                                   .replace('!', '')
                                                                   .replace('&', ''))).name
        start = time.time()
        if owner_role in ctx.author.roles:
            msg = await ctx.send(f"Changing Nicknames...")
            i = 0
            aborted = False
            lastnick = "noone"
            config = yaml.safe_load(open("config.yml", encoding='utf-8'))
            for member in ctx.guild.members:
                if ctx.guild.owner_id != member.id and not aborted:
                    await asyncio.sleep(0.21)
                    i += 1
                    end = time.time()
                    # Functions:
                    if option == "change":
                        current_nick = nick
                    elif option == "append":
                        current_nick = member.name + nick
                    elif option == "prepend":
                        current_nick = nick + member.name
                    elif option == "confuse":
                        current_nick = lastnick
                        lastnick = member.name
                    else:
                        current_nick = member.name
                    # Use default nicknames:
                    if member.name in config['default_nicknames']:
                        current_nick = config['default_nicknames'][member.name]
                    await member.edit(nick=current_nick)
                    try:
                        await msg.edit(content=f"Already changed {i} Nicks"
                                               f"\nNow changing the nick of {member.name} to {current_nick}"
                                               f"\nElapsed:{round(end - start, 1)}s")
                    except discord.NotFound:
                        aborted = True

            end = time.time()
            if nick == "":
                try:
                    await msg.edit(content=f"Reset nicknames of {i} members in {round(end - start, 2)}s")
                except discord.NotFound:
                    await ctx.send("Aborted")
            else:
                try:
                    await msg.edit(content=f"Renamed {i} members to {nick} in {round(end - start, 2)}s")
                except discord.NotFound:
                    await ctx.send("Aborted")
        else:
            await ctx.send(f"{ctx.bot.author} tried to set nicks for all, though isn't an owner ")


def setup(bot):
    bot.add_cog(Utils(bot))
