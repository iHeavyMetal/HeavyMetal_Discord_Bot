import discord
import random
from discord.ext import commands
from errors import handle_admin_commands_errors, custom_error_handler
from decouple import config
from datetime import datetime

intents = discord.Intents.all()
client = discord.Client(intents=intents)
client = commands.Bot(intents=intents, command_prefix = '!', help_command=None)

def is_admin():                                                        # checks permissions to execute the command.
    async def role_check(ctx):                                             # in this case the author must belong to the 'Admin' group
        return any(role.name == "Admin" for role in ctx.author.roles)     # easier ==> @commands.has_role('Admin')
    return commands.check(role_check)                                      # @commands.has_permissions(manage_messages = True)

#def is_me(ctx):
#    return ctx.author.id == PASTE_ID_HERE      # checks permission by DISCORD_ID. @commands.check(is_me)


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

@client.command(aliases=["adminpomoc", "adminkomendy", "adminobocie"])
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
    admin_user = ctx.author
    admin_channel = await admin_user.create_dm()
    await admin_channel.send(embed=komendy) #send dm
    await ctx.message.delete() #delete message !adminhelp from chat
@adminhelp.error
async def adminhelp_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Nie masz wystarczających uprawnień do wykonania tej komendy.")
    else:
        raise error

########################   Admin commands   ###########################

@client.group()
async def edit(ctx):
    pass

@edit.command()
@is_admin()
async def servername(ctx, *, input):
    server_name = await ctx.guild.edit(name=input)
    await ctx.send(f'Zmieniłem nazwę serwera na: "{server_name.name}"')
    print("Servername changed!")

@edit.command()
@is_admin()
async def createtextchannel(ctx, *, input):
    text_channel = await ctx.guild.create_text_channel(name=input)
    await ctx.send(f'Utworzono nowy kanał tekstowy: {text_channel.name}')
    print("Text channel created!")

@edit.command()
@is_admin()
async def createvoicechannel(ctx, *, input):
   voice_channel = await ctx.guild.create_voice_channel(name=input)
   await ctx.send(f'Utworzono nowy kanał głosowy: {voice_channel.name}')
   print("Voice channel created!")

@edit.command()
@is_admin()
async def createrole(ctx, *, input):
   role = await ctx.guild.create_role(name=input)
   await ctx.send(f'Utworzono nową rolę: {role.name}')
   print("New role created!")

@client.command()
@is_admin()
async def kick(ctx, member: discord.Member, *, reason = None):
    await ctx.guild.kick(member, reason=reason)

@client.command()
@is_admin()
async def ban(ctx, member: discord.Member, *, reason = None):
    await ctx.guild.ban(member, reason=reason)

@client.command()
@is_admin()
async def unban(ctx, *, input):
    name, discriminator = input.split("#")
    async for entry in ctx.guild.bans(limit=150):
        username = entry.user.name
        disc = entry.user.discriminator
        if name == username and discriminator == disc:
            await ctx.guild.unban(entry.user)

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

@client.command()
@is_admin()
async def mute(ctx, user : discord.Member):
    await user.edit(mute = True)
    print("User muted")

@client.command()
@is_admin()
async def unmute(ctx, user : discord.Member):
    await user.edit(mute = False)
    print("User unmuted")

@client.command()
@is_admin()
async def deafen(ctx, user : discord.Member):
    await user.edit(deafen = True)
    print("User deafen")

@client.command()
@is_admin()
async def undeafen(ctx, user : discord.Member):
    await user.edit(deafen = False)
    print("User undeafen")

@client.command()
@is_admin()
async def voicekick(ctx, user : discord.Member):
    await user.edit(voice_channel = None)
    print("User kicked")


########################   Errors handle   ###########################
@servername.error
@createtextchannel.error
@createvoicechannel.error
@createrole.error
@kick.error
@ban.error
@unban.error
@deletemessages.error
@mute.error
@unmute.error
@deafen.error
@undeafen.error
@voicekick.error
async def command_error(ctx, error):
    await handle_admin_commands_errors(ctx, error)

token= config('TOKEN') #read token from .env file
client.run(token, reconnect=True)