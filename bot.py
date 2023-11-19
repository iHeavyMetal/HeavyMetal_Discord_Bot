import discord
import random
from discord.ext import commands
from decouple import config
from datetime import datetime

intents = discord.Intents.all()
client = discord.Client(intents=intents)
client = commands.Bot(intents=intents, command_prefix = '!', help_command=None)

def is_admin():
    async def predicate(ctx):
        return any(role.name == "Admin" for role in ctx.author.roles)
    return commands.check(predicate)

@client.event
async def on_ready():
    print("Online!")

@client.event
async def on_resume():
    print("Resume Online!")

@client.event
async def on_message(msg):
    print(f"Message from: {msg.author}: {msg.content}")  # print message
    author_name = msg.author.mention
    if msg.author == client.user:
        return

    if msg.content.lower().startswith('cześć'):
        print("Command on_message!")
        await msg.channel.send('Cześć! ' + author_name)

    await client.process_commands(msg)

@client.event
async def on_member_join(member):
    guild = member.guild
    guildname = guild.name
    dmchannel = await member.create_dm()
    await dmchannel.send(f"Witamy na discordzie {guildname}!")

@client.event
async def on_raw_reaction_add(payload):
    emoji = payload.emoji.name
    member = payload.member
    message_id = payload.message_id
    guild_id = payload.guild_id
    guild = client.get_guild(guild_id)

    if emoji == "✍️" and message_id == 1158011769759993990:
        role = discord.utils.get(guild.roles, name = "Write_Fan")
        await member.add_roles(role)

    if emoji == "💩" and message_id == 1158011796490293258:
        role = discord.utils.get(guild.roles, name = "Emoji_Fan")
        await member.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload):
    emoji = payload.emoji.name
    message_id = payload.message_id
    guild_id = payload.guild_id
    guild = client.get_guild(guild_id)
    user_id = payload.user_id
    member = guild.get_member(user_id)
    if emoji == "✍️" and message_id == 1158011769759993990:
        role = discord.utils.get(guild.roles, name = "Write_Fan")
        await member.remove_roles(role)

    if emoji == "💩" and message_id == 1158011796490293258:
        role = discord.utils.get(guild.roles, name = "Emoji_Fan")
        await member.remove_roles(role)

@client.command()
async def ping(ctx):
    print("Command !ping")
    await ctx.send("Pong!")

@client.command()
async def rzutmoneta(ctx):
    number = random.randint(1,2)

    if number == 1:
        await ctx.send("Orzeł")
    if number == 2:
        await ctx.send("Reszka")

@client.command()
async def pkn(ctx, hand):
    hands = ["👊", "✌️", "✋",]
    bothand = random.choice(hands)
    await ctx.send(bothand)
    if hand == bothand:
        await ctx.send("Remis")
    elif hand == "✌️":
        if bothand == "👊":
            await ctx.send("Wygrałem!")
        if bothand == "✋":
            await  ctx.send("Przegrałem!😭 ")
    elif hand == "✋":
        if bothand == "✌️":
            await ctx.send("Wygrałem!")
        if bothand == "👊":
            await  ctx.send("Przegrałem!😭 ")
    elif hand == "👊":
        if bothand == "✋":
            await ctx.send("Wygrałem!")
        if bothand == "✌️":
            await  ctx.send("Przegrałem!😭 ")

