import datetime
import os
import pickle
import random

from collections import defaultdict
from typing import Sequence

from discord import Client
from discord.ext import commands, tasks
from discord.member import Member
from discord.member import Member

def isSunday() -> bool: 
    return datetime.datetime.today().weekday() == 6

class Selection(commands.Cog):
    def __init__(self, bot: Client, role: str, symbols: list[str] = [""]):
        self.bot = bot
        self.symbols = symbols

        self.set_role(role)
        self.load_history()

        self.select.start()

    def set_role(self, name: str) -> None:
        for guild in self.bot.guilds:
            for role in guild.roles:
                if role.name == name:
                    self.role = role
                    break

    utc  = datetime.timezone.utc
    time = datetime.time(hour=18, minute=0, tzinfo=utc)

    @tasks.loop(time=time)
    async def select(self) -> None:
        if not isSunday(): return

        for guild in self.bot.guilds:
            # get all members, which are not bots
            members = list(filter( lambda m: m.bot == False, guild.members))

            await self.clear_role(members)

            lucker = random.choice(members)
            await lucker.add_roles(self.role)
            await self.announce(lucker)
            self.history[lucker] += 1

    async def clear_role(self, members: Sequence[Member]) -> None:
        for member in members:
            await member.remove_roles(self.role)

    async def announce(self, member: Member) -> None:
        channel = self.bot.guilds[0].text_channels[0]
        await channel.send(f'{random.choice(self.symbols)} Unser Blümchen der Woche ist {member.name} {random.choice(self.symbols)}')

    def save_history(self) -> None:
        with open('output/history.pkl', 'wb') as file:
            pickle.dump(self.history, file)

    def load_history(self) -> None:
        if not os.path.exists('output/history.pkl'):
            self.history = defaultdict(int)
            self.save_history()

        with open('output/history.pkl', 'rb') as file:
            self.history = pickle.load(file)

