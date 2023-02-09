import os
from random import randint
import discord
from datetime import datetime
import requests
from discord.ext import commands
from discord import app_commands

from data_ import guilds
# from main import interaction.client.all_gifs


class Gifs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="pat", description="Pat someone")#, guilds=guilds)
    async def pat(self, interaction, user: discord.User):
        embed = discord.Embed(description="<@{}> pats <@{}> !".format(interaction.user.id, user.id), colour=0xB991FF,
                              timestamp=datetime.utcnow())
        embed.set_footer(text="Dislate")
        number = randint(0, 49)
        embed.set_image(url=interaction.client.all_gifs["pat"]["results"][number]["media_formats"]["gif"]["url"])
        await interaction.response.send_message(embed=embed)
        requests.get("https://tenor.googleapis.com/v2/search?q={}&key={}&client_key={}&limit={}".format(
            interaction.client.all_gifs["pat"]["results"][number]["id"], os.environ.get("TENOR"), "Dislate", "pat"))

    @app_commands.command(name="kiss", description="Kiss someone")#, guilds=guilds)
    async def kiss(self, interaction, user: discord.User):
        embed = discord.Embed(description="<@{}> kisses <@{}> !".format(interaction.user.id, user.id), colour=0xB991FF,
                              timestamp=datetime.utcnow())
        embed.set_footer(text="Dislate")
        number = randint(0, 49)
        embed.set_image(url=interaction.client.all_gifs["kiss"]["results"][number]["media_formats"]["gif"]["url"])
        await interaction.response.send_message(embed=embed)
        requests.get("https://tenor.googleapis.com/v2/search?q={}&key={}&client_key={}&limit={}".format(
            interaction.client.all_gifs["kiss"]["results"][number]["id"], os.environ.get("TENOR"), "Dislate", "kiss"))

    @app_commands.command(name="hit", description="Hit someone")#, guilds=guilds)
    async def hit(self, interaction, user: discord.User):
        embed = discord.Embed(description="<@{}> hits <@{}> !".format(interaction.user.id, user.id), colour=0xB991FF,
                              timestamp=datetime.utcnow())
        embed.set_footer(text="Dislate")
        number = randint(0, 49)
        embed.set_image(url=interaction.client.all_gifs["hit"]["results"][number]["media_formats"]["gif"]["url"])
        await interaction.response.send_message(embed=embed)
        requests.get("https://tenor.googleapis.com/v2/search?q={}&key={}&client_key={}&limit={}".format(
            interaction.client.all_gifs["hit"]["results"][number]["id"], os.environ.get("TENOR"), "Dislate", "hit"))

    @app_commands.command(name="slap", description="Slap someone")#, guilds=guilds)
    async def slap(self, interaction, user: discord.User):
        embed = discord.Embed(description="<@{}> slaps <@{}> !".format(interaction.user.id, user.id), colour=0xB991FF,
                              timestamp=datetime.utcnow())
        embed.set_footer(text="Dislate")
        number = randint(0, 49)
        embed.set_image(url=interaction.client.all_gifs["slap"]["results"][number]["media_formats"]["gif"]["url"])
        await interaction.response.send_message(embed=embed)
        requests.get("https://tenor.googleapis.com/v2/search?q={}&key={}&client_key={}&limit={}".format(
            interaction.client.all_gifs["slap"]["results"][number]["id"], os.environ.get("TENOR"), "Dislate", "slap"))

    @app_commands.command(name="happy", description="Show that you're happy.")#, guilds=guilds)
    async def happy(self, interaction):
        embed = discord.Embed(description="<@{}> is happy !".format(interaction.user.id), colour=0xB991FF,
                              timestamp=datetime.utcnow())
        embed.set_footer(text="Dislate")
        number = randint(0, 49)
        embed.set_image(url=interaction.client.all_gifs["happy"]["results"][number]["media_formats"]["gif"]["url"])
        await interaction.response.send_message(embed=embed)
        requests.get("https://tenor.googleapis.com/v2/search?q={}&key={}&client_key={}&limit={}".format(
            interaction.client.all_gifs["happy"]["results"][number]["id"], os.environ.get("TENOR"), "Dislate", "happy"))

    @app_commands.command(name="sad", description="Show that you're sad")#, guilds=guilds)
    async def sad(self, interaction):
        embed = discord.Embed(description="<@{}> is sad !".format(interaction.user.id), colour=0xB991FF,
                              timestamp=datetime.utcnow())
        embed.set_footer(text="Dislate")
        number = randint(0, 49)
        embed.set_image(url=interaction.client.all_gifs["sad"]["results"][number]["media_formats"]["gif"]["url"])
        await interaction.response.send_message(embed=embed)
        requests.get("https://tenor.googleapis.com/v2/search?q={}&key={}&client_key={}&limit={}".format(
            interaction.client.all_gifs["sad"]["results"][number]["id"], os.environ.get("TENOR"), "Dislate", "sad"))

    @app_commands.command(name="angry", description="Show that you're angry.")#, guilds=guilds)
    async def angry(self, interaction, user: discord.User):
        embed = discord.Embed(description="<@{}> is angry at <@{}> !".format(interaction.user.id, user.id), colour=0xB991FF,
                              timestamp=datetime.utcnow())
        embed.set_footer(text="Dislate")
        number = randint(0, 49)
        embed.set_image(url=interaction.client.all_gifs["angry"]["results"][number]["media_formats"]["gif"]["url"])
        await interaction.response.send_message(embed=embed)
        requests.get("https://tenor.googleapis.com/v2/search?q={}&key={}&client_key={}&limit={}".format(
            interaction.client.all_gifs["angry"]["results"][number]["id"], os.environ.get("TENOR"), "Dislate", "angry"))

    @app_commands.command(name="hungry", description="Are you hungry enough to use this command ?")#, guilds=guilds)
    async def hungry(self, interaction):
        embed = discord.Embed(description="<@{}> is hungry...".format(interaction.user.id), colour=0xB991FF,
                              timestamp=datetime.utcnow())
        embed.set_footer(text="Dislate")
        number = randint(0, 49)
        embed.set_image(url=interaction.client.all_gifs["hungry"]["results"][number]["media_formats"]["gif"]["url"])
        await interaction.response.send_message(embed=embed)
        requests.get("https://tenor.googleapis.com/v2/search?q={}&key={}&client_key={}&limit={}".format(
            interaction.client.all_gifs["hungry"]["results"][number]["id"], os.environ.get("TENOR"), "Dislate", "hungry"))

    @app_commands.command(name="jealous", description="Are you jealous of someone ?")#, guilds=guilds)
    async def jealous(self, interaction, user: discord.User):
        embed = discord.Embed(description="<@{}> is jealous of <@{}>.".format(interaction.user.id, user.id),
                              colour=0xB991FF,
                              timestamp=datetime.utcnow())
        embed.set_footer(text="Dislate")
        number = randint(0, 49)
        embed.set_image(url=interaction.client.all_gifs["jealous"]["results"][number]["media_formats"]["gif"]["url"])
        await interaction.response.send_message(embed=embed)
        requests.get("https://tenor.googleapis.com/v2/search?q={}&key={}&client_key={}&limit={}".format(
            interaction.client.all_gifs["jealous"]["results"][number]["id"], os.environ.get("TENOR"), "Dislate", "jealous"))

    @app_commands.command(name="innocent", description="Are you truly innocent to invoke this command ?")#, guilds=guilds)
    async def innocent(self, interaction):
        embed = discord.Embed(description="<@{}> is innocent... really ?".format(interaction.user.id), colour=0xB991FF,
                              timestamp=datetime.utcnow())
        embed.set_footer(text="Dislate")
        number = randint(0, 49)
        embed.set_image(url=interaction.client.all_gifs["innocent"]["results"][number]["media_formats"]["gif"]["url"])
        await interaction.response.send_message(embed=embed)
        requests.get("https://tenor.googleapis.com/v2/search?q={}&key={}&client_key={}&limit={}".format(
            interaction.client.all_gifs["innocent"]["results"][number]["id"], os.environ.get("TENOR"), "Dislate", "innocent"))

    @app_commands.command(name="bigbraintime", description="It's big brain time !")#, guilds=guilds)
    async def bigbraintime(self, interaction):
        embed = discord.Embed(description="<@{}> is having a big brain time !".format(interaction.user.id), colour=0xB991FF,
                              timestamp=datetime.utcnow())
        embed.set_footer(text="Dislate")
        number = randint(0, 49)
        embed.set_image(url=interaction.client.all_gifs["big brain time"]["results"][number]["media_formats"]["gif"]["url"])
        await interaction.response.send_message(embed=embed)
        requests.get("https://tenor.googleapis.com/v2/search?q={}&key={}&client_key={}&limit={}".format(
            interaction.client.all_gifs["big brain time"]["results"][number]["id"], os.environ.get("TENOR"), "Dislate", "big brain time"))

    @app_commands.command(name="sus", description="Psst, tell me who's sus.")#, guilds=guilds)
    async def sus(self, interaction, user: discord.User):
        embed = discord.Embed(description="<@{}> is sus.".format(user.id), colour=0xB991FF,
                              timestamp=datetime.utcnow())
        embed.set_footer(text="Dislate")
        number = randint(0, 49)
        embed.set_image(url=interaction.client.all_gifs["sus"]["results"][number]["media_formats"]["gif"]["url"])
        await interaction.response.send_message(embed=embed)
        requests.get("https://tenor.googleapis.com/v2/search?q={}&key={}&client_key={}&limit={}".format(
            interaction.client.all_gifs["sus"]["results"][number]["id"], os.environ.get("TENOR"), "Dislate", "sus"))

    @app_commands.command(name="cringe", description="Looks like someone is cringe.")#, guilds=guilds)
    async def cringe(self, interaction, user: discord.User):
        embed = discord.Embed(description="<@{}> is so cringe.".format(user.id), colour=0xB991FF,
                              timestamp=datetime.utcnow())
        embed.set_footer(text="Dislate")
        number = randint(0, 49)
        embed.set_image(url=interaction.client.all_gifs["cringe"]["results"][number]["media_formats"]["gif"]["url"])
        await interaction.response.send_message(embed=embed)
        requests.get("https://tenor.googleapis.com/v2/search?q={}&key={}&client_key={}&limit={}".format(
            interaction.client.all_gifs["cringe"]["results"][number]["id"], os.environ.get("TENOR"), "Dislate", "cringe"))

    @app_commands.command(name="strange", description="To use when someone is acting strange.")#, guilds=guilds)
    async def strange(self, interaction, user: discord.User):
        embed = discord.Embed(description="<@{}> is acting strange...".format(user.id), colour=0xB991FF,
                              timestamp=datetime.utcnow())
        embed.set_footer(text="Dislate")
        number = randint(0, 49)
        embed.set_image(url=interaction.client.all_gifs["strange"]["results"][number]["media_formats"]["gif"]["url"])
        await interaction.response.send_message(embed=embed)
        requests.get("https://tenor.googleapis.com/v2/search?q={}&key={}&client_key={}&limit={}".format(
            interaction.client.all_gifs["strange"]["results"][number]["id"], os.environ.get("TENOR"), "Dislate", "strange"))

    @app_commands.command(name="dab", description="Dab whenever you want.")#, guilds=guilds)
    async def dab(self, interaction, user: discord.User):
        embed = discord.Embed(description="<@{}> dabs !".format(user.id), colour=0xB991FF,
                              timestamp=datetime.utcnow())
        embed.set_footer(text="Dislate")
        number = randint(0, 49)
        embed.set_image(url=interaction.client.all_gifs["dab"]["results"][number]["media_formats"]["gif"]["url"])
        await interaction.response.send_message(embed=embed)
        requests.get("https://tenor.googleapis.com/v2/search?q={}&key={}&client_key={}&limit={}".format(
            interaction.client.all_gifs["dab"]["results"][number]["id"], os.environ.get("TENOR"), "Dislate", "dab"))

    @app_commands.command(name="dealer", description="When you want to report a dealer.")#, guilds=guilds)
    async def dealer(self, interaction, user: discord.User):
        embed = discord.Embed(description="<@{}> got some deals !".format(user.id), colour=0xB991FF,
                              timestamp=datetime.utcnow())
        embed.set_footer(text="Dislate")
        number = randint(0, 49)
        embed.set_image(url=interaction.client.all_gifs["dealer"]["results"][number]["media_formats"]["gif"]["url"])
        await interaction.response.send_message(embed=embed)
        requests.get("https://tenor.googleapis.com/v2/search?q={}&key={}&client_key={}&limit={}".format(
            interaction.client.all_gifs["dealer"]["results"][number]["id"], os.environ.get("TENOR"), "Dislate", "dealer"))


async def setup(bot):
    await bot.add_cog(Gifs(bot))

