import discord
from discord.ext import commands

class BotCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ########################   Welcome DM message  ###########################

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        guildname = guild.name
        dmchannel = await member.create_dm()
        await dmchannel.send(f"Witamy na discordzie {guildname}!")  # set a welcome DM message

    ########################   Give a role  ###########################

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        emoji = payload.emoji.name
        member = payload.member
        message_id = payload.message_id
        guild_id = payload.guild_id
        guild = self.bot.get_guild(guild_id)

        if emoji == "🤘" and message_id == 1179667778261766144:       # set the emoji and message ID
            role = discord.utils.get(guild.roles, name="HeavyMetal_Fan")    #set the role name
            await member.add_roles(role)

        if emoji == "💩" and message_id == 1179669093503217725:      # set the emoji and message ID
            role = discord.utils.get(guild.roles, name="Disco_Fan")    #set the role name
            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        emoji = payload.emoji.name
        message_id = payload.message_id
        guild_id = payload.guild_id
        guild = self.bot.get_guild(guild_id)
        user_id = payload.user_id
        member = guild.get_member(user_id)
        if emoji == "🤘" and message_id == 1179667778261766144:      # set the emoji and message ID
            role = discord.utils.get(guild.roles, name="HeavyMetal_Fan")    #set the role name
            await member.remove_roles(role)

        if emoji == "💩" and message_id == 1179669093503217725:      # set the emoji and message ID
            role = discord.utils.get(guild.roles, name="Disco_Fan")    #set the role name
            await member.remove_roles(role)

async def setup(bot):
    await bot.add_cog(BotCog(bot))