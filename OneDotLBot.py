from discord.ext import commands
import discord, random
from discord import app_commands
# Some API integrations from different libraries
# Spotify Integration
import spotipy
from spotipy.oauth2 import SpotifyOAuth

BOT_TOKEN="" #Enter your bot token here
SP_ID="" #Enter your Spotify ID here
SP_SECRET="" #Enter your Spotify Secret here

bot = commands.Bot(command_prefix='1.l ',intents=discord.Intents.all())
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'Bot is ready and working as {bot.user.name} - {bot.user.id}')
    await bot.tree.sync()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="onedotl.ct.ws"))

@bot.event
async def on_command_error(ctx,error):
    embed = discord.Embed(title="Error",description=f"An error occured: {error}",color=discord.Color.red())
    await ctx.reply(embed=embed)

@bot.command()
async def ping(ctx):
    await ctx.reply(f'Ping Check: {round(bot.latency*1000)}ms')

@bot.command()
async def info(ctx):
    embed = discord.Embed(title='1.L Bot',description='A bot made by EmxrDev',color=discord.Color.blue())
    embed.add_field(name='Creator',value='EmxrDev',inline=False)
    embed.add_field(name='Prefix',value="1.l (Don't forget putting space after 1.l)",inline=False)
    embed.add_field(name='Commands',value='ping, info, invite, eightball, whoiam, fakeban, rusroulette | rr, createslur, searchsong, searchartist, searchalbum, searchplaylist.\nType `1.l help <command>` to get an info about it.',inline=False)
    embed.add_field(name="Website",value="https://onedotl.ct.ws/",inline=False)
    embed.add_field(name="Other Projects",value="PackageIndex: https://onedotl.ct.ws/PackageIndex/")
    await ctx.reply(embed=embed)

@bot.tree.command(description="Get the bot's information")
async def info(i:discord.Interaction):
    embed = discord.Embed(title='1.L Bot',description='A bot made by EmxrDev',color=discord.Color.blue())
    embed.add_field(name='Creator',value='EmxrDev',inline=False)
    embed.add_field(name='Prefix',value="1.l (Don't forget putting space after 1.l)",inline=False)
    embed.add_field(name='Commands',value='ping, info, invite, eightball, whoiam, fakeban, rusroulette | rr, createslur, searchsong, searchartist, searchalbum, searchplaylist.\nType `1.l help <command>` to get an info about it.',inline=False)
    embed.add_field(name="Website",value="https://onedotl.ct.ws/",inline=False)
    embed.add_field(name="Other Projects",value="PackageIndex: https://onedotl.ct.ws/PackageIndex/")
    await i.response.reply_message(embed=embed)

@bot.command()
async def invite(ctx):
    await ctx.reply("Invite the bot to your server or use the tree commands whenever you want:\nhttps://discord.com/oauth2/authorize?client_id=1330470721876529152")

@bot.tree.command(description="Get the bot's invite link")
async def invite(i:discord.Interaction):
    await i.response.reply_message("Invite the bot to your server or use the tree commands whenever you want:\nhttps://discord.com/oauth2/authorize?client_id=1330470721876529152")

@bot.command(name="8ball")
async def eightball(ctx,*,question):
    responses = ['Yes','No','Maybe','Ask again later','I don\'t know','I\'m not sure','I can\'t answer that','I don\'t think so','I think so']
    await ctx.reply(f'Question: **{question}**\nAnswer: **{random.choice(responses)}**')

@bot.tree.command(description="Ask a question and get an answer")
@app_commands.describe(question="Question to ask")
async def eightball(i:discord.Interaction,question:str):
    responses = ['Yes','No','Maybe','Ask again later','I don\'t know','I\'m not sure','I can\'t answer that','I don\'t think so','I think so']
    await i.response.reply_message(f'Question: **{question}**\nAnswer: **{random.choice(responses)}**')

