from discord.ext import commands

class UserCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self,msg):
        print(f"Message from: {msg.author}: {msg.content}")  # print message
        author_name = msg.author.mention
        if msg.author == self.bot.user:
            return

        if msg.content.lower().startswith('cześć'):
            print("Command on_message!")
            await msg.channel.send('Cześć! ' + author_name)

        await self.bot.process_commands(msg)

    @commands.command()
    async def black(self,ctx):
        await ctx.send("White")


async def setup(bot):
    await bot.add_cog(UserCog(bot))