#!/bin/python3
# TODO: 1) Fill out unwritten documentation

# Import Pycord and other needed packages
import discord, asyncio, os
from discord.ext import commands
# Import API Keys from .env file
from dotenv import load_dotenv
load_dotenv()

# Initilize bot object and intents
bot = commands.Bot()
bot.intents.all()

# Guild IDs list for command registration to the server. Although the bot is currently
# written with the assumption that it is only in one server, pycord requires this in
# list form as it has to assume the bot may be in many discords at once.
guilds=[int(os.getenv('GUILDS'))]
token=os.getenv('DISCORD_BOT_TOKEN')

if __name__ == "__main__":

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')

    # == EVENT FLAGS ==
    # Function runs when bot connection finalizes
    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user}")

    # == SLASH COMMANDS ==
    # /hello - Just a test function
    @bot.slash_command(guild_ids=guilds,
            description='Just a test function.')
    async def ping(ctx):
        await ctx.respond("Pong!", ephemeral=True)

    bot.run(token)

