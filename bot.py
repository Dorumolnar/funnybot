import discord
import asyncio
import os
from discord.ext import commands

startup_extensions = ["General", "Fun"]
bot = commands.Bot(".")

@bot.event
async def on_ready():
    print('I am ready!')
    await bot.change_presence(game=discord.Game(name='Type .help for help!'))

class Main_Commands():
    def  __init__(self, bot):
        self.bot = bot

@bot.command(pass_context=True)
async def ping(ctx):
    await bot.say("Pong!")

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = "{}: {}".format(type(e).__name__, e)
            print("Failed to load extension {}\n{}".format(extension, exc))

bot.run(os.getenv('TOKEN'))
