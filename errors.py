import discord
from discord.ext import commands

def admin_error_handler(error_message):
    async def error_handler(ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(error_message)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Brak argumentu')
        else:
            raise error                                                         #co to daje?
    return error_handler

async def handle_admin_commands_errors(ctx, error):                             #1!!!!!!!!!!!!!!!!!!!!!!!!!!! dlaczego nalezy zaimportować obie metody do skryptu bota? jeżeli zrobię tak jak poniżej to będzie można usunąć te dwie linie?
    await admin_error_handler("Nie masz wystarczających uprawnień do wykonania tej komendy.")(ctx, error)  #admin_error_handler jako async. Zamiast error_message tekst. Dlaczego tu jest (ctx, error)

async def deletemessages_error_handler(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('Nie masz wystarczających uprawnień do wykonania tej komendy.')
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Musisz podać ilość wiadomości, które chcesz usunąć lub "/ dzień miesiąć"')

async def pkn_error_handler(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Musisz wybrać jedną z emotek: 👊, ✌️ lub ✋')