@client.command(aliases=["pomoc", "komendy", "obocie"])
async def help(ctx):
    print("Command !help")
    komendy = discord.Embed(title = "Komendy", description = "Takich komend możesz użyć do obsługi bota:", color = discord.Colour.brand_red())
    komendy.set_thumbnail(url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTo4uWpxUr3VyhR5WhZI-lMvy-1aqe-xzPyLA&usqp=CAU")
    komendy.add_field(name = "!ping", value = "Bot zawsze odbije piłeczkę 😒", inline=False)
    komendy.add_field(name = "!rzutmoneta", value="Bot rzuci monetą", inline=False)
    komendy.add_field(name = "!pkn", value="Użyj emoji-   👊, ✌️, ✋, aby zagrać w papier, kamień, nożyce 🤘", inline=False)
    await ctx.send(embed = komendy)

########### N A P R A W I C ########
# @client.group()
# async def admin(ctx):
#     pass
# @admin.command()
#
# @client.group()
# async def edit(ctx): #zmien nazwe na admin
#     pass
#
#
# @edit.command()
# async def servername(ctx,password,server_id,*,input):
#     if password == "123" and ctx.channel.type == discord.ChannelType.private:
#         guild = client.get_guild(server_id)
#         if guild:
#             await ctx.guild.edit(name=input)
#             await ctx.send("Nazwa została zmieniona")
#             print("Zmieniono nazwę serwera")
#         else:
#             await ctx.send("Błędne ID serwera")
#     else:
#         await ctx.send("Password NOK")
# #============================ponizej info z CHgpt. nalezy stworzyć hierarchie dla komend admina====================================
# @bot.group(name="admin", help="Komendy administracyjne")
# async def admin(ctx):
#     if ctx.invoked_subcommand is None:
#         await ctx.send("Dostępne komendy administracyjne: !admin kick, !admin ban, !admin warn")
#
# @admin.command(name="kick")
# async def kick(ctx, user: discord.Member):
#
#
# @admin.command(name="ban")
# async def ban(ctx, user: discord.Member):
#
#
# @admin.command(name="warn")
# async def warn(ctx, user: discord.Member):
#


@client.group()
async def edit(ctx):
    pass

@edit.command()
@is_admin()
async def servername(ctx, *, input):
    server_name = await ctx.guild.edit(name=input)
    await ctx.send(f'Zmieniłem nazwę serwera na: "{server_name.name}"')
    print("Servername changed!")

@servername.error
async def servername_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Nie masz wystarczających uprawnień do wykonania tej komendy.")
    else:
        raise error

@edit.command()
@is_admin()
async def createtextchannel(ctx, *, input):
    text_channel = await ctx.guild.create_text_channel(name=input)
    await ctx.send(f'Utworzono nowy kanał tekstowy: {text_channel.name}')
    print("Text channel created!")

@createtextchannel.error
async def createtextchannel_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Nie masz wystarczających uprawnień do wykonania tej komendy.")
    else:
        raise error

@edit.command()
@is_admin()
async def createvoicechannel(ctx, *, input):
   voice_channel = await ctx.guild.create_voice_channel(name=input)
   await ctx.send(f'Utworzono nowy kanał głosowy: {voice_channel.name}')
   print("Voice channel created!")

@createvoicechannel.error
async def createvoicechannel_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Nie masz wystarczających uprawnień do wykonania tej komendy.")
    else:
        raise error

@edit.command()
@is_admin()
async def createrole(ctx, *, input):
   role = await ctx.guild.create_role(name=input)
   await ctx.send(f'Utworzono nową rolę: {role.name}')
   print("New role created!")

@createrole.error
async def createrole_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Nie masz wystarczających uprawnień do wykonania tej komendy.")
    else:
        raise error

@client.command()
@is_admin()
async def kick(ctx, member: discord.Member, *, reason = None):
    await ctx.guild.kick(member, reason=reason)

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Nie masz wystarczających uprawnień do wykonania tej komendy.")
    else:
        raise error

@client.command()
@is_admin()
async def ban(ctx, member: discord.Member, *, reason = None):
    await ctx.guild.ban(member, reason=reason)

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Nie masz wystarczających uprawnień do wykonania tej komendy.")
    else:
        raise error

@client.command()
@is_admin()
async def unban(ctx, *, input):
    name, discriminator = input.split("#")
    async for entry in ctx.guild.bans(limit=150):
        username = entry.user.name
        disc = entry.user.discriminator
        if name == username and discriminator == disc:
            await ctx.guild.unban(entry.user)

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Nie masz wystarczających uprawnień do wykonania tej komendy.")
    else:
        raise error

@client.command()
@is_admin()
async def deletemessages(ctx, amount, day : int = None, month : int = None, year : int = datetime.now().year):
    if amount == '/':     #!deletemessages / day month
        if day == None or month == None:
            return
        else:
            await ctx.channel.purge(after = datetime(year, month, day))
            print("after - Messages deleted!")
    else:
        await ctx.channel.purge(limit = int(amount)+1)
        print("limit - Messages deleted!")
@deletemessages.error
async def deletemessages_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Nie masz wystarczających uprawnień do wykonania tej komendy.")
    else:
        raise error

token= config('TOKEN') #read token from .env file
client.run(token, reconnect=True)