@bot.command()
async def whoiam(ctx, m:discord.Member=None):
    if m == None:
        m = ctx.author
    await ctx.reply(f'You are **{m.mention}**\nYour ID is **{m.id}**\nYour account was created at **{m.created_at}**\nYou joined this server at **{m.joined_at}**')

@bot.tree.command(description="Get information about yourself or someone else")
@app_commands.describe(member="Who to get information about (Don't mention anyone to get your own information)")
async def whoiam(i:discord.Interaction, member:discord.Member=None):
    if member == None:
        member= i.user
        await i.response.reply_message(f'You are **{member.mention}**\nYour ID is **{member.id}**\nYour account was created at **{member.created_at}**\nYou joined this server at **{member.joined_at}**')

@bot.command()
async def fakeban(ctx, member:discord.Member,*,reason=None):
    if reason == None:
        reason = 'No reason provided'
        await ctx.reply(f'{member.mention} has been banned from entire world for **{reason}**')
    else:
        await ctx.reply(f'{member.mention} has been banned from the entire world for **{reason}**!')
@bot.tree.command(description="Fake ban someone")
@app_commands.describe(member="Who to ban")
@app_commands.describe(reason="Reason for banning")
async def fakeban(i:discord.Interaction,member:discord.Member,reason:str):
    if reason == None:
        reason = 'No reason provided'
        await i.response.reply_message(f'{member.mention} has been banned from the entire world for **{reason}**!')
    else:
        await i.response.reply_message(f'{member.mention} has been banned from the entire world for **{reason}**!')
@bot.command(name="rusroulette",aliases=['rr'])
async def rusroulette(ctx,round:str=None):
    chamber = random.randint(1,6)
    if round == None:
        await ctx.reply(f'You have to choose a round to play')
    else:
        if int(round) > 6 or int(round) < 1:
            await ctx.reply(f'You can only choose a round from 1 to 6')
        else:
            if chamber == int(round):
                await ctx.reply(f'You shot yourself in the head and died. Better luck next time (in hell lol).')
            else:
                await ctx.reply(f'You survived. You were lucky this time. (Hand was {chamber})')
@bot.tree.command(description="Play Russian Roulette")
@app_commands.describe(guess="Guess the hand you want to shoot")
async def rusroulette(i:discord.Interaction,guess:str):
    chamber = random.randint(1,6)
    if guess == None:
        await i.response.reply_message(f'You have to choose a round to play')
    else:
        if int(guess) > 6 or int(guess) < 1:
            await i.response.reply_message(f'You can only choose a round from 1 to 6')
        else:
            if chamber == int(guess):
                await i.response.reply_message(f'You shot yourself in the head and died. Better luck next time (in hell lol).')
            else:
                await i.response.reply_message(f'You survived. You were lucky this time. (Hand was {chamber})')
@bot.command()
async def createslur(ctx):
    twoandfive = ['a','e','i','o','u']
    remaining = ['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','y','z']
    slur = random.choice(remaining) + random.choice(twoandfive) + random.choice(remaining) + random.choice(remaining) + random.choice(twoandfive) + random.choice(remaining)
    await ctx.reply(f"{ctx.author.mention}'s new slur is **{slur}**")
@bot.tree.command(description="Create a new slur")
async def createslur(i:discord.Interaction):
    twoandfive = ['a','e','i','o','u']
    remaining = ['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','y','z']
    slur = random.choice(remaining) + random.choice(twoandfive) + random.choice(remaining) + random.choice(remaining) + random.choice(twoandfive) + random.choice(remaining)
    await i.response.reply_message(f"{i.user.mention}'s new slur is **{slur}**")
