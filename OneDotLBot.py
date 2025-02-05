from discord.ext import commands
import discord, random, subprocess, os
from discord import app_commands
# Some API integrations from different libraries
# Spotify Integration
import spotipy
from spotipy.oauth2 import SpotifyOAuth
# Youtube Music Integration
import yt_dlp
# waifu.pics Integration
from waifu import WaifuClient
waifuclient = WaifuClient()
ytdl_format_options = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'quiet': True,
}
ydl = yt_dlp.YoutubeDL(ytdl_format_options)

BOT_TOKEN="ENTER YOUR BOT TOKEN HERE"

bot = commands.Bot(command_prefix='1.l ',intents=discord.Intents.all())
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'Bot is ready and working as {bot.user.name} - {bot.user.id}')
    await bot.tree.sync()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="onedotl.ct.ws"))

@bot.event
async def on_command_error(ctx:commands.Context,error):
    command = (ctx.message.content).replace("1.l ","")
    embed = discord.Embed(title=f"Oops! Command `{command}` raised an error",description=f"Error info: {error}",color=discord.Color.red())
    await ctx.reply(embed=embed)

@bot.command()
async def ping(ctx):
    await ctx.reply(f'Ping Check: {round(bot.latency*1000)}ms')

@bot.command()
async def info(ctx):
    embed = discord.Embed(title='1.L Bot',description='A bot made by EmxrDev',color=discord.Color.blue())
    embed.set_thumbnail(url="https://imgur.com/XjNwixm.png")
    embed.add_field(name='Creator',value='EmxrDev',inline=False)
    embed.add_field(name='Prefix',value="1.l (Don't forget putting space after 1.l)",inline=False)
    embed.add_field(name='Commands',value='ping, info, invite, eightball, whoiam, fakeban, rusroulette | rr, createslur, searchsong, searchartist, searchalbum, searchplaylist.\nType `1.l help <command>` to get an info about it.',inline=False)
    embed.add_field(name="Website",value="https://onedotl.ct.ws/",inline=False)
    embed.add_field(name="Other Projects",value="PackageIndex: https://onedotl.ct.ws/PackageIndex/")
    await ctx.reply(embed=embed)

@bot.tree.command(description="Get the bot's information")
async def info(i:discord.Interaction):
    embed = discord.Embed(title='1.L Bot',description='A bot made by EmxrDev',color=discord.Color.blue())
    embed.set_thumbnail(url="https://imgur.com/XjNwixm.png")
    embed.add_field(name='Creator',value='EmxrDev',inline=False)
    embed.add_field(name='Prefix',value="1.l (Don't forget putting space after 1.l)",inline=False)
    embed.add_field(name='Commands',value='ping, info, invite, eightball, whoiam, fakeban, rusroulette | rr, createslur, searchsong, searchartist, searchalbum, searchplaylist.\nType `1.l help <command>` to get an info about it.',inline=False)
    embed.add_field(name="Website",value="https://onedotl.ct.ws/",inline=False)
    embed.add_field(name="Other Projects",value="PackageIndex: https://onedotl.ct.ws/PackageIndex/")
    await i.response.send_message(embed=embed)

@bot.command()
async def invite(ctx):
    await ctx.reply("Invite the bot to your server or use the tree commands whenever you want:\nhttps://discord.com/oauth2/authorize?client_id=1330470721876529152")

@bot.tree.command(description="Get the bot's invite link")
async def invite(i:discord.Interaction):
    await i.response.send_message("Invite the bot to your server or use the tree commands whenever you want:\nhttps://discord.com/oauth2/authorize?client_id=1330470721876529152")

@bot.command(name="8ball")
async def eightball(ctx,*,question):
    responses = ['Yes','No','Maybe','Ask again later','I don\'t know','I\'m not sure','I can\'t answer that','I don\'t think so','I think so']
    await ctx.reply(f'Question: **{question}**\nAnswer: **{random.choice(responses)}**')

@bot.tree.command(description="Ask a question and get an answer")
@app_commands.describe(question="Question to ask")
async def eightball(i:discord.Interaction,question:str):
    responses = ['Yes','No','Maybe','Ask again later','I don\'t know','I\'m not sure','I can\'t answer that','I don\'t think so','I think so']
    await i.response.send_message(f'Question: **{question}**\nAnswer: **{random.choice(responses)}**')

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
        await i.response.send_message(f'You are **{member.mention}**\nYour ID is **{member.id}**\nYour account was created at **{member.created_at}**\nYou joined this server at **{member.joined_at}**')

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
        await i.response.send_message(f'{member.mention} has been banned from the entire world for **{reason}**!')
    else:
        await i.response.send_message(f'{member.mention} has been banned from the entire world for **{reason}**!')
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
        await i.response.send_message(f'You have to choose a round to play')
    else:
        if int(guess) > 6 or int(guess) < 1:
            await i.response.send_message(f'You can only choose a round from 1 to 6')
        else:
            if chamber == int(guess):
                await i.response.send_message(f'You shot yourself in the head and died. Better luck next time (in hell lol).')
            else:
                await i.response.send_message(f'You survived. You were lucky this time. (Hand was {chamber})')
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
    await i.response.send_message(f"{i.user.mention}'s new slur is **{slur}**")
@bot.command()
async def help(ctx:commands.Context,command=None,only_w=None):
    if command == None:
        embed = discord.Embed(title="Help",description="Help Submenu",color=0x00ff00)
        embed.set_thumbnail (url="https://imgur.com/XjNwixm.png")
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
    elif command=="play":
        embed = discord.Embed(title="Help",description="Information about the play command",color=0x00ff00)
        embed.add_field(name="Description",value="Play a song on 1.L FM",inline=False)
        embed.add_field(name="Usage",value="`1.l play <song>`",inline=False)
        await ctx.reply(embed=embed)
    elif command=="stop":
        embed = discord.Embed(title="Help",description="Information about the stop command",color=0x00ff00)
        embed.add_field(name="Description",value="Stop the current song on 1.L FM", inline=False)
        embed.add_field(name="Usage",value="`1.l stop`",inline=False)
        await ctx.reply(embed=embed)
    elif command=="leave":
        embed = discord.Embed(title="Help",description="Information about the leave command",color=0x00ff00)
        embed.add_field(name="Description",value="Leave the voice channel", inline=False)
        embed.add_field(name="Usage",value="`1.l leave`",inline=False)
        await ctx.reply(embed=embed)
    elif command=="w":
        if only_w==None:
            embed = discord.Embed(title="Help",description="Information about the w command",color=0x00ff00)
            embed.add_field(name="Description",value="Search for waifu's",inline=False)
            embed.add_field(name="Usage",value="1.l w<category> ['approve' if wkill]",inline=False)
            embed.set_footer(text="Use '1.l help w category' to view categories")
            await ctx.reply(embed=embed)
        elif only_w=="category":
            embed = discord.Embed(title="waifu.pics Categories",description="Categories for the w command")
            embed.add_field(name="Categories",value="'waifu','neko','shinobu','megumin','bully','cuddle','cry','hug','awoo','kiss','lick','pat','smug','bonk','yeet','blush','smile','wave','highfive','handhold','nom','bite','glomp','slap','kill','kick','happy','wink','poke','dance','cringe'",inline=False)
            embed.add_field(name="Commands",value="'waifu','wneko','wshinobu','wmegumin','wbully','wcuddle','wcry','whug','wawoo','wkiss','wlick','wpat','wsmug','wbonk','wyeet','wblush','wsmile','wwave','whighfive','whandhold','wnom','wbite','wglomp','wslap','wkill approve','wkick','whappy','wwink','wpoke','wdance','wcringe','wrandom'",inline=False)
            await ctx.reply(embed=embed)
    else:
        given_command = (ctx.message.content).replace("1.l help ","")
        embed = discord.Embed(title="Help",description=f"Command {given_command} not found.",color=0xff0000)
        await ctx.reply(embed=embed)
