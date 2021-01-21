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
    await channel.send(f"👌 My💯 friend 👬here📍**{member.name}**👦🏻he 🤪 is 😛 already 😘 taken 🔞\n"
                       f" 🅰️nd he is 🤣cracked 😤 at Fortnite 🎮 my 👦🏿guy 👨🖥️\n"
                       f" AWnnWn 🍆 💦 🤤 🍑 AuwWan 😩✊🍆💦🍆✊😩")


@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message):
        await message.add_reaction('❤')
    await bot.process_commands(message)


@bot.event
async def on_ready():
    channel = bot.get_channel(config["channels"]["text"]["main"])
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
