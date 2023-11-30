import discord

from discord.ext import commands
from datetime import datetime
from errors import (deletemessages_error_handler,
                    handle_admin_commands_errors,
                    )

def is_admin():                                                     #jak zaimportować is_admin z głównego pliku?
    async def role_check(ctx):
        return any(role.name == "Admin" for role in ctx.author.roles)

    return commands.check(role_check)

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ########################   Admin !edit commands group   ###########################

    @commands.group()
    async def edit(self, ctx):
        pass

    ########################   Change server name   ###########################

    @edit.command()
    @is_admin()
    async def servername(self, ctx, *, input):
        server_name = await ctx.guild.edit(name=input)
        await ctx.send(f'Zmieniłem nazwę serwera na: "{server_name.name}"')
        print("Servername changed!")

    @servername.error
    async def admin_commands_error(self, ctx, error):
        await handle_admin_commands_errors(ctx, error)
    ########################   Create  tetext channel   ###########################

    @edit.command()
    @is_admin()
    async def createtextchannel(self, ctx, *, input):
        text_channel = await ctx.guild.create_text_channel(name=input)
        await ctx.send(f'Utworzyłem nowy kanał tekstowy: {text_channel.name}')
        print("Text channel created!")

    #######################    create voice channel    ########################

    @edit.command()
    @is_admin()
    async def createvoicechannel(self, ctx, *, input):
        voice_channel = await ctx.guild.create_voice_channel(name=input)
        await ctx.send(f'Utworzono nowy kanał głosowy: {voice_channel.name}')
        print("Voice channel created!")

    #######################    create voice role    ########################

    @edit.command()
    @is_admin()
    async def createrole(self, ctx, *, input):
        role = await ctx.guild.create_role(name=input)
        await ctx.send(f'Utworzono nową rolę: {role.name}')
        print("New role created!")

    #######################    kick user    ########################

    @commands.command()
    @is_admin()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await ctx.guild.kick(member, reason=reason)

    #######################    ban user    ########################

    @commands.command()
    @is_admin()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await ctx.guild.ban(member, reason=reason)

    #######################    unban user    ########################

    @commands.command()
    @is_admin()
    async def unban(self, ctx, *, input):
        name, discriminator = input.split("#")
        async for entry in ctx.guild.bans(limit=150):
            username = entry.user.name
            disc = entry.user.discriminator
            if name == username and discriminator == disc:
                await ctx.guild.unban(entry.user)

    #######################    delete messages    ########################

    @commands.command()
    @is_admin()
    async def deletemessages(self, ctx, amount, day: int = None, month: int = None, year: int = datetime.now().year):
        if amount == '/':  # !deletemessages / day month
            if day == None or month == None:
                return
            else:
                await ctx.channel.purge(after=datetime(year, month, day))
                print("after - Messages deleted!")
        else:
            await ctx.channel.purge(limit=int(amount) + 1)
            print("limit - Messages deleted!")

    @deletemessages.error
    async def delmsg_error(self, ctx, error):
        await deletemessages_error_handler(ctx, error)

    #######################    mute user    ########################

    @commands.command()
    @is_admin()
    async def mute(self, ctx, user: discord.Member):
        await user.edit(mute=True)
        print("User muted")

    #######################    unmute user    ########################

    @commands.command()
    @is_admin()
    async def unmute(self, ctx, user: discord.Member):
        await user.edit(mute=False)
        print("User unmuted")

    #######################    deafen user    ########################

    @commands.command()
    @is_admin()
    async def deafen(self, ctx, user: discord.Member):
        await user.edit(deafen=True)
        print("User deafen")

    #######################    undeafen user    ########################

    @commands.command()
    @is_admin()
    async def undeafen(self, ctx, user: discord.Member):
        await user.edit(deafen=False)
        print("User undeafen")

    #######################    kick user from voice channel    ########################

    @commands.command()
    @is_admin()
    async def voicekick(self, ctx, user: discord.Member):
        await user.edit(voice_channel=None)
        print("User kicked")

async def setup(bot):
    await bot.add_cog(AdminCog(bot))