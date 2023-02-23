import asyncio
import typing

import discord
from datetime import datetime
import sqlite3
from discord import app_commands
from discord.ext import commands
from random import randint, choices
from game_data import *
from game_func import *

class ballbutton(discord.ui.Button):
    def __init__(self, ballname, player_id):
        self.ballname = ballname
        self.player_id = player_id
        ballid = ballsid[listballs.index(ballname)]
        if ballid is not None:
            ballid = ballsid[listballs.index(ballname)]
            super().__init__(emoji="<{}:{}>".format(ballname, ballid))
        else:
            super().__init__(label=ballname)

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        assert interaction.user.id == self.player_id
        view:Balls = self.view
        view.sentball = self.ballname
        view.stop()

class Balls(discord.ui.View):
    sentball:str = None
    def __init__(self, balldic:dict, player_id:int, timeout):
        super().__init__(timeout=timeout)
        self.balldic = balldic
        self.player_id = player_id
        for key in list(self.balldic.keys()):
            if self.balldic[key]>0:
                self.add_item(ballbutton(key, player_id))

class Box(discord.ui.View):
    page:int = 1
    sort:int = 0
    def __init__(self, player_id:int, name:str, color:int, language:int, max_pages:int, page:int, box:list, timeout):
        self.player_id = player_id
        self.name = name
        self.color = color
        self.max_pages = max_pages
        self.page=page-1
        self.box = box
        self.language = language
        super().__init__(timeout=timeout)

    async def on_timeout(self) -> None:
        self.stop()

    @discord.ui.button(label="previous")
    async def previous(self, interaction:discord.Interaction, button:discord.ui.Button):
        if interaction.user.id == self.player_id:
            self.page = (self.page-1)%self.max_pages
            embed = getboxembed(self.name, self.color, self.language, self.max_pages, self.page, self.box, self.sort)
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="next")
    async def next(self, interaction:discord.Interaction, button:discord.ui.Button):
        if interaction.user.id == self.player_id:
            self.page = (self.page+1)%self.max_pages
            embed = getboxembed(self.name, self.color, self.language, self.max_pages, self.page, self.box, self.sort)
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="sort")
    async def newsort(self, interaction:discord.Interaction, button:discord.ui.Button):
        if interaction.user.id == self.player_id:
            self.sort = (self.sort+1)%4
            embed = getboxembed(self.name, self.color, self.language, self.max_pages, self.page, self.box, self.sort)
            await interaction.response.edit_message(embed=embed, view=self)
"""
class Trade(discord.ui.View):
    success:bool = False
    confirmed1:bool = False
    confirmed2:bool = False
    name1:str = None
    name2:str = None
    def __init__(self, id1:int, id2:int, name1:str, name2:str, timeout):
        super().__init__(timeout=timeout)
        self.message = None
        self.id1 = id1
        self.id2 = id2
        self.name1 = name1
        self.name2 = name2

    async def disable(self) -> None:
        for item in self.children:
            item.disabled = True
        await self.message.edit_original_message(view=self)

    async def on_timeout(self) -> None:
        await self.disable()

    @discord.ui.button(label="Confirm ({})".format(name1), style=discord.ButtonStyle.red)
    async def confirm1(self, interaction:discord.Interaction, button:discord.ui.Button):
        if interaction.user.id == self.id1:
            if self.confirmed2:
                self.success = True
                self.stop()
                #await self.disable()
                return
            self.confirmed1 = True
            button.style = discord.ButtonStyle.success
            button.label = "Confirmed"
            button.disabled = True
            await interaction.response.edit_message(view=self)
        if interaction.user.id == self.id2:
            await interaction.client.get_channel(interaction.channel_id).send("Click on the other button to confirm the trade.", mention_author=True)

    @discord.ui.button(label="Confirm ({})".format(name2), style=discord.ButtonStyle.red)
    async def confirm2(self, interaction:discord.Interaction, button:discord.ui.Button):
        if interaction.user.id == self.id2:
            if self.confirmed1:
                self.success = True
                self.stop()
                #await self.disable()
                return
            self.confirmed2 = True
            button.style = discord.ButtonStyle.success
            button.label = "Confirmed"
            button.disabled = True
            await interaction.response.edit_message(view=self)
        if interaction.user.id == self.id1:
            await interaction.client.get_channel(interaction.channel_id).send("Click on the other button to confirm the trade.", mention_author=True)"""

class TradeButton(discord.ui.Button):
    def __init__(self, id1:int, id2:int, name:str, first:bool):
        self.id1 = id1
        self.id2 = id2
        self.first = first
        super().__init__(label="Confirm ({})".format(name), style=discord.ButtonStyle.red)

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        assert interaction.user.id in [self.id1, self.id2]
        view:Trade = self.view
        if (interaction.user.id == self.id2 and not self.first) or (interaction.user.id == self.id1 and self.first):
            if view.confirmed1 and not self.first:
                view.success = True
                view.stop()
                return
            elif view.confirmed2 and self.first:
                view.success = True
                view.stop()
                return
            if self.first:
                view.confirmed1 = True
            else:
                view.confirmed2 = True
            self.style = discord.ButtonStyle.success
            self.label = "Confirmed"
            self.disabled = True
            await interaction.response.edit_message(view=view)
            return
        await interaction.client.get_channel(interaction.channel_id).send("Click on the other button to confirm the trade.", mention_author=True)