@bot.command()
async def help(ctx:commands.Context,command=None):
    if command == None:
        embed = discord.Embed(title="Help",description="Help Submenu",color=0x00ff00)
        embed.add_field(name="",value="[Click here](https://onedotl.ct.ws/1LBot/) to view the commands of 1.L Bot",inline=False)
        embed.add_field(name="",value="Other links\n[PackageIndex](https://onedotl.ct.ws/PackageIndex/)")
        await ctx.reply(embed=embed)
    elif command == "ping":
        embed = discord.Embed(title="Help",description="Information about the ping command",color=0x00ff00)
        embed.add_field(name="Description",value="Check the bot's latency",inline=False)
        embed.add_field(name="Usage",value="`1.l ping`",inline=False)
        await ctx.reply(embed=embed)
    elif command == "info":
        embed = discord.Embed(title="Help",description="Information about the info command",color=0x00ff00)
        embed.add_field(name="Description",value="Get the bot's information",inline=False)
        embed.add_field(name="Usage",value="`1.l info`",inline=False)
        await ctx.reply(embed=embed)
    elif command == "invite":
        embed = discord.Embed(title="Help",description="Information about the invite command",color=0x00ff00)
        embed.add_field(name="Description",value="Get the bot's invite link",inline=False)
        embed.add_field(name="Usage",value="`1.l invite`",inline=False)
        await ctx.reply(embed=embed)
    elif command == "8ball":
        embed = discord.Embed(title="Help",description="Information about the 8ball command",color=0x00ff00)
        embed.add_field(name="Description",value="Ask a question and get an answer",inline=False)
        embed.add_field(name="Usage",value="`1.l 8ball <question>`",inline=False)
        await ctx.reply(embed=embed)
    elif command == "whoiam":
        embed = discord.Embed(title="Help",description="Information about the whoiam command",color=0x00ff00)
        embed.add_field(name="Description",value="Get information about yourself or someone else",inline=False)
        embed.add_field(name="Usage",value="`1.l whoiam <user>`",inline=False)
        await ctx.reply(embed=embed)
    elif command == "fakeban":
        embed = discord.Embed(title="Help",description="Information about the fakeban command",color=0x00ff00)
        embed.add_field(name="Description",value="Fakely ban a member from the server",inline=False)
        embed.add_field(name="Usage",value="`1.l fakeban <user>`",inline=False)
        await ctx.reply(embed=embed)
    elif command == "rusroulette" or command == "rr":
        embed = discord.Embed(title="Help",description="Information about the rusroulette command",color=0x00ff00)
        embed.add_field(name="Description",value="Play Russian Roulette",inline=False)
        embed.add_field(name="Usage",value="`1.l rusroulette | rr <round>`",inline=False)
        await ctx.reply(embed=embed)
    elif command == "createslur":
        embed = discord.Embed(title="Help",description="Information about the createslur command",color=0x00ff00)
        embed.add_field(name="Description",value="Create a new slur",inline=False)
        embed.add_field(name="Usage",value="`1.l createslur`",inline=False)
        await ctx.reply(embed=embed)
    elif command == "searchsong":
        embed = discord.Embed(title="Help",description="Information about the searchsong command",color=0x00ff00)
        embed.add_field(name="Description",value="Search for a song on Spotify",inline=False)
        embed.add_field(name="Usage",value="`1.l searchsong <song>`",inline=False)
        await ctx.reply(embed=embed)
    elif command == "searchartist":
        embed = discord.Embed(title="Help",description="Information about the searchartist command",color= 0x00ff00)
        embed.add_field(name="Description",value="Search for an artist on Spotify",inline=False)
        embed.add_field(name="Usage",value="`1.l searchartist <artist>`",inline=False)
        await ctx.reply(embed=embed)
    elif command == "searchalbum":
        embed = discord.Embed(title="Help",description="Information about the searchalbum command",color=0x00ff00)
        embed.add_field(name="Description",value="Search for an album on Spotify",inline=False)
        embed.add_field(name="Usage",value="`1.l searchalbum <album>`",inline=False)
        await ctx.reply(embed=embed)
    elif command == "searchplaylist":
        embed = discord.Embed(title="Help",description="Information about the searchplaylist command",color=0x00ff00)
        embed.add_field(name="Description",value="Search for a playlist on Spotify",inline=False)
        embed.add_field(name="Usage",value="`1.l searchplaylist <playlist>`",inline=False)
        await ctx.reply(embed=embed)
    elif command=="pypi":
        embed = discord.Embed(title="Help",description="Information about the pypi command",color=0x00ff00)
        embed.add_field(name="Description",value="Search for a package on PyPI",inline=False)
        embed.add_field(name="Usage",value="`1.l pypi <package>`",inline=False)
        await ctx.reply(embed=embed)
    elif command=="apt":
        embed = discord.Embed(title="Help",description="Information about the apt command",color=0x00ff00)
        embed.add_field(name="Description",value="Search for a package on APT",inline=False)
        embed.add_field(name="Usage",value="`1.l apt <package>`",inline=False)
        await ctx.reply(embed=embed)
    elif command=="winget":
        embed = discord.Embed(title="Help",description="Information about the winget command",color=0x00ff00)
        embed.add_field(name="Description",value="Search for a package on Winget",inline=False)
        embed.add_field(name="Usage",value="`1.l winget <package>`",inline=False)
        await ctx.reply(embed=embed)
    else:
        given_command = (ctx.message.content).replace("1.l help ","")
        embed = discord.Embed(title="Help",description=f"Command {given_command} not found.",color=0xff0000)
        await ctx.reply(embed=embed)

# Spotify Commands

@bot.command()
async def searchsong(ctx,*,song):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="SP_ID",client_secret="SP_SECRET",redirect_uri="https://spotify.com/"))
    results = sp.search(q=song,limit=1)
    song = results['tracks']['items'][0]
    seconds = int(song['duration_ms'] / 1000)
    minutes = int(seconds / 60)
    real_seconds = seconds % 60
    if len(str(real_seconds)) == 1:
        real_seconds = f"0{real_seconds}"
    duration = f"{minutes}:{real_seconds}"
    embed = discord.Embed(title=song['name'],description=song['artists'][0]['name'],color=discord.Color.green())
    embed.set_thumbnail(url=song['album']['images'][0]['url'])
    embed.add_field(name="Album",value=song['album']['name'],inline=False)
    embed.add_field(name="Duration",value=str(duration),inline=False)
    embed.add_field(name="Release Date",value=song['album']['release_date'],inline=False)
    embed.add_field(name="Listen on Spotify",value=f"[Click here]({song['external_urls']['spotify']})",inline=False)
    await ctx.reply(embed=embed)
@bot.tree.command(description="Search for a song on Spotify")
@app_commands.describe(song="Song to search")
async def searchsong(i:discord.Interaction,*,song:str):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="SP_ID",client_secret="SP_SECRET",redirect_uri="https://spotify.com/"))
    results = sp.search(q=song,limit=1)
    song = results['tracks']['items'][0]
    seconds = int(song['duration_ms'] / 1000)
    minutes = int(seconds / 60)
    real_seconds = seconds % 60
    if len(str(real_seconds)) == 1:
        real_seconds = f"0{real_seconds}"
    duration = f"{minutes}:{real_seconds}"
    embed = discord.Embed(title=song['name'],description=song['artists'][0]['name'],color=discord.Color.green())
    embed.set_thumbnail(url=song['album']['images'][0]['url'])
    embed.add_field(name="Album",value=song['album']['name'],inline=False)
    embed.add_field(name="Duration",value=str(duration),inline=False)
    embed.add_field(name="Release Date",value=song['album']['release_date'],inline=False)
    embed.add_field(name="Listen on Spotify",value=f"[Click here]({song['external_urls']['spotify']})",inline=False)
    await i.response.reply_message(embed=embed)
    
@bot.command()
async def searchartist(ctx,*,artist):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="SP_ID",client_secret="SP_SECRET",redirect_uri="https://spotify.com/"))
    results = sp.search(q=artist,limit=1,type='artist')
    if results['artists']['items'] == []:
        await ctx.reply(f'Artist not found')
    else:
        user = results['artists']['items'][0]
        embed = discord.Embed(title=user['name'],description=user['genres'][0],color=discord.Color.green())
        embed.set_thumbnail(url=user['images'][0]['url'])
        embed.add_field(name="Followers",value=user['followers']['total'],inline=False)
        embed.add_field(name="Popularity",value=user['popularity'],inline=False)
        embed.add_field(name="Listen on Spotify",value=f"[Click here]({user['external_urls']['spotify']})",inline=False)
        await ctx.reply(embed=embed)
@bot.tree.command(description="Search for an artist on Spotify")
@app_commands.describe(artist="Artist to search")
async def searchartist(i:discord.Interaction,*,artist:str):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="SP_ID",client_secret="SP_SECRET",redirect_uri="https://spotify.com/"))
    results = sp.search(q=artist,limit=1,type='artist')
    if results['artists']['items'] == []:
        await i.response.reply_message(f'Artist not found')
    else:
        user = results['artists']['items'][0]
        embed = discord.Embed(title=user['name'],description=user['genres'][0],color=discord.Color.green())
        embed.set_thumbnail(url=user['images'][0]['url'])
        embed.add_field(name="Followers",value=user['followers']['total'],inline=False)
        embed.add_field(name="Popularity",value=user['popularity'],inline=False)
        embed.add_field(name="Listen on Spotify",value=f"[Click here]({user['external_urls']['spotify']})",inline=False)
        await i.response.reply_message(embed=embed)
@bot.command()
async def searchalbum(ctx,*,album):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="SP_ID",client_secret="SP_SECRET",redirect_uri="https://spotify.com/"))  
    results = sp.search(q=album,limit=1,type='album')
    if results['albums']['items'] == []:
        await ctx.reply(f'Album not found')
    else:
        user = results['albums']['items'][0]
        embed = discord.Embed(title=user['name'],description=user['artists'][0]['name'],color=discord.Color.green())
        embed.set_thumbnail(url=user['images'][0]['url'])
        embed.add_field(name="Release Date",value=user['release_date'],inline=False)
        embed.add_field(name="Total Tracks",value=user['total_tracks'],inline=False)
        embed.add_field(name="Listen on Spotify",value=f"[Click here]({user['external_urls']['spotify']})",inline=False)
        await ctx.reply(embed=embed)
@bot.tree.command(description="Search for an album on Spotify")
@app_commands.describe(album="Album to search")
async def searchalbum(i:discord.Interaction,*,album:str):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="SP_ID",client_secret="SP_SECRET",redirect_uri="https://spotify.com/"))  
    results = sp.search(q=album,limit=1,type='album')
    if results['albums']['items'] == []:
        await i.response.reply_message(f'Album not found')
    else:
        user = results['albums']['items'][0]
        embed = discord.Embed(title=user['name'],description=user['artists'][0]['name'],color=discord.Color.green())
        embed.set_thumbnail(url=user['images'][0]['url'])
        embed.add_field(name="Release Date",value=user['release_date'],inline=False)
        embed.add_field(name="Total Tracks",value=user['total_tracks'],inline=False)
        embed.add_field(name="Listen on Spotify",value=f"[Click here]({user['external_urls']['spotify']})",inline=False)
        await i.response.reply_message(embed=embed)
@bot.command()
async def searchplaylist(ctx,*,playlist):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="SP_ID",client_secret="SP_SECRET",redirect_uri="https://spotify.com/"))  
    results = sp.search(q=playlist,limit=1,type='playlist')
    if results['playlists']['items'] == []:
        await ctx.reply(f'Playlist not found')
    else:
        user = results['playlists']['items'][0]
        embed = discord.Embed(title=user['name'],description=user['description'],color=discord.Color.green())
        embed.set_thumbnail(url=user['images'][0]['url'])
        embed.add_field(name="Total Tracks",value=user['tracks']['total'],inline=False)
        embed.add_field(name="Owner",value=user['owner']['display_name'],inline=False)
        embed.add_field(name="Listen on Spotify",value=f"[Click here]({user['external_urls']['spotify']})",inline=False)
        await ctx.reply(embed=embed)