@bot.tree.command(name="help",description="Search for a command's help page")
@app_commands.describe(command="Command to view the help page")
async def help(i:discord.Interaction,command:str):
    if command == None:
        embed = discord.Embed(title="Help",description="Help Submenu",color=0x00ff00)
        embed.add_field(name="",value="[Click here](https://onedotl.ct.ws/1LBot/) to view the commands of 1.L Bot",inline=False)
        embed.add_field(name="",value="Other links\n[PackageIndex](https://onedotl.ct.ws/PackageIndex/)")
        await i.response.send_message(embed=embed)
    elif command == "ping":
        embed = discord.Embed(title="Help",description="Information about the ping command",color=0x00ff00)
        embed.add_field(name="Description",value="Check the bot's latency",inline=False)
        embed.add_field(name="Usage",value="`1.l ping`",inline=False)
        await i.response.send_message(embed=embed)
    elif command == "info":
        embed = discord.Embed(title="Help",description="Information about the info command",color=0x00ff00)
        embed.add_field(name="Description",value="Get the bot's information",inline=False)
        embed.add_field(name="Usage",value="`1.l info`",inline=False)
        await i.response.send_message(embed=embed)
    elif command == "invite":
        embed = discord.Embed(title="Help",description="Information about the invite command",color=0x00ff00)
        embed.add_field(name="Description",value="Get the bot's invite link",inline=False)
        embed.add_field(name="Usage",value="`1.l invite`",inline=False)
        await i.response.send_message(embed=embed)
    elif command == "8ball":
        embed = discord.Embed(title="Help",description="Information about the 8ball command",color=0x00ff00)
        embed.add_field(name="Description",value="Ask a question and get an answer",inline=False)
        embed.add_field(name="Usage",value="`1.l 8ball <question>`",inline=False)
        await i.response.send_message(embed=embed)
    elif command == "whoiam":
        embed = discord.Embed(title="Help",description="Information about the whoiam command",color=0x00ff00)
        embed.add_field(name="Description",value="Get information about yourself or someone else",inline=False)
        embed.add_field(name="Usage",value="`1.l whoiam <user>`",inline=False)
        await i.response.send_message(embed=embed)
    elif command == "fakeban":
        embed = discord.Embed(title="Help",description="Information about the fakeban command",color=0x00ff00)
        embed.add_field(name="Description",value="Fakely ban a member from the server",inline=False)
        embed.add_field(name="Usage",value="`1.l fakeban <user>`",inline=False)
        await i.response.send_message(embed=embed)
    elif command == "rusroulette" or command == "rr":
        embed = discord.Embed(title="Help",description="Information about the rusroulette command",color=0x00ff00)
        embed.add_field(name="Description",value="Play Russian Roulette",inline=False)
        embed.add_field(name="Usage",value="`1.l rusroulette | rr <round>`",inline=False)
        await i.response.send_message(embed=embed)
    elif command == "createslur":
        embed = discord.Embed(title="Help",description="Information about the createslur command",color=0x00ff00)
        embed.add_field(name="Description",value="Create a new slur",inline=False)
        embed.add_field(name="Usage",value="`1.l createslur`",inline=False)
        await i.response.send_message(embed=embed)
    elif command == "searchsong":
        embed = discord.Embed(title="Help",description="Information about the searchsong command",color=0x00ff00)
        embed.add_field(name="Description",value="Search for a song on Spotify",inline=False)
        embed.add_field(name="Usage",value="`1.l searchsong <song>`",inline=False)
        await i.response.send_message(embed=embed)
    elif command == "searchartist":
        embed = discord.Embed(title="Help",description="Information about the searchartist command",color= 0x00ff00)
        embed.add_field(name="Description",value="Search for an artist on Spotify",inline=False)
        embed.add_field(name="Usage",value="`1.l searchartist <artist>`",inline=False)
        await i.response.send_message(embed=embed)
    elif command == "searchalbum":
        embed = discord.Embed(title="Help",description="Information about the searchalbum command",color=0x00ff00)
        embed.add_field(name="Description",value="Search for an album on Spotify",inline=False)
        embed.add_field(name="Usage",value="`1.l searchalbum <album>`",inline=False)
        await i.response.send_message(embed=embed)
    elif command == "searchplaylist":
        embed = discord.Embed(title="Help",description="Information about the searchplaylist command",color=0x00ff00)
        embed.add_field(name="Description",value="Search for a playlist on Spotify",inline=False)
        embed.add_field(name="Usage",value="`1.l searchplaylist <playlist>`",inline=False)
        await i.response.send_message(embed=embed)
    elif command=="pypi":
        embed = discord.Embed(title="Help",description="Information about the pypi command",color=0x00ff00)
        embed.add_field(name="Description",value="Search for a package on PyPI",inline=False)
        embed.add_field(name="Usage",value="`1.l pypi <package>`",inline=False)
        await i.response.send_message(embed=embed)
    elif command=="apt":
        embed = discord.Embed(title="Help",description="Information about the apt command",color=0x00ff00)
        embed.add_field(name="Description",value="Search for a package on APT",inline=False)
        embed.add_field(name="Usage",value="`1.l apt <package>`",inline=False)
        await i.response.send_message(embed=embed)
    elif command=="winget":
        embed = discord.Embed(title="Help",description="Information about the winget command",color=0x00ff00)
        embed.add_field(name="Description",value="Search for a package on Winget",inline=False)
        embed.add_field(name="Usage",value="`1.l winget <package>`",inline=False)
        await i.response.send_message(embed=embed)
    elif command=="play":
        embed = discord.Embed(title="Help",description="Information about the play command",color=0x00ff00)
        embed.add_field(name="Description",value="Play a song on 1.L FM",inline=False)
        embed.add_field(name="Usage",value="`1.l play <song>`",inline=False)
        await i.response.send_message(embed=embed)
    elif command=="stop":
        embed = discord.Embed(title="Help",description="Information about the stop command",color=0x00ff00)
        embed.add_field(name="Description",value="Stop the current song on 1.L FM", inline=False)
        embed.add_field(name="Usage",value="`1.l stop`",inline=False)
        await i.response.send_message(embed=embed)
    elif command=="leave":
        embed = discord.Embed(title="Help",description="Information about the leave command",color=0x00ff00)
        embed.add_field(name="Description",value="Leave the voice channel", inline=False)
        embed.add_field(name="Usage",value="`1.l leave`",inline=False)
        await i.response.send_message(embed=embed)
    elif command=="waifu":
        embed = discord.Embed(title="Help",value="Information about the waifu command",color=0x00ff00)
        embed.add_field(name="Description",value="Find some waifus on waifu.pics")
        embed.add_field(name="Usage",value="1.l waifu <category>")
        embed.set_footer("see /help waifucategory for categories")
    elif command=="waifucategory":
        embed = discord.Embed(title="waifu.pics Categories",description="Categories for the waifu command")
        embed.add_field(name="Categories",value="'waifu','neko','shinobu','megumin','bully','cuddle','cry','hug','awoo','kiss','lick','pat','smug','bonk','yeet','blush','smile','wave','highfive','handhold','nom','bite','glomp','slap','kill','kick','happy','wink','poke','dance','cringe'",inline=False)
        await i.response.send_message(embed=embed)
    else:
        embed = discord.Embed(title="Help",description=f"Command {command} not found.",color=0xff0000)
        await i.response.send_message(embed=embed)

# Spotify Commands

@bot.command()
async def searchsong(ctx,*,song):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="6721a7c2e0324de79394d67a6e54bb87",client_secret="4b4b4bbf2ad9489a9fdaf70888445c05",redirect_uri="https://spotify.com/"))
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
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="6721a7c2e0324de79394d67a6e54bb87",client_secret="4b4b4bbf2ad9489a9fdaf70888445c05",redirect_uri="https://spotify.com/"))
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
    await i.response.send_message(embed=embed)
    
@bot.command()
async def searchartist(ctx,*,artist):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="6721a7c2e0324de79394d67a6e54bb87",client_secret="4b4b4bbf2ad9489a9fdaf70888445c05",redirect_uri="https://spotify.com/"))  
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
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="6721a7c2e0324de79394d67a6e54bb87",client_secret="4b4b4bbf2ad9489a9fdaf70888445c05",redirect_uri="https://spotify.com/"))  
    results = sp.search(q=artist,limit=1,type='artist')
    if results['artists']['items'] == []:
        await i.response.send_message(f'Artist not found')
    else:
        user = results['artists']['items'][0]
        embed = discord.Embed(title=user['name'],description=user['genres'][0],color=discord.Color.green())
        embed.set_thumbnail(url=user['images'][0]['url'])
        embed.add_field(name="Followers",value=user['followers']['total'],inline=False)
        embed.add_field(name="Popularity",value=user['popularity'],inline=False)
        embed.add_field(name="Listen on Spotify",value=f"[Click here]({user['external_urls']['spotify']})",inline=False)
        await i.response.send_message(embed=embed)
@bot.command()
async def searchalbum(ctx,*,album):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="6721a7c2e0324de79394d67a6e54bb87",client_secret="4b4b4bbf2ad9489a9fdaf70888445c05",redirect_uri="https://spotify.com/"))  
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
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="6721a7c2e0324de79394d67a6e54bb87",client_secret="4b4b4bbf2ad9489a9fdaf70888445c05",redirect_uri="https://spotify.com/"))  
    results = sp.search(q=album,limit=1,type='album')
    if results['albums']['items'] == []:
        await i.response.send_message(f'Album not found')
    else:
        user = results['albums']['items'][0]
        embed = discord.Embed(title=user['name'],description=user['artists'][0]['name'],color=discord.Color.green())
        embed.set_thumbnail(url=user['images'][0]['url'])
        embed.add_field(name="Release Date",value=user['release_date'],inline=False)
        embed.add_field(name="Total Tracks",value=user['total_tracks'],inline=False)
        embed.add_field(name="Listen on Spotify",value=f"[Click here]({user['external_urls']['spotify']})",inline=False)
        await i.response.send_message(embed=embed)
@bot.command()
async def searchplaylist(ctx,*,playlist):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="6721a7c2e0324de79394d67a6e54bb87",client_secret="4b4b4bbf2ad9489a9fdaf70888445c05",redirect_uri="https://spotify.com/"))  
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
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="6721a7c2e0324de79394d67a6e54bb87",client_secret="4b4b4bbf2ad9489a9fdaf70888445c05",redirect_uri="https://spotify.com/"))  
    results = sp.search(q=playlist,limit=1,type='playlist')
    if results['playlists']['items'] == []:
        await i.response.send_message(f'Playlist not found')
    else:
        user = results['playlists']['items'][0]
        embed = discord.Embed(title=user['name'],description=user['description'],color=discord.Color.green())
        embed.set_thumbnail(url=user['images'][0]['url'])
        embed.add_field(name="Total Tracks",value=user['tracks']['total'],inline=False)
        embed.add_field(name="Owner",value=user['owner']['display_name'],inline=False)
        embed.add_field(name="Listen on Spotify",value=f"[Click here]({user['external_urls']['spotify']})",inline=False)
        await i.response.send_message(embed=embed)

# PackageIndex Integration

@bot.command()
async def pypi(ctx,*,pack):
    url = f"https://pypi.org/project/{pack}/"
    embed = discord.Embed(title=f"<:packageindex:1335205813060505672> PackageIndex",description=f"<:pypi:1335205628116729886> PyPI",color=discord.Color.green())
    embed.add_field(name=f"{pack} on PyPI",value=f"Check out {url} for more info")
    await ctx.reply(embed=embed)
@bot.tree.command(name="pypi",description="View a Python package on PyPI")
@app_commands.describe(pack="Package to view")
async def pypi(i:discord.Interaction,*,pack:str):
    url = f"https://pypi.org/project/{pack}/"
    embed = discord.Embed(title=f"<:packageindex:1335205813060505672> PackageIndex",description=f"<:pypi:1335205628116729886> PyPI",color=discord.Color.green())
    embed.add_field(name=f"{pack} on PyPI",value=f"Check out {url} for more info")
    await i.response.send_message(embed=embed)
@bot.command()
async def apt(ctx,*,pack):
    url = f"https://packages.ubuntu.com/search?keywords={pack}&searchon=names&suite=focal&section=all"
    embed = discord.Embed(title=f"<:packageindex:1335205813060505672> PackageIndex",description=f"<:ubuntu:1335205642054664265> APT (Ubuntu)",color=discord.Color.green())
    embed.add_field(name=f"{pack} on APT (Ubuntu)",value=f"Check out {url} for more info")
    await ctx.reply(embed=embed)
@bot.tree.command(name="apt",description="View a package on APT (Ubuntu)")
@app_commands.describe(pack="Package to view")
async def apt(i:discord.Interaction,*,pack:str):
    url = f"https://packages.ubuntu.com/search?keywords={pack}&searchon=names&suite=focal&section=all"
    embed = discord.Embed(title=f"<:packageindex:1335205813060505672> PackageIndex",description=f"<:ubuntu:1335205642054664265> APT (Ubuntu)",color=discord.Color.green())
    embed.add_field(name=f"{pack} on APT (ubuntu)",value=f"Check out {url} for more info")
    await i.response.send_message(embed=embed)
@bot.command()
async def winget(ctx,*,pack):
    url = f"https://winget.run/search?query={pack}"
    embed = discord.Embed(title=f"<:packageindex:1335205813060505672> PackageIndex",description=f"<:winget:1335205653605515355> WinGet",color=discord.Color.green())
    embed.add_field(name=f"{pack} on WinGet",value=f"Check out {url} for more info")
    await ctx.reply(embed=embed)
@bot.tree.command(name="winget",description="View a package on Winget")
@app_commands.describe(pack="Package to view")
async def winget(i:discord.Interaction,*,pack:str):
    url = f"https://winget.run/search?query={pack}"
    embed = discord.Embed(title=f"<:packageindex:1335205813060505672> PackageIndex",description=f"<:winget:1335205653605515355> WinGet",color=discord.Color.green())
    embed.add_field(name=f"{pack} on WinGet",value=f"Check out {url} for more info")
    await i.response.send_message(embed=embed)

# Music player commands

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
        await ctx.voice_client.disconnect()
        embed= discord.Embed(title="<:radio:1335306029231112282> 1.L FM",description="<:exit:1335310968204562474> Left the voice channel",color=discord.Color.red())
        await ctx.reply(embed=embed)
    else:
        embed= discord.Embed(title="<:radio:1335306029231112282> 1.L FM", description="<:noplay:1335309663259987968> Not in a voice channel",color=discord.Color.red())
        await ctx.reply(embed=embed)
@bot.command()
async def play(ctx, *, search_query):
    if ctx.author.voice:
        if ctx.voice_client is None:
            vc = await ctx.author.voice.channel.connect()
        else:
            vc = ctx.voice_client
        embed=discord.Embed(title="<:radio:1335306029231112282> 1.L FM",description=f"Searching `{search_query}` on 1.L FM...",color=discord.Color.green())
        await ctx.send(embed=embed)
    else:
        embed1=discord.Embed(title="Error",description="You must need to be in a voice channel")
        return
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'm4a',
        'noplaylist': True,
        'postprocessors': [
            {'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            'preferredquality': '192',
            }
            ],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch:{search_query}, ", download=False)['entries'][0]
            audio_url = info['formats'][7]['url']
            title = info['title']
            channel = info['uploader']
            thumbnail = info['thumbnail']
        except Exception as e:
            await ctx.send(f"Hata: {e}")
            return
    if not vc.is_playing():
        ffmpeg_opts = {
            'options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -loglevel debug -filter:a volume=0.2'
        }
        vc.play(discord.FFmpegPCMAudio(audio_url, **ffmpeg_opts),after=lambda e: print(f"Finished playing: {title}"))
        embed2=discord.Embed(title="<:radio:1335306029231112282> 1.L FM",description=f"Found `{search_query}`",color=discord.Color.green())
        embed2.set_thumbnail(url="https://imgur.com/Q1gtNvt.png")
        embed2.set_image(url=thumbnail)
        embed2.add_field(name="<a:play:1335255616943296617> Now Playing", value="", inline=False)
        embed2.add_field(name="Title", value=title, inline=False)
        embed2.add_field(name="Channel", value=channel, inline=False)
        await ctx.reply(embed=embed2)
    else:
        embed3=discord.Embed(title="<:radio:1335306029231112282> 1.L FM",description="<:alrplay:1335309374767235163> There is a song playing. Please wait for it to finish.")
        await ctx.reply(embed=embed3)
@bot.command()
async def stop(ctx):
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        embed4=discord.Embed(title="<:radio:1335306029231112282> 1.L FM", description="<:stop:1335256203948851311> Song stopped.",color=discord.Color.red())
        await ctx.reply(embed=embed4)
    else:
        embed5=discord.Embed(title="<:radio:1335306029231112282> 1.L FM", description="<:noplay:1335309663259987968> There is no song playing.",color=discord.Color.red())
        await ctx.reply(embed=embed5)

# waifu.pics Commands

@bot.command()
async def waifu(ctx:commands.Context):
    pic : str = waifuclient.sfw(category='waifu',many=False)
    embed = discord.Embed(title="1.Ldae",description="Waifu category")
    embed.set_image(url=pic)
    embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
    await ctx.reply(embed=embed)
@bot.command()
async def wneko(ctx:commands.Context):
    pic : str = waifuclient.sfw(category='neko',many=False)
    embed = discord.Embed(title="1.Ldae",description="Neko category")
    embed.set_image(url=pic)
    embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
    await ctx.reply(embed=embed)
@bot.command()
async def wshinobu(ctx:commands.Context):
    pic : str = waifuclient.sfw(category='shinobu',many=False)
    embed = discord.Embed(title="1.Ldae",description="Shinobu category")
    embed.set_image(url=pic)
    embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
    await ctx.reply(embed=embed)
@bot.command()
async def wmegumin(ctx:commands.Context):
    pic : str = waifuclient.sfw(category='megumin',many=False)
    embed = discord.Embed(title="1.Ldae",description="Megumin category")
    embed.set_image(url=pic)
    embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
    await ctx.reply(embed=embed)
@bot.command()
async def wbully(ctx:commands.Context):
    pic : str = waifuclient.sfw(category='bully',many=False)
    embed = discord.Embed(title="1.Ldae",description="Bully category")
    embed.set_image(url=pic)
    embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
    await ctx.reply(embed=embed)
@bot.command()
async def wcuddle(ctx:commands.Context):
    pic : str = waifuclient.sfw(category='cuddle',many=False)
    embed = discord.Embed(title="1.Ldae",description="Cuddle category")
    embed.set_image(url=pic)
    embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
    await ctx.reply(embed=embed)
@bot.command()
async def wcry(ctx:commands.Context):
    pic : str = waifuclient.sfw(category='cry',many=False)
    embed = discord.Embed(title="1.Ldae",description="Cry category")
    embed.set_image(url=pic)
    embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
    await ctx.reply(embed=embed)
@bot.command()
async def whug(ctx:commands.Context):
    pic : str = waifuclient.sfw(category='hug',many=False)
    embed = discord.Embed(title="1.Ldae",description="Hug category")
    embed.set_image(url=pic)
    embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
    await ctx.reply(embed=embed)
@bot.command()
async def wawoo(ctx:commands.Context):
    pic : str = waifuclient.sfw(category='awoo',many=False)
    embed = discord.Embed(title="1.Ldae",description="Awoo category")
    embed.set_image(url=pic)
    embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
    await ctx.reply(embed=embed)
@bot.command()
async def wkiss(ctx:commands.Context):
    pic : str = waifuclient.sfw(category='kiss',many=False)
    embed = discord.Embed(title="1.Ldae",description="Kiss category")
    embed.set_image(url=pic)
    embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
    await ctx.reply(embed=embed)
@bot.command()
async def wlick(ctx:commands.Context):
    pic : str = waifuclient.sfw(category='lick',many=False)
    embed = discord.Embed(title="1.Ldae",description="Lick category")
    embed.set_image(url=pic)
    embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
    await ctx.reply(embed=embed)
@bot.command()
async def wpat(ctx:commands.Context):
    pic : str = waifuclient.sfw(category='pat',many=False)
    embed = discord.Embed(title="1.Ldae",description="Pat category")
    embed.set_image(url=pic)
    embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
    await ctx.reply(embed=embed)
@bot.command()
async def wsmug(ctx:commands.Context):
    pic : str = waifuclient.sfw(category='smug',many=False)
    embed = discord.Embed(title="1.Ldae",description="Smug category")
    embed.set_image(url=pic)
    embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
    await ctx.reply(embed=embed)
@bot.command()
async def wbonk(ctx:commands.Context):
    pic : str = waifuclient.sfw(category='bonk',many=False)
    embed = discord.Embed(title="1.Ldae",description="Bonk category")
    embed.set_image(url=pic)
    embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
    await ctx.reply(embed=embed)
@bot.command()
async def wyeet(ctx:commands.Context):
    pic : str = waifuclient.sfw(category='yeet',many=False)
    embed = discord.Embed(title="1.Ldae",description="Yeet category")
    embed.set_image(url=pic)
    embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
    await ctx.reply(embed=embed)
@bot.command()
async def wblush(ctx:commands.Context):
    pic : str = waifuclient.sfw(category='blush',many=False)
    embed = discord.Embed(title="1.Ldae",description="Blush category")
    embed.set_image(url=pic)
    embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
    await ctx.reply(embed=embed)
@bot.command()
async def wsmile(ctx:commands.Context):
    pic : str = waifuclient.sfw(category='smile',many=False)
    embed = discord.Embed(title="1.Ldae",description="Smile category")
    embed.set_image(url=pic)
    embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
    await ctx.reply(embed=embed)
@bot.command()
async def wwave(ctx:commands.Context):
    pic : str = waifuclient.sfw(category='wave',many=False)
    embed = discord.Embed(title="1.Ldae",description="Wave category")
    embed.set_image(url=pic)
    embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
    await ctx.reply(embed=embed)
@bot.command()
async def whighfive(ctx:commands.Context):
    pic : str = waifuclient.sfw(category='highfive',many=False)
    embed = discord.Embed(title="1.Ldae",description="Highfive category")
    embed.set_image(url=pic)
    embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
    await ctx.reply(embed=embed)
@bot.command()
async def whandhold(ctx:commands.Context):
    pic : str = waifuclient.sfw(category='handhold',many=False)
    embed = discord.Embed(title="1.Ldae",description="Handhold category")
    embed.set_image(url=pic)
    embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
    await ctx.reply(embed=embed)
@bot.command()
async def wnom(ctx:commands.Context):
    pic : str = waifuclient.sfw(category='nom',many=False)
    embed = discord.Embed(title="1.Ldae",description="Nom category")
    embed.set_image(url=pic)
    embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
    await ctx.reply(embed=embed)
@bot.command()
async def wbite(ctx:commands.Context):
    pic : str = waifuclient.sfw(category='bite',many=False)
    embed = discord.Embed(title="1.Ldae",description="Bite category")
    embed.set_image(url=pic)
    embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
    await ctx.reply(embed=embed)
@bot.command()
async def wglomp(ctx:commands.Context):
    pic : str = waifuclient.sfw(category='glomp',many=False)
    embed = discord.Embed(title="1.Ldae",description="Glomp category")
    embed.set_image(url=pic)
    embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
    await ctx.reply(embed=embed)
@bot.command()
async def wslap(ctx:commands.Context):
    pic : str = waifuclient.sfw(category='slap',many=False)
    embed = discord.Embed(title="1.Ldae",description="Slap category")
    embed.set_image(url=pic)
    embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
    await ctx.reply(embed=embed)
@bot.command()
async def wkill(ctx:commands.Context,register=None):
    if register!="approve":
        await ctx.reply("You need to type 'approve' if you want to get an image from this category")
    else:
        pic : str = waifuclient.sfw(category='kill',many=False)
        embed = discord.Embed(title="1.Ldae",description=":warning: Kill category")
        embed.set_image(url=pic)
        embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
        await ctx.reply(embed=embed)
@bot.command()
async def wkick(ctx:commands.Context):
    pic : str = waifuclient.sfw(category='kick',many=False)
    embed = discord.Embed(title="1.Ldae",description="Kick category")
    embed.set_image(url=pic)
    embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
    await ctx.reply(embed=embed)
@bot.command()
async def whappy(ctx:commands.Context):
    pic : str = waifuclient.sfw(category='happy',many=False)
    embed = discord.Embed(title="1.Ldae",description="Happy category")
    embed.set_image(url=pic)
    embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
    await ctx.reply(embed=embed)
@bot.command()
async def wwink(ctx:commands.Context):
    pic : str = waifuclient.sfw(category='wink',many=False)
    embed = discord.Embed(title="1.Ldae",description="Wink category")
    embed.set_image(url=pic)
    embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
    await ctx.reply(embed=embed)
@bot.command()
async def wpoke(ctx:commands.Context):
    pic : str = waifuclient.sfw(category='poke',many=False)
    embed = discord.Embed(title="1.Ldae",description="Poke category")
    embed.set_image(url=pic)
    embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
    await ctx.reply(embed=embed)
@bot.command()
async def wdance(ctx:commands.Context):
    pic : str = waifuclient.sfw(category='dance',many=False)
    embed = discord.Embed(title="1.Ldae",description="Dance category")
    embed.set_image(url=pic)
    embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
    await ctx.reply(embed=embed)
@bot.command()
async def wcringe(ctx:commands.Context):
    pic : str = waifuclient.sfw(category='cringe',many=False)
    embed = discord.Embed(title="1.Ldae",description="Cringe category")
    embed.set_image(url=pic)
    embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
    await ctx.reply(embed=embed)
@bot.command()
async def wrandom(ctx:commands.Context):
    categorylist = ('waifu','neko','shinobu','megumin','bully','cuddle','cry','hug','awoo','kiss','lick','pat','smug','bonk','yeet','blush','smile','wave','highfive','handhold','nom','bite','glomp','slap','kill','kick','happy','wink','poke','dance','cringe')
    category=random.choice(categorylist)
    pic : str = waifuclient.sfw(category=category,many=False)
    embed = discord.Embed(title="1.Ldae",description=f"Random category: {category}")
    embed.set_image(url=pic)
    embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
    await ctx.reply(embed=embed)
@bot.tree.command(description="Find some waifus over waifu.pics")
@app_commands.describe(category="Searching category. Use /help waifucategory to view all ccategories.")
@app_commands.describe(register="Confirmation for kill category. Type approve to use kill category.")
async def waifu(i:discord.Integration,category:str=None,register:str=None):
    if category==None:
        await i.response.send_message("You need to give a category. View `1.l help w category` to view them")
    elif category=="waifu":
        pic : str = waifuclient.sfw(category='waifu',many=False)
        embed = discord.Embed(title="1.Ldae",description="Waifu category")
        embed.set_image(url=pic)
        embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
        await i.response.send_message(embed=embed)
    elif category=="neko":
        pic : str = waifuclient.sfw(category='neko',many=False)
        embed = discord.Embed(title="1.Ldae",description="Neko category")
        embed.set_image(url=pic)
        embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
        await i.response.send_message(embed=embed)
    elif category=="shinobu":
        pic : str = waifuclient.sfw(category='shinobu',many=False)
        embed = discord.Embed(title="1.Ldae",description="Shinobu category")
        embed.set_image(url=pic)
        embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
        await i.response.send_message(embed=embed)
    elif category=="megumin":
        pic : str = waifuclient.sfw(category='megumin',many=False)
        embed = discord.Embed(title="1.Ldae",description="Megumin category")
        embed.set_image(url=pic)
        embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
        await i.response.send_message(embed=embed)
    elif category=="bully":
        pic : str = waifuclient.sfw(category='bully',many=False)
        embed = discord.Embed(title="1.Ldae",description="Bully category")
        embed.set_image(url=pic)
        embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
        await i.response.send_message(embed=embed)
    elif category=="cuddle":
        pic : str = waifuclient.sfw(category='cuddle',many=False)
        embed = discord.Embed(title="1.Ldae",description="Cuddle category")
        embed.set_image(url=pic)
        embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
        await i.response.send_message(embed=embed)
    elif category=="cry":
        pic : str = waifuclient.sfw(category='cry',many=False)
        embed = discord.Embed(title="1.Ldae",description="Cry category")
        embed.set_image(url=pic)
        embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
        await i.response.send_message(embed=embed)
    elif category=="hug":
        pic : str = waifuclient.sfw(category='hug',many=False)
        embed = discord.Embed(title="1.Ldae",description="Hug category")
        embed.set_image(url=pic)
        embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
        await i.response.send_message(embed=embed)
    elif category=="awoo":
        pic : str = waifuclient.sfw(category='awoo',many=False)
        embed = discord.Embed(title="1.Ldae",description="Awoo category")
        embed.set_image(url=pic)
        embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
        await i.response.send_message(embed=embed)
    elif category=="kiss":
        pic : str = waifuclient.sfw(category='kiss',many=False)
        embed = discord.Embed(title="1.Ldae",description="Kiss category")
        embed.set_image(url=pic)
        embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
        await i.response.send_message(embed=embed)
    elif category=="lick":
        pic : str = waifuclient.sfw(category='lick',many=False)
        embed = discord.Embed(title="1.Ldae",description="Lick category")
        embed.set_image(url=pic)
        embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
        await i.response.send_message(embed=embed)
    elif category=="pat":
        pic : str = waifuclient.sfw(category='pat',many=False)
        embed = discord.Embed(title="1.Ldae",description="Pat category")
        embed.set_image(url=pic)
        embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
        await i.response.send_message(embed=embed)
    elif category=="smug":
        pic : str = waifuclient.sfw(category='smug',many=False)
        embed = discord.Embed(title="1.Ldae",description="Smug category")
        embed.set_image(url=pic)
        embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
        await i.response.send_message(embed=embed)
    elif category=="bonk":
        pic : str = waifuclient.sfw(category='bonk',many=False)
        embed = discord.Embed(title="1.Ldae",description="Bonk category")
        embed.set_image(url=pic)
        embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
        await i.response.send_message(embed=embed)
    elif category=="yeet":
        pic : str = waifuclient.sfw(category='yeet',many=False)
        embed = discord.Embed(title="1.Ldae",description="Yeet category")
        embed.set_image(url=pic)
        embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
        await i.response.send_message(embed=embed)
    elif category=="blush":
        pic : str = waifuclient.sfw(category='blush',many=False)
        embed = discord.Embed(title="1.Ldae",description="Blush category")
        embed.set_image(url=pic)
        embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
        await i.response.send_message(embed=embed)
    elif category=="smile":
        pic : str = waifuclient.sfw(category='smile',many=False)
        embed = discord.Embed(title="1.Ldae",description="Smile category")
        embed.set_image(url=pic)
        embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
        await i.response.send_message(embed=embed)
    elif category=="wave":
        pic : str = waifuclient.sfw(category='wave',many=False)
        embed = discord.Embed(title="1.Ldae",description="Wave category")
        embed.set_image(url=pic)
        embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
        await i.response.send_message(embed=embed)
    elif category=="highfive":
        pic : str = waifuclient.sfw(category='highfive',many=False)
        embed = discord.Embed(title="1.Ldae",description="Highfive category")
        embed.set_image(url=pic)
        embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
        await i.response.send_message(embed=embed)
    elif category=="handhold":
        pic : str = waifuclient.sfw(category='handhold',many=False)
        embed = discord.Embed(title="1.Ldae",description="Handhold category")
        embed.set_image(url=pic)
        embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
        await i.response.send_message(embed=embed)
    elif category=="nom":
        pic : str = waifuclient.sfw(category='nom',many=False)
        embed = discord.Embed(title="1.Ldae",description="Nom category")
        embed.set_image(url=pic)
        embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
        await i.response.send_message(embed=embed)
    elif category=="bite":
        pic : str = waifuclient.sfw(category='bite',many=False)
        embed = discord.Embed(title="1.Ldae",description="Bite category")
        embed.set_image(url=pic)
        embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
        await i.response.send_message(embed=embed)
    elif category=="glomp":
        pic : str = waifuclient.sfw(category='glomp',many=False)
        embed = discord.Embed(title="1.Ldae",description="Glomp category")
        embed.set_image(url=pic)
        embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
        await i.response.send_message(embed=embed)
    elif category=="slap":
        pic : str = waifuclient.sfw(category='slap',many=False)
        embed = discord.Embed(title="1.Ldae",description="Slap category")
        embed.set_image(url=pic)
        embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
        await i.response.send_message(embed=embed)
    elif category=="kill":
        if register!="approve":
            await i.response.send_message("You need to type 'approve' if you want to get an image from this category")
        else:
            pic : str = waifuclient.sfw(category='kill',many=False)
            embed = discord.Embed(title="1.Ldae",description=":warning: Kill category")
            embed.set_image(url=pic)
            embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
            await i.response.send_message(embed=embed)
    elif category=="kick":
        pic : str = waifuclient.sfw(category='kick',many=False)
        embed = discord.Embed(title="1.Ldae",description="Kick category")
        embed.set_image(url=pic)
        embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
        await i.response.send_message(embed=embed)
    elif category=="happy":
        pic : str = waifuclient.sfw(category='happy',many=False)
        embed = discord.Embed(title="1.Ldae",description="Happy category")
        embed.set_image(url=pic)
        embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
        await i.response.send_message(embed=embed)
    elif category=="wink":
        pic : str = waifuclient.sfw(category='wink',many=False)
        embed = discord.Embed(title="1.Ldae",description="Wink category")
        embed.set_image(url=pic)
        embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
        await i.response.send_message(embed=embed)
    elif category=="poke":
        pic : str = waifuclient.sfw(category='poke',many=False)
        embed = discord.Embed(title="1.Ldae",description="Poke category")
        embed.set_image(url=pic)
        embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
        await i.response.send_message(embed=embed)
    elif category=="dance":
        pic : str = waifuclient.sfw(category='dance',many=False)
        embed = discord.Embed(title="1.Ldae",description="Dance category")
        embed.set_image(url=pic)
        embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
        await i.response.send_message(embed=embed)
    elif category=="cringe":
        pic : str = waifuclient.sfw(category='cringe',many=False)
        embed = discord.Embed(title="1.Ldae",description="Cringe category")
        embed.set_image(url=pic)
        embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
        await i.response.send_message(embed=embed)
    elif category=="random":
        categorylist = ('waifu','neko','shinobu','megumin','bully','cuddle','cry','hug','awoo','kiss','lick','pat','smug','bonk','yeet','blush','smile','wave','highfive','handhold','nom','bite','glomp','slap','kill','kick','happy','wink','poke','dance','cringe')
        category=random.choice(categorylist)
        pic : str = waifuclient.sfw(category=category,many=False)
        embed = discord.Embed(title="1.Ldae",description=f"Random category: {category}")
        embed.set_image(url=pic)
        embed.add_field(name="",value="[waifu.pics](https://waifu.pics)\n:warning: 1.L Bot is **NOT** responsible with gore, sexual etc. images\n:warning: All of the results that appears are legal images. Every character is over legal age.")
        await i.response.send_message(embed=embed)
    else:
        await i.response.send_message(f"There's no category named {category}. Please use `/help waifucategory` to view the categories.")
bot.run(BOT_TOKEN)
