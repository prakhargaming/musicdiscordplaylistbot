# -*- coding: utf-8 -*-
"""
Created on Sat Aug 14 19:32:54 2021

@author: sinha
"""

# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)