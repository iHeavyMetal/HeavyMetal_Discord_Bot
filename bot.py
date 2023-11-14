import discord
import random
from discord.ext import commands
from decouple import config

intents = discord.Intents.all()
client = discord.Client(intents=intents)
client = commands.Bot(intents=intents, command_prefix = '!', help_command=None)

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

@client.group()
async def admin(ctx):
    pass

########### N A P R A W I C ########


#@admin.command()
    



# @client.group()
# async def edit(ctx): #zmien nazwe na admin
#     pass


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
#============================ponizej info z CHgpt. nalezy stworzyć hierarchie dla komend admina====================================
# @bot.group(name="admin", help="Komendy administracyjne")
# async def admin(ctx):
#     if ctx.invoked_subcommand is None:
#         await ctx.send("Dostępne komendy administracyjne: !admin kick, !admin ban, !admin warn")
#
# @admin.command(name="kick")
# async def kick(ctx, user: discord.Member):
#     # Implementacja komendy kick
#
# @admin.command(name="ban")
# async def ban(ctx, user: discord.Member):
#     # Implementacja komendy ban
#
# @admin.command(name="warn")
# async def warn(ctx, user: discord.Member):
#     # Implementacja komendy warn






token= config('TOKEN') #read token from .env file
client.run(token, reconnect=True)