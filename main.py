import discord
from discord.ext import commands
import os
import yaml
token = os.environ.get('TOKEN')
description = '''e-chill bot'''
intents = discord.Intents.default()
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix='$', description=description, intents=intents)
config = yaml.safe_load(open("config.yml", encoding='utf-8'))


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(config["channels"]["text"]["main"])
    embed = discord.Embed(description=f".・。.・hey, **{member.mention}**.\n" +
                                      f"welcome to {channel.guild.name}* . +\n" +
                                      f'・{bot.get_channel(config["channels"]["text"]["color"]).mention}\n' +
                                      f'・{bot.get_channel(config["channels"]["text"]["roles"]).mention}\n' +
                                      "────────────── ✧\n" +
                                      "⠀☆ - follow tos.\n" +
                                      "⠀☆ - don't be annoying.\n" +
                                      "⠀☆ - have fun.\n" +
                                      "────────────── ✧\n" +
                                      f"・{channel.guild.member_count} member to join * . +")
    embed.set_thumbnail(
        url="https://images-ext-2.discordapp.net/external/bzHX-J4WolmEqnD4ctUSLVPc7u1j3slHVSoJqFzEqwo/https/i.ibb.co/MkYmhYk/kindpng-4215227.png?width=361&height=480")
    embed.set_image(url="https://i.ibb.co/34GCrRh/ezgif-com-gif-maker.gif")
    embed.set_footer(text=".・。.・゜✭・.・✫・゜・。.•••")
    await channel.send(embed=embed)


@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message):
        await message.add_reaction('❤')
    await bot.process_commands(message)


@bot.event
async def on_ready():
    channel = bot.get_channel(config["channels"]["text"]["status"])
    if config["ready_message"] == "":
        config["ready_message"] = "."
    bot.status_msg = await channel.send(config["ready_message"])
    print(config["ready_message"])
    for extension in config["extensions"]:
        try:
            bot.load_extension(extension)
            print(extension + ' loaded successfully')
        except Exception as e:
            print(e)


@bot.command()
async def reload(ctx, extension):
    """Reloads an Extension"""
    try:
        bot.reload_extension(extension)
    except Exception as e:
        await ctx.send(e)
    else:
        await ctx.send(extension + " reloaded successfully")


@bot.command()
async def load(ctx, extension):
    """Loads an Extension"""
    try:
        bot.load_extension(extension)
    except Exception as e:
        await ctx.send(e)
    else:
        await ctx.send(extension + " loaded successfully")


@bot.command()
async def unload(ctx, extension):
    """Unloads an Extension"""
    try:
        bot.unload_extension(extension)
    except Exception as e:
        await ctx.send(e)
    else:
        await ctx.send(extension + " unloaded successfully")
bot.run(config['token'])
