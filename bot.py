import discord
import random

from discord.ext import commands
from errors import (
    admin_error_handler,
    handle_admin_commands_errors,
    deletemessages_error_handler,
    )
from decouple import config


intents = discord.Intents.all()
bot = discord.Client(intents=intents)
bot = commands.Bot(intents=intents, command_prefix = '!', help_command=None)

def is_admin():                                                            # checks permissions to execute the command.
    async def role_check(ctx):                                             # in this case the author must belong to the 'Admin' group
        return any(role.name == "Admin" for role in ctx.author.roles)      # easier ==> @commands.has_role('Admin')
    return commands.check(role_check)                                      # @commands.has_permissions(manage_messages = True)

#def is_me(ctx):
#    return ctx.author.id == PASTE_ID_HERE      # checks permission by DISCORD_ID. @commands.check(is_me)

@bot.command(aliases=["pomoc", "komendy", "obocie"])
async def help(ctx):
    print("Command !help")
    komendy = discord.Embed(title = "Komendy", description = "Takich komend możesz użyć do obsługi bota:", color = discord.Colour.brand_red())
    komendy.set_thumbnail(url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTo4uWpxUr3VyhR5WhZI-lMvy-1aqe-xzPyLA&usqp=CAU")
    komendy.add_field(name = "!ping", value = "Bot zawsze odbije piłeczkę 😒", inline=False)
    komendy.add_field(name = "!rzutmoneta", value="Bot rzuci monetą", inline=False)
    komendy.add_field(name = "!pkn", value="Użyj emoji-   👊, ✌️, ✋, aby zagrać w papier, kamień, nożyce 🤘", inline=False)
    await ctx.send(embed = komendy)

@bot.command(aliases=["adminpomoc", "adminkomendy", "adminobocie"])
@is_admin()
async def adminhelp(ctx):
    print("Command !adminhelp")
    komendy = discord.Embed(title = "Komendy Admin", description = "Komendy dla administracji.", color = discord.Colour.gold())
    komendy.set_thumbnail(url = "https://tr.rbxcdn.com/8781ac05c8061e4d64e35904dcf300fd/420/420/Image/Png")
    komendy.add_field(name = "!edit servername", value = "Zmiana nazwy serwera. Nazwy ze spacjami sa dozwolone.", inline=False)
    komendy.add_field(name = "!edit createtextchannel", value="Tworzenie kanału tekstowego na górze listy kanałów.", inline=False)
    komendy.add_field(name = "!edit createvoicechannel", value="Tworzenie kanału głosowego na górze listy kanałów.", inline=False)
    komendy.add_field(name = "!edit createrole", value="Tworzenie nowej roli na serwerze.", inline=False)
    komendy.add_field(name = "!kick", value="Kick użytkownika.", inline=False)
    komendy.add_field(name = "!ban", value="Ban użytkownika.", inline=False)
    komendy.add_field(name = "!unban", value="Unban użytkownika.", inline=False)
    komendy.add_field(name = "!deletemessages", value="Usunięcie wiadomości tekstowych. Możliwośc usunięcia określonej liczby wiadomości oraz wiadomości wysłanych po konkretnej dacie '!deletemessages / day month'.", inline=False)
    komendy.add_field(name="!mute", value="Zmutowanie użytkownika.", inline=False)
    komendy.add_field(name="!unmute", value="Odmutowanie użytkownika.", inline=False)
    komendy.add_field(name="!deafen", value="Ogłuszenie użytkownika.", inline=False)
    komendy.add_field(name="!undeafen", value="Przywrócenie odsłuchu użytkownikowi.", inline=False)
    komendy.add_field(name="!voicekick", value="Kick użytkownika z kanału głosowego.", inline=False)
    komendy.add_field(name="!reload_admin", value="Przeładowanie pliku cogs_admin.", inline=False)
    komendy.add_field(name="!reload_bot", value="Przeładowanie pliku cogs_bot.", inline=False)
    komendy.add_field(name="!reload_user", value="Przeładowanie pliku cogs_user.", inline=False)
    admin_user = ctx.author
    admin_channel = await admin_user.create_dm()
    await admin_channel.send(embed=komendy) #send dm
    await ctx.message.delete() #delete message !adminhelp from chat

########################   Errors handle   ###########################

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Nie znalazłem takiej komendy. Listę komend możesz sprawdzić wpisując !help, !pomoc, !komendy, !obocie :disguised_face: ')

#@servername.error
#@createtextchannel.error
#@createvoicechannel.error
#@createrole.error
# @kick.error
# @ban.error
# @unban.error
# @mute.error
# @unmute.error
# @deafen.error
# @undeafen.error
# @voicekick.error
@adminhelp.error
async def admin_commands_error(ctx, error):
    await handle_admin_commands_errors(ctx, error)

########################   Cogs commands   ###########################

@bot.command()
@is_admin()
async def reload_admin(ctx):
    await bot.reload_extension("cogs_admin")
    await ctx.message.delete()
    await  ctx.send("Done!")
    print(">>>>>>>>>>>>>>>Admin extension reloaded<<<<<<<<<<<<<<<")

@bot.command()
@is_admin()
async def reload_bot(ctx):
    await bot.reload_extension("cogs_bot")
    await ctx.message.delete()
    await  ctx.send("Done!")
    print(">>>>>>>>>>>>>>>Bot extension reloaded<<<<<<<<<<<<<<<")

@bot.command()
@is_admin()
async def reload_user(ctx):
    await bot.reload_extension("cogs_user")
    await ctx.message.delete()
    await  ctx.send("Done!")
    print(">>>>>>>>>>>>>>>User extension reloaded<<<<<<<<<<<<<<<")

########################   Cogs load and online status  ###########################

@bot.event
async def on_ready():
    print(">>>>>>>>>>>>>>>Online!<<<<<<<<<<<<<<<")
    await bot.load_extension("cogs_admin")
    print(">>>>>>>>>>>>>>>Admin extension loaded<<<<<<<<<<<<<<<")
    await bot.load_extension("cogs_bot")
    print(">>>>>>>>>>>>>>>Bot extension loaded<<<<<<<<<<<<<<<")
    await bot.load_extension("cogs_user")
    print(">>>>>>>>>>>>>>>User extension loaded<<<<<<<<<<<<<<<")

########################   Login and connect   ###########################

@bot.event
async def on_resumed():
    print(">>>>>>>>>>>>>>>Connection resumed!<<<<<<<<<<<<<<<")

token= config('TOKEN') #read token from .env file
bot.run(token, reconnect=True)