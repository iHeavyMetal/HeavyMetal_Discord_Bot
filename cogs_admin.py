import discord

from discord.ext import commands


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

async def setup(bot):
    await bot.add_cog(AdminCog(bot))