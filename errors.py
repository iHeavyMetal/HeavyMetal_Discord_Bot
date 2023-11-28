import discord
from discord.ext import commands

def custom_error_handler(error_message):
    async def error_handler(ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(error_message)
        else:
            raise error
    return error_handler

async def handle_admin_commands_errors(ctx, error):
    await custom_error_handler("Nie masz wystarczających uprawnień do wykonania tej komendy.")(ctx, error)