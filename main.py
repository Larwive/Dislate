import deepl
#from keep_alive import keep_alive
import discord
# from discord import app_commands
import os
from discord.ext import commands
from datetime import datetime
from data_ import authorized_channels, auth_languages, dic, help_text

intents = discord.Intents.all()
"""
# Pour les commandes slash
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)"""

bot = commands.Bot(command_prefix=".", intents=intents)  # Change le préfix ici
# slash = SlashCommand(bot, sync_commands=True)

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
        await ctx.send(translator.translate_text("Error while trying to translate.", target_lang=tl))


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


@tree.command(name = "tr", description = "My first application Command", guild=discord.Object(id=743319254107029584))
async def first_command(interaction, target_language:str):
  #try:
  print(0)
  message = await interaction.channel.fetch_message(interaction.message.reference.message_id)
  print(1)
  result = translator.translate_text(message.content, target_lang=str(target_language))
  print(2)
  await interaction.response.send_message(result.text)
  #except:
  await interaction.response.send_message("Error while trying to translate.")
  #await interaction.response.send_message("Hello!")

@tree.command(name = "help", description = "The command that helps you use dislate.", guilds=[discord.Object(743319254107029584), discord.Object(1021336800079380480)])"""


@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def h(ctx):
    embed = discord.Embed(title="Help", description="A Discord bot that uses deepl.", colour=0xB991FF,
                          timestamp=datetime.utcnow())
    embed.set_footer(text="Dislate")
    embed.add_field(name="**__List of available target languages__**", value=help_text, inline=False)
    embed.add_field(name="**__Commands__**",
                    value="**say** *text* : Repeat what you say.\n**tr** *target_language* : Translate the message you are responding to into the target language.",
                    inline=False)
    # await ctx.send("A Discord bot that uses deepl.\n\n : **\n\n\n**__Commands__**:\n)
    await ctx.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"You're under cooldown, please try again in {round(error.retry_after, 2)} seconds.")


@bot.event
async def on_ready():
    # await tree.sync(guild=discord.Object(id=743319254107029584))
    # await tree.sync(guild=discord.Object(id=1021336800079380480))
    print("Logged in as {0.user}".format(bot))


#keep_alive()
# bot.add_cog(Owner(bot))
# bot.add_command(randomen)

bot.run(str(os.environ.get("TOKEN", None)))
# client.run(os.environ["token"])
