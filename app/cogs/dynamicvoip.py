import discord, asyncio, os
from discord.ext import commands
guilds=[int(os.getenv('GUILDS'))]

# TODO:
# *) Create database index for channel entries
# *) Refactor environment input as an alternative to command based updates to database
# *) Have channels created manually automatically be added to database
# *) /joinrequest
# *) Dynamic Voice Propogation

# The channel category ID for voice channels
vc_category=int(os.getenv('VC_CATEGORY'))
# The channel ID of the greenroom vc.
greenroom=int(os.getenv('GREENROOM'))
# For dynamic voice channel generation. First value is for the naming convention,
# second value is for the master dynamic voice channel ID.
dyn_voip=('dynvoip-', int(os.getenv('DYN_VOIP')))
# List of voice channels that are blacklisted from automatic removal
perm_voip=list(map(int, os.getenv('PERM_VOIP').split(',')))

class Dynamicvoip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # == EVENT FLAGS ==
    # Function runs when bot connection finalizes
    @discord.Cog.listener()
    async def on_ready(self):
        print("Dynamicvoip loaded!")

    # https://docs.pycord.dev/en/master/api.html?highlight=on_voice_state_update#discord.on_voice_state_update
    @discord.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # print((member, before, after))
        try:
            # if after.channel.id is dyn_voip[1]:
            if before.channel.id not in perm_voip:
                if len(before.channel.members) == 0:
                    await before.channel.delete()
        except:
            pass
    
    #https://docs.pycord.dev/en/master/api.html?highlight=on_voice_state_update#discord.on_thread_update
    @discord.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        # The bot should use the DM string of the reaction.message value to determine
        # the intent of the action, and also verifiy that reaction.message.author is 
        # itself to prevent bypass.
        pass

    # == SLASH COMMANDS ==
    # /privatevoip - Creates private voice channels, requires a name argument
    #   the invite argument takes @mentions to add @roles or @users to the permissions
    #   of the generated voice channel. If none given, then only the creater can join.
    @discord.slash_command(guild_ids=guilds,
            description='Create private VC')
    async def privatevoip(self, ctx, name, invite=None):
        # Mostly just not sure what can error here, will do testing later.
        try:
            invite = invite.split(' ')
        except Exception as e:
            await ctx.respond(str(e), ephemeral=True)
        
        # Just grabbing some objects to use later
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
                    # print(i)
                    user = await self.bot.get_or_fetch_user(int(i[2:-1])) 
                    members.append(user)
        except Exception as e:
            await ctx.respond(str(e), ephemeral=True)

        # We create the channel, and assign the channel object to a variable for adding
        # the user permissions later. We assign it with connection perms denied for the
        # default user group.
        channel = await ctx.guild.create_voice_channel("🔇" + name, category=category,
                overwrites=deny_dict)
        # Later, I want to rewrite the dictionary structure to also set these
        # permissions, but for now we'll iterate through the user list and set them one
        # by one. This allows the users in the members list to connect to the channel.
        for i in members:
            await channel.set_permissions(i, connect=True, priority_speaker=True, 
                    mute_members=True, move_members=True)
        await ctx.respond("Voice Channel Created!", ephemeral=True)

    # /yoink - While in generated channels, you can /yoink @someone to pull them into
    # your channel, regardless of there perms. Is mostly for when people want to request
    # to join a room, or when you're waiting in a voip for streaming, but you don't want
    # unexpected visitors in your stream.
    @discord.slash_command(guild_ids=guilds, 
            description='Moves users from greenroom into current VC')
    async def yoink(self, ctx, target):
        member_converter = commands.MemberConverter()
        target = await member_converter.convert(ctx, target[2:-1])
        try: 
            if ctx.author.voice.channel.id not in perm_voip:
                if target.voice.channel.id == greenroom:
                    perms = ctx.author.voice.channel.overwrites_for(ctx.author)
                    if perms.connect != False:
                        await target.move_to(ctx.author.voice.channel)
                        await ctx.respond("Moved!", ephemeral=True)
                    else:
                        await ctx.respond("You don't have permissions for this channel!",
                            ephemeral=True)
                else:
                    await ctx.respond("User not found in Greenroom!", ephemeral=True)
            else:
                await ctx.respond("You can't use this in a public room!", 
                    ephemeral=True)
        except Exception as e:
            # await ctx.respond("Invalid conditions!", ephemeral=True)
            await ctx.respond(e, ephemeral=True)

#========================================================================================
#==                                     TO IMPLEMENT                                   ==
#========================================================================================

    # /joinrequest - While a user is in the greenroom, they can use the command and point
    # at a user who is in a private vc. The bot will then DM every user who HAS PERMS and
    # is IN the channel a message, and on confirmation, will move the user into the vc.
    @discord.slash_command(guild_ids=guilds, 
            description='Requests users to allow joining private VC')
    async def joinrequest(self, ctx):
        # The command should get the user object of the @mention, then find what voice 
        # channel they are in, check if the @everyone permission is blocked. If it is
        # blocked, iterate through every user in the voice channel, and see if they have
        # permissions in the channel, and if so, dm a message for confirmation. Some
        # code will likely need to be written for an event flag for when people add
        # emoji for messages.
        await ctx.respond("Not Yet Emplimented...", ephemeral=True)

    # Will fill out later. 
    @discord.slash_command(guild_ids=guilds, 
            description='Moves all users to Homeroom and removes current VC')
    async def unprivate(self, ctx, channel=None):
        await ctx.respond("Not Yet Emplimented...", ephemeral=True)

def setup(bot):
    bot.add_cog(Dynamicvoip(bot))
