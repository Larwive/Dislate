import asyncio
from typing import Optional, Literal

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
from game_func import *

from discord.ext.commands import Greedy

from data_ import authorized_channels, auth_languages, dic, help_text_source, help_text_target, quotes, chars, guilds

gifs_number = 100
#all_gifs = {}



intents = discord.Intents.all()


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=".", intents=intents)

    async def setup_hook(self):
        await self.load_extension('gifs')
        await self.load_extension('game_cogs')


bot = MyBot()

bot.all_gifs = {}
# bot = commands.Bot(command_prefix=".", intents=intents)  # Change le préfix ici
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


"""
@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(
  ctx, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")"""

@bot.event
async def on_ready():
    #for guild in guilds:
        #await bot.tree.sync(guild=guild)
    await bot.tree.sync()
    #await bot.setup_hook()
    searchs = ["pat", "kiss", "hit", "slap", "happy", "sad", "angry", "hungry", "jealous", "innocent", "big brain time",
               "sus", "cringe", "strange", "dab", "dealer"]
    # try:
    for i, search in enumerate(searchs):
        r = requests.get("https://tenor.googleapis.com/v2/search?q={}&key={}&client_key={}&limit={}".format(search, os.environ.get("TENOR"), "Dislate", 50))
        if r.status_code == 200:
            bot.all_gifs[searchs[i]] = json.loads(r.content)
            # print(json.loads(r.content)["results"][40])
            # print(gifs)
    # except:
    # pass
    #await bot.tree.sync(guild=discord.Object(id=1021336800079380480))

    if not os.path.exists("data.db"):
        init_game()
        init_lock()
        init_poke()
        init_options()
        init_teams()

    print("Logged in as {0.user}".format(bot))


# keep_alive()
# bot.add_cog(Owner(bot))
# bot.add_command(randomen)
#bot.load_extension("gifs.py")


bot.run(token=str(os.environ.get("TOKEN", None)))


# asyncio.run(main())
# client.run(str(os.environ.get("TOKEN", None)))
