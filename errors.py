import discord
from discord.ext import commands

def admin_error_handler(error_message):
    async def error_handler(ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(error_message)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Brak argumentu')
        else:
            raise error
    return error_handler

async def handle_admin_commands_errors(ctx, error):
    await admin_error_handler("Nie masz wystarczających uprawnień do wykonania tej komendy.")(ctx, error)

async def deletemessages_error_handler(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('Nie masz wystarczających uprawnień do wykonania tej komendy.')
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Musisz podać ilość wiadomości, które chcesz usunąć lub "/ dzień miesiąć"')

async def pkn_error_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Musisz wybrać jedną z emotek: 👊, ✌️ lub ✋')

