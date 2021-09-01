"""
Created on Mon Jul 26 16:46:21 2021

@author: Prakhar Sinha
contact yungdaggerprakhar#9381 on Discord for help!
"""

import os

import discord
from dotenv import load_dotenv

import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CLIENT_ID = os.getenv('client_id')
CLIENT_SECRET = os.getenv('client_secret')
REDIRECT_URI = os.getenv('redirect_uri')
SCOPE = os.getenv('scope')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

#all pertinant client information is stored in a dictionary under this format
#{'Guild Name':[READY, playlist_message, collective_playlist, channel_scope]}
client_dictionary = {}

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):

    if client_dictionary[message.guild][0] != True and message.content.lower() == "^setup playlist bot":
         client_dictionary[message.guild] = [False, 'Playlist Message', 'Collective Playlist', []] 

         await message.channel.send("You have not configured the playlist bot yet! Would you like to? [y/n]")
         async def on_message(new_message):
             if new_message.content.lower() == "y":
                 new_message.channel.send("""What channels do you want this bot have access to? Note that you will have
                 manually give the bot access to these channels after this. Type the exact name of the channels (CaSe_SensITVe). After you 
                 typed the name of all channels, type "exit" to continue setup.""")
                 while True:
                     async def on_message(newer_message):
                         if newer_message.content.lower() == "exit":
                             break
                         else:
                             client_dictionary[message.guild][3].append(newer_message)
                 new_message.channel.send("""What channels do you want this bot have access to? Note that you will have
                 manually give the bot access to these channels after this. Type the exact name of the channels (CaSe_SensITVe). After you 
                 typed the name of all channels, type "exit" to continue setup.""")



    playlist_message = "Here's the DAC Collective Playlist "
    collective_playlist = "https://open.spotify.com/playlist/4c8FH7aJ1zZFEfRo3sZ0Hw?si=39b55fd759964ebf"
    channel_scope = ["music-recs"]

    if message.author == client.user:
        return
    
    if message.content.lower() == "^dac playlist":
        await message.channel.send(playlist_message + collective_playlist)
    
    try: 
        if message.content.startswith("https://open.spotify") == True:
            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                           client_secret=CLIENT_SECRET,
                                                           redirect_uri=REDIRECT_URI,
                                                           scope=SCOPE))
            sp.playlist_remove_all_occurrences_of_items(collective_playlist, [message.content])
            sp.playlist_add_items(collective_playlist, [message.content])
    except:
        if str(message.channel) in channel_scope:
            await message.channel.send("Something went wrong. Prakhar messed up probably or maybe the link you provided was wrong.")
        raise discord.DiscordException

client.run(TOKEN)