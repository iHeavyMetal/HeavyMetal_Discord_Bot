import random
from discord.ext import commands

class UserCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ########################   Replying to messages and printing messages in the console  ###########################

    @commands.Cog.listener()
    async def on_message(self,msg):
        print(f"Message from: {msg.author}: {msg.content}")  # printing messages in the console
        author_name = msg.author.mention
        if msg.author == self.bot.user:
            return
        if msg.content.lower().startswith(('cześć', 'czesc')):          #set message the bot should respond to
            print("Command on_message!")
            await msg.channel.send('Cześć! ' + author_name)  #respond message

        await self.bot.process_commands(msg)

    ########################   Ping-Pong game ###########################

    @commands.command()
    async def ping(self, ctx):
        print("Command !ping")
        await ctx.send("Pong!")

    ######################## Coin flip    ###########################

    @commands.command()
    async def rzutmoneta(self, ctx):
        number = random.randint(1, 2)

        if number == 1:
            await ctx.send("Orzeł")         #heads
        if number == 2:
            await ctx.send("Reszka")        #tails

async def setup(bot):
    await bot.add_cog(UserCog(bot))