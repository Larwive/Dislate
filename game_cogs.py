import discord
from datetime import datetime
from discord import app_commands
from random import randint
from game_data import *
from game_func import *

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @app_commands.command(hidden = True)
    @app_commands.cooldown(1, 1, commands.BucketType.user)
    async def reset(self, ctx):
        if ctx.message.author.id in authors:
            data = db.prefix("player")
            for name in data:
                del db[name]
            await ctx.send("Successfully resetted all players\' data.")
        else:
            await ctx.send("This command is reserved to the *dealer*.")

    @app_commands.command(hidden = True)
    @app_commands.cooldown(1, 1, commands.BucketType.user)
    async def resoption(self, ctx):
        if ctx.message.author.id in authors:
            # Rajouter toutes les listes qui comportent les données des joueurs.
            data = db.prefix("option")
            for name in data:
                del db[name]
            await ctx.send("Successfully resetted all players\' options.")
        else:
            await ctx.send("This command is reserved to the *dealer*.")

    @app_commands.command(hidden = True)
    async def addpoke(self, ctx, id, number: typing.Optional[int] = 1, shiny: typing.Optional[bool] = False):
        if ctx.message.author.id in authors:
            try:
                id = str(ctx.message.mentions[0].id)
            except:
                id = str(id)
            number -= 1
            datas = setdata(id, None)
            datas = add_pokemon(id, number, datas, shiny)
            # db["player_data"+str(id)] = datas
            await ctx.send \
                ("You gave a{} {} to {}.".format(["", " shiny"][int(shiny)], dex[number][0].capitalize(), str(id)))



    @app_commands.command(hidden = True)
    async def se(self, ctx, giveid, dexnumber: typing.Optional[int] = 1, shiny: typing.Optional[bool] = False):
        if ctx.message.author.id in authors:
            try:
                giveid = ctx.message.mentions[0].id
            except:
                giveid = str(giveid)
            datas = setdata(giveid, None)
            datas[21] = [True, dexnumber, shiny]
            await ctx.send \
                ("You gave a {}{} special encounter to {}.".format(["", "shiny "][shiny], dex[dexnumbe r -1][0], giveid))
            # db["player_data"+giveid] = datas

    @app_commands.command(hidden = True)
    async def clearrb(self, ctx, clearid: typing.Optional[str] = "373707498479288330"):
        if ctx.message.author.id in authors:
            try:
                clearid = str(ctx.message.mentions[0].id)
            except:
                clearid = str(clearid)
            datas = setdata(clearid, None)
            datas[17] = 0
            # db["player_data"+clearid] = datas
            await ctx.send("Cleared the rb recoil.")

    @app_commands.command(hidden = True)
    async def moneymoneymoney(self, ctx, giveid: typing.Optional[str] = "373707498479288330"):
        if ctx.message.author.id in authors:
            try:
                giveid = str(ctx.message.mentions[0].id)
            except:
                giveid = str(giveid)
            datas = setdata(giveid, None)
            datas[9] += 10000
            # db["player_data"+giveid] = datas