@bot.tree.command(description="Search for a playlist on Spotify")
@app_commands.describe(playlist="Playlist to search")
async def searchplaylist(i:discord.Interaction,*,playlist:str):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="SP_ID",client_secret="SP_SECRET",redirect_uri="https://spotify.com/"))
    results = sp.search(q=playlist,limit=1,type='playlist')
    if results['playlists']['items'] == []:
        await i.response.reply_message(f'Playlist not found')
    else:
        user = results['playlists']['items'][0]
        embed = discord.Embed(title=user['name'],description=user['description'],color=discord.Color.green())
        embed.set_thumbnail(url=user['images'][0]['url'])
        embed.add_field(name="Total Tracks",value=user['tracks']['total'],inline=False)
        embed.add_field(name="Owner",value=user['owner']['display_name'],inline=False)
        embed.add_field(name="Listen on Spotify",value=f"[Click here]({user['external_urls']['spotify']})",inline=False)
        await i.response.reply_message(embed=embed)

# PackageIndex Integration
@bot.command()
async def pypi(ctx,*,pack):
    url = f"https://pypi.org/project/{pack}/"
    embed = discord.Embed(title=f"{pack} on PyPI",description=f"Check out {url} for more info",color=discord.Color.green())
    embed.set_thumbnail(url="https://onedotl.ct.ws/1LBot/assets/PyPI-Logo-notext.svg.png")
    await ctx.reply(embed=embed)
@bot.tree.command(name="pypi",description="View a Python package on PyPI")
@app_commands.describe(pack="Package to view")
async def pypi(i:discord.Interaction,*,pack:str):
    url = f"https://pypi.org/project/{pack}/"
    embed = discord.Embed(title=f"{pack} on PyPI",description=f"Check out {url} for more info",color=discord.Color.green())
    embed.set_thumbnail(url="https://onedotl.ct.ws/1LBot/assets/PyPI-Logo-notext.svg.png")
    await i.response.reply_message(embed=embed)
@bot.command()
async def apt(ctx,*,pack):
    url = f"https://packages.ubuntu.com/search?keywords={pack}&searchon=names&suite=focal&section=all"
    embed = discord.Embed(title=f"{pack} on Ubuntu",description=f"Check out {url} for more info",color=discord.Color.green())
    embed.set_thumbnail(url="https://onedotl.ct.ws/1LBot/assets/ubuntu-logo.png")
    await ctx.reply(embed=embed)
@bot.tree.command(name="apt",description="View a package on Ubuntu")
@app_commands.describe(pack="Package to view")
async def apt(i:discord.Interaction,*,pack:str):
    url = f"https://packages.ubuntu.com/search?keywords={pack}&searchon=names&suite=focal&section=all"
    embed = discord.Embed(title=f"{pack} on Ubuntu",description=f"Check out {url} for more info",color=discord.Color.green())
    embed.set_thumbnail(url="https://onedotl.ct.ws/1LBot/assets/ubuntu-logo.png")
    await i.response.reply_message(embed=embed)
@bot.command()
async def winget(ctx,*,pack):
    url = f"https://winget.run/search?query={pack}"
    embed = discord.Embed(title=f"{pack} on Winget",description=f"Check out {url} for more info",color=discord.Color.green())
    embed.set_thumbnail(url="https://onedotl.ct.ws/1LBot/assets/winget-logo.png")
    await ctx.reply(embed=embed)
@bot.tree.command(name="winget",description="View a package on Winget")
@app_commands.describe(pack="Package to view")
async def winget(i:discord.Interaction,*,pack:str):
    url = f"https://winget.run/search?query={pack}"
    embed = discord.Embed(title=f"{pack} on Winget",description=f"Check out {url} for more info",color=discord.Color.green())
    embed.set_thumbnail(url="https://onedotl.ct.ws/1LBot/assets/winget-logo.png")
    await i.response.reply_message(embed=embed)
bot.run(BOT_TOKEN)