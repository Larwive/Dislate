import deepl
from random import randint
import requests
import json
# from keep_alive import keep_alive
import discord
from discord import app_commands
import os
from discord.ext import commands
from datetime import datetime
from data_ import authorized_channels, auth_languages, dic, help_text_source, help_text_target, quotes, chars

gifs_number = 100
all_gifs = {}

guilds = [discord.Object(743319254107029584), discord.Object(1021336800079380480)]

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=".", intents=intents)  # Change le préfix ici
bot.remove_command('help')
# slash = SlashCommand(bot, sync_commands=True)
# Pour les commandes slash
# client = discord.Client(intents=intents)
# tree = app_commands.CommandTree(bot)

translator = deepl.Translator(str(os.environ.get("DEEPL")))
print("Translator connected.")


# @commands.cooldown(1, 3, commands.BucketType.user)
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def tr(ctx, target_language):
    try:
        tl = str(target_language).upper()
        message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        result = translator.translate_text(message.content, target_lang=tl)
        embed = discord.Embed(title=translator.translate_text("Original message", target_lang=tl),
                              description=message.content, colour=0xB991FF, timestamp=datetime.utcnow())
        embed.set_footer(text="Dislate")
        embed.add_field(name=translator.translate_text("**Translation to {}**".format(dic[tl]), target_lang=tl),
                        value=result.text, inline=False)
        await ctx.send(embed=embed)
        print(ctx.message.author)
    except:
        await ctx.send("Error while trying to translate.")


@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def say(ctx, text):
    await ctx.send(str(text))


@bot.event
async def on_message(message):
    if ((message.channel.id in authorized_channels) and (message.author.id != 1068621642508550296) and (
            message.content[0] != ".")):
        tl = auth_languages[authorized_channels.index(message.channel.id)]
        try:
            result = translator.translate_text(message.content, target_lang=tl)
            embed = discord.Embed(
                title=translator.translate_text("**Translation to {}**".format(dic[tl]), target_lang=tl),
                description=result.text, colour=0xB991FF, timestamp=datetime.utcnow())
            embed.set_footer(text="Dislate")
            await message.channel.send(embed=embed)
        except:
            await message.channel.send(translator.translate_text("Error while trying to translate.", target_lang=tl))
    await bot.process_commands(message)


"""
#@commands.cooldown(1, 1, commands.BucketType.user)
@bot.command()
async def randomen(ctx):
  await ctx.send("This brings you to a random page of Bulbapedia : https://bulbapedia.bulbagarden.net/wiki/Special:Random")
"""


@bot.tree.command(name="translate", description="A translator using Deepl.", guilds=guilds)
async def translate(interaction, text: str, target_language: str, source_language: str = "EN"):
    try:
        result = translator.translate_text(text, source_lang=str(source_language).upper(),
                                           target_lang=str(target_language).upper())
        await interaction.response.send_message(result.text)
    except:
        await interaction.response.send_message("Error while trying to translate.")


@bot.tree.command(name="ping", description="A command to use every day.", guilds=guilds)
async def ping(interaction):
    try:
        await interaction.response.send_message("<@360439679775932416>")
    except:
        pass


@bot.tree.command(name="pat", description="Pat someone", guilds=guilds)
async def pat(interaction, user: discord.User):
    embed = discord.Embed(description="<@{}> pats <@{}> !".format(interaction.user.id, user.id), colour=0xB991FF,
                          timestamp=datetime.utcnow())
    embed.set_footer(text="Dislate")
    number = randint(0, 49)
    embed.set_image(url=all_gifs["pat"]["results"][number]["media_formats"]["gif"]["url"])
    await interaction.response.send_message(embed=embed)
    requests.get("https://tenor.googleapis.com/v2/search?q={}&key={}&client_key={}&limit={}".format(
        all_gifs["pat"]["results"][number]["id"], os.environ.get("TENOR"), "Dislate", "pat"))


@bot.tree.command(name="kiss", description="Kiss someone", guilds=guilds)
async def kiss(interaction, user: discord.User):
    embed = discord.Embed(description="<@{}> kisses <@{}> !".format(interaction.user.id, user.id), colour=0xB991FF,
                          timestamp=datetime.utcnow())
    embed.set_footer(text="Dislate")
    number = randint(0, 49)
    embed.set_image(url=all_gifs["kiss"]["results"][number]["media_formats"]["gif"]["url"])
    await interaction.response.send_message(embed=embed)
    requests.get("https://tenor.googleapis.com/v2/search?q={}&key={}&client_key={}&limit={}".format(
        all_gifs["kiss"]["results"][number]["id"], os.environ.get("TENOR"), "Dislate", "kiss"))


@bot.tree.command(name="hit", description="Hit someone", guilds=guilds)
async def hit(interaction, user: discord.User):
    embed = discord.Embed(description="<@{}> hits <@{}> !".format(interaction.user.id, user.id), colour=0xB991FF,
                          timestamp=datetime.utcnow())
    embed.set_footer(text="Dislate")
    number = randint(0, 49)
    embed.set_image(url=all_gifs["hit"]["results"][number]["media_formats"]["gif"]["url"])
    await interaction.response.send_message(embed=embed)
    requests.get("https://tenor.googleapis.com/v2/search?q={}&key={}&client_key={}&limit={}".format(
        all_gifs["hit"]["results"][number]["id"], os.environ.get("TENOR"), "Dislate", "hit"))


@bot.tree.command(name="slap", description="Slap someone", guilds=guilds)
async def slap(interaction, user: discord.User):
    embed = discord.Embed(description="<@{}> slaps <@{}> !".format(interaction.user.id, user.id), colour=0xB991FF,
                          timestamp=datetime.utcnow())
    embed.set_footer(text="Dislate")
    number = randint(0, 49)
    embed.set_image(url=all_gifs["slap"]["results"][number]["media_formats"]["gif"]["url"])
    await interaction.response.send_message(embed=embed)
    requests.get("https://tenor.googleapis.com/v2/search?q={}&key={}&client_key={}&limit={}".format(
        all_gifs["slap"]["results"][number]["id"], os.environ.get("TENOR"), "Dislate", "slap"))


@bot.tree.command(name="happy", description="Show that you're happy.", guilds=guilds)
async def happy(interaction):
    embed = discord.Embed(description="<@{}> is happy !".format(interaction.user.id), colour=0xB991FF,
                          timestamp=datetime.utcnow())
    embed.set_footer(text="Dislate")
    number = randint(0, 49)
    embed.set_image(url=all_gifs["happy"]["results"][number]["media_formats"]["gif"]["url"])
    await interaction.response.send_message(embed=embed)
    requests.get("https://tenor.googleapis.com/v2/search?q={}&key={}&client_key={}&limit={}".format(
        all_gifs["happy"]["results"][number]["id"], os.environ.get("TENOR"), "Dislate", "happy"))


@bot.tree.command(name="sad", description="Show that you're sad", guilds=guilds)
async def sad(interaction):
    embed = discord.Embed(description="<@{}> is sad !".format(interaction.user.id), colour=0xB991FF,
                          timestamp=datetime.utcnow())
    embed.set_footer(text="Dislate")
    number = randint(0, 49)
    embed.set_image(url=all_gifs["sad"]["results"][number]["media_formats"]["gif"]["url"])
    await interaction.response.send_message(embed=embed)
    requests.get("https://tenor.googleapis.com/v2/search?q={}&key={}&client_key={}&limit={}".format(
        all_gifs["sad"]["results"][number]["id"], os.environ.get("TENOR"), "Dislate", "sad"))


@bot.tree.command(name="angry", description="Show that you're angry.", guilds=guilds)
async def angry(interaction, user: discord.User):
    embed = discord.Embed(description="<@{}> is angry at <@{}> !".format(interaction.user.id, user.id), colour=0xB991FF,
                          timestamp=datetime.utcnow())
    embed.set_footer(text="Dislate")
    number = randint(0, 49)
    embed.set_image(url=all_gifs["angry"]["results"][number]["media_formats"]["gif"]["url"])
    await interaction.response.send_message(embed=embed)
    requests.get("https://tenor.googleapis.com/v2/search?q={}&key={}&client_key={}&limit={}".format(
        all_gifs["angry"]["results"][number]["id"], os.environ.get("TENOR"), "Dislate", "angry"))


@bot.tree.command(name="hungry", description="Are you hungry enough to use this command ?", guilds=guilds)
async def hungry(interaction):
    embed = discord.Embed(description="<@{}> is hungry...".format(interaction.user.id), colour=0xB991FF,
                          timestamp=datetime.utcnow())
    embed.set_footer(text="Dislate")
    number = randint(0, 49)
    embed.set_image(url=all_gifs["hungry"]["results"][number]["media_formats"]["gif"]["url"])
    await interaction.response.send_message(embed=embed)
    requests.get("https://tenor.googleapis.com/v2/search?q={}&key={}&client_key={}&limit={}".format(
        all_gifs["hungry"]["results"][number]["id"], os.environ.get("TENOR"), "Dislate", "hungry"))


@bot.tree.command(name="jealous", description="Are you jealous of someone ?", guilds=guilds)
async def jealous(interaction, user: discord.User):
    embed = discord.Embed(description="<@{}> is jealous of <@{}>.".format(interaction.user.id, user.id),
                          colour=0xB991FF,
                          timestamp=datetime.utcnow())
    embed.set_footer(text="Dislate")
    number = randint(0, 49)
    embed.set_image(url=all_gifs["jealous"]["results"][number]["media_formats"]["gif"]["url"])
    await interaction.response.send_message(embed=embed)
    requests.get("https://tenor.googleapis.com/v2/search?q={}&key={}&client_key={}&limit={}".format(
        all_gifs["jealous"]["results"][number]["id"], os.environ.get("TENOR"), "Dislate", "jealous"))


@bot.tree.command(name="innocent", description="Are you truly innocent to invoke this command ?", guilds=guilds)
async def innocent(interaction):
    embed = discord.Embed(description="<@{}> is innocent... really ?".format(interaction.user.id), colour=0xB991FF,
                          timestamp=datetime.utcnow())
    embed.set_footer(text="Dislate")
    number = randint(0, 49)
    embed.set_image(url=all_gifs["innocent"]["results"][number]["media_formats"]["gif"]["url"])
    await interaction.response.send_message(embed=embed)
    requests.get("https://tenor.googleapis.com/v2/search?q={}&key={}&client_key={}&limit={}".format(
        all_gifs["innocent"]["results"][number]["id"], os.environ.get("TENOR"), "Dislate", "innocent"))


@bot.tree.command(name="bigbraintime", description="It's big brain time !", guilds=guilds)
async def bigbraintime(interaction):
    embed = discord.Embed(description="<@{}> is having a big brain time !".format(interaction.user.id), colour=0xB991FF,
                          timestamp=datetime.utcnow())
    embed.set_footer(text="Dislate")
    number = randint(0, 49)
    embed.set_image(url=all_gifs["big brain time"]["results"][number]["media_formats"]["gif"]["url"])
    await interaction.response.send_message(embed=embed)
    requests.get("https://tenor.googleapis.com/v2/search?q={}&key={}&client_key={}&limit={}".format(
        all_gifs["big brain time"]["results"][number]["id"], os.environ.get("TENOR"), "Dislate", "big brain time"))


@bot.tree.command(name="sus", description="Psst, tell me who's sus.", guilds=guilds)
async def sus(interaction, user: discord.User):
    embed = discord.Embed(description="<@{}> is sus.".format(user.id), colour=0xB991FF,
                          timestamp=datetime.utcnow())
    embed.set_footer(text="Dislate")
    number = randint(0, 49)
    embed.set_image(url=all_gifs["sus"]["results"][number]["media_formats"]["gif"]["url"])
    await interaction.response.send_message(embed=embed)
    requests.get("https://tenor.googleapis.com/v2/search?q={}&key={}&client_key={}&limit={}".format(
        all_gifs["sus"]["results"][number]["id"], os.environ.get("TENOR"), "Dislate", "sus"))


@bot.tree.command(name="cringe", description="Looks like someone is cringe.", guilds=guilds)
async def cringe(interaction, user: discord.User):
    embed = discord.Embed(description="<@{}> is so cringe.".format(user.id), colour=0xB991FF,
                          timestamp=datetime.utcnow())
    embed.set_footer(text="Dislate")
    number = randint(0, 49)
    embed.set_image(url=all_gifs["cringe"]["results"][number]["media_formats"]["gif"]["url"])
    await interaction.response.send_message(embed=embed)
    requests.get("https://tenor.googleapis.com/v2/search?q={}&key={}&client_key={}&limit={}".format(
        all_gifs["cringe"]["results"][number]["id"], os.environ.get("TENOR"), "Dislate", "cringe"))


@bot.tree.command(name="strange", description="To use when someone is acting strange.", guilds=guilds)
async def strange(interaction, user: discord.User):
    embed = discord.Embed(description="<@{}> is acting strange...".format(user.id), colour=0xB991FF,
                          timestamp=datetime.utcnow())
    embed.set_footer(text="Dislate")
    number = randint(0, 49)
    embed.set_image(url=all_gifs["strange"]["results"][number]["media_formats"]["gif"]["url"])
    await interaction.response.send_message(embed=embed)
    requests.get("https://tenor.googleapis.com/v2/search?q={}&key={}&client_key={}&limit={}".format(
        all_gifs["strange"]["results"][number]["id"], os.environ.get("TENOR"), "Dislate", "strange"))


@bot.tree.command(name="dab", description="Dab whenever you want.", guilds=guilds)
async def dab(interaction, user: discord.User):
    embed = discord.Embed(description="<@{}> dabs !".format(user.id), colour=0xB991FF,
                          timestamp=datetime.utcnow())
    embed.set_footer(text="Dislate")
    number = randint(0, 49)
    embed.set_image(url=all_gifs["dab"]["results"][number]["media_formats"]["gif"]["url"])
    await interaction.response.send_message(embed=embed)
    requests.get("https://tenor.googleapis.com/v2/search?q={}&key={}&client_key={}&limit={}".format(
        all_gifs["dab"]["results"][number]["id"], os.environ.get("TENOR"), "Dislate", "dab"))


@bot.tree.command(name="dealer", description="When you want to report a dealer.", guilds=guilds)
async def dealer(interaction, user: discord.User):
    embed = discord.Embed(description="<@{}> got some deals !".format(user.id), colour=0xB991FF,
                          timestamp=datetime.utcnow())
    embed.set_footer(text="Dislate")
    number = randint(0, 49)
    embed.set_image(url=all_gifs["dealer"]["results"][number]["media_formats"]["gif"]["url"])
    await interaction.response.send_message(embed=embed)
    requests.get("https://tenor.googleapis.com/v2/search?q={}&key={}&client_key={}&limit={}".format(
        all_gifs["dealer"]["results"][number]["id"], os.environ.get("TENOR"), "Dislate", "dealer"))


# @tree.command(name = "help", description = "The command that helps you use dislate.", guilds=[discord.Object(743319254107029584), discord.Object(1021336800079380480)])
# """"""

@bot.tree.command(name="randomquote", description="Sends a random quote", guilds=guilds)
async def quote(interaction):
    await interaction.response.send_message(quotes[randint(0, len(quotes) - 1)])


@bot.tree.command(name="convert", description="Convert any base from 2 to 36 into another base", guilds=guilds)
async def convert(interaction, startbase: app_commands.Range[int, 2, 36], targetbase: app_commands.Range[int, 2, 36],
                  value: str):
    l = len(value)
    n = 0
    value = value.upper()
    for i in range(l - 1, -1, -1):
        n += chars.index(value[i]) * startbase ** (l - 1 - i)
    res = ""
    while n:
        res = chars[n % targetbase] + res
        n = n // targetbase
    await interaction.response.send_message(res)


@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def h(ctx):
    embed = discord.Embed(title="Help", description="A Discord bot that uses deepl.", colour=0xB991FF,
                          timestamp=datetime.utcnow())
    embed.set_footer(text="Dislate")
    embed.add_field(name="**__List of available source languages__**", value=help_text_source, inline=False)
    embed.add_field(name="**__List of available target languages__**", value=help_text_target, inline=False)
    embed.add_field(name="**__Commands__**",
                    value="**say** *text* : Repeat what you say.\n**tr** *target_language* : Translate the message you are responding to into the target language.",
                    inline=False)

    await ctx.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"You're under cooldown, please try again in {round(error.retry_after, 2)} seconds.")


@bot.event
async def on_ready():
    for guild in guilds:
        await bot.tree.sync(guild=guild)
    searchs = ["pat", "kiss", "hit", "slap", "happy", "sad", "angry", "hungry", "jealous", "innocent", "big brain time",
               "sus", "cringe", "strange", "dab", "dealer"]
    # try:
    for i, search in enumerate(searchs):
        r = requests.get("https://tenor.googleapis.com/v2/search?q={}&key={}&client_key={}&limit={}".format(search,
                                                                                                            os.environ.get(
                                                                                                                "TENOR"),
                                                                                                            "Dislate",
                                                                                                            50))
        if r.status_code == 200:
            all_gifs[searchs[i]] = json.loads(r.content)
            # print(json.loads(r.content)["results"][40])
            # print(gifs)
    # except:
    # pass
    # await bot.tree.sync(guild=discord.Object(id=1021336800079380480))
    print("Logged in as {0.user}".format(bot))


# keep_alive()
# bot.add_cog(Owner(bot))
# bot.add_command(randomen)

bot.run(str(os.environ.get("TOKEN", None)))
# client.run(str(os.environ.get("TOKEN", None)))
