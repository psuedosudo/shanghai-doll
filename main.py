#!/bin/python3
# TODO: 1) Create @bot.event for on_disconnect to handle channel culling
#       2) Fill out unwritten documentation
#       3) Add links to relevant documentation in doc blocks
#       4) Setup github
#       5) Research Cogs and how we may utilize them.

import discord, asyncio, sys
from discord.ext import commands

# Initilize bot object and intents
bot = commands.Bot()
bot.intents.all()

# Variables for use later
guilds=[196640093350395915]
vc_category=392461674218651658
perm_voip=[392475931165327360]

# TODO: Replace with system variable impport
token=""

if __name__ == "__main__":
    # Function runs when bot connection finalizes
    @bot.event
    async def on_ready():
        print(f"We have logged in as {bot.user}")


    # /hello - Just a test function
    @bot.slash_command(guild_ids=guilds,
            description='Just a test function.')
    async def ping(ctx):
        # await ctx.respond("Hello!")
        await ctx.respond("Pong!", ephemeral=True)

    # /privatevoip - Creates private voice channels, requires a name argument
    #   the invite argument takes @mentions to add @roles or @users to the permissions
    #   of the generated voice channel. If none given, then only the creater can join.
    @bot.slash_command(guild_ids=guilds,
            description='Create private VC')
    async def privatevoip(ctx, name, invite=None):
        # Mostly just not sure what can error here, will do testing later.
        try:
            invite = invite.split(' ')
        except:
            pass
        
        members = [ctx.author]
        category = discord.utils.get(ctx.guild.categories, id = vc_category)
        everyone = ctx.guild.default_role

        # overwrites attribute for create_voice_channel requires the group/user and the
        # PermissionOverwrite object be in a key:pair dictionary, so this sets that up.
        deny = discord.PermissionOverwrite()
        deny.connect = False
        deny_dict = {everyone: deny}

        # We need to collect user objects from the invite variable if they were given.
        # Discord has mentions formatted as <@!ID>, so we iterate through the given
        # mentions, parse out the mess, and append the user objects to the members list.
        # The user ID needs to be an intiger.
        try:
            if invite != None:
                for i in invite:
                    # We use get_or_fetch_user because the user likely isn't cached.
                    user = await bot.get_or_fetch_user(int(i[3:-1])) 
                    members.append(user)
        except Exception as e:
            await ctx.respond(str(e), ephemeral=True)

        # We create the channel, and assign the channel object to a variable for adding
        # the user permissions later. We assign it with connection perms denied for the
        # default user group.
        channel = await ctx.guild.create_voice_channel(name, category=category,
                overwrites=deny_dict)
        # Later, I want to rewrite the dictionary structure to also set these
        # permissions, but for now we'll iterate through the user list and set them one
        # by one. This allows the users in the members list to connect to the channel.
        for i in members:
            await channel.set_permissions(i, connect=True)
        await ctx.respond("Voice Channel Created!", ephemeral=True)


    # /yoink - While in generated channels, you can /yoink @someone to pull them into
    # your channel, regardless of there perms. Is mostly for when people want to request
    # to join a room, or when you're waiting in a voip for streaming, but you don't want
    # unexpected visitors in your stream.
    @bot.slash_command(guild_ids=guilds, 
            description='Moves users from greenroom into current VC')
    async def yoink(ctx):
        # Should first check to see if issuer is either not in achannel, or the channel
        # they're in is a perm_voip, and if true, deny the command. If they are in a 
        # generated channel, check if the @mentioned user is in the greenroom. If they
        # are, then move them into the issuer's voice channel.
        await ctx.respond("Not Yet Emplimented...", ephemeral=True)


    # Will fill out later. 
    @bot.slash_command(guild_ids=guilds, 
            description='Moves all users to Homeroom and removes current VC')
    async def unprivate(ctx, channel=None):
        await ctx.respond("Not Yet Emplimented...", ephemeral=True)


    # Will fill out later 
    @bot.slash_command(guild_ids=guilds, 
            description='Shows current level status, or @someone\'s status')
    async def rpg(ctx):
        await ctx.respond("Not Yet Emplimented...", ephemeral=True)

    bot.run(token)
