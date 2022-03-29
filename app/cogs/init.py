import discord, asyncio, os
from discord.ext import commands
guilds=[int(os.getenv('GUILDS'))]

class Initialize(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.bot.user}")

    @discord.slash_command(guild_ids=guilds,
            description='Just a test function.')
    async def ping(self, ctx):
        await ctx.respond("Pong!", ephemeral=True)

def setup(bot):
    bot.add_cog(Initialize(bot))
