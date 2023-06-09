#! /bin/env python3

import logging
import random

from discord import Intents
from discord.ext import commands
from discord.ext.commands import Context

from src.selection import Selection as Weekly_bluemchen


intents = Intents.default()
intents.message_content = True
intents.members         = True

blume = commands.Bot(command_prefix='reee_', intents=intents)

symbols = ['🌻', '🌹', '🌸','🌼','🌺','🏵️', '🧡']

@blume.listen()
async def on_ready() -> None:
    print(f'We have logged in as {blume.user}')

    await blume.add_cog(
            Weekly_bluemchen(
                bot = blume, 
                role = 'blümchen', 
                symbols = symbols,
            ))

@blume.command()
async def stats(ctx: Context) -> None:
    selection = blume.get_cog('Selection')
    user = ctx.author
    history = selection.__getattribute__('history')
    await ctx.send(f'{user.name} war {history[user]} unser Blümchen der Woche! {random.choice(symbols)}')

with open('credentials', 'r') as credentials:
    token   = credentials.read()
    handler = logging.FileHandler(filename='output/discord.log', encoding='utf-8', mode='w')

    blume.run(token, log_handler=handler)