class Main(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @app_commands.command(aliases=["dex"])
  @app_commands.cooldown(1, 10, commands.BucketType.user)
  async def d(self, ctx, *args):
    '''The dex command show the dex page of a specific Pokémon. Make sure to put the special forms name before the name of the Pokémon.\nExamples : \n`.dex bulbasaur`\n`.dex shiny bulbasaur`
    '''
    language = setlanguage(ctx.message.author.id)
    options = setoption(ctx.message.author.id)
    shiny = args[0].lower() in ["shiny", "chromatique", "schillernden", "schillerndes", "異色", "發光", "빛나는", "iro chigai", "色違い"]
    if shiny:
      argument = " ".join(args[1:]).lower()
    else:
      argument = " ".join(args).lower()
    if len(argument.split(" ")) > 1: #Cherche d'abord si le nom donné est exact
      found = -1
      if argument in ["mr. mime", "m. mime", "pantimos", "魔牆人偶", "마임맨", "barrierd", "バリヤード"]:
        found = 121
      for i in range(len(dex_forms)):
        for j in range(len(languages)):
          if argument == dex_forms[i][j].lower():
            found = i
            break
        if found != -1:
          break
      if found == -1: #Sinon cherche dans les mots-clés
        for i in range(len(forms)):
          check = 0 #Vérifie que tous les adjectifs de formes sont dans forms.
          for test in argument.split(" "):
            print(test)
            if test in forms[i]:
              check += 1
            else:
              break
          if check == len(argument.split(" ")):
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
        await ctx.send("Form not found, please check the spelling.")
        return
    else:
      try:
        if 0<int(argument)<=len(dex):
          number = int(argument)-1
        else:
          await ctx.send("Invalid dex number.")
          return
      except:
        number = -1
        for i in range(len(dex)):
          if argument in dex[i]:
            number = i
            break
        if number == -1:
          await ctx.send(["Pokémon not found. Check the spelling.", "Pokémon non trouvé. Vérifie l'orthographe.", "Pokémon nicht gefunden. Prüfe die Rechtschreibung.", "找不到神奇寶貝。 檢查拼寫。", "포켓몬을 찾을 수 없습니다. 철자를 확인하십시오.", "Pokemon ga mitsukarimasen. Superu o kakuninshitekudasai.", "ポケモンが見つかりません。 スペルを確認してください。"][language])
          return
      list_name = dex[number]
      found_types = types[number]
      stats = base_stats[number]
      if shiny:
        sprite = "http://play.pokemonshowdown.com/sprites/ani-shiny/"+dex[number][0].replace(" ","_")+".gif"
      else:
        sprite = "http://play.pokemonshowdown.com/sprites/ani/"+dex[number][0].replace(". ","")+".gif"
    embed = getdex(list_name, found_types, stats, sprite, language, options, number, ctx.message.author.id, ctx.message.author, shiny)
    await ctx.send(embed = embed)

  @app_commands.command()
  @app_commands.cooldown(1, 900, commands.BucketType.user)
  async def typechart(self, ctx):
    await ctx.send("From Bulbapedia.")
    await ctx.send("https://cdn.discordapp.com/attachments/754349043714621540/792404761563496448/Capture_decran_2020-12-26_a_15.53.16.png")

    class Miscellaneous(commands.Cog):
        def __init__(self, bot):
            self.bot = bot

        @app_commands.command()
        @app_commands.cooldown(1, 10, commands.BucketType.user)
        async def option(self, ctx, *args):
            '''The option command show the togglables options and the current options' state for you. To toggle an option make sure it is listed in the `.option` command and do `.option *OptionToToggle*`. You can toggle/change multiple options at a time by sparating them with a space.\nExamples : \n`.option`\n`.option v.o.l.`\n`.option color 0x123456`
            '''
            options = setoption(ctx.message.author.id)
            if len(args) == 0:
                embed = discord.Embed(title="Options",
                                      description="Use `.option *argument*` to toggle or change options. You can toggle multiple options at a time.",
                                      colour=options[2], timestamp=datetime.utcnow())
                embed.set_footer(text="SHAdOw")
                embed.add_field(name="`v.o.l.`",
                                value="Let the `.dex` command show the Pokémon names in other languages. Now " +
                                      ["**off**", "**on**"][int(options[0])] + ".", inline=True)
                embed.add_field(name="`reset`", value="Put your options to their default values.", inline=True)
                embed.add_field(name="`color`",
                                value="Put the hexadecimal value of the color you want the embeds' line to be.",
                                inline=True)
                embed.add_field(name="`language`",
                                value="Put the language code you want the game and some commands to be. Available languages : `en`, `fr`, `ge`, `ch`, `ko`, `jr`, `ja`\nCurrently set language : " +
                                      ["`English`", "`Français`", "`Deutsche`", "`中文`", "`한국어`", "`Hifumi`",
                                       "`日文`"][options[3]], inline=True)
                embed.add_field(name="`link`", value="Add a link to an external Dex page with the dex command. Now " +
                                                     ["**off**", "**on**"][int(options[5])] + ".", inline=True)
                embed.add_field(name="`gamestats`",
                                value="Add your stats to the dex page. Now " + ["**off**", "**on**"][
                                    int(options[6])] + ".", inline=True)
                embed.add_field(name="`Privacy`",
                                value="Enable privacy to not let other people see your box. Now {}.".format(
                                    ["**off**", "**on**"][int(options[6])]))
                embed.add_field(name="Examples",
                                value="`.option v.o.l.`, `.option prefix ;`, `.option reset`, `.option color FFFBCA`",
                                inline=True)
                await ctx.send(embed=embed)
                return
            if "v.o.l." in args:  # view other languages
                options[0] = not (options[0])
            if "color" in args and args.index("color") < len(args):
                try:
                    color = int(args[args.index("color") + 1], 16)
                    options[2] = color
                except:
                    await ctx.send("Invalid color value.")
                    return
            if "lang" in args and args.index("lang") < len(args):
                lang = args[args.index("lang") + 1]
                if lang in languages:
                    options[3] = languages.index(lang)
                else:
                    await ctx.send("Incorrect language. It needs to be among `" + "`, `".join(languages) + "`.")
            if "link" in args:  # view link
                options[5] = not (options[5])
            if "gamestats" in args:  # view game stats
                options[6] = not (options[6])
            if "raritycolor" in args:  # view game stats
                options[7] = not (options[7])
            if "reset" in args:
                options = defaultoption
            if "privacy" in args:
                options[4] = not (options[4])
            db["option" + str(ctx.message.author.id)] = options
            embed = discord.Embed(title="Options", description="Your current options", colour=options[2],
                                  timestamp=datetime.utcnow())
            embed.set_footer(text="SHAdOw")
            embed.add_field(name="`v.o.l.`", value=["`Off`", "`On`"][int(options[0])], inline=True)
            embed.add_field(name="`Prefix`", value="`.`", inline=True)
            embed.add_field(name="`Language`",
                            value=["`English`", "`Français`", "`Deutsche`", "`中文`", "`한국어`", "`Hifumi`", "`日文`"][
                                options[3]], inline=True)
            embed.add_field(name="`Link`", value=["`Off`", "`On`"][int(options[5])], inline=True)
            embed.add_field(name="`Privacy`", value=["`Off`", "`On`"][int(options[4])], inline=True)
            await ctx.send(embed=embed)

        @app_commands.command()
        @app_commands.cooldown(1, 1, commands.BucketType.user)
        async def randomen(self, ctx):
            await ctx.send(
                "This brings you to a random page of Bulbapedia : https://bulbapedia.bulbagarden.net/wiki/Special:Random")

        @app_commands.command()
        @app_commands.cooldown(1, 1, commands.BucketType.user)
        async def randomfr(self, ctx):
            await ctx.send(
                "This brings you to a random page of Poképédia : https://www.pokepedia.fr/Sp%C3%A9cial:Page_au_hasard")

        @app_commands.command()
        @app_commands.cooldown(1, 900, commands.BucketType.user)
        async def message(self, ctx, *message: typing.Optional[str]):
            '''Use this command to send a message to the owner of the bot. Don't be shy !
            '''
            options = setoption(ctx.message.author.id)
            try:
                embed = discord.Embed(title="Message by user",
                                      description="`Author :`" + str(ctx.message.author) + " / " + str(
                                          ctx.message.author.id), colour=options[2], timestamp=datetime.utcnow())
                embed.add_field(name="`Message :`", value=" ".join(message), inline=False)
                embed.set_footer(text="SHAdOw")
                await bot.get_channel(794211311214788608).send(embed=embed)
                await ctx.send("Message sent.")
            except:
                await ctx.send("Your message must be 1024 or fewer in length.")

        @app_commands.command()
        @app_commands.cooldown(1, 20, commands.BucketType.user)
        async def lang(self, ctx):
            '''Use this command to change the language of some parts of the bot. English : `en`\nFrench : `fr`\nGerman : `ge`\nChinese : `ch`\nKorean : `ko`\nJapanese (romaji) : `jr`\nJapanese : `ja`
            '''
            await ctx.send(
                "English : `en`\nFrench : `fr`\nGerman : `ge`\nChinese : `ch`\nKorean : `ko`\nJapanese (romaji) : `jr`\nJapanese : `ja`")

            def check(m):
                return m.author.id == ctx.message.author.id and m.content.lower() in languages

            options = setoption(ctx.message.author.id)
            try:
                language = await bot.wait_for("message", check=check, timeout=30)
                options[3] = languages.index(language.content.lower())
                db["option" + str(ctx.message.author.id)] = options
                await ctx.send("Changed language to " + language.content.lower() + ".")
            except:
                await ctx.send("Timeout. Please retry.")

        @app_commands.command()
        @app_commands.cooldown(1, 2, commands.BucketType.user)
        async def calc(self, ctx, expression):
            try:
                if eval(expression) % 1 == 0:
                    await ctx.send(int(eval(expression)))
                else:
                    await ctx.send(eval(expression))
            except:
                await ctx.send("Invalid syntax. Ask around or visit https://www.python.org/ to get helped.")

        @app_commands.command(hidden=True)
        async def test(self, ctx):
            await ctx.send("!f")

    class Game(commands.Cog):
        '''Those are the game's commands.
        '''

        def __init__(self, bot):
            self.bot = bot

        @app_commands.command(aliases=["tr"])
        @app_commands.cooldown(1, 10, commands.BucketType.user)
        async def trade(self, ctx, idt, *args):
            '''Use this command to trade with other players. Syntax : `.trade <id or mention> <"shiny" (optional)> <Dexnumber1> <"shiny" (optional)> <Dexnumber2>`
            '''
            try:
                idt = str(ctx.message.mentions[0].id)
            except:
                idt = str(idt)
            id = str(ctx.message.author.id)
            tradero = setdata(id, None)
            tradert = setdata(idt, None)
            shiny1 = args[0].lower() in ["shiny", "chromatique", "schillernden", "schillerndes", "異色", "發光", "빛나는",
                                         "iro chigai", "色違い"]
            print(1)
            if shiny1:
                shiny2 = args[2].lower() in ["shiny", "chromatique", "schillernden", "schillerndes", "異色", "發光",
                                             "빛나는", "iro chigai", "色違い"]
                poke1 = int(args[1])
                if shiny2:
                    poke2 = int(args[3])
                else:
                    poke2 = int(args[2])
            else:
                shiny2 = args[1].lower() in ["shiny", "chromatique", "schillernden", "schillerndes", "異色", "發光",
                                             "빛나는", "iro chigai", "色違い"]
                poke1 = int(args[0])
                if shiny2:
                    poke2 = int(args[2])
                else:
                    poke2 = int(args[1])
                    print(2)
            if tradero[7][poke1 - 1][int(shiny1)] < 1:
                await ctx.send("You don't have the Pokémon you're proposing.")
                return
            if tradert[7][poke2 - 1][int(shiny2)] < 1:
                await ctx.send("The other player doesn't have the Pokémon you want.")
                return

            def check1(m):
                return str(m.author.id) == id and m.channel == ctx.message.channel and m.content.lower() == "confirm"

            def check2(m):
                return str(m.author.id) == idt and m.channel == ctx.message.channel and m.content.lower() == "confirm"

            try:
                await ctx.send(
                    "<@{}> Type **`confirm`** to confirm this trade :\n Your **{}{}** for his/her **{}{}**.".format(id,
                                                                                                                    ["",
                                                                                                                     "shiny "][
                                                                                                                        int(shiny1)],
                                                                                                                    dex[
                                                                                                                        poke1 - 1][
                                                                                                                        0],
                                                                                                                    ["",
                                                                                                                     "shiny "][
                                                                                                                        int(shiny2)],
                                                                                                                    dex[
                                                                                                                        poke2 - 1][
                                                                                                                        0]))
                await bot.wait_for("message", check=check1, timeout=20.0)
            except asyncio.TimeoutError:
                return await ctx.send("Timeout. Trade canceled.")
            try:
                await ctx.send(
                    "<@{}> Type **`confirm`** to confirm this trade :\n Your **{}{}** for his/her **{}{}**.".format(idt,
                                                                                                                    ["",
                                                                                                                     "shiny "][
                                                                                                                        int(shiny2)],
                                                                                                                    dex[
                                                                                                                        poke2 - 1][
                                                                                                                        0],
                                                                                                                    ["",
                                                                                                                     "shiny "][
                                                                                                                        int(shiny1)],
                                                                                                                    dex[
                                                                                                                        poke1 - 1][
                                                                                                                        0]))
                await bot.wait_for("message", check=check2, timeout=20.0)
            except asyncio.TimeoutError:
                return await ctx.send("Timeout. Trade canceled.")
            tradero[7][poke1 - 1][int(shiny1)] -= 1
            tradert[7][poke2 - 1][int(shiny2)] -= 1
            tradero[7][poke2 - 1][int(shiny2)] += 1
            tradert[7][poke1 - 1][int(shiny1)] += 1
            embed = discord.Embed(title="Trade",
                                  description="||I know you clicked on this so give the owner 10 coins now.||",
                                  colour=0x000000, timestamp=datetime.utcnow())
            embed.set_footer(text="SHAdOw")
            embed.add_field(name="Successful trade",
                            value="{}'s **{}{}** :left_right_arrow: {}'s **{}{}**".format(tradero[0],
                                                                                          ["", "shiny "][int(shiny1)],
                                                                                          dex[poke1 - 1][0], tradert[0],
                                                                                          ["", "shiny "][int(shiny2)],
                                                                                          dex[poke2 - 1][0]),
                            inline=True)
            print(2)
            await bot.get_channel(842381061056233553).send(embed=embed)
            await ctx.send("You traded succesfully.")

        @app_commands.command()
        @app_commands.cooldown(1, 2, commands.BucketType.user)
        async def e(self, ctx, spawnnumber: typing.Optional[int] = -1, shiny: typing.Optional[int] = 0):
            '''Use this command to catch some Pokémon.
            '''
            se = ""
            id = ctx.message.author.id
            datas = setdata(id, ctx.message.author)
            options = setoption(id)
            color, language = options[2], options[3]
            try:
                specialencounter = datas[21]
            except:
                await ctx.send("Do `.play` before playing !")
            fakee, raree, luckye = False, False, False
            spawnweight = [1511000000, 750000000, 150000000, 50000000, 7000000, 5000000, 1890000, 20000, 10000, 1]

            def is_correct(m):
                return m.author.id == id and m.content.lower() in listballs and datas[10][
                    listballs.index(m.content.lower())] > 0

            if datas[22][0] > 0:
                for i in range(6, len(spawnweight)):
                    spawnweight[i] = int(spawnweight[i] / 2)
                datas[22][0] -= 1
                fakee = True
            if datas[22][1] > 0:
                for i in range(6, len(spawnweight)):
                    spawnweight[i] *= 2
                datas[22][1] -= 1
                raree = True
            if datas[22][2] > 0 and datas[9] > 2500:
                for i in range(6, len(spawnweight)):
                    spawnweight[i] *= 2
                datas[22][2] -= 1
                datas[23][13] += 1
                datas[9] -= 2500
                # luckye = True
            if ctx.message.author.id in authors and spawnnumber > 0:
                shiny = bool(shiny)
                spawnnumber = spawnnumber - 1
                rarity = getrarity(spawnnumber + 1)
            elif specialencounter[0]:
                spawnnumber = specialencounter[1] - 1
                shiny = specialencounter[2]
                rarity = getrarity(spawnnumber + 1)
                datas[21] = [False, 0, 0]
                se = " **Special encounter**"
            else:
                shiny = choices([True, False], weights=[1, 8192])[0]
                rarity = choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], weights=spawnweight)[0]
                spawnnumber = choices(
                    [commonpool, uncommonpool, rarepool, rarerpool, veryrarepool, pseudolegendarypool, legendarypool,
                     mythicalpool, ultrabeastpool, god][rarity])[0] - 1

            Rarity = rarityname[rarity]
            spawn = dex[spawnnumber]
            if options[7]:
                color = [0x77AA, 0x3388, 0x335566, 0x552222, 0x771111, 0x442255, 0x837465, 0x33FF33, 0x123456, 0xFFFFFF,
                         0x222211][rarity]

            name = datas[0]
            pokemon = spawn[language].capitalize()
            embedtitle = pokemon + " #" + str(spawnnumber + 1)
            if shiny:
                embedtitle = ":star2: " + embedtitle
                color = 0xFFFFFF - color

            embed = discord.Embed(title=embedtitle, description=name, colour=color, timestamp=datetime.utcnow())
            embed.set_footer(text="SHAdOw")
            if rarity > 5 or shiny:
                rarespawns = discord.Embed(title="A " + embedtitle + " spawned !" + se, description=Rarity,
                                           colour=color, timestamp=datetime.utcnow())
                rarespawns.set_footer(text="SHAdOw")
                if shiny:
                    rarespawns.set_image(
                        url="http://play.pokemonshowdown.com/sprites/ani-shiny/" + spawn[0].replace(" ", "_") + ".gif")
                else:
                    rarespawns.set_image(
                        url="http://play.pokemonshowdown.com/sprites/ani/" + spawn[0].replace(". ", "") + ".gif")
                await bot.get_channel(831389415858896896).send(embed=rarespawns)

            if shiny:
                text = "Rarity : 1/8192\nCaught : " + str(datas[7][spawnnumber][1])
            else:
                text = "Rarity : " + Rarity + "\nInbox : " + str(datas[7][spawnnumber][0])
            if datas[10][0] > 0:
                text += "\n`pb` Pokéball : " + str(datas[10][0])
            if datas[10][1] > 0:
                text += "\n`gb` Greatball : " + str(datas[10][1])
            if datas[10][2] > 0:
                text += "\n`ub` Ultraball : " + str(datas[10][2])
            if datas[10][3] > 0:
                text += "\n`mb` Masterball : " + str(datas[10][3])
            if datas[10][4] > 0:
                text += "\n`rb` Recoilball : " + str(datas[10][4])
            if datas[17] > 0:
                text += "\nRecoil left : " + str(datas[17])
            if datas[10][5] > 0:
                text += "\n`bb` Beastball : " + str(datas[10][5])
            if datas[10][6] > 0:
                text += "\n`qb` Quickball : " + str(datas[10][6])
            if datas[10][7] > 0:
                text += "\n`db` Dreamball : " + str(datas[10][7])
            if datas[10][8] > 0:
                text += "\n`cb` Cloneball : " + str(datas[10][8])
            if datas[10][9] > 0:
                text += "\n`prb` Premier ball : " + str(datas[10][9])

            embed.add_field(name="`What to do ?`", value=text, inline=False)
            if shiny:
                embed.set_image(
                    url="http://play.pokemonshowdown.com/sprites/ani-shiny/" + spawn[0].replace(" ", "_") + ".gif")
            else:
                embed.set_image(
                    url="http://play.pokemonshowdown.com/sprites/ani/" + spawn[0].replace(". ", "") + ".gif")
            encounter = await ctx.send(embed=embed)

            try:
                sentball = await bot.wait_for("message", check=is_correct, timeout=20.0)
            except asyncio.TimeoutError:
                return await encounter.edit(content="{} fled !".format(pokemon))
            sentball = sentball.content.lower()
            randomcatch = randint(0, 100)
            if sentball == "mb":
                iscaught = 99
            elif sentball == "fb":
                iscaught == 50
            else:
                iscaught = catchrate[rarity] + ballcr[listballs.index(sentball)] - 80 * int(shiny) - 50 * (
                            datas[17] > 0) - int(2 * datas[17] / (25 * datas[18][1])) + 40 * int(
                    rarity == 8 and sentball == "bb") + 150 * int(
                    datas[19][1] == spawnnumber and sentball == "db") + 150 * int(
                    datas[19][0] == spawnnumber and sentball == "cb") - 40 * (int(spawnnumber > 721))
            if fakee:
                iscaught += 20
            if raree:
                iscaught -= 20
            datas[17] = max(datas[17] - 1, 0)
            if sentball == "rb":
                datas[17] += 100 - datas[18][0]
            datas[10][listballs.index(sentball)] -= 1 + int(fakee) + int(raree)
            datas[23][listballs.index(sentball)] += 1
            embed = discord.Embed(title=embedtitle, description=name, colour=color, timestamp=datetime.utcnow())
            embed.set_footer(text="SHAdOw")
            if shiny:
                embed.set_image(
                    url="http://play.pokemonshowdown.com/sprites/ani-shiny/" + spawn[0].replace(" ", "_") + ".gif")
            else:
                embed.set_image(
                    url="http://play.pokemonshowdown.com/sprites/ani/" + spawn[0].replace(". ", "") + ".gif")
            state = 0
            if randomcatch > iscaught and sentball == "qb":
                retry = choices([False, True], weights=[1, 1])[0]
                if retry and datas[10][9] < 1:
                    state = 1  # Chanceux mais pas d'honor ball.
                elif retry and datas[10][9] > 0:
                    datas[10][9] -= 1
                    iscaught += 10
                    randomcatch = randint(0, 100)
                    state = 2  # Chanceux avec honor ball

            if randomcatch <= iscaught:
                gotmoney = randint([99, 120, 300, 600, 1300, 500, 10000, 20000, 10000, 200000][rarity],
                                   [120, 200, 400, 800, 1800, 750, 15000, 25000, 100000, 2000000][rarity])
                coinbonus = int(gotmoney * datas[10][10] * 0.05)
                datas[14] += gotmoney
                datas[9] += gotmoney
                datas = add_pokemon(id, spawnnumber, datas, shiny, True)
                text = "You caught {} !\nRarity : {} \nCatch power : {} | Catch number : {}\nYou earned {} coins.".format(
                    pokemon, Rarity, iscaught, randomcatch, gotmoney)
                if coinbonus > 0:
                    text += "You got {} bonus coins.".format(coinbonus)
                if datas[17] > 0:
                    luck = randint(1, 100 + datas[18][2])
                    if luck > 95:
                        reduction = randint(1, 5)
                        datas[17] = max(0, datas[17] - reduction)
                        text += "\nLucky ! Your recoil got reduced by " + str(reduction) + "."
                        if state > 0:
                            text += "You got lucky and an Premier ball was thrown."

                    # await message.channel.send("You caught {} !\nCatch power : {}  Catch number : {}\nYou earned {} coins.".format(pokemon, iscaught, randomcatch, gotmoney))
            else:
                text = "{} broke free !\nRarity : {} \nCatch power : {} | Catch number : {}".format(pokemon, Rarity,
                                                                                                    iscaught,
                                                                                                    randomcatch)
            if state > 0:
                if state == 1:
                    text += "You got lucky but you didn't have Premier ball."
                elif state == 2:
                    text += "You got lucky but the Pokémon still fled."

            embed.add_field(name="`Result`", value=text)
            await encounter.edit(embed=embed)
            # db["player_data"+str(id)] = datas

        @app_commands.command(aliases=["pc"])
        @app_commands.cooldown(1, 5, commands.BucketType.user)
        async def box(self, ctx, page: typing.Optional[int] = 1, sort: typing.Optional[int] = 1,
                      id: typing.Optional[int] = -1):
            '''The box command show your owned Pokémon. The default box page is the first one with the national dex number order. You can choose to see a certain page or with a certain sorting order. You must give the page number if you specify the sorting order.\nSyntax : `.box <page> <sorting order number>`\nSorting order : \n`1 (Default)` : The national dex number order.\n`2` : The descending rarity order.\n`3` : The ascending rarity order.\n`4` : The descending order with shinies first.\nExamples : \n`.box`\n`.box 1 1`\n`.box 2 4`
            '''
            # sort = 1:Ordre pokédex, 2:Ordre rareté descendant, 3:Ordre rareté ascendant, 4:Ordre rareté descendant avec shinys en premiers
            print(1)
            if id != -1:
                try:
                    id = str(ctx.message.mentions[0].id)
                except:
                    id = str(id)
            else:
                id = ctx.message.author.id
            print(2)
            datas = setdata(id, None)
            options = setoption(id)
            sortedbox, text, total, color, language = 0, "", 0, options[2], options[3]
            print(3)
            if int(ctx.message.author.id) != id and options[4]:
                await ctx.send("You can't see his/her box.")
                return
            if sort > 4:
                sort = 4
            for i in range(len(dex)):
                scanning = datas[7][i]
                if scanning[0] > 0 or scanning[1] > 0:
                    total += 1
            total = int((total - 1) / 20) + 1
            try:
                if sort == 1:
                    for i in range(len(dex)):
                        if sortedbox >= 20 * page:
                            break
                        scanning = datas[7][i]  # [0]
                        print(scanning)
                        if scanning[0] > 0 or scanning[1] > 0:
                            rarity = rarityname[getrarity(i + 1)]
                            sortedbox += 1
                            if sortedbox > 20 * (page - 1):
                                text += "`" + str(i + 1) + "` `" + rarity + "` " + str(scanning[0]) + " | " + str(
                                    scanning[1]) + "  " + dex[i][language].capitalize() + "\n"
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
                                text += "`" + str(i + 1) + "` `" + rarity + "` " + str(scanning[0]) + " | " + str(
                                    scanning[1]) + "  " + dex[i][language].capitalize() + "\n"
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
                                text += "`" + str(i + 1) + "` `" + rarity + "` " + str(scanning[0]) + " | " + str(
                                    scanning[1]) + "  " + dex[i][language].capitalize() + "\n"
                    for i in generalpool:
                        i -= 1
                        if sortedbox >= 20 * page:
                            break
                        scanning = datas[7][i]
                        if scanning[0] > 0 and i not in alreadyadded:
                            rarity = rarityname[getrarity(i + 1)]
                            sortedbox += 1
                            if sortedbox > 20 * (page - 1):
                                text += "`" + str(i + 1) + "` `" + rarity + "` " + str(scanning[0]) + " | " + str(
                                    scanning[1]) + "  " + dex[i][language].capitalize() + "\n"
            except:
                text = "Invalid page number."
            embed = discord.Embed(title=datas[0] + "'s box", colour=color, timestamp=datetime.utcnow())
            embed.set_footer(text="SHAdOw")
            embed.add_field(name="Page " + str(page) + "/" + str(total), value=text, inline=True)
            await ctx.send(embed=embed)

        @app_commands.command()
        async def sr(self, ctx):
            '''Use this command to see your spawn rates.
            '''
            spawnweight = [1511000000, 750000000, 150000000, 50000000, 7000000, 5000000, 1890000, 20000, 10000, 1]
            datas = setdata(ctx.message.author.id, str(ctx.message.author))
            if datas[22][0] > 0:
                for i in range(6, len(spawnweight)):
                    spawnweight[i] = int(spawnweight[i] / 2)
            if datas[22][1] > 0:
                for i in range(6, len(spawnweight)):
                    spawnweight[i] *= 2
            if datas[22][2] > 0 and datas[9] > 2500:
                for i in range(6, len(spawnweight)):
                    spawnweight[i] *= 2
            somme = sum(spawnweight)
            await ctx.send(
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

        @app_commands.command(aliases=["nickname"])
        @app_commands.cooldown(1, 900, commands.BucketType.user)
        async def rename(self, ctx, name: typing.Optional[str]):
            '''This command to rename yourself in the game.\nsSyntax : `.rename <newname>`
            '''
            datas = setdata(ctx.message.author.id, str(ctx.message.author))
            datas[0] = name
            # db["player_data"+str(ctx.message.author.id)] = datas
            await ctx.send("You successfully renamed yourself into " + name + ".")

        @app_commands.command()
        @app_commands.cooldown(1, 900, commands.BucketType.user)
        async def quit(self, ctx):
            '''Use this command to erase all your game datas.
            '''
            keys = db.prefix("player_data")
            if "player_data" + str(ctx.message.author.id) in keys:
                await ctx.send(
                    "You have 10 seconds to type `yes` if you really want to erase your datas. You won't be able to retrieve them.")

                def check(m):
                    return m.author.id == ctx.message.author.id and m.content.lower() == "yes"

                await bot.wait_for("message", check=check, timeout=10)
                del db["player_data" + str(ctx.message.author.id)]
                await ctx.send("Your data was successfully deleted.")
            else:
                await ctx.send("You haven\'t started your adventure yet.")

        @app_commands.command(aliases=["sh", "shop"])
        @app_commands.cooldown(1, 10, commands.BucketType.user)
        async def s(self, ctx, buying: typing.Optional[int] = -1, amount: typing.Optional[int] = 1):
            '''Use this command to see the shop and buy things in it.\nSyntax : `.s <itemnumber> <amount>`
            '''
            id = ctx.message.author.id
            if buying > -1:
                if buying == 10:
                    await ctx.send("You can't buy Premier ball !")
                    return
                bought, moneyleft, amuletnumber = additems(buying, amount, id, str(ctx.message.author))
                if amuletnumber > 50 and buying == 11:
                    await ctx.send("You already have 50 amulet coins !")
                    return
                if bought:
                    await ctx.send("You bought " + str(amount) + " " + buyableitems[buying - 1][1] + " and have " + str(
                        moneyleft) + " :coin: left.")
                    return
            options = setoption(id)
            datas = setdata(id, str(ctx.message.author))
            embed = discord.Embed(title="Shop",
                                  description="`Buy what you need !` You have " + str(datas[9]) + " :coin:.",
                                  colour=options[2], timestamp=datetime.utcnow())
            embed.set_footer(text="SHAdOw")
            embed.add_field(name="`Items`", value="\n".join([" | ".join(
                ["`" + str(buyableitems[i][0]) + " : " + buyableitems[i][1] + "`",
                 "Cost : " + str(buyableitems[i][2]) + " :coin:", "`Earned : " + str(datas[10][i])]) + "`" for i in
                                                             range(len(buyableitems))]), inline=True)
            await ctx.send(embed=embed)

        @app_commands.command(aliases=["item", "items", "bag", "inventory"])
        @app_commands.cooldown(1, 10, commands.BucketType.user)
        async def i(self, ctx):
            '''Use this command see what you got in your bag.
            '''
            id = ctx.message.author.id
            datas = setdata(id, str(ctx.message.author))
            options = setoption(id)
            embed = discord.Embed(title="Bag", description=str(datas[9]) + " :coin:", colour=options[2],
                                  timestamp=datetime.utcnow())
            embed.set_footer(text="SHAdOw")
            embed.add_field(name="`Balls`", value="\n".join(
                [" : ".join(["`" + str(buyableitems[i][1]) + "`", str(datas[10][i])]) for i in
                 range(len(buyableitems))]), inline=True)
            await ctx.send(embed=embed)

        @app_commands.command(aliases=["release"])
        @app_commands.cooldown(1, 7, commands.BucketType.user)
        async def rls(self, ctx, releasing: typing.Optional[str] = "-1", amount: typing.Optional[int] = 1,
                      shiny: typing.Optional[bool] = False):
            '''Use this command to release your Pokémon.\nSyntax : `.rls d` to release all your duplicates except Legendary, Mythical, Ultrabest and God ones.\n`.rls <dexnumber> <amount>
            '''
            id = str(ctx.message.author.id)
            datas = setdata(id, str(ctx.message.author))
            locked = datas[20]
            try:
                releasing = int(releasing)
            except:
                pass
            if releasing == "d":
                dupes = [0, 0, 0, 0, 0, 0]
                gotmoney = 0
                for i in range(len(datas[7])):
                    if i in locked:
                        continue
                    release = datas[7][i]
                    if release[0] > 0:
                        rarity = getrarity(i + 1)
                        if rarity > 5:
                            continue
                        dupes[rarity] += release[0] - 1
                        gotmoney += (release[0] - 1) * releasemoney[rarity]
                        release[0] = 1
                datas[9] += gotmoney
                datas[14] += gotmoney
                # db["player_data"+id] = datas
                await ctx.send(
                    "You got {} coins by releasing\n{} common\n{} uncommon\n{} rare\n{} rarer\n{} very rare\n{} pseudo legendary".format(
                        gotmoney, dupes[0], dupes[1], dupes[2], dupes[3], dupes[4], dupes[5]))
                return
            if releasing > 0:
                if datas[7][releasing - 1][int(shiny)] - amount < 0:
                    await ctx.send("You can't release something you don't own.")
                    return
                language = setlanguage(id)
                datas[7][releasing - 1][int(shiny)] -= amount
                rarity = getrarity(releasing)
                gotmoney = amount * releasemoney[rarity] * 1000 ** int(shiny)
                datas[9] += gotmoney
                datas[14] += gotmoney
                # db["player_data"+id] = datas
                released = dex[releasing - 1][language].capitalize()
                if shiny:
                    released = "shiny " + released
                await ctx.send("You released {} {} and got {} coins.".format(amount, released, gotmoney))

        @app_commands.command()
        @app_commands.cooldown(1, 15, commands.BucketType.user)
        async def fr(self, ctx, amount: typing.Optional[int] = 0):
            '''Use this command to activate the fake razz's effect. Fake razz divides by 2 the Legendary, Mythical, Ultrabeast and God spawn rates but gives you a 20 catch power bonus for 50 encounters each.\nSyntax : `.fr <amount>`
            '''
            id = ctx.message.author.id
            datas = setdata(id, str(ctx.message.author))
            fakeamount = datas[10][11]
            if amount < 1:
                if datas[22][0] < 1:
                    await ctx.send(
                        "You don't have any fake razz effect activated. Activate or buy some in the shop ! You currently have {} fake razz.".format(
                            fakeamount))
                else:
                    await ctx.send(
                        "The fake razz is activated for {} more encounter. You have {} fake razz now.".format(
                            datas[22][0], fakeamount))
                    return
            elif amount > fakeamount:
                await ctx.send("You don't have that many fake razz. You only have {} now.".format(fakeamount))
                return
            else:
                datas[10][11] -= amount
                datas[23][11] += amount
                datas[22][0] += amount * 50
                await ctx.send("Fake razz is now activated for {} more encounters.".format(datas[22][0]))
                # db["player_data"+str(id)] = datas

        @app_commands.command(aliases=["rarerazz"])
        @app_commands.cooldown(1, 15, commands.BucketType.user)
        async def rr(self, ctx, amount: typing.Optional[int] = 0):
            '''Use this command to activate the rare razz's effect. Rare razz doubles Legendary, Mythical, Ultrabeast and God spawn rates but gives you a -20 catch power malus for 50 encounters each.\nSyntax : `.rr <amount>`
            '''
            id = ctx.message.author.id
            datas = setdata(id, str(ctx.message.author))
            rareamount = datas[10][12]
            if amount < 1:
                if datas[22][1] < 1:
                    await ctx.send(
                        "You don't have any rare razz effect activated. Activate or buy some in the shop ! You currently have {} rare razz.".format(
                            rareamount))
                else:
                    await ctx.send(
                        "The rare razz is activated for {} more encounter. You have {} rare razz now.".format(
                            datas[22][1], rareamount))
                    return
            elif amount > rareamount:
                await ctx.send("You don't have that many rare razz. You only have {} now.".format(rareamount))
                return
            else:
                datas[10][12] -= amount
                datas[23][12] += 1
                datas[22][1] += amount * 50
                await ctx.send("Rare razz is now activated for {} more encounters.".format(datas[22][1]))
                # db["player_data"+str(id)] = datas

        @app_commands.command(aliases=["luckymachine"])
        @app_commands.cooldown(1, 15, commands.BucketType.user)
        async def lm(self, ctx, amount: typing.Optional[int] = 0):
            '''Use this command to activate the lucky machine for a certain amount of encounters. It doubles the Legendary, Mythical, Ultrabeast and God spawn rates but costs 2500 coins each encounter.\nSyntax : `.lm <amount>`
            '''
            id = str(ctx.message.author.id)
            datas = setdata(id, str(ctx.message.author))
            if amount < 1:
                if datas[22][2] < 1:
                    await ctx.send(
                        "The lucky machine isn't activated. Activate it by specifying the number of encounter.")
                else:
                    await ctx.send("The lucky machine is activated for {} more encounter.".format(datas[22][2]))
            else:
                datas[22][2] += amount
                await ctx.send("The lucky machine is now activated for {} more encounters.".format(datas[22][2]))
                # db["player_data"+id] = datas

        @app_commands.command(aliases=["recoilball"])
        @app_commands.cooldown(1, 10, commands.BucketType.user)
        async def rb(self, ctx, upgrading: typing.Optional[str] = ""):
            '''Upgrade your recoilball here.\nReducer : Reduces the number of recoiled encounters a recoilball will give.\nEffect : Reduces the reduction of catch power due to recoil.\nLuck : Give you a higher chance of reducing your accumulated recoil when catching a Pokémon.\nSyntax : `.rb <reducer/effect/luck>`
            '''
            id = str(ctx.message.author.id)
            datas = setdata(id, str(ctx.message.author))
            if upgrading.lower() in ["reducer", "effect", "luck"]:
                upgrade = ["reducer", "effect", "luck"].index(upgrading.lower())
                cost = 100 * 20 ** datas[18][upgrade]
                if datas[9] < cost:
                    await ctx.send("You need " + str(cost - datas[9]) + " more coins to upgrade the " +
                                   ["reducer.", "effect.", "luck."][upgrade])
                else:
                    datas[9] -= cost
                    datas[18][upgrade] += 1
                    await ctx.send("You spent {} to upgrade the recoilball's {} to level {}.".format(cost, ["reducer",
                                                                                                            "effect",
                                                                                                            "luck"][
                        upgrade], datas[18][upgrade]))
                    # db["player_data"+id] = datas
                    return
            options = setoption(id)
            embed = discord.Embed(title="Recoilball", description="Upgrades", colour=options[2],
                                  timestamp=datetime.utcnow())
            embed.set_footer(text="SHAdOw")
            reducertext = "Reduces the number of recoiled encounters a recoilball will give. Current level : " + str(
                datas[18][0])
            if datas[18][0] < 20:
                reducertext += "\nNext cost : " + str(100 * 20 ** datas[18][0])
            effecttext = "Reduces the reduction of catch power due to recoil. Current level : " + str(datas[18][1])
            if datas[18][1] < 20:
                effecttext += "\nNext cost : " + str(100 * 20 ** datas[18][1])
            lucktext = "Give you a higher chance of reducing your accumulated recoil. Current level : " + str(
                datas[18][2])
            if datas[18][2] < 20:
                lucktext += "\nNext cost : " + str(100 * 20 ** datas[18][2])
            embed.add_field(name="`Reducer`", value=reducertext, inline=True)
            embed.add_field(name="`Effect`", value=effecttext, inline=True)
            embed.add_field(name="`Luck`", value=lucktext, inline=True)
            await ctx.send(embed=embed)

        @app_commands.command(aliases=["profile", "stat"])
        @app_commands.cooldown(1, 10, commands.BucketType.user)
        async def stats(self, ctx):
            '''`yaml
            Flex on your stats with this.
            '''
            print(ctx.message.author)
            datas = setdata(str(ctx.message.author.id), str(ctx.message.author))
            options = setoption(ctx.message.author.id)
            embed = discord.Embed(title=datas[0] + "'s stats", description="`Stats`", colour=options[2],
                                  timestamp=datetime.utcnow())
            embed.set_footer(text="SHAdOw")
            embed.add_field(name="`Caught Pokémon`", value=str(datas[12]), inline=True)
            embed.add_field(name="`Total earned money`", value=str(datas[14]), inline=True)
            embed.add_field(name="`Thrown balls`", value="\n".join(
                ["`{}` : {}".format(listballs[i], datas[23][i]) for i in range(len(listballs))]), inline=False)
            embed.add_field(name="`Used razz`",
                            value="`Fake razz` : {}\n`Rare razz` : {}".format(datas[23][11], datas[23][12]),
                            inline=True)
            embed.add_field(name="`Lucky machine activation`", value="{} encounters.".format(datas[23][13]),
                            inline=False)
            await ctx.send(embed=embed)

        @app_commands.command()
        @app_commands.cooldown(1, 10, commands.BucketType.user)
        async def lock(self, ctx, locking: typing.Optional[int] = 0):
            '''Use this command to lock up to 50 Pokémon from being released by `.rls d`. Legendary, Mythical, Ultrabeast, God and Egg rarities are locked by default. \nSyntax : `.lock <dexnumber>`
            '''
            id = str(ctx.message.author.id)
            datas = setdata(id, str(ctx.message.author))
            locked = datas[20]
            language = setlanguage(id)
            if locking > 0:
                try:
                    locking -= 1
                    if locking in locked:
                        locked.remove(locking)
                        await ctx.send("You unlocked {} from release.".format(dex[locking][language].capitalize()))
                    else:
                        if len(locked) > 49:
                            await ctx.send("You already locked 50 Pokémon from release.")
                            return
                        locked.append(locking)
                        locked.sort()
                        await ctx.send(
                            "You added {} to your locked Pokémon.".format(dex[locking][language].capitalize()))
                    datas[20] = locked
                    # db["player_data"+id] = datas
                except:
                    await ctx.send("Invalid Pokémon number.")
                    return
            if len(locked) == 0:
                await ctx.send("You can see your locked Pokémon here.")
                return
            text = "Locked Pokémon :\n"
            for i in locked:
                text += "`{} : {}` {}\n".format(i + 1, rarityname[getrarity(i + 1)], dex[i][language].capitalize())
            await ctx.send(text)

        @app_commands.command()
        @app_commands.cooldown(1, 10, commands.BucketType.user)
        async def partner(self, ctx, partner: typing.Optional[int] = 0):
            '''Set your partner Pokémon to get the clone ball boost and some other advantages. \nSyntax : `.partner <dexnumber>`
            '''
            datas = setdata(ctx.message.author.id, str(ctx.message.author))
            language = setlanguage(ctx.message.author.id)
            try:
                if 0 < partner < len(dex):
                    if datas[7][partner - 1][0] + datas[7][partner - 1][1] > 0:
                        datas[19][0] = partner - 1
                        await ctx.send("You set {} as your partner.".format(dex[partner - 1][language]).capitalize())
                        # db["player_data"+str(ctx.message.author.id)] = datas
                    else:
                        await ctx.send("You don't have {} yet !".format(dex[partner - 1][language].capitalize()))
                else:
                    await ctx.send("Your current partner is {}.".format(dex[datas[19][0]][language].capitalize()))
            except:
                await ctx.send("Invalid number.")

        @app_commands.command()
        @app_commands.cooldown(1, 10, commands.BucketType.user)
        async def dream(self, ctx, dream: typing.Optional[int] = 0):
            '''Set your dreamed Pokémon here to get the dream ball boost. \nSyntax : `.dream <dexnumber>`
            '''
            datas = setdata(ctx.message.author.id, str(ctx.message.author))
            language = setlanguage(ctx.message.author.id)
            try:
                if 0 < dream < len(dex):
                    datas[19][1] = dream - 1
                    await ctx.send("You set {} as your dream Pokémon.".format(dex[dream - 1][language].capitalize()))
                    # db["player_data"+str(ctx.message.author.id)] = datas
                else:
                    await ctx.send("Your current dream Pokémon is {}.".format(dex[datas[19][1]][language].capitalize()))
            except:
                await ctx.send("Invalid number.")

        @app_commands.command()
        @app_commands.cooldown(1, 60, commands.BucketType.user)
        async def play(self, ctx):
            '''Use this command to play the game !
            '''
            keys = db.prefix("player_data")
            if "player_data" + str(ctx.message.author.id) in keys:
                color = setoption(ctx.message.author.id)[2]
                player_data = db["player_data" + str(ctx.message.author.id)]
                name = player_data[0]
                embed = discord.Embed(title=places[player_data[1]][0], description=name, colour=color,
                                      timestamp=datetime.utcnow())
                embed.set_footer(text="SHAdOw")
                embed.add_field(name="`What to do ?`", value="`.e` \nGame under development.", inline=False)
                embed.set_image(url=places_pic[places[player_data[1]][0]])
                await ctx.send(embed=embed)
            else:
                setdata(ctx.message.author.id, str(ctx.message.author), True)
                await ctx.send(
                    "https://cdn.discordapp.com/attachments/754349043714621540/793349869019856906/Professeur_Chen-LGPE.png")  # Professeur Chen.
                await ctx.send(
                    "Hey you ! Welcome to the world of Pokémon.\nI\'m the professor Oak.\nI study Pokémon. They live everywhere in this world and in harmony with humans. Some use them as companions while others do battles with them.\nYour name is " + str(
                        ctx.message.author) + ", right ?\nReady to begin your adventure ?\nA brand new world is waiting you !\nDo `.play` to play.")

        @app_commands.command()
        @app_commands.cooldown(1, 3, commands.BucketType.user)
        async def give(self, ctx, recid: typing.Optional[str] = "373707498479288330", money: typing.Optional[int] = 0):
            '''Use this command to give money to other players. \nSyntax : `.give <id or mention> <amount>`
            '''
            id = str(ctx.message.author.id)
            try:
                recid = str(ctx.message.mentions[0].id)
            except:
                recid = str(recid)
            givedatas = setdata(id, str(ctx.message.author))
            receivedatas = setdata(recid, None)
            if money < 0 and int(id) not in authors:
                await ctx.send("You can't steal money !")
                return
            if givedatas[9] < money and int(id) not in authors:
                await ctx.send("You don't have enough money !")
                return
            if id == recid:
                await ctx.send("You gave {} coins to {}. But it seems it's yourself.".format(money, recid))
                return
            if int(id) not in authors:
                givedatas[9] -= money
            receivedatas[9] += money - 1 * int(money > 0)
            # db["player_data"+id] = givedatas
            # db["player_data"+recid] = receivedatas
            print(1)
            embed = discord.Embed(title="Money transaction",
                                  description="||I know you clicked on this so give the owner 10 coins now.||",
                                  colour=0x000000, timestamp=datetime.utcnow())
            embed.set_footer(text="SHAdOw")
            embed.add_field(name="Successful transaction",
                            value="{} gave {} coins to {}.".format(givedatas[0], money - 1, receivedatas[0]),
                            inline=True)
            print(2)
            await bot.get_channel(842381697642922004).send(embed=embed)
            await ctx.send("You gave {} coins to {} (with a 1 coin fee).".format(money - 1, recid))

        @app_commands.command(aliases=["balls"])
        @app_commands.cooldown(1, 10, commands.BucketType.user)
        async def ball(self, ctx):
            '''Use this command to see what the balls do.`
            '''
            id = ctx.message.author.id
            options = setoption(id)
            datas = setdata(id, str(ctx.message.author))
            embed = discord.Embed(title="Balls", description="`Balls wiki`", colour=options[2],
                                  timestamp=datetime.utcnow())
            embed.set_footer(text="SHAdOw")
            embed.add_field(name="Pokéball `pb`", value="Adds 10 catch power.\nYou own {} now.".format(datas[10][0]),
                            inline=True)
            embed.add_field(name="Greatball `gb`", value="Adds 15 catch power.\nYou own {} now.".format(datas[10][1]),
                            inline=True)
            embed.add_field(name="Ultraball `ub`", value="Adds 25 catch power.\nYou own {} now.".format(datas[10][2]),
                            inline=True)
            embed.add_field(name="Masterball `mb`",
                            value="Put the catch power to 99 no matter what except if a rare razz is activated.\nYou own {} now.".format(
                                datas[10][3]), inline=True)
            embed.add_field(name="Recoilball `rb`",
                            value="Adds 100 catch power but reduces the catch power by 50 for 100 encounters. During the recoil, every 12.5 recoiled encounters left reduces the catch power by 1. You can upgrade the recoilball using `.rb` to reduce those drawbacks.\nYou own {} now.".format(
                                datas[10][4]), inline=True)
            embed.add_field(name="Beastball `bb`",
                            value="Adds 20 catch power and gives 40 bonus catch power if you're catching an Ultra-beast.\nYou own {} now.".format(
                                datas[10][5]), inline=True)
            embed.add_field(name="Quickball `qb`",
                            value="Adds 15 catch power and has 50% chance to let you throw a Premierball to the same Pokémon. The catch power will then be augmented of 10. You need to have at least a Premierball in your bag to do this.\nYou own {} now.".format(
                                datas[10][6]), inline=True)
            embed.add_field(name="Dreamball `db`",
                            value="Adds 10 catch power and gives 150 bonus catch power if you're catching your dreamed Pokémon. To set your dreamed Pokémon do `.dream`.\nYou own {} now.".format(
                                datas[10][7]), inline=True)
            embed.add_field(name="Cloneball `cb`",
                            value="Adds 10 catch power and gives 150 bonus catch power if you're catching your partner Pokémon. To set your partner Pokémon do `.partner`.\nYou own {} now.".format(
                                datas[10][8]), inline=True)
            embed.add_field(name="Premierball `prb`",
                            value="Adds 10 catch power. Is the only ball you can throw if the Quickball's special effect is triggered.\nYou own {} now.".format(
                                datas[10][9]), inline=True)
            embed.add_field(name="Fifty-fifty ball `fb`",
                            value="Put the catch power to 50 no matter what except if a rare razz is activated.\nYou own {} now.".format(
                                datas[10][10]), inline=True)
            await ctx.send(embed=embed)

        @app_commands.command(aliases=["quiz"])
        @app_commands.has_role("Trivia Organizer")
        @app_commands.cooldown(10, 900, commands.BucketType.user)
        async def trivia(self, ctx):
            if ctx.message.channel.id != 834362605140705291:
                await ctx.send(bot.get_channel(834362605140705291).mention)
            keys = db.prefix("player_data")
            difficulty = choices([0, 1, 2, 3, 4], weights=[700, 200, 140, 50, 1])[0]
            questionset = [trivias1, trivias2, trivias3, trivias4, trivias5][difficulty]
            question = randint(0, len(questionset) - 1)
            quiz = await bot.get_channel(834362605140705291).send(
                "Difficulty : {}\n{}".format(difficulty + 1, questionset[question][0]))

            def check(m):
                return m.content.lower() in questionset[question][1:] and "player_data" + str(m.author.id) in keys

            try:
                answer = await bot.wait_for("message", check=check, timeout=120)
            except asyncio.TimeoutError:
                return await ctx.send("Timeout. Correct answer was {}.".format(questionset[question][1]))

            id = answer.author.id
            datas = setdata(id, None)
            moneyprize = randint(100 * 2 ** (difficulty + 1), 500 * 2 ** (difficulty + 1))
            datas[9] += moneyprize
            datas[14] += moneyprize
            datas[24] += moneyprize
            await quiz.edit(content="Difficulty : {}\n{}\nCorrect answer was given by {}.".format(difficulty + 1,
                                                                                                  questionset[question][
                                                                                                      0], datas[0]))

            await bot.get_channel(834362605140705291).send("{} won {} coins as a prize.".format(datas[0], moneyprize))
