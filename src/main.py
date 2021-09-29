import os
import discord
from random import randrange
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True,  # Commands aren't case-sensitive
    intents=intents
)

bot.author_id = 158267528705998853  # Change to your discord id!!!

@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier

@bot.command()
async def name(ctx):
    await ctx.send(ctx.message.author.name)

@bot.command()
async def count(ctx):
    online = []
    idle = []
    offline = []
    do_not_disturb = []
    for guild in bot.guilds:
        for member in guild.members:
            #if (member.name != bot.user):
            if (member.status == discord.Status.online):
                online.append(member)
            if (member.status == discord.Status.idle):
                idle.append(member)
            if (member.status == discord.Status.offline):
                offline.append(member)
            if (member.status == discord.Status.dnd):
                do_not_disturb.append(member)
                
    online_str = "Online users :\n"
    for member in online:
        online_str += "\t" + member.name + "\n"
    
    idle_str = "Idled users :\n"
    for member in idle:
        idle_str += "\t" + member.name + "\n"

    offline_str = "Offline users :\n"
    for member in offline:
        offline_str += "\t" + member.name + "\n"

    dnd_str = "Do not disturb users :\n"
    for member in do_not_disturb:
        dnd_str += "\t" + member.name + "\n"

    await ctx.send(online_str + idle_str + offline_str + dnd_str)

@bot.command()
async def admin(ctx, user_name):
    if not discord.utils.get(ctx.guild.roles, name="Admin"):
        perms = discord.Permissions(manage_channels=True, kick_members=True, ban_members=True)
        await ctx.guild.create_role(name="Admin", colour=discord.Colour(0xFFFF00), permissions=perms)
    role = discord.utils.get(ctx.guild.roles, name="Admin")
    user = discord.utils.get(bot.get_all_members(), name=user_name)
    await user.add_roles(role)

@bot.command()
async def mute(ctx, user_name):
    if not discord.utils.get(ctx.guild.roles, name="Ghost"):
        perms = discord.Permissions(send_messages=False)
        await ctx.guild.create_role(name="Ghost", colour=discord.Colour(0x000000), permissions=perms)
    role = discord.utils.get(ctx.guild.roles, name="Ghost")
    user = discord.utils.get(bot.get_all_members(), name=user_name)
    if (role in user.roles):
        await user.remove_roles(role)
    else:
        await user.add_roles(role)

@bot.command()
async def ban(ctx, user_name):
    user = discord.utils.get(bot.get_all_members(), name=user_name)
    await user.ban()

@bot.command()
async def xkcd(ctx):
    random = randrange(1, 2522)
    await ctx.send("https://xkcd.com/{}/".format(random))

@bot.command()
async def poll(ctx, question, *reactions):
    if (len(reactions) == 1):
        await ctx.send("{} Erreur, pas assez de choix".format(ctx.message.author.mention))
        return
    str = "@here\n" + question + "\n"
    message = await ctx.send(str)
    if (len(reactions) == 0):
        await message.add_reaction('\N{THUMBS UP SIGN}')
        await message.add_reaction('\N{THUMBS DOWN SIGN}')
    else:
        try:
            for emoji in reactions:
                await message.add_reaction(emoji)
        except Exception:
            await ctx.send("{} Erreur, emoji non valide".format(ctx.message.author.mention))
            await message.delete()

token = ""
bot.run(token)  # Starts the bot