class Trade(discord.ui.View):
    success:bool = False
    confirmed1:bool = False
    confirmed2:bool = False
    def __init__(self, id1:int, id2:int, name1:str, name2:str, timeout):
        super().__init__(timeout=timeout)
        self.add_item(TradeButton(id1, id2, name1, True))
        self.add_item(TradeButton(id1, id2, name2, False))

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(hidden = True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def reset(self, ctx):
        if ctx.message.author.id in authors:
            data = sqlite3.connect("data.db")
            cursor = data.cursor()
            cursor.execute("DROP TABLE poke")
            data.commit()
            data.close()
            await ctx.send("Successfully resetted all players\' data.")
        else:
            await ctx.send("This command is reserved to the *dealer*.")

    @commands.command(hidden = True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def resoption(self, ctx):
        if ctx.message.author.id in authors:
            # Rajouter toutes les listes qui comportent les données des joueurs.
            data = sqlite3.connect("data.db")
            cursor = data.cursor()
            cursor.execute("DROP TABLE option")
            data.commit()
            data.close()
            await ctx.send("Successfully resetted all players\' options.")
        else:
            await ctx.send("This command is reserved to the *dealer*.")

    @commands.command(hidden=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def delete(self, ctx, user_id):
        if ctx.message.author.id not in authors:
            return
        data = sqlite3.connect("data.db")
        cursor = data.cursor()
        cursor.execute("DELETE FROM options WHERE id==?", user_id)
        cursor.execute("DELETE FROM game WHERE id==?", user_id)
        cursor.execute("DELETE FROM locked WHERE id==?", user_id)
        cursor.execute("DELETE FROM poke WHERE id==?", user_id)
        data.commit()
        data.close()

    @commands.command(hidden = True)
    async def addpoke(self, ctx, target_id, number: typing.Optional[int] = 1, shiny: typing.Optional[bool] = False):
        if ctx.message.author.id in authors:
            try:
                target_id = ctx.message.mentions[0].id
            except:
                target_id = target_id
            add_pokemon(target_id, number-1, shiny, amount=1)
            await ctx.send("You gave a{} {} to {}.".format(["", " shiny"][shiny], dex[number][0].capitalize(), id))

    @commands.command(hidden = True)
    async def se(self, ctx, giveid, dexnumber: typing.Optional[int] = 1, shiny: typing.Optional[bool] = False):
        if ctx.message.author.id in authors:
            try:
                giveid = ctx.message.mentions[0].id
            except:
                giveid = str(giveid)
            setdata(giveid, "game", "seenabled, sedex, seisshiny", [True, dexnumber, shiny])
            await ctx.send("You gave a {}{} special encounter to {}.".format(["", "shiny "][shiny], dex[dexnumber -1][0], giveid))

    @commands.command(hidden = True)
    async def clearrb(self, ctx, clearid: typing.Optional[str] = "373707498479288330"):
        if ctx.message.author.id in authors:
            try:
                clearid = str(ctx.message.mentions[0].id)
            except:
                clearid = str(clearid)
            #datas = setdata(clearid, None)
            #datas[17] = 0
            setdata(clearid, "game", "recleft", [0])
            await ctx.send("Cleared the rb recoil.")

    @commands.command(hidden = True)
    async def moneymoneymoney(self, ctx):#, giveid: typing.Optional[str] = "373707498479288330"):
        """if ctx.message.author.id in authors:
            try:
                giveid = str(ctx.message.mentions[0].id)
            except:
                giveid = str(giveid)"""
        setdata(867494961866997760, "game", "money", None, [100000000])


class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="dex", description="Show the dex entry for a scpecific Pokémon") #aliases=["dex"]
    @app_commands.checks.cooldown(1, 10)
    async def d(self, interaction:discord.Interaction, search:str, shiny:typing.Optional[bool]=False):
        """The dex command show the dex page of a specific Pokémon. Make sure to put the special forms name before the name of the Pokémon.\nExamples : \n`.dex bulbasaur`\n`.dex shiny bulbasaur`
        """
        player_id = interaction.user.id
        language = getdata(player_id, "options", "language")
        if language is None:
            await interaction.response.send_message("Use the `/play` command before playing !", ephemeral=True)
            return
        language = language[0]
        #options = getoption(interaction.user.id)
        #shiny = args[0].lower() in ["shiny", "chromatique", "schillernden", "schillerndes", "異色", "發光", "빛나는", "iro chigai", "色違い"]
        #if shiny:
        #    argument = " ".join(args[1:]).lower()
        #else:
        #    argument = " ".join(args).lower()
        if len(search.split(" ")) > 1: #Cherche d'abord si le nom donné est exact
            found = -1
            if search in ["mr. mime", "m. mime", "pantimos", "魔牆人偶", "마임맨", "barrierd", "バリヤード"]:
                found = 121
            for i in range(len(dex_forms)):
                for j in range(len(languages)):
                    if search == dex_forms[i][j].lower():
                        found = i
                        break
                if found != -1:
                    break
            if found == -1: #Sinon cherche dans les mots-clés
                for i in range(len(forms)):
                    check = 0 #Vérifie que tous les adjectifs de formes sont dans forms.
                    for test in search.split(" "):
                        if test in forms[i]:
                            check += 1
                        else:
                            break
                    if check == len(search.split(" ")):
                        found = i
                        break
            list_name = dex_forms[found]
            found_types = dex_forms[found][-4]
            stats = dex_forms[found][-3]
            number = dex_forms[found][-5]
            if shiny:
                sprite = dex_forms[found][-1]
            else:
                sprite = dex_forms[found][-2]
            if found == -1:
                await interaction.response.send_message("Form not found, please check the spelling.", ephemeral=True)
                return
        else:
            try:
                if 0<int(search)<=len(dex):
                    number = int(search)-1
                else:
                    await interaction.response.send_message("Invalid dex number.", ephemeral=True)
                    return
            except:
                number = -1
                for i in range(len(dex)):
                    if search in dex[i]:
                        number = i
                        break
                if number == -1:
                    await interaction.response.send_message(["Pokémon not found. Check the spelling.", "Pokémon non trouvé. Vérifie l'orthographe.", "Pokémon nicht gefunden. Prüfe die Rechtschreibung.", "找不到神奇寶貝。 檢查拼寫。", "포켓몬을 찾을 수 없습니다. 철자를 확인하십시오.", "Pokemon ga mitsukarimasen. Superu o kakuninshitekudasai.", "ポケモンが見つかりません。 スペルを確認してください。"][language])
                    return
            list_name = dex[number]
            found_types = types[number]
            stats = base_stats[number]
            if shiny:
                sprite = "http://play.pokemonshowdown.com/sprites/ani-shiny/"+dex[number][0].replace(" ","_")+".gif"
            else:
                sprite = "http://play.pokemonshowdown.com/sprites/ani/"+dex[number][0].replace(". ","")+".gif"
        embed = getdex(list_name, found_types, stats, sprite, language, number+1, player_id, shiny)
        await interaction.response.send_message(embed = embed)

    @app_commands.command(name="typechart", description="Show the Pokémon typechart")
    @app_commands.checks.cooldown(1, 900)
    async def typechart(self, interaction):
        await interaction.response.send_message("From Bulbapedia.\nhttps://cdn.discordapp.com/attachments/754349043714621540/792404761563496448/Capture_decran_2020-12-26_a_15.53.16.png")

    @d.error
    @typechart.error
    async def on_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(
                f"You're under cooldown, please try again in {round(error.retry_after, 2)} seconds.", ephemeral=True)


class Miscellaneous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.checks.cooldown(1, 10)
    async def option(self, interaction:discord.Interaction):
        """The option command show the togglables options and the current options' state for you. To toggle an option make sure it is listed in the `.option` command and do `.option *OptionToToggle*`. You can toggle/change multiple options at a time by sparating them with a space.\nExamples : \n`.option`\n`.option v.o.l.`\n`.option color 0x123456`
        """
        language = getdata(interaction.user.id, "options", "language")
        if language is None:
            await interaction.response.send_message("Use the  `/play` command before playing !", ephemeral=True)
            return
        language = language[0]
        # options = getoption(interaction.user.id)

        vol, color, privacy, dexlink, gamestats, raritycolor = getdata(interaction.user.id, "options", "vol, color, privacy, dexlink, gamestats, raritycolor")
        embed = discord.Embed(title="Options",
                              description="Your current options",
                              colour=color, timestamp=datetime.utcnow())
        embed.set_footer(text="Dislate")
        embed.add_field(name="`v.o.l.`",
                        value="Let the `.dex` command show the Pokémon names in other languages. Now {}.".format(["**off**", "**on**"][vol]), inline=True)
        #embed.add_field(name="`reset`", value="Put your options to their default values.", inline=True)
        embed.add_field(name="`color`",
                        value="Put the hexadecimal value of the color you want the embeds' line to be. Current color : `{}`".format(hex(color)),
                        inline=True)
        embed.add_field(name="`language`",
                        value="Put the language code you want the game and some commands to be. Available languages : `en`, `fr`, `ge`, `ch`, `ko`, `jr`, `ja`\nCurrently set language : {}".format(
                            ["`English`", "`Français`", "`Deutsche`", "`中文`", "`한국어`", "`Hifumi`",
                             "`日文`"][language]), inline=True)
        embed.add_field(name="`link`", value="Add a link to an external Dex page with the dex command. Now {}.".format(["**off**", "**on**"][dexlink]), inline=True)
        embed.add_field(name="`gamestats`",
                        value="Add your stats to the dex page. Now {}.".format(["**off**", "**on**"][
                                                                                   gamestats]), inline=True)
        embed.add_field(name="`privacy`",
                        value="Enable privacy to not let other people see your box. Now {}.".format(
                            ["**off**", "**on**"][privacy]),
                        inline=True)
        await interaction.response.send_message(embed=embed)
        return

    """
        if "color" in args and args.index("color") < len(args):
            try:
                color = int(args[args.index("color") + 1], 16)
                options[2] = color
            except:
                await ctx.send("Invalid color value.")
                return

        if "reset" in args:
            options = defaultoption

        db["option{}".format(interaction.user.id)] = options
        embed = discord.Embed(title="Options", description="Your current options", colour=options[2],
                              timestamp=datetime.utcnow())
        embed.set_footer(text="Dislate")
        embed.add_field(name="`v.o.l.`", value=["`Off`", "`On`"][int(options[0])], inline=True)
        embed.add_field(name="`Prefix`", value="`.`", inline=True)
        embed.add_field(name="`Language`",
                        value=["`English`", "`Français`", "`Deutsche`", "`中文`", "`한국어`", "`Hifumi`", "`日文`"][
                            options[3]], inline=True)
        embed.add_field(name="`Link`", value=["`Off`", "`On`"][int(options[5])], inline=True)
        embed.add_field(name="`Privacy`", value=["`Off`", "`On`"][int(options[4])], inline=True)
        await interaction.response.send_message(embed=embed)"""

    @app_commands.command(name="randomen", description="Send you to a random Bulbapedia page")
    @app_commands.checks.cooldown(1, 1)
    async def randomen(self, interaction):
        await interaction.response.send_message(
            "This brings you to a random page of Bulbapedia : https://bulbapedia.bulbagarden.net/wiki/Special:Random")

    @app_commands.command(name="randomfr", description="Send you to a random Poképédia page")
    @app_commands.checks.cooldown(1, 1)
    async def randomfr(self, interaction):
        await interaction.response.send_message(
            "This brings you to a random page of Poképédia : https://www.pokepedia.fr/Sp%C3%A9cial:Page_au_hasard")

    @app_commands.command(name="message", description="Use this command to send a message to the owner of the bot. Don't be shy !")
    @app_commands.checks.cooldown(1, 900)
    async def message(self, interaction:discord.Interaction, message: str):
        """Use this command to send a message to the owner of the bot. Don't be shy !
        """
        #try:
        embed = discord.Embed(title="Message by user",
                              description="`Author :`{} / {}".format(interaction.user, interaction.user.id), colour=0x234564, timestamp=datetime.utcnow())
        embed.add_field(name="`Message :`", value=message, inline=False)
        embed.set_footer(text="Dislate")
        await interaction.client.get_channel(1076922920472948806).send(embed=embed)
        await interaction.response.send_message("Message sent.", ephemeral=True)
        #except:
            #await interaction.response.send_message("Your message must be 1024 or fewer in length.", ephemeral=True )

    @app_commands.command(name="toggle", description="Toggle your options")
    @app_commands.checks.cooldown(1, 5)
    async def toggle(self, interaction:discord.Interaction, option:str):
        """Use this command to change your options
        """
        short = ["vol", "privacy", "dexlink", "gamestats", "raritycolor"]
        if option.lower() not in short:
            await interaction.response.send_message("Incorrrect option.", ephemeral=True)
            return
        #try:
        current = getdata(interaction.user.id, "options", option)
        if current is None:
            await interaction.response.send_message("Use the  `/play` command before playing !", ephemeral=True)
            return
        current = current[0]
        new = (current+1)%2
        setdata(interaction.user.id, "options", option, new)
        await interaction.response.send_message("{} is now {}.".format(["`View other languages`", "`Privacy`", "`Links in dex`", "`Game stats`", "`Rarity color`"][short.index(option)], ["disabled", "enabled"][new]))
        #except:
        #    await interaction.response.send_message("An error occurred. Please retry or contact the owner.", ephemeral=True)

    @toggle.autocomplete('option')
    async def option_autocomplete(self, interaction: discord.Interaction, current:str) -> typing.List[app_commands.Choice[str]]:
        names = ["View other languages", "Privacy", "Links in dex", "Game stats", "Rarity color"]
        short = ["vol", "privacy", "dexlink", "gamestats", "raritycolor"]
        return [app_commands.Choice(name=names[short.index(l)], value=l) for l in short if current.lower() in l.lower()]

    @app_commands.command(name="setlanguage", description="Set the language of some parts of Dislate")
    @app_commands.checks.cooldown(1, 20)
    async def lang(self, interaction:discord.Interaction, lang:str):
        """Use this command to change the language of some parts of the bot. English : `en`\nFrench : `fr`\nGerman : `ge`\nChinese : `ch`\nKorean : `ko`\nJapanese (romaji) : `jr`\nJapanese : `ja`
        """
        if lang.lower() not in languages:
            await interaction.response.send_message("Incorrrect language.", ephemeral=True)
            return
        try:
            setdata(interaction.user.id, "options", "language", languages.index(lang.lower()))
            #setlanguage(interaction.user.id, languages.index(lang.lower()))
            await interaction.response.send_message("Changed language to {}.".format(lang.lower()))
        except:
            await interaction.response.send_message("An error occurred. Please retry or contact the owner.", ephemeral=True)

    @lang.autocomplete('lang')
    async def lang_autocomplete(self, interaction: discord.Interaction, current: str, ) -> typing.List[app_commands.Choice[str]]:
        names = ["English", "Français", "Deutsch", "中文", "한국인", "日本語", "日本語"]
        return [
            app_commands.Choice(name=names[languages.index(l)], value=l)
            for l in languages if current.lower() in l.lower()
        ]

    @app_commands.command(name="calc", description="Use this calculator to compute Python expression")
    @app_commands.checks.cooldown(1, 2)
    async def calc(self, interaction:discord.Interaction, expression:str):
        try:
            if eval(expression) % 1 == 0:
                await interaction.response.send_message(int(eval(expression)))
            else:
                await interaction.response.send_message(eval(expression))
        except:
            await interaction.response.send_message("Invalid syntax. Ask around or visit https://www.python.org/ to get helped.", ephemeral=True)

    @app_commands.command(name="test", description="Nothing")
    async def test(self, interaction):
        await interaction.response.send_message("!f")

    @option.error
    @randomen.error
    @randomfr.error
    @message.error
    @toggle.error
    @lang.error
    @calc.error
    async def on_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(
                f"You're under cooldown, please try again in {round(error.retry_after, 2)} seconds.", ephemeral=True)

class Game(commands.Cog):
    """The game's commands.
    """
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="trade", description="Trade Pokémon with other trainers")
    @app_commands.checks.cooldown(1, 10)
    async def trade(self, interaction:discord.Interaction, player:discord.User, pokemon1:int, pokemon2:int, shiny1: typing.Optional[bool] = False, shiny2: typing.Optional[bool] = False):
        """Use this command to trade with other players. Syntax : `.trade <id or mention> <"shiny" (optional)> <Dexnumber1> <"shiny" (optional)> <Dexnumber2>`
        """
        print("start")
        other_id = player.id
        player_id = interaction.user.id
        print(other_id, player_id)
        #tradero = setdata(id, None)
        #tradert = setdata(idt, None)
        name1 = getdata(player_id, "options", "name")
        print(name1)
        if name1 is None:
            await interaction.response.send_message("Use the `/play` command before playing !", ephemeral=True)
            return
        print(5)
        name2 = getdata(other_id, "options", "name")
        print(name2)
        if name2 is None:
            await interaction.response.send_message("Use the `/play` command before playing !", ephemeral=True)
            return
        #shiny1 = args[0].lower() in ["shiny", "chromatique", "schillernden", "schillerndes", "異色", "發光", "빛나는", "iro chigai", "色違い"]

        print("poke{}".format(["mon", "shi"][shiny1]))
        pokeamount = extract(player_id, "poke{}".format(["mon", "shi"][shiny1]), pokemon1)
        print(pokeamount)
        if pokeamount < 1:
            await interaction.response.send_message("You don't have the Pokémon you're proposing.", ephemeral=True)
            return
        print("poke{}".format(["mon", "shi"][shiny2]))
        pokeamount = extract(other_id, "poke{}".format(["mon", "shi"][shiny2]), pokemon2)
        if pokeamount < 1:
            await interaction.response.send_message("The other player doesn't have the Pokémon you want.", ephemeral=True)
            return
        print("amount passed")
        """def check1(m):
            return str(m.author.id) == id and m.channel == ctx.message.channel and m.content.lower() == "confirm"

        def check2(m):
            return str(m.author.id) == idt and m.channel == ctx.message.channel and m.content.lower() == "confirm"""
        text = "{}'s **{}{}** :left_right_arrow: {}'s **{}{}**".format(name1[0], ["", "shiny "][shiny1], dex[pokemon1 - 1][0], name2[0], ["", "shiny "][shiny2], dex[pokemon2 - 1][0])
        embed = discord.Embed(title="Trade",
                              description="||I know you clicked on this so give the owner 10 coins now.||",
                              colour=0x000000, timestamp=datetime.utcnow())
        embed.set_footer(text="Dislate")
        embed.add_field(name="Trade offer",
                        value=text, inline=True)
        view = Trade(player_id, other_id, name1[0], name2[0], 20)
        await interaction.response.send_message(embed=embed, view=view)
        await view.wait()
        if not view.success:
            await interaction.edit_original_response(content="Trade canceled.\n"+text)
            return
        """try:
            await interaction.response.send_message(
                "<@{}> Type **`confirm`** to confirm this trade :\n Your **{}{}** for his/her **{}{}**.".format(id, ["", "shiny "][int(shiny1)], dex[poke1 - 1][0], ["", "shiny "][int(shiny2)], dex[poke2 - 1][0]))
            await interaction.client.wait_for("message", check=check1, timeout=20.0)
        except asyncio.TimeoutError:
            return await interaction.response.send_message("Timeout. Trade canceled.")
        try:
            await interaction.response.send_message(
                    "<@{}> Type **`confirm`** to confirm this trade :\n Your **{}{}** for his/her **{}{}**.".format(idt, ["", "shiny "][int(shiny2)], dex[poke2 - 1][0], ["", "shiny "][int(shiny1)], dex[poke1 - 1][0]))
            await bot.wait_for("message", check=check2, timeout=20.0)
        except asyncio.TimeoutError:
            return await interaction.response.send_message("Timeout. Trade canceled.", ephemeral=True)"""
        add_pokemon(player_id, pokemon1, shiny1, amount=-1)
        add_pokemon(other_id, pokemon2, shiny2, amount=-1)
        add_pokemon(player_id, pokemon2, shiny2, amount=1)
        add_pokemon(other_id, pokemon1, shiny1, amount=1)
        #tradero[7][poke1 - 1][int(shiny1)] -= 1
        #tradert[7][poke2 - 1][int(shiny2)] -= 1
        #tradero[7][poke2 - 1][int(shiny2)] += 1
        #tradert[7][poke1 - 1][int(shiny1)] += 1
        embed = discord.Embed(title="Trade", colour=0x000000, timestamp=datetime.utcnow())
        embed.set_footer(text="Dislate")
        embed.add_field(name="Successful trade",
                            value="{}'s **{}{}** :left_right_arrow: {}'s **{}{}**".format(name1[0], ["", "shiny "][shiny1], dex[pokemon1 - 1][0], name2[0], ["", "shiny "][shiny2], dex[pokemon2 - 1][0]), inline=True)
        await interaction.client.get_channel(1078020371271389214).send(embed=embed)
        await interaction.edit_original_response(content="You succesfully traded.", embed=embed, view=None)

    @app_commands.command(name="encounter", description="Encounter a Pokémon")
    @app_commands.checks.cooldown(1, 2)
    async def encounter(self, interaction):
        """Use this command to catch some Pokémon.
        """
        se = ""
        player_id = interaction.user.id
        #datas = setdata(player_id, interaction.user)
        options = getdata(player_id, "options", "name, color, language, raritycolor")
        if options is None:
            await interaction.response.send_message("Use the  `/play` command before playing !", ephemeral=True)
            return
        name, color, language, raritycolor = options

        frazzleft, rrazzleft, lmleft, money, pb, gb, ub, mb, rb, bb, qb, db, cb, prb, fb, recleft, rbred, rbeffect, rbluck, amuletcoin, seenabled, sedex, seisshiny, partner, dreamed, money, totalmoney = getdata(player_id, "game", "frazzleft, rrazzleft, lmleft, money, pb, gb, ub, mb, rb, bb, qb, db, cb, prb, fb, recleft, rbred, rbeffect, rbluck, amuletcoin, seenabled, sedex, seisshiny, partner, dreamed, money, totalmoney")
        add_game = {}
        change_game = {}
        #specialencounter = datas[21]

        fakee, raree, luckye = False, False, False


        #def is_correct(m):
        #    return m.author.id == player_id and m.content.lower() in listballs and datas[10][
        #        listballs.index(m.content.lower())] > 0
        spawnweight = getspawnweights(player_id)
        effecttext = ""

        if frazzleft > 0:
            add_game["frazzleft"] = -1
            effecttext = "Fake razz ({} encounter{} left)".format(frazzleft, ["s", ""][frazzleft==1])
            fakee = True

        if rrazzleft > 0:
            add_game["rrazzleft"] = -1
            effecttext += "\nRare razz ({} encounter{} left)".format(rrazzleft, ["s", ""][rrazzleft==1])
            raree = True

        if lmleft > 0 and money > 2500:
            add_game["lmleft"] = -1
            add_game["lmencounter"] = 1
            add_game["money"] = -2500
            effecttext += "\nLucky machine ({} encounter{} left)".format(lmleft, ["s", ""][lmleft==1])
            luckye = True
        if recleft>0:
            effecttext += "\nRecoil ({} encounter{} left)".format(recleft, ["s", ""][recleft == 1])
        if seenabled:
            spawnnumber = sedex - 1
            shiny = seisshiny
            rarity = getrarity(spawnnumber + 1)
            change_game["seenabled"] = 0
            se = " **Special encounter**"
        else:
            shiny = choices([True, False], weights=[1, 8192])[0]
            rarity = choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], weights=spawnweight)[0]
            spawnnumber = choices(
                [commonpool, uncommonpool, rarepool, rarerpool, veryrarepool, pseudolegendarypool, legendarypool,
                    mythicalpool, ultrabeastpool, god][rarity])[0] - 1
        if dreamed == spawnnumber:
            effecttext += "\nThis is your dreamed Pokémon !"
        if partner == spawnnumber:
            effecttext += "\nThis is your partner Pokémon !"
        Rarity = rarityname[rarity]
        spawn = dex[spawnnumber]
        if raritycolor:
            color = [0x77AA, 0x3388, 0x335566, 0x552222, 0x771111, 0x442255, 0x837465, 0x33FF33, 0x123456, 0xFFFFFF,
                        0x222211][rarity]

        pokemon = spawn[language].capitalize()
        embedtitle = "{} #{}".format(pokemon, spawnnumber + 1)
        if shiny:
            embedtitle = ":star2: {}".format(embedtitle)
            color = 0xFFFFFF - color

        embed = discord.Embed(title=embedtitle, description=name, colour=color, timestamp=datetime.utcnow())
        embed.set_footer(text="Dislate")
        if rarity > 5 or shiny:
            rarespawns = discord.Embed(title="A {} spawned !{}".format(embedtitle, se), description=Rarity,
                                           colour=color, timestamp=datetime.utcnow())
            rarespawns.set_footer(text="Dislate")
            if shiny:
                rarespawns.set_image(
                    url="http://play.pokemonshowdown.com/sprites/ani-shiny/{}.gif".format(spawn[0].replace(" ", "_")))
            else:
                rarespawns.set_image(
                    url="http://play.pokemonshowdown.com/sprites/ani/{}.gif".format(spawn[0].replace(". ", "")))
            await interaction.client.get_channel(1076902678099140758).send(embed=rarespawns)

        if shiny:
            cshiny = extract(player_id, "cpokeshi", spawnnumber+1)
            text = "Rarity : 1/8192\nCaught : {}".format(cshiny)
        else:
            normal = extract(player_id, "cpokemon", spawnnumber+1)
            text = "Rarity : {}\nCaught : {}".format(Rarity, normal)
        balldic = {}
        if pb > 0:
            text += "\n<:pb:{}> Pokéball : {}".format(ballsid[listballs.index("pb")], pb)
            balldic["pb"] = pb
        if gb > 0:
            text += "\n<:gb:{}> Greatball : {}".format(ballsid[listballs.index("gb")], gb)
            balldic["gb"] = gb
        if ub > 0:
            text += "\n<:ub:{}> Ultraball : {}".format(ballsid[listballs.index("ub")], ub)
            balldic["ub"] = ub
        if mb > 0:
            text += "\n<:mb:{}> Masterball : {}".format(ballsid[listballs.index("mb")], mb)
            balldic["mb"] = mb
        if rb > 0:
            text += "\n`rb` Recoilball : {}".format(rb)
            balldic["rb"] = rb
        #if recleft > 0:
        #    text += "\nRecoil left : {}".format(recleft)
        if bb > 0:
            text += "\n<:bb:{}> Beastball : {}".format(ballsid[listballs.index("bb")], bb)
            balldic["bb"] = bb
        if qb > 0:
            text += "\n<:qb:{}> Quickball : {}".format(ballsid[listballs.index("qb")], qb)
            balldic["qb"] = qb
        if db > 0:
            text += "\n<:db:{}> Dreamball : {}".format(ballsid[listballs.index("db")], db)
            balldic["db"] = db
        if cb > 0:
            text += "\n`cb` Cloneball : {}".format(cb)
            balldic["cb"] = cb
        if prb > 0:
            text += "\n<:prb:{}> Premier ball : {}".format(ballsid[listballs.index("prb")] , prb)
            balldic["prb"] = prb
        if fb > 0:
            text += "\n`fb` Fifty-fifty ball : {}".format(fb)
            balldic["fb"] = fb

        embed.add_field(name="`What to do ?`", value=text, inline=False)
        if fakee or raree or luckye:
            embed.add_field(name="`Active effects`", value=effecttext, inline=False)
        if shiny:
            embed.set_image(
                url="http://play.pokemonshowdown.com/sprites/ani-shiny/{}.gif".format(spawn[0].replace(" ", "_")))
        else:
            embed.set_image(
                url="http://play.pokemonshowdown.com/sprites/ani/{}.gif".format(spawn[0].replace(". ", "")))
        view = Balls(balldic, player_id, timeout=20)
        await interaction.response.send_message(embed=embed, view=view)
        await view.wait()

        """
        try:
            sentball = await interaction.response.send_message("message", check=is_correct, timeout=20.0)
        except asyncio.TimeoutError:
            return await encounter.edit(content="{} fled !".format(pokemon))
        
        sentball = sentball.content.lower()"""
        sentball = view.sentball
        if sentball is None:
            return await interaction.edit_original_response(content="{} fled !".format(pokemon), embed=None, view=None)

        randomcatch = randint(0, 100)
        if sentball == "mb":
            iscaught = 99
        elif sentball == "fb":
            iscaught = 50
        else:
            iscaught = catchrate[rarity] + ballcr[listballs.index(sentball)] - 80 * int(shiny) - 50 * (
                    recleft > 0) - int(2 * recleft / (1+25 * rbeffect)) + 60 * int(
                rarity == 8 and sentball == "bb") + 150 * int(
                dreamed == spawnnumber and sentball == "db") + 150 * int(
                partner == spawnnumber and sentball == "cb")
        if fakee:
            iscaught += 20
        if raree:
            iscaught -= 10
        change_game["recleft"] = max(recleft - 1, 0)
        recleft = max(recleft - 1, 0)
        #datas[17] = max(datas[17] - 1, 0)
        if sentball == "rb":
            add_game["recleft"] = 100-rbred
            recleft = 100-rbred+recleft
            #datas[17] += 100 - datas[18][0]
        add_game[sentball] = -1#-fakee-raree
        add_game["{}used".format(sentball)] = 1
        embed = discord.Embed(title=embedtitle, description="{} sent a <:{}:{}>".format(name, sentball, ballsid[listballs.index(sentball)]), colour=color, timestamp=datetime.utcnow())
        embed.set_footer(text="Dislate")
        if shiny:
            embed.set_image(
                url="http://play.pokemonshowdown.com/sprites/ani-shiny/{}.gif".format(spawn[0].replace(" ", "_")))
        else:
            embed.set_image(
                url="http://play.pokemonshowdown.com/sprites/ani/{}.gif".format(spawn[0].replace(". ", "")))
        state = 0
        if randomcatch > iscaught and sentball == "qb":
            retry = choices([False, True])[0]
            if retry and prb < 1:
                state = 1  # Chanceux mais pas d'honor ball.
            elif retry and prb > 0:
                add_game["prb"] = -1
                #datas[10][9] -= 1
                iscaught += 10
                randomcatch = randint(0, 100)
                state = 2  # Chanceux avec honor ball

        if randomcatch <= iscaught:
            if state == 2: # Si une honor ball a été lancée et la capture est réussie
                state = 3
            gotmoney = randint([99, 120, 300, 600, 1300, 500, 10000, 20000, 10000, 200000][rarity],
                                [120, 200, 400, 800, 1800, 750, 15000, 25000, 100000, 2000000][rarity])
            coinbonus = int(gotmoney * amuletcoin * 0.05)
            add_game["money"] = gotmoney+coinbonus
            add_game["totalmoney"] = gotmoney+coinbonus
            add_game["caught"] = 1
            #datas[14] += gotmoney
            #datas[9] += gotmoney
            add_pokemon(player_id, spawnnumber+1, shiny, updateiv=True)
            text = "You caught {} !\nRarity : {} \nCatch power : {} | Catch number : {}\nYou earned {} coins.".format(
                pokemon, Rarity, iscaught, randomcatch, gotmoney)
            if coinbonus > 0:
                text += "You got {} bonus coins.".format(coinbonus)
            if recleft > 0:
                luck = randint(1, 100 + rbluck)
                if luck > 95:
                    reduction = randint(1, 5)
                    change_game["recleft"] = max(0, recleft - reduction)
                    text += "\nLucky ! Your recoil got reduced by {}.".format(reduction)
                    if state > 0:
                        text += "You got lucky and an Premier ball was thrown."

                    # await message.channel.send("You caught {} !\nCatch power : {}  Catch number : {}\nYou earned {} coins.".format(pokemon, iscaught, randomcatch, gotmoney))
        else:
            text = "{} broke free !\nRarity : {} \nCatch power : {} | Catch number : {}".format(pokemon, Rarity,
                                                                                                    iscaught,
                                                                                                    randomcatch)
        if state > 0:
            if state == 1:
                text += "\nYou got lucky but you didn't have Premier ball."
            elif state == 2:
                text += "\nYou got lucky but the Pokémon still fled."
            else:
                text += "\nYou got lucky and caught the Pokémon."
        #change_values, add_values = "", ""
        embed.add_field(name="`Result`", value=text)
        change_values, add_values = [], []
        change_keys = ", ".join(list(change_game.keys()))
        for key in list(change_game.keys()):
            #change_values = change_values+str(change_game[key])+", "
            change_values.append(change_game[key])
        add_keys = ", ".join(list(add_game.keys()))
        for key in list(add_game.keys()):
            #add_values = add_values+str(add_game[key])+", "
            add_values.append(add_game[key])
        setdata(player_id, "game", change_keys, change_values)
        setdata(player_id, "game", add_keys, None, add_values)
        await interaction.edit_original_response(embed=embed, view=None)

        # db["player_data"+str(id)] = datas

    @app_commands.command(name="box", description="Show your boxes") # aliases=["pc"]
    @app_commands.checks.cooldown(1, 5)
    async def box(self, interaction:discord.Interaction, user: discord.User = None, page: typing.Optional[int] = 1):
        """The box command show your owned Pokémon. The default box page is the first one with the national dex number order. You can choose to see a certain page or with a certain sorting order. You must give the page number if you specify the sorting order.\nSyntax : `.box <page> <sorting order number>`\nSorting order : \n`1 (Default)` : The national dex number order.\n`2` : The descending rarity order.\n`3` : The ascending rarity order.\n`4` : The descending order with shinies first.\nExamples : \n`.box`\n`.box 1 1`\n`.box 2 4`
        """
        # sort = 1:Ordre pokédex, 2:Ordre rareté descendant, 3:Ordre rareté ascendant, 4:Ordre rareté descendant avec shinys en premiers
        if user is not None:
            user_id = user.id
        else:
            user_id = interaction.user.id
        options = getdata(user_id, "options", "color, language, privacy, name")
        if options is None:
            await interaction.response.send_message("Use the `/play` command before playing !", ephemeral=True)
            return

        sortedbox, total, color, language, privacy, name = 0, 0, options[0], options[1], options[2], options[3]
        if interaction.user.id != user_id and privacy:
            await interaction.response.send_message("You can't see this player's box.", ephemeral=True)
            return
        box = []
        for i in range(1, len(dex), 5):
            pack = extractlist(user_id, "pokemon", i)
            spack = extractlist(user_id, "pokeshi", i)
            #scanning = datas[7][i]
            for j in range(5):
                if pack[j] > 0 or spack[j]:
                    rarity = getrarity(i+j)
                    box.append([i+j, pack[j], spack[j], rarity])
        max_pages = max(len(box)-1, 0)//20+1
        if page>max_pages:
            page = max_pages
        embed = getboxembed(name, color, language, max_pages, page-1, box, 0)
        view = Box(interaction.user.id, name, color, language, max_pages, page, box, 20)
        await interaction.response.send_message(embed=embed, view=view)

        await view.wait()
        await interaction.edit_original_response(view=None)
        #await view.disable()

                    #total += 1
        #total = int((total - 1) / 20) + 1
        """
        try:
            if sort == 1:
                for i in range(len(dex)):
                    if sortedbox >= 20 * page:
                        break
                    scanning = datas[7][i]  # [0]
                    if scanning[0] > 0 or scanning[1] > 0:
                        rarity = rarityname[getrarity(i + 1)]
                        sortedbox += 1
                        if sortedbox > 20 * (page - 1):
                            text += "`{}` `{}` {} | {} {}\n".format(i+1, rarity, scanning[0], scanning[1], dex[i][language].capitalize())
            elif sort in [2, 3]:
                if sort == 2:
                    generalpool = god + ultrabeastpool + mythicalpool + legendarypool + egg + pseudolegendarypool + veryrarepool + rarerpool + rarepool + uncommonpool + commonpool
                else:
                    generalpool = commonpool + uncommonpool + rarepool + rarerpool + veryrarepool + pseudolegendarypool + egg + legendarypool + mythicalpool + ultrabeastpool + god
                for i in generalpool:
                    i -= 1
                    if sortedbox >= 20 * page:
                        break
                    scanning = datas[7][i]
                    if scanning[0] > 0 or scanning[1] > 0:
                        rarity = rarityname[getrarity(i + 1)]
                        sortedbox += 1
                        if sortedbox > 20 * (page - 1):
                            text += "`{}` `{}` {} | {} {}\n".format(i+1, rarity, scanning[0], scanning[1], dex[i][language].capitalize())
            elif sort == 4:
                generalpool = god + ultrabeastpool + mythicalpool + legendarypool + egg + pseudolegendarypool + veryrarepool + rarerpool + rarepool + uncommonpool + commonpool
                alreadyadded = []
                for i in generalpool:
                    i -= 1
                    if sortedbox >= 20 * page:
                        break
                    scanning = datas[7][i]
                    if scanning[1] > 0:
                        rarity = rarityname[getrarity(i + 1)]
                        sortedbox += 1
                        alreadyadded.append(i)
                        if sortedbox > 20 * (page - 1):
                            text += "`{}` `{}` {} | {} {}\n".format(i+1, rarity, scanning[0], scanning[1], dex[i][language].capitalize())
                for i in generalpool:
                    i -= 1
                    if sortedbox >= 20 * page:
                        break
                    scanning = datas[7][i]
                    if scanning[0] > 0 and i not in alreadyadded:
                        rarity = rarityname[getrarity(i + 1)]
                        sortedbox += 1
                        if sortedbox > 20 * (page - 1):
                            text += "`{}` `{}` {} | {} {}\n".format(i+1, rarity, scanning[0], scanning[1], dex[i][language].capitalize())
        except:
            text = "Invalid page number."
        """

    @app_commands.command(name="spawnrates", description="Show your current Pokémon spawn rates")
    @app_commands.checks.cooldown(1, 5)
    async def spawnrates(self, interaction):
        """Use this command to see your spawn rates.
        """
        language = getdata(interaction.user.id, "options", "language")
        if language is None:
            await interaction.response.send_message("Use the  `/play` command before playing !", ephemeral=True)
            return

        spawnweight = getspawnweights(interaction.user.id)
        somme = sum(spawnweight)
        await interaction.response.send_message(
            "`Common :` 1/{}\n`Uncommon :` 1/{}\n`Rare :` 1/{}\n`Rarer :` 1/{}\n`Very rare :` 1/{}\n`Pseudo legendary :` 1/{}\n`Legendary :` 1/{}\n`Mythical :` 1/{}\n`Ultra beast :` 1/{}\n`God :` 1/{}".format(
                int(not (spawnweight[0] == 0)) * somme / (spawnweight[0] ** int(not (spawnweight[0] == 0))),
                int(not (spawnweight[1] == 0)) * somme / (spawnweight[1] ** int(not (spawnweight[1] == 0))),
                int(not (spawnweight[2] == 0)) * somme / (spawnweight[2] ** int(not (spawnweight[2] == 0))),
                int(not (spawnweight[3] == 0)) * somme / (spawnweight[3] ** int(not (spawnweight[3] == 0))),
                int(not (spawnweight[4] == 0)) * somme / (spawnweight[4] ** int(not (spawnweight[4] == 0))),
                int(not (spawnweight[5] == 0)) * somme / (spawnweight[5] ** int(not (spawnweight[5] == 0))),
                int(not (spawnweight[6] == 0)) * somme / (spawnweight[6] ** int(not (spawnweight[6] == 0))),
                int(not (spawnweight[7] == 0)) * somme / (spawnweight[7] ** int(not (spawnweight[7] == 0))),
                int(not (spawnweight[8] == 0)) * somme / (spawnweight[8] ** int(not (spawnweight[8] == 0))),
                int(not (spawnweight[9] == 0)) * somme / (spawnweight[9] ** int(not (spawnweight[9] == 0)))))

    @app_commands.command(name="rename", description="Change your game name") # aliases=["nickname"]
    @app_commands.checks.cooldown(1, 900)
    async def rename(self, interaction:discord.Interaction, name:str):
        """This command to rename yourself in the game.\nsSyntax : `/rename <newname>`
        """
        player_id = interaction.user.id
        setdata(player_id, "options", "name", "'{}'".format(name))
        await interaction.response.send_message("You successfully renamed yourself into {}.".format(name))

    @app_commands.command(name="shop", description="Visit the shop to buy items") # aliases=["sh", "shop"]
    @app_commands.checks.cooldown(1, 10)
    async def shop(self, interaction:discord.Interaction, item: typing.Optional[str] = None, amount: app_commands.Range[int, 1]=1):
        """Use this command to see the shop and buy things in it.\nSyntax : `.s <itemnumber> <amount>`
        """
        player_id = interaction.user.id
        color = getdata(player_id, "options", "color")
        if color is None:
            await interaction.response.send_message("Use the  `/play` command before playing !", ephemeral=True)
            return
        color = color[0]
        short = []
        for i in range(len(buyableitems)):
            short.append(buyableitems[i][0])

        if item is None:
            amounts = getdata(player_id, "game", ", ".join(short) + ", money")
            embed = discord.Embed(title="Shop",
                                  description="`Buy what you need !` You have {} :coin:.".format(amounts[-1]),
                                  colour=color, timestamp=datetime.utcnow())
            embed.set_footer(text="Dislate")

            embed.add_field(name="`Items`", value="\n".join([" | ".join(
                ["`{}`".format(buyableitems[i][1]),
                 "Cost : {} :coin:".format(buyableitems[i][2]), "`Earned : {}`".format(amounts[i])]) for i in
                range(len(buyableitems))]), inline=True)
            await interaction.response.send_message(embed=embed)
            return
        if item not in short:
            await interaction.response.send_message("Incorrect item.", ephemeral=True)
            return
        ind = short.index(item)
        money, amuletcoin = getdata(player_id, "game", "money, amuletcoin")
        if money<buyableitems[ind][2]*amount:
            await interaction.response.send_message("You don't have enough coins !.", ephemeral=True)
            return
        if item=="amuletcoin" and amuletcoin+amount>50:
            amount = 50-amuletcoin
        setdata(player_id, "game", item+", money", None, [amount, -buyableitems[ind][2]*amount])
        if item=="pb" and amount>9:
            setdata(player_id, "game", "prb", None, [amount//10])
        #bought, moneyleft, amuletnumber = additems(item, amount, player_id, str(ctx.message.author))

        await interaction.response.send_message(
            "You bought {} {} and have {} :coin: left.".format(amount, buyableitems[ind][1], money-buyableitems[ind][2]*amount))
        return

    @shop.autocomplete('item')
    async def shop_autocomplete(self, interaction: discord.Interaction, current: str,) -> typing.List[app_commands.Choice[str]]:
        names = ["Pokéball", "Greatball", "Ultraball", "Masterball", "Recoilball", "Beastball", "Quickball", "Dreamball", "Cloneball", "Fifty-fifty ball", "Amulet coin", "Fake razz", "Rare razz"]
        short = ["pb", "gb", "ub", "mb", "rb", "bb", "qb", "db", "cb", "fb", "amuletcoin", "frazz", "rrazz"]
        return [app_commands.Choice(name=names[short.index(l)], value=l) for l in short if current.lower() in l.lower()]

    @app_commands.command(name="inventory", description="Show your inventory") # aliases=["item", "items", "bag", "inventory"]
    @app_commands.checks.cooldown(1, 10)
    async def inventory(self, interaction):
        """Use this command see what you got in your bag.
        """
        player_id = interaction.user.id
        color = getdata(player_id, "options", "color")
        if color is None:
            await interaction.response.send_message("Use the `/play` command before playing !", ephemeral=True)
            return
        color = color[0]
        short = []
        for i in range(len(allitems)):
            short.append(allitems[i][0])
        amounts = getdata(player_id, "game", ", ".join(short)+", money")
        embed = discord.Embed(title="Bag", description="{} :coin:".format(amounts[-1]), colour=color,
                              timestamp=datetime.utcnow())

        embed.set_footer(text="Dislate")
        embed.add_field(name="`Items`", value="\n".join(
            [" : ".join(["`{}`".format(allitems[i][1]), str(amounts[i])]) for i in
             range(len(allitems))]), inline=True)
        await interaction.response.send_message(embed=embed)
    @app_commands.command(name="release", description="Release your Pokémon") # aliases=["rls"]
    @app_commands.checks.cooldown(1, 7)
    async def release(self, interaction:discord.Interaction, releasing: typing.Optional[str] = "d", amount: typing.Optional[int] = 1,
                      shiny: typing.Optional[bool] = False):
        """Use this command to release your Pokémon.\nSyntax : `.rls d` to release all your duplicates except Legendary, Mythical, Ultrabest and God ones.\n`.rls <dexnumber> <amount>
        """
        player_id = interaction.user.id
        #datas = setdata(id, str(interaction.user))
        #locked = datas[20]
        locked = getdata(player_id, "locked", "*")
        if locked is None:
            await interaction.response.send_message("Use the `/play` command before playing !", ephemeral=True)
            return
        locked = list(locked)[1:]

        if releasing == "d":
            box = []
            for i in range(1, len(dex), 5):
                pack = extractlist(player_id, "pokemon", i)

                for j in range(5):
                    if pack[j] > 1:
                        rarity = getrarity(i + j)
                        if rarity<6:
                            box.append([i + j, pack[j], rarity])
            dupes = [0, 0, 0, 0, 0, 0]
            gotmoney = 0
            if len(box) == 0:
                await interaction.response.send_message("You have no duplicates to release !", ephemeral=True)
                return
            for i in range(len(box)):
                if box[i][0] in locked:
                    continue

                rarity = box[i][2]
                #if rarity > 5:
                #    continue
                dupes[rarity] += box[i][1] - 1
                gotmoney += (box[i][1] - 1) * releasemoney[rarity]
                add_pokemon(player_id, box[i][0], False, False, -box[i][1] + 1)
                #release[0] = 1
            setdata(player_id, "game", "money, totalmoney", None, [gotmoney, gotmoney])
            #datas[9] += gotmoney
            #datas[14] += gotmoney
            # db["player_data"+id] = datas
            await interaction.response.send_message(
                "You got {} coins by releasing\n{} common\n{} uncommon\n{} rare\n{} rarer\n{} very rare\n{} pseudo legendary".format(
                    gotmoney, dupes[0], dupes[1], dupes[2], dupes[3], dupes[4], dupes[5]))
            return
        try:
            releasing = int(releasing)
        except:
            await interaction.response.send_message("Invalid argument : `d` to release duplicates, dex number to release a specific Pokémon", ephemeral=True)
            return
        if releasing > 0:
            if shiny:
                pokeamount = extract(player_id, "pokeshi", releasing)
            else:
                pokeamount = extract(player_id, "pokemon", releasing)
                print(pokeamount)
            if pokeamount - amount < 0:
                await interaction.response.send_message("You can't release Pokémon you don't own.", ephemeral=True)
                return
            language, = getdata(player_id, "options", "language")
            #datas[7][releasing - 1][int(shiny)] -= amount
            add_pokemon(player_id, releasing, shiny, updateiv=False, amount=-amount)
            rarity = getrarity(releasing)
            gotmoney = amount * releasemoney[rarity] * 1000 ** int(shiny)
            setdata(player_id, "game", "money, totalmoney", None, [gotmoney, gotmoney])
            # db["player_data"+id] = datas
            released = dex[releasing - 1][language].capitalize()
            if shiny:
                released = "shiny " + released
            await interaction.response.send_message("You released {} {} and got {} coins.".format(amount, released, gotmoney))

    @app_commands.command(name="fakerazz", description="Activate the effect of the fake razz")
    @app_commands.checks.cooldown(1, 15)
    async def fakerazz(self, interaction:discord.Interaction, amount: app_commands.Range[int, 0]=0):
        """Use this command to activate the fake razz's effect. Fake razz divides by 2 the Legendary, Mythical, Ultrabeast and God spawn rates but gives you a 20 catch power bonus for 50 encounters each.\nSyntax : `.fr <amount>`
        """
        player_id = interaction.user.id
        frazz = getdata(player_id, "game", "frazz, frazzleft")
        if frazz is None:
            await interaction.response.send_message("Use the `/play` command before playing !", ephemeral=True)
            return
        frazz, frazzleft = frazz
        if not amount:
            if frazzleft < 1:
                await interaction.response.send_message(
                    "You don't have any fake razz effect activated. Activate or buy some in the shop ! You currently have {} fake razz.".format(
                        frazz))
                return
            else:
                await interaction.response.send_message(
                    "The fake razz effect is active for {} more encounter. You have {} fake razz now.".format(
                        frazzleft, frazz))
                return
        elif amount > frazz:
            await interaction.response.send_message("You don't have that many fake razz. You only have {} now.".format(frazz))
            return
        else:
            setdata(player_id, "game", "frazz, frazzused, frazzleft", None, [-amount, amount, 50*amount])
            frazzleft+=50*amount
            await interaction.response.send_message("Fake razz is now activated for {} more encounters.".format(frazzleft))
            # db["player_data"+str(id)] = datas

    @app_commands.command(name="rarerazz", description="Activate your rare razz") # aliases=["rr"]
    @app_commands.checks.cooldown(1, 15)
    async def rarerazz(self, interaction:discord.Interaction, amount: app_commands.Range[int, 0]=0):
        """Use this command to activate the rare razz's effect. Rare razz doubles Legendary, Mythical, Ultrabeast and God spawn rates but gives you a -20 catch power malus for 50 encounters each.\nSyntax : `.rr <amount>`
        """
        player_id = interaction.user.id
        rrazz = getdata(player_id, "game", "rrazz, rrazzleft")
        if rrazz is None:
            await interaction.response.send_message("Use the `/play` command before playing !", ephemeral=True)
            return
        rrazz, rrazzleft = rrazz
        if not amount :
            if rrazzleft < 1:
                await interaction.response.send_message(
                    "You don't have any rare razz effect activated. Activate or buy some in the shop ! You currently have {} rare razz.".format(
                        rrazz))
                return
            else:
                await interaction.response.send_message(
                    "The rare razz effect is active for {} more encounter. You have {} rare razz now.".format(
                        rrazzleft, rrazz))
                return
        elif amount > rrazz:
            await interaction.response.send_message(
                "You don't have that many rare razz. You only have {} now.".format(rrazz))
            return
        else:
            setdata(player_id, "game", "rrazz, rrazzused, rrazzleft", None, [-amount, amount, 50 * amount])
            rrazzleft += 50 * amount
            await interaction.response.send_message(
                "Rare razz is now activated for {} more encounters.".format(rrazzleft))

    @app_commands.command(name="luckymachine", description="Activate the lucky machine") #aliases=["luckymachine"]
    @app_commands.checks.cooldown(1, 15)
    async def luckymachine(self, interaction:discord.Interaction, amount: app_commands.Range[int, 0]=0):
        """Use this command to activate the lucky machine for a certain amount of encounters. It triples the Legendary, Mythical, Ultrabeast and God spawn rates but costs 2500 coins each encounter.\nSyntax : `.lm <amount>`
        """
        player_id = interaction.user.id
        lmleft = getdata(player_id, "game", "lmleft")
        if lmleft is None:
            await interaction.response.send_message("Use the `/play` command before playing !", ephemeral=True)
            return
        lmleft = lmleft[0]
        if not amount:
            if lmleft < 1:
                await interaction.response.send_message(
                    "The lucky machine isn't activated. Activate it by specifying the number of encounter.")
            else:
                await interaction.response.send_message("The lucky machine is activated for {} more encounter.".format(lmleft))
        else:
            lmleft += amount
            setdata(player_id, "game", "lmleft", None, [amount])
            await interaction.response.send_message("The lucky machine is now activated for {} more encounters.".format(lmleft))
            # db["player_data"+id] = datas

    @app_commands.command(name="recoilball", description="See and upgrade your recoil ball") #aliases=["rb"]
    @app_commands.checks.cooldown(1, 5)
    async def recoilball(self, interaction:discord.Interaction, upgrade: typing.Optional[str] = None):
        """Upgrade your recoilball here.\nReducer : Reduces the number of recoiled encounters a recoilball will give.\nEffect : Reduces the reduction of catch power due to recoil.\nLuck : Give you a higher chance of reducing your accumulated recoil when catching a Pokémon.\nSyntax : `.rb <reducer/effect/luck>`
        """
        player_id = interaction.user.id
        #datas = setdata(id, str(interaction.user))
        money = getdata(player_id, "game", "money")
        if money is None:
            await interaction.response.send_message("Use the `/play` command before playing !", ephemeral=True)
            return
        money = money[0]
        if upgrade is None:
            color, = getdata(player_id, "options", "color")
            rbred, rbeffect, rbluck = getdata(player_id, "game", "rbred, rbeffect, rbluck")
            embed = discord.Embed(title="Recoilball", description="Money : {}".format(money), colour=color,
                                  timestamp=datetime.utcnow())
            embed.set_footer(text="Dislate")
            reducertext = "Reduces the number of recoiled encounters a recoilball will give. Current level : {}".format(
                rbred)
            if rbred < 20:
                reducertext += "\nNext cost : {}".format(100 * 2 ** rbred)
            effecttext = "Reduces the reduction of catch power due to recoil. Current level : {}".format(rbeffect)
            if rbeffect < 20:
                effecttext += "\nNext cost : {}".format(100 * 2 ** rbeffect)
            lucktext = "Give you a higher chance of reducing your accumulated recoil. Current level : {}".format(rbluck)
            if rbluck < 20:
                lucktext += "\nNext cost : {}".format(100 * 2 ** rbluck)
            embed.add_field(name="`Reducer`", value=reducertext, inline=True)
            embed.add_field(name="`Effect`", value=effecttext, inline=True)
            embed.add_field(name="`Luck`", value=lucktext, inline=True)
            await interaction.response.send_message(embed=embed)
            return
        if upgrade.lower() in ["rbred", "rbeffect", "rbluck"]:
            upgrade = upgrade.lower()
            ind = ["rbred", "rbeffect", "rbluck"].index(upgrade)
            #upgrade = ["reducer", "effect", "luck"].index(upgrade.lower())
            level, = getdata(player_id, "game", upgrade)
            if level>19:
                await interaction.response.send_message("You can't upgrade your recoil ball's {} any further.".format(["reducer", "effect", "luck"][ind]), ephemeral=True)
                return
            cost = 100 * 2 ** level
            if money < cost:
                await interaction.response.send_message("You need {} more coins to upgrade the {}".format(cost-money, ["reducer.", "effect.", "luck."][ind]))
            else:
                setdata(player_id, "game", "money, {}".format(upgrade), None, [-cost, 1])
                #datas[9] -= cost
                #datas[18][upgrade] += 1
                await interaction.response.send_message("You spent {} to upgrade the recoilball's {} to level {}.".format(cost, ["reducer", "effect", "luck"][ind], level+1))
                # db["player_data"+id] = datas
        else:
            await interaction.response.send_message("Invalid argument.", ephemeral=True)


    @recoilball.autocomplete('upgrade')
    async def shop_autocomplete(self, interaction: discord.Interaction, current: str,) -> typing.List[app_commands.Choice[str]]:
        names = ["reducer", "effect", "luck"]
        short = ["rbred", "rbeffect", "rbluck"]
        return [
            app_commands.Choice(name=names[short.index(l)], value=l)
            for l in short if current.lower() in l.lower()
        ]
    @app_commands.command(name="stats", description="Flex on your stats with this command") # aliases=["profile", "stat"]
    @app_commands.checks.cooldown(1, 10)
    async def stats(self, interaction):
        """`yaml
        Flex on your stats with this.
        """
        player_id = interaction.user.id
        #datas = setdata(str(interaction.userr.id), str(interaction.user))
        #options = getoption(interaction.user.id)
        options = getdata(player_id, "options", "name, color")
        if options is None:
            await interaction.response.send_message("Use the `/play` command before playing !", ephemeral=True)
            return
        name, color = options
        caught, totalmoney, pbused, gbused, ubused, mbused, rbused, bbused, qbused, dbused, cbused, prbused, fbused, frazzused, rrazzused, lmencounter = getdata(player_id, "game", "caught, totalmoney, pbused, gbused, ubused, mbused, rbused, bbused, qbused, dbused, cbused, prbused, fbused, frazzused, rrazzused, lmencounter")
        embed = discord.Embed(title="{}'s stats".format(name), description="`Stats`", colour=color,
                              timestamp=datetime.utcnow())
        embed.set_footer(text="Dislate")
        embed.add_field(name="`Caught Pokémon`", value=str(caught), inline=True)
        embed.add_field(name="`Total earned money`", value=str(totalmoney), inline=True)
        used = [pbused, gbused, ubused, mbused, rbused, bbused, qbused, dbused, cbused, prbused, fbused]

        embed.add_field(name="`Thrown balls`", value="\n".join(
            ["`{}` : {}".format(listballs[i], str(used[i])) for i in range(len(listballs))]), inline=False)
        embed.add_field(name="`Used razz`",
                        value="`Fake razz` : {}\n`Rare razz` : {}".format(frazzused, rrazzused),
                        inline=True)
        embed.add_field(name="`Lucky machine activation`", value="{} encounter(s).".format(lmencounter),
                        inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="lock", description="Use this command to lock Pokémon from being released")
    @app_commands.checks.cooldown(1, 5)
    async def lock(self, interaction:discord.Interaction, locking: typing.Optional[int] = 0):
        """Use this command to lock up to 50 Pokémon from being released by `.rls d`. Legendary, Mythical, Ultrabeast, God and Egg rarities are locked by default. \nSyntax : `.lock <dexnumber>`
        """
        player_id = interaction.user.id
        language = getdata(player_id, "options", "language")
        if language is None:
            await interaction.response.send_message("Use the `/play` command before playing !", ephemeral=True)
            return
        language = language[0]
        locked = list(getdata(player_id, "locked", "*"))[1:]
        locked = [i for i in locked if i>0]
        if locking > 0:
            if locking<len(dex):
                if locking in locked:
                    locked.remove(locking)
                    locked = locked+[0]*(50-len(locked))
                    setdata(player_id, "locked", lockstr, locked)
                    await interaction.response.send_message("You unlocked {} from release.".format(dex[locking-1][language].capitalize()))
                    return
                else:
                    if len(locked) > 49:
                        await interaction.response.send_message("You already locked 50 Pokémon from release.")
                        return
                    locked.append(locking)
                    locked.sort()
                    locked = locked + [0] * (50 - len(locked))
                    setdata(player_id, "locked", lockstr, locked)
                    await interaction.response.send_message(
                        "You added {} to your locked Pokémon.".format(dex[locking-1][language].capitalize()))
                    return
            else:
                await interaction.response.send_message("Invalid Pokémon number.")
                return
        if len(locked) == 0:
            await interaction.response.send_message("You don't have any locked Pokémon !", ephemeral=True)
            return
        text = "Locked Pokémon :\n"
        for i in locked:
            if not i:
                break
            text += "`{} : {}` {}\n".format(i, rarityname[getrarity(i)], dex[i-1][language].capitalize())
        await interaction.response.send_message(text)

    @app_commands.command(name="partner", description="Set your partner Pokémon")
    @app_commands.checks.cooldown(1, 10)
    async def partner(self, interaction:discord.Interaction, new_partner: typing.Optional[int] = 0):
        """Set your partner Pokémon to get the clone ball boost and some other advantages. \nSyntax : `/partner <dexnumber>`
        """
        player_id = interaction.user.id
        language = getdata(player_id, "options", "language")
        if language is None:
            await interaction.response.send_message("Use the `/play` command before playing !", ephemeral=True)
            return
        language = language[0]
        if new_partner<0 or new_partner >len(dex):
            await interaction.response.send_message("Invalid number.", ephemeral=True)
            return
        if new_partner == 0:
            partner, = getdata(player_id, "game", "partner")
            if partner:
                await interaction.response.send_message("Your current Pokémon partner is {}.".format(dex[partner-1][language].capitalize()))
                return
            await interaction.response.send_message("You haven't set a Pokémon partner yet.", ephemeral=True)
            return
        normal = extract(player_id, "pokemon", new_partner)
        shiny = extract(player_id, "pokeshi", new_partner)

        if normal + shiny > 0:
            setdata(player_id, "game", "partner", new_partner)
            # datas[19][0] = partner
            await interaction.response.send_message("You set {} as your partner.".format(dex[new_partner - 1][language].capitalize()))
            # db["player_data"+str(ctx.message.author.id)] = datas
        else:
            await interaction.response.send_message("You don't have {} in your box !".format(dex[new_partner - 1][language].capitalize()))

    @app_commands.command(name="dream", description="Set your dreamed Pokémon")
    @app_commands.checks.cooldown(1, 10)
    async def dream(self, interaction:discord.Interaction, new_dream: typing.Optional[int] = 0):
        """Set your dreamed Pokémon here to get the dream ball boost. \nSyntax : `.dream <dexnumber>`
        """
        player_id = interaction.user.id
        language = getdata(player_id, "options", "language")
        if language is None:
            await interaction.response.send_message("Use the `/play` command before playing !", ephemeral=True)
            return
        language = language[0]
        if new_dream < 0 or new_dream > len(dex):
            await interaction.response.send_message("Invalid number.", ephemeral=True)
            return
        if new_dream == 0:
            dream, = getdata(player_id, "game", "dreamed")
            if dream:
                await interaction.response.send_message(
                    "Your current dreamed Pokémon is {}.".format(dex[dream - 1][language].capitalize()))
                return
            await interaction.response.send_message("You haven't set a dreamed Pokémon yet.", ephemeral=True)
            return

        setdata(player_id, "game", "dreamed", new_dream)
        # datas[19][0] = partner
        await interaction.response.send_message(
            "You set {} as your dreamed Pokémon.".format(dex[new_dream - 1][language].capitalize()))

    @app_commands.command(name="play", description="Start your Pokémon journey")
    @app_commands.checks.cooldown(2, 5)
    async def play(self, interaction:discord.Interaction):
        """Use this command to play the game !
        """
        player_id, name = interaction.user.id, str(interaction.user).split("#")[0]
        language = getdata(player_id, "options", "language")
        if language is None:
            createdata(player_id, name)
            embed = discord.Embed(title="Hey you !", description="Welcome to the world of Pokémon.\nI\'m the professor Oak and I study Pokémon. They live everywhere in this world and in harmony with humans. Some use them as companions while others do battles with them.\nYour name is {}, right ?\nReady to begin your adventure ?\nA brand new world is waiting you !\nUse `/play` to play.".format(
                    name), colour=0x000000,
                                  timestamp=datetime.utcnow())
            embed.set_footer(text="Dislate")

            embed.set_image(url="https://cdn.discordapp.com/attachments/754349043714621540/793349869019856906/Professeur_Chen-LGPE.png")
            await interaction.response.send_message(embed=embed)
        else:
            language, name, color = getdata(player_id, "options", "language, name, color")
            #player_data = db["player_data{}".format(id)]
            place, = getdata(player_id, "game", "place")
            embed = discord.Embed(title=places[place][0], description=name, colour=color,
                                  timestamp=datetime.utcnow())
            embed.set_footer(text="Dislate")
            embed.add_field(name="`What to do ?`", value="`/encounter` \nGame under development.", inline=False)
            embed.set_image(url=places_pic[places[place][0]])
            await interaction.response.send_message(embed=embed)


    @app_commands.command(name="give", description="Give money to other players")
    @app_commands.checks.cooldown(1, 3)
    async def give(self, interaction:discord.Interaction, to: discord.User, amount: app_commands.Range[int, 1]):
        """Use this command to give money to other players. \nSyntax : `.give <id or mention> <amount>`
        """
        player_id = interaction.user.id
        money = getdata(player_id, "game", "money")
        if money is None:
            await interaction.response.send_message("Use the `/play` command before playing !", ephemeral=True)
            return
        money = money[0]
        recid = to.id
        language = getdata(recid, "options", "language")
        if language is None:
            await interaction.response.send_message("The other player needs to use the `/play` command before receiving money !", ephemeral=True)
            return
        if player_id == recid:
            await interaction.response.send_message("Are you really trying to give yourself money ?")
            return
        #givedatas = setdata(id, str(interaction.user))
        #receivedatas = setdata(recid, None)
        if money < amount:
            amount = money
        setdata(player_id, "game", "money", None, [-amount])
        setdata(recid, "game", "money", None, [amount])
        #givedatas[9] -= amount
        #receivedatas[9] += amount - 1
        # db["player_data"+id] = givedatas
        # db["player_data"+recid] = receivedatas
        embed = discord.Embed(title="Money transaction",
                              description="||I know you clicked on this so give the owner 10 coins now.||",
                              colour=0x000000, timestamp=datetime.utcnow())
        embed.set_footer(text="Dislate")
        embed.add_field(name="Successful transaction",
                        value="{} ({}) gave {} coins to {} ({}).".format(player_id, interaction.user, amount, recid, to),
                        inline=True)
        await interaction.client.get_channel(1076902638534271016).send(embed=embed)
        await interaction.response.send_message("You gave {} coins to {}.".format(amount, to))

    @app_commands.command(name="balls", description="Show what balls can do") # aliases=["balls"]
    @app_commands.checks.cooldown(1, 10)
    async def ball(self, interaction):
        """Use this command to see what the balls do.`
        """
        player_id = interaction.user.id
        #options = getoption(id)
        color = getdata(player_id, "options", "color")
        if color is None:
            await interaction.response.send_message("Use the `/play` command before playing !", ephemeral=True)
            return
        color = color[0]
        pb, gb, ub, mb, rb, bb, qb, db, cb, prb, fb = getdata(player_id, "game", "pb, gb, ub, mb, rb, bb, qb, db, cb, prb, fb")
        #datas = setdata(id, str(interaction.user))
        embed = discord.Embed(title="Balls", description="`Balls wiki`", colour=color,
                              timestamp=datetime.utcnow())
        embed.set_footer(text="Dislate")
        embed.add_field(name="Pokéball `pb`", value="Adds 10 catch power.\nYou own {} now.".format(pb),
                        inline=True)
        embed.add_field(name="Greatball `gb`", value="Adds 15 catch power.\nYou own {} now.".format(gb),
                        inline=True)
        embed.add_field(name="Ultraball `ub`", value="Adds 35 catch power.\nYou own {} now.".format(ub),
                        inline=True)
        embed.add_field(name="Masterball `mb`",
                        value="Put the catch power to 99 no matter what except if a rare razz is activated.\nYou own {} now.".format(
                            mb), inline=True)
        embed.add_field(name="Recoilball `rb`",
                        value="Adds 100 catch power but reduces the catch power by 50 for 100 encounters. During the recoil, every 12.5 recoiled encounters left reduces the catch power by 1. You can upgrade the recoilball using `/rb` to reduce those drawbacks.\nYou own {} now.".format(
                            rb), inline=True)
        embed.add_field(name="Beastball `bb`",
                        value="Adds 20 catch power and gives 60 bonus catch power if you're catching an Ultra-beast.\nYou own {} now.".format(
                            bb), inline=True)
        embed.add_field(name="Quickball `qb`",
                        value="Adds 25 catch power and has 50% chance to let you throw a Premierball to the same Pokémon. The catch power will then be augmented of 10. You need to have at least a Premierball in your bag to do this.\nYou own {} now.".format(
                            qb), inline=True)
        embed.add_field(name="Dreamball `db`",
                        value="Adds 10 catch power and gives 150 bonus catch power if you're catching your dreamed Pokémon. To set your dreamed Pokémon do `/dream`.\nYou own {} now.".format(
                            db), inline=True)
        embed.add_field(name="Cloneball `cb`",
                        value="Adds 10 catch power and gives 150 bonus catch power if you're catching your partner Pokémon. To set your partner Pokémon do `/partner`.\nYou own {} now.".format(
                            cb), inline=True)
        embed.add_field(name="Premierball `prb`",
                        value="Adds 10 catch power. Is the only ball you can throw if the Quickball's special effect is triggered.\nYou own {} now.".format(
                            prb), inline=True)
        embed.add_field(name="Fifty-fifty ball `fb`",
                        value="Put the catch power to 50 no matter what except if a rare razz is activated.\nYou own {} now.".format(
                            fb), inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    """
    @app_commands.command(name="trivia", description="Start a trivia session") # aliases=["quiz"]
    #@app_commands.has_role("Trivia Organizer")
    @app_commands.checks.cooldown(10, 900)
    async def trivia(self, interaction):
        if ctx.message.channel.id != 834362605140705291:
            await interaction.response.send_message(interaction.client.get_channel(834362605140705291).mention)
        keys = db.prefix("player_data")
        difficulty = choices([0, 1, 2, 3, 4], weights=[700, 200, 140, 50, 1])[0]
        questionset = [trivias1, trivias2, trivias3, trivias4, trivias5][difficulty]
        question = randint(0, len(questionset) - 1)
        quiz = await interaction.client.get_channel(834362605140705291).send(
            "Difficulty : {}\n{}".format(difficulty + 1, questionset[question][0]))

        def check(m):
            return m.content.lower() in questionset[question][1:] and "player_data" + str(m.author.id) in keys

        try:
            answer = await interaction.client.wait_for("message", check=check, timeout=120)
        except asyncio.TimeoutError:
            return await interaction.send("Timeout. Correct answer was {}.".format(questionset[question][1]))

        id = answer.author.id
        datas = setdata(id, None)
        moneyprize = randint(100 * 2 ** (difficulty + 1), 500 * 2 ** (difficulty + 1))
        datas[9] += moneyprize
        datas[14] += moneyprize
        datas[24] += moneyprize
        await quiz.edit(content="Difficulty : {}\n{}\nCorrect answer was given by {}.".format(difficulty + 1,
                                                                                              questionset[question][
                                                                                                  0], datas[0]))

        await interaction.client.get_channel(834362605140705291).send("{} won {} coins as a prize.".format(datas[0], moneyprize))"""

    @trade.error
    @encounter.error
    @box.error
    @spawnrates.error
    @rename.error
    @shop.error
    @inventory.error
    @release.error
    @fakerazz.error
    @rarerazz.error
    @luckymachine.error
    @recoilball.error
    @stats.error
    @lock.error
    @partner.error
    @dream.error
    @play.error
    @give.error
    @ball.error
    async def on_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(
                f"You're under cooldown, please try again in {round(error.retry_after, 2)} seconds.", ephemeral=True)
async def setup(bot):
    await bot.add_cog(Owner(bot))
    await bot.add_cog(Main(bot))
    await bot.add_cog(Miscellaneous(bot))
    await bot.add_cog(Game(bot))