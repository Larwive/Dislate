from datetime import datetime
from random import randint

import discord
import sqlite3
from game_data import *

chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def createdata(player_id, name):
  data = sqlite3.connect('data.db')
  cursor = data.cursor()
  cursor.execute("INSERT INTO options (id, name) VALUES(?, ?)", (player_id, name))
  cursor.execute("INSERT INTO game (id) VALUES(?)", (player_id,))
  cursor.execute("INSERT INTO locked (id) VALUES(?)", (player_id,))
  cursor.execute("INSERT INTO poke (id) VALUES(?)", (player_id,))
  cursor.execute("INSERT INTO teams (id) VALUES(?)", (player_id,))
  data.commit()
  data.close()

def init_options(): #v.o.l., unused, color, language, privacy, link to dex, see game stats (secret), Color depending on rarity (secret)
  data = sqlite3.connect('data.db')
  cursor = data.cursor()
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS options(
       id INTEGER PRIMARY KEY,
       name TEXT,
       vol INTEGER DEFAULT 0,
       color INTEGER DEFAULT 0,
       language INTEGER DEFAULT 0,
       privacy INTEGER DEFAULT 0,
       dexlink INTEGER DEFAULT 0,
       gamestats INTEGER DEFAULT 0,
       raritycolor INTEGER DEFAULT 0
  )
  """)
  data.commit()
  data.close()

def init_game():
  data = sqlite3.connect('data.db')
  cursor = data.cursor()
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS game(
       id INTEGER PRIMARY KEY,
       place INTEGER DEFAULT 0,
       team TEXT DEFAULT "0-0-0-0-0-0",
       scenario INTEGER DEFAULT 0,
       money INTEGER DEFAULT 5000,
       totalmoney INTEGER DEFAULT 5000,
       caught INTEGER DEFAULT 0,
       recleft INTEGER DEFAULT 0,
       rbred INTEGER DEFAULT 0,
       rbeffect INTEGER DEFAULT 0,
       rbluck INTEGER DEFAULT 0,
       partner INTEGER DEFAULT 0,
       dreamed INTEGER DEFAULT 0,
       seenabled INTEGER DEFAULT 0,
       sedex INTEGER DEFAULT 0,
       seisshiny INTEGER DEFAULT 0,
       amuletcoin INTEGER DEFAULT 0,
       pb INTEGER DEFAULT 50,
       pbused INTEGER DEFAULT 0,
       gb INTEGER DEFAULT 20,
       gbused INTEGER DEFAULT 0,
       ub INTEGER DEFAULT 3,
       ubused INTEGER DEFAULT 0,
       mb INTEGER DEFAULT 0,
       mbused INTEGER DEFAULT 0,
       rb INTEGER DEFAULT 0,
       rbused INTEGER DEFAULT 0,
       bb INTEGER DEFAULT 0,
       bbused INTEGER DEFAULT 0,
       qb INTEGER DEFAULT 0,
       qbused INTEGER DEFAULT 0,
       db INTEGER DEFAULT 0,
       dbused INTEGER DEFAULT 0,
       cb INTEGER DEFAULT 0,
       cbused INTEGER DEFAULT 0,
       prb INTEGER DEFAULT 0,
       prbused INTEGER DEFAULT 0,
       fb INTEGER DEFAULT 0,
       fbused INTEGER DEFAULT 0,
       rrazz INTEGER DEFAULT 0,
       rrazzleft INTEGER DEFAULT 0,
       rrazzused INTEGER DEFAULT 0,
       frazz INTEGER DEFAULT 0,
       frazzleft INTEGER DEFAULT 0,
       frazzused INTEGER DEFAULT 0,
       lmleft INTEGER DEFAULT 0,
       lmencounter INTEGER DEFAULT 0,
       hatched INTEGER DEFAULT 0,
       triviamoney INTEGER DEFAULT 0
  )
  """)
  data.commit()
  data.close()

def init_lock():
  data = sqlite3.connect('data.db')
  cursor = data.cursor()
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS locked(
    id INTEGER PRIMARY KEY,
    lock1 INTEGER DEFAULT 0,
    lock2 INTEGER DEFAULT 0,
    lock3 INTEGER DEFAULT 0,
    lock4 INTEGER DEFAULT 0,
    lock5 INTEGER DEFAULT 0,
    lock6 INTEGER DEFAULT 0,
    lock7 INTEGER DEFAULT 0,
    lock8 INTEGER DEFAULT 0,
    lock9 INTEGER DEFAULT 0,
    lock10 INTEGER DEFAULT 0,
    lock11 INTEGER DEFAULT 0,
    lock12 INTEGER DEFAULT 0,
    lock13 INTEGER DEFAULT 0,
    lock14 INTEGER DEFAULT 0,
    lock15 INTEGER DEFAULT 0,
    lock16 INTEGER DEFAULT 0,
    lock17 INTEGER DEFAULT 0,
    lock18 INTEGER DEFAULT 0,
    lock19 INTEGER DEFAULT 0,
    lock20 INTEGER DEFAULT 0,
    lock21 INTEGER DEFAULT 0,
    lock22 INTEGER DEFAULT 0,
    lock23 INTEGER DEFAULT 0,
    lock24 INTEGER DEFAULT 0,
    lock25 INTEGER DEFAULT 0,
    lock26 INTEGER DEFAULT 0,
    lock27 INTEGER DEFAULT 0,
    lock28 INTEGER DEFAULT 0,
    lock29 INTEGER DEFAULT 0,
    lock30 INTEGER DEFAULT 0,
    lock31 INTEGER DEFAULT 0,
    lock32 INTEGER DEFAULT 0,
    lock33 INTEGER DEFAULT 0,
    lock34 INTEGER DEFAULT 0,
    lock35 INTEGER DEFAULT 0,
    lock36 INTEGER DEFAULT 0,
    lock37 INTEGER DEFAULT 0,
    lock38 INTEGER DEFAULT 0,
    lock39 INTEGER DEFAULT 0,
    lock40 INTEGER DEFAULT 0,
    lock41 INTEGER DEFAULT 0,
    lock42 INTEGER DEFAULT 0,
    lock43 INTEGER DEFAULT 0,
    lock44 INTEGER DEFAULT 0,
    lock45 INTEGER DEFAULT 0,
    lock46 INTEGER DEFAULT 0,
    lock47 INTEGER DEFAULT 0,
    lock48 INTEGER DEFAULT 0,
    lock49 INTEGER DEFAULT 0,
    lock50 INTEGER DEFAULT 0
  )
  """)
  data.commit()
  data.close()

def init_teams():
  data = sqlite3.connect('data.db')
  cursor = data.cursor()
  #cursor.execute("ALTER TABLE game ADD COLUMN currentteam DEFAULT 0")
  #cursor.execute("ALTER TABLE game ADD COLUMN teamapply DEFAULT 0")
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS teams(
    id INTEGER PRIMARY KEY,
    teamrocket INTEGER DEFAULT 0,
    teamaqua INTEGER DEFAULT 0,
    teammagma INTEGER DEFAULT 0,
    teamgalaxie INTEGER DEFAULT 0,
    teamplasma INTEGER DEFAULT 0,
    teamflare INTEGER DEFAULT 0,
    teamskull INTEGER DEFAULT 0,
    aether INTEGER DEFAULT 0,
    teamrainbowrocket INTEGER DEFAULT 0,
    teamyell INTEGER DEFAULT 0,
    macrocosmos INTEGER DEFAULT 0,
    teamstar INTEGER DEFAULT 0,
    groupeombre INTEGER DEFAULT 0,
    bataillonphobos INTEGER DEFAULT 0,
    sombresheros INTEGER DEFAULT 0,
    teambreak INTEGER DEFAULT 0,
    teamgorocket INTEGER DEFAULT 0
  )
  """)
  cursor.execute("""
  DROP TABLE global
  """)
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS global(
    teamrocketsuccess INTEGER DEFAULT 0,
    teamaquasuccess INTEGER DEFAULT 0,
    teammagmasuccess INTEGER DEFAULT 0,
    teamgalaxiesuccess INTEGER DEFAULT 0,
    teamplasmasuccess INTEGER DEFAULT 0,
    teamflaresuccess INTEGER DEFAULT 0,
    teamskullsuccess INTEGER DEFAULT 0,
    aethersuccess INTEGER DEFAULT 0,
    teamrainbowrocketsuccess INTEGER DEFAULT 0,
    teamyellsuccess INTEGER DEFAULT 0,
    macrocosmossuccess INTEGER DEFAULT 0,
    teamstarsuccess INTEGER DEFAULT 0,
    groupeombresuccess INTEGER DEFAULT 0,
    bataillonphobossuccess INTEGER DEFAULT 0,
    sombresherossuccess INTEGER DEFAULT 0,
    teambreaksuccess INTEGER DEFAULT 0,
    teamgorocketsuccess INTEGER DEFAULT 0
  )
  """)
  cursor.execute("INSERT INTO global (teamrocketsuccess) VALUES(?)", (0,))
  data.commit()
  data.close()

def init_poke():
  data = sqlite3.connect('data.db')
  cursor = data.cursor()
  cursor.execute("""CREATE TABLE IF NOT EXISTS poke(id INTEGER PRIMARY KEY)""")
  for i in range(1,1500, 5):
      #col = "{}{}".format("0"*((i<10)+(i<100)+(i<1000)), i)
      cursor.execute("""ALTER TABLE poke ADD COLUMN pokemon{} TEXT DEFAULT "0-0-0-0-0" """.format(i))
      cursor.execute("""ALTER TABLE poke ADD COLUMN pokeshi{} TEXT DEFAULT "0-0-0-0-0" """.format(i))
      cursor.execute("""ALTER TABLE poke ADD COLUMN iv{} TEXT DEFAULT "0-0-0-0-0" """.format(i))
      cursor.execute("""ALTER TABLE poke ADD COLUMN cpokemon{} TEXT DEFAULT "0-0-0-0-0" """.format(i))
      cursor.execute("""ALTER TABLE poke ADD COLUMN cpokeshi{} TEXT DEFAULT "0-0-0-0-0" """.format(i))
  data.commit()
  data.close()

  """
##Options updater
def optionupdater():
  keys = db.prefix("option")
  for data in keys:
    newdatas = db[data]
    while len(newdatas) > len(defaultoption):
      newdatas.pop()
    if len(newdatas) < len(defaultoption):
      for i in range(len(newdatas), len(defaultoption)):
        newdatas.append(defaultoption[i])
      db[data] = newdatas

##Player_data updater
def dataupdater():
  keys = db.prefix("player_data")
  datas = [None, 2, [False for _ in range(len(dex))], [0 for _ in range(len(dex))], [0 for _ in range(len(dex))], [False for _ in range(len(dex))], [None, None, None, None, None, None], [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] for _ in range(len(dex))], 2, 1000, [20, 10, 5]+[0 for _ in range(997)], 0, 0, [0 for _ in range(len(dex))], 1000, False, [0 for _ in range(len(dex))], 0, [1, 1, 1], [None, None], [], [False, 0, 0], [0, 0, 0], [0 for _ in range(15)], 0   ]
  datanumbers = len(datas) #Voir game.py
  for data in keys:
    newdatas = db[data]
    while len(newdatas) > datanumbers:
      newdatas.pop()
    if len(newdatas) < datanumbers:
      for i in range(len(newdatas), datanumbers):
        newdatas.append(datas[i])
      db[data] = newdatas"""

def getdata(player_id, table, key):
  data = sqlite3.connect("data.db")
  cursor = data.cursor()
  cursor.execute("SELECT {} FROM {} WHERE id=={}".format(key, table, player_id))
  result = cursor.fetchone()
  data.close()
  return result

def setdata(player_id, table, key, new_data, add=None):
  data = sqlite3.connect("data.db")
  cursor = data.cursor()
  if add is not None:
    cursor.execute("SELECT {} FROM {} WHERE id=={}".format(key, table, player_id))
    res = list(cursor.fetchone())
    for i in range(len(add)):
      #res[i] = int(res[i])
      if add[i]:
        res[i] += add[i]
    new_data = res
  new_data = str(new_data)
  if new_data[0] == '[':
    new_data = str(new_data)[1:]
  if new_data[-1] == ']':
    new_data = str(new_data)[:-1]
  print("UPDATE {} SET ({})=({}) WHERE id=={}".format(table, key, new_data, player_id))
  cursor.execute("UPDATE {} SET ({})=({}) WHERE id=={}".format(table, key, new_data, player_id))
  data.commit()
  data.close()

def getglobal(key):
  data = sqlite3.connect("data.db")
  cursor = data.cursor()
  cursor.execute("SELECT {} FROM global".format(key))
  result = cursor.fetchone()
  print(result)
  data.close()
  return result

def setglobal(key, new_data, add=None):
  data = sqlite3.connect("data.db")
  cursor = data.cursor()
  if add is not None:
    cursor.execute("SELECT {} FROM global".format(key))
    res = list(cursor.fetchone())
    for i in range(len(add)):
      # res[i] = int(res[i])
      if add[i]:
        res[i] += add[i]
    new_data = res
  new_data = str(new_data)
  if new_data[0] == '[':
    new_data = str(new_data)[1:]
  if new_data[-1] == ']':
    new_data = str(new_data)[:-1]

  print("UPDATE global SET ({})=({})".format(key, new_data))
  cursor.execute("UPDATE global SET ({})=({})".format(key, new_data))
  data.commit()
  data.close()

def getoption(player_id):
  data =  sqlite3.connect("data.db")
  cursor = data.cursor()
  cursor.execute("SELECT * FROM options WHERE id=={}".format(player_id))
  options = cursor.fetchone()
  data.close()
  return options

def getgame(player_id, name):
  data = sqlite3.connect("data.db")
  cursor = data.cursor()
  cursor.execute("SELECT * FROM data WHERE id=={}".format(player_id))
  result = cursor.fetchone()
  if result is not None:
    data.close()
    return result[0]
  cursor.execute("INSERT INTO data (id, name) VALUES(?, ?)",
            (player_id, name))
  data.commit()
  cursor.execute("SELECT * FROM data WHERE id=={}".format(player_id))
  result = cursor.fetchone()
  data.close()
  return result[0]

def getspawnweights(player_id:int):
  spawnweight = spawnweights.copy()
  frazzleft, rrazzleft, lmleft, money = getdata(player_id, "game", "frazzleft, rrazzleft, lmleft, money")
  if frazzleft > 0:
    for i in range(6, len(spawnweight)):
      spawnweight[i] = int(spawnweight[i] / 2)
  if rrazzleft > 0:
    for i in range(6, len(spawnweight)):
      spawnweight[i] *= 2
  if lmleft > 0 and money > 2500:
    for i in range(6, len(spawnweight)):
      spawnweight[i] *= 3
  return spawnweight
"""def additems(item, amount, id):
  try:
    item = int(item) -1
    if item < len(buyableitems) and amount > 0:
      datas = getdata(id)
      price = buyableitems[item][2]*amount
      if price > datas[9]:
        return False, False, 51
      if datas[10][10] + amount > 50 and item == 10: #Amulet coins
        return False, False, 51
      if True: #À modifier ?
        datas[10][item] += amount
        datas[9] -= price
        if item == 0 and amount > 9:
          datas[10][9] += amount//10
        db["player_data"+str(id)] = datas
        return True, datas[9], datas[10][10]
    return False, False, 51
  except:
    return False, False, 51"""

def getdex(list_name, found_types, stats, sprite, language, number:int, player_id, shiny):
  vol, dexlink, gamestats = getdata(player_id, "options", "vol, dexlink, gamestats")
  #datas = getgame(player_id, name)
  iv = extract(player_id, "iv", number)
  if shiny:
    caught = extract(player_id, "cpokeshi", number)
    inbox = extract(player_id, "pokeshi", number)
  else:
    caught = extract(player_id, "cpokemon", number)
    inbox = extract(player_id, "pokemon", number)
  if number is None:
    embed = discord.Embed(title = "Pokédex", description = list_name[language].capitalize(), colour = [0xA8A878, 0xC03028, 0xA890F0, 0xA040A0, 0xE0C068, 0xB8A038, 0xA8B820, 0x705898, 0xB8B8D0, 0xF08030, 0x6890F0, 0x78C850, 0xF8D030, 0xF85888, 0x98D8D8, 0x7038F8, 0x705848, 0xEE99AC][types[0]], timestamp = datetime.utcnow())
  else:
    embed = discord.Embed(title = "Pokédex", description = list_name[language].capitalize()+" #"+str(number)+" "+rarityname[getrarity(number)], colour = [0xA8A878, 0xC03028, 0xA890F0, 0xA040A0, 0xE0C068, 0xB8A038, 0xA8B820, 0x705898, 0xB8B8D0, 0xF08030, 0x6890F0, 0x78C850, 0xF8D030, 0xF85888, 0x98D8D8, 0x7038F8, 0x705848, 0xEE99AC][found_types[0]], timestamp = datetime.utcnow())
  embed.set_footer(text = "Dislate")
  embed.set_image(url=sprite)
  strypes = types_name[found_types[0]][language]
  defense_effectiveness = [row[found_types[0]] for row in type_chart]
  weakness, double_weakness, immunity, resistance, double_resistance = [], [], [], [], []
  if len(found_types) == 2:
    strypes += ", "+types_name[found_types[1]][language]
    for i in range(18):
      defense_effectiveness[i] *= type_chart[i,found_types[1]]
  for i in range(18):
    if defense_effectiveness[i] == 2:
      weakness.append(i)
    elif defense_effectiveness[i] == 4:
      double_weakness.append(i)
    elif defense_effectiveness[i] == 0:
      immunity.append(i)
    elif defense_effectiveness[i] == 0.5:
      resistance.append(i)
    elif defense_effectiveness[i] == 0.25:
      double_resistance.append(i)
  embed.add_field(name = ["`Types`","`Types`", "`Typen`", "`属性`", "`유형`", "`Taipu`", "`タイプ`"][language], value = strypes, inline = False)
  embed.add_field(name = ["`Base stats (Hp/Atk/Def/Spa/Spd/Spe)`", "`Stats de base (Pv/Att/Def/ASp/DSp/Vit)`", "`Statuswerte (Kra/Ang/Ver/SpA/SpV/Ini)`", "`能力 (Hp/攻击/防御/特攻/特防/速度)`", "`통계 (Hp/공격/방어/특수공격/특수방어/스피드)`", "`Sutētasu (Kō geki/Bōgyo/Toku kō/Toku bō/Subaya-sa)`", "`ステータス (Hp/こうげき/ぼうぎょ/とくこう/とくぼう/すばやさ)`"][language], value = str(stats[0])+"/"+str(stats[1])+"/"+str(stats[2])+"/"+str(stats[3])+"/"+str(stats[4])+"/"+str(stats[5]), inline = False)
  if len(weakness) != 0:
    weak = types_name[weakness[0]][language]
    for i in range(1,len(weakness)):
        weak += ", "+types_name[weakness[i]][language]
  else:
    weak = ["None", "Aucun", "Nein", "沒有", "아니", "Bangō", "番号"][language]
  if len(double_weakness) != 0:
    douweak = types_name[double_weakness[0]][language]
    for i in range(1,len(double_weakness)):
      douweak += ", "+types_name[double_weakness[i]][language]
  else:
    douweak = ["None", "Aucun", "Nein", "沒有", "아니", "Bangō", "番号"][language]
  if len(immunity) != 0:
    immune = types_name[immunity[0]][language]
    for i in range(1,len(immunity)):
      douweak += ", "+types_name[immunity[i]][language]
  else:
    immune = ["None", "Aucun", "Nein", "沒有", "아니", "Bangō", "番号"][language]
  if len(resistance) != 0:
    resist = types_name[resistance[0]][language]
    for i in range(1,len(resistance)):
      resist += ", "+types_name[resistance[i]][language]
  else:
    resist = ["None", "Aucun", "Nein", "沒有", "아니", "Bangō", "番号"][language]
  if len(double_resistance) != 0:
    dousist = types_name[double_resistance[0]][language]
    for i in range(1,len(double_resistance)):
      dousist += ", "+types_name[double_resistance[i]][language]
  else:
    dousist = ["None", "Aucun", "Nein", "沒有", "아니", "Bangō", "番号"][language]
  embed.add_field(name = ["`Double weakness", "`Double faiblesse", "`Doppelte Schwäche", "`雙重弱點", "`이중 약점", "`Nijū no jakuten", "`二重の弱点"][language]+" (x4)`", value = douweak, inline = True)
  embed.add_field(name = ["`Weakness", "`Faiblesse", "`Schwäche", "`弱點", "`약점", "`Jakuten", "`弱点"][language]+" (x2)`", value = weak, inline = True)
  embed.add_field(name = ["`Immunity", "`Immunité", "`Immunität", "`免疫", "`면역", "`Men'eki", "`免疫"][language]+" (x0)`", value = immune, inline = True)
  embed.add_field(name = ["`Resistance", "`Résistance", "`Widerstand", "`抵抗", "`저항", "`Teikō", "`抵抗"][language]+" (x0.5)`", value = resist, inline = True)
  embed.add_field(name = ["`Double resistance", "`Double résistance", "`Doppelter Widerstand", "`雙重抵抗", "`이중 저항", "`Nijū teikō", "`二重抵抗"][language]+" (x0.25)`", value = dousist, inline = True)
  if vol: # options[0]: #View other languages.
    embed.add_field(name = ["`Name in other languages`", "`Noms dans d'autres langues`", "`Namen in anderen Sprachen`", "`用其他語言命名`", "`다른 언어로 된 이름`", "`Hoka no gengo no namae`", "`他の言語の名前`"][language], value = ["English", "Anglais", "Englische Sprache", "英文", "영어", "Eigo", "英語"][language]+" : "+list_name[0].capitalize()+"\n"+["French", "Français", "Französisch Sprache", "法文", "프랑스 국민", "Furansugo", "フランス語"][language]+" : "+list_name[1].capitalize()+"\n"+["Japanese", "Japonais", "Japanisch Sprache", "日文", "일본어", "Hifumi", "日本語"][language]+" : "+list_name[6]+" / "+list_name[5].capitalize()+"\n"+["Chinese", "Chinois", "Chinesische Sprache", "中文", "중국어", "Chūgokugo", "中国語"][language]+" : "+list_name[3]+"\n"+["German", "Allemand", "Deutsche Sprache", "德國的語言", "독일어", "Doitsugo", "ドイツ語"][language]+" : "+list_name[2].capitalize()+"\n"+["Korean", "Coréen", "Koreanische Sprache", "朝鮮語", "한국어", "Kankoku-go", "韓国語"][language]+" : "+list_name[4], inline = False)
  if dexlink: #options[5]: #View links
    embed.add_field(name = ["`Link`", "`Lien`", "`Link`", "`網站`", "`사이트 링크`", "`Saito rinku`", "`サイトリンク`"][language], value = ["https://bulbapedia.bulbagarden.net/wiki/"+list_name[language]+"_(Pok%C3%A9mon)", "https://www.pokepedia.fr/"+list_name[language], "https://www.pokewiki.de/"+list_name[language], "https://wiki.52poke.com/wiki/"+list_name[language], "https://pokemonkorea.co.kr/pokedex", "https://wiki.xn--rckteqa2e.com/wiki/"+list_name[language], "https://wiki.xn--rckteqa2e.com/wiki/"+list_name[language]][language], inline = True)
  if gamestats: #options[6]: #View game stats
    embed.add_field(name = ["`Caught`", "`Capturé`", "`Erfassung`", "`捕獲`", "`포착`", "`Kyapuchā`", "`キャプチャー`"][language], value = caught, inline = True)
    embed.add_field(name = ["`Inbox`", "`Dans le pc`", "`Erfassung`", "`捕獲`", "`포착`", "`Kyapuchā`", "`キャプチャー`"][language], value = inbox, inline = True)
    #embed.add_field(name = ["`IVs (Hp/Atk/Def/Spa/Spd/Spe)`", "`IVs (Pv/Att/Def/ASp/DSp/Vit)`", "`IVs (Kra/Ang/Ver/SpA/SpV/Ini)`", "`IVs (Hp/攻击/防御/特攻/特防/速度)`", "`IVs (Hp/공격/방어/특수공격/특수방어/스피드)`", "`IVs (Kō geki/Bōgyo/Toku kō/Toku bō/Subaya-sa)`", "`IVs (Hp/こうげき/ぼうぎょ/とくこう/とくぼう/すばやさ)`"][language], value = "{}/{}/{}/{}/{}/{}".format(datas[7][number][2], datas[7][number][3], datas[7][number][4], datas[7][number][5], datas[7][number][6], datas[7][number][7]), inline = True)
    embed.add_field(name="`IVs`",
                    value=str(iv),
                    inline=True)
  return embed

def extract(player_id:int, incomplete_key:str, dex_number:int):
  """
  Read datas from the poke table.
  :param player_id: The Discord id of the player
  :param incomplete_key: The key you want to complete
  :param dex_number: The dex number's data you want to read
  :return: The read value
  """
  data = sqlite3.connect("data.db")
  cursor = data.cursor()
  cursor.execute("SELECT {}{} FROM poke WHERE id=={}".format(incomplete_key, dex_number-(dex_number-1)%5, player_id))
  result, = cursor.fetchone()
  data.close()
  result = result.split("-")[(dex_number-1)%5]
  l = len(result)
  n = 0
  for i in range(l - 1, -1, -1):
    n += chars.index(result[i]) * 36 ** (l - 1 - i)
  return n

def extractlist(player_id:int, incomplete_key:str, dex_number:int):
  """
  Read datas from the poke table.
  :param player_id: The Discord id of the player
  :param incomplete_key: The key you want to complete
  :param dex_number: The dex number's data you want to read
  :return: The read value
  """
  data = sqlite3.connect("data.db")
  cursor = data.cursor()
  cursor.execute("SELECT {}{} FROM poke WHERE id=={}".format(incomplete_key, dex_number-(dex_number-1)%5, player_id))
  result, = cursor.fetchone()
  data.close()
  result = result.split("-")#[(dex_number-1)%5]
  L = []
  for amount in result:
    l = len(amount)
    n = 0
    for i in range(l - 1, -1, -1):
      n += chars.index(amount[i]) * 36 ** (l - 1 - i)
    L.append(n)
  return L

def write(datas:str, dex_number:int, new_value:int, add:int=0):
  """
  Write datas for the poke table.
  :param datas: The result of the sql query for the datas you want to write
  :param dex_number: The dex number you want to act on
  :param new_value: The new value for the dex number data (ignored if the parameter add is filled)
  :param add: Update the data by adding the add value (default to 0)
  :return: The updated data
  """
  #data = datas[dex_number-1-(dex_number-1)%5+1] # Utile ?
  data = datas.split("-")

  if add:
    value = data[(dex_number - 1)%5]
    l = len(value)
    n = add
    for i in range(l - 1, -1, -1):
      n += chars.index(value[i]) * 36 ** (l - 1 - i)
  else:
    n = new_value

  if n>=60466175:
    n=60466175
  res = ""
  while n:
      res = chars[n % 36] + res
      n = n // 36
  data[(dex_number-1)%5] = res
  return "'{}'".format("-".join(data))
def add_pokemon(player_id:int, dex_number:int, shininess:bool, updateiv:bool=False, amount:int=1):
  """
  :param player_id: The Discord id of the player
  :param dex_number: The dex number of the Pokémon to be added
  :param shininess: Booleean indicating whether the Pokémon is shiny or not
  :param updateiv: Booleen indicating whether the IVs should be updated (if it's a real encounter)
  :param amount: The amount to be added
  :return: The updated (ivdata, pokedata) tuple
  """
  data = sqlite3.connect("data.db")
  cursor = data.cursor()
  actualkey = dex_number-(dex_number-1)%5
  if shininess:
    cursor.execute("SELECT pokeshi{}, iv{}, cpokeshi{} FROM poke WHERE id=={}".format(actualkey, actualkey, actualkey, player_id))
    pokedata, ivdata, cpokedata = cursor.fetchone()
  else:
    cursor.execute("SELECT pokemon{}, iv{}, cpokemon{} FROM poke WHERE id=={}".format(actualkey, actualkey, actualkey, player_id))
    pokedata, ivdata, cpokedata = cursor.fetchone()
  print(pokedata, ivdata, cpokedata)
  data.close()
  pokedata = write(pokedata, dex_number, None, amount)
  cpokedata = write(cpokedata, dex_number, None, amount)
  iv = randint(0, 31)
  if updateiv and (iv > extract(player_id, "iv", dex_number)):
    ivdata = write(ivdata, dex_number, iv)
  else:
    ivdata = "'{}'".format(ivdata)
  if shininess:
    setdata(player_id, "poke", "pokeshi{}, iv{}, cpokeshi{}".format(actualkey, actualkey, actualkey), "{}, {}, {}".format(pokedata, ivdata, cpokedata))
  else:
    setdata(player_id, "poke", "pokemon{}, iv{}, cpokemon{}".format(actualkey, actualkey, actualkey), "{}, {}, {}".format(pokedata, ivdata, cpokedata))
  """
  if updateiv: #Real catch
    datas[13+3*int(shininess)][dex_number] += 1
    datas[12] += 1"""

def getboxtext(box:list, page:int, sort:int, language:int):
  if sort == 0:
    box.sort(key=lambda row: (row[0]))
  elif sort == 1:
    box.sort(key=lambda row: (-row[3]))
  elif sort == 2:
    box.sort(key=lambda row: (row[3]))
  elif sort == 3:
    box.sort(key=lambda row: (-row[2], -row[3]))
  text = ""
  for i in range(page*20, min((page+1)*20, len(box))):
    text += "`{}` `{}` {} | {} {}\n".format(box[i][0], rarityname[box[i][3]], box[i][1], box[i][2],
                                              dex[box[i][0]-1][language].capitalize())
  return text

def getboxembed(name:str, color:int, language:int, max_pages:int, page:int, box:list, sort:int):
  text = getboxtext(box, page, sort, language)
  sortedby = ["Dex order", "Rarity descending", "Rarity ascending", "Rarity descending with shinies first"]
  embed = discord.Embed(title="{}'s box".format(name), colour=color, timestamp=datetime.utcnow())
  embed.set_footer(text="Dislate")
  embed.add_field(name="Page {}/{} ({})".format(page+1, max_pages, sortedby[sort]), value=text, inline=True)
  return embed

def team_effect(number:int, in_team:list):
  """
  :param number: The dex number of the Pokémon minus 1
  :param in_team: The list of boolean indicating whether the player is in teams
  :return: The number of boosts
  """
  boost:float = 0
  for i in range(len(in_team)):
    if in_team[i]:
      pokemon_types = types[number]
      if i==1: #Team Rocket
        boost = 4 in pokemon_types or number in [149, 150] #Boost si le Pokémon est de type poison
      if i==2: #Team Aqua
        boost += 10 in pokemon_types #Boost si le Pokémon est de type eau
      if i==3:
        boost += 9 in pokemon_types or 4 in pokemon_types #Boost si le Pokémon est de type feu ou sol
      if i==4:
        boost += 13 in pokemon_types or 16 in pokemon_types or number in [482, 483, 486] #Boost si le Pokémon est de type psy ou ténébres
      if i==5:
        boost += number in [642, 643, 646] #Boost en relâchant des Pokémon
      if i==6:
        boost += 9 in pokemon_types or number in [715, 716, 717] #Boost si le Pokémon est de type feu
      if i==7:
        boost += 6 in pokemon_types or 4 in pokemon_types #Boost si le Pokémon est de type insecte ou poison
      if i==8:
        boost += bool(getrarity(number+1) == 8 or number in [790, 791, 799])
      if i==9:
        boost += 1
      if i==10:
        boost += 16 in pokemon_types #Boost si le Pokémon est de type ténébres
      if i==11:
        boost += number in [887, 888, 889]
      if i==12:
        boost += 16 in pokemon_types or 9 in pokemon_types or 3 in pokemon_types or 17 in pokemon_types or 1 in pokemon_types #Boost si le Pokémon est de type Ténébres, Feu, Poison, Fée ou Combat
      if 12<i<18:
        boost += .5
  return boost

def update_contribution(player_id, achieved:str, pokemon_number:int=0, released:int=0):
  applied_team = getdata(player_id, "game", "teamapply")
  applied_team = applied_team[0]
  if achieved == "caught":
    print("HERE")
    pokemon_type = types[pokemon_number]
    print(pokemon_type)
    if applied_team == 1 and any(pokemon_type[i] in [3] for i in range(len(pokemon_type))): # Team Rocket
      setdata(player_id, "teams", "teamrocket", None, [1])
    elif applied_team == 2 and any(pokemon_type[i] in [10] for i in range(len(pokemon_type))): # Team Aqua
      setdata(player_id, "teams", "teamaqua", None, [1])
    elif applied_team == 3 and any(pokemon_type[i] in [4, 9] for i in range(len(pokemon_type))): # Team Magma
      setdata(player_id, "teams", "teammagma", None, [1])
    elif applied_team == 4 and any(pokemon_type[i] in [13, 16] for i in range(len(pokemon_type))): # Team Galaxie
      setdata(player_id, "teams", "teamgalaxie", None, [1])
    elif applied_team == 6 and any(pokemon_type[i] in [9] for i in range(len(pokemon_type))): # Team Flare
      setdata(player_id, "teams", "teamflare", None, [1])
    elif applied_team == 7 and any(pokemon_type[i] in [3, 6] for i in range(len(pokemon_type))): # Team Skull
      setdata(player_id, "teams", "teamskull", None, [1])
    elif applied_team == 10 and any(pokemon_type[i] in [16] for i in range(len(pokemon_type))): # Team Yell
      setdata(player_id, "teams", "teamyell", None, [1])
    elif applied_team == 12 and any(pokemon_type[i] in [1, 3, 9, 16, 17] for i in range(len(pokemon_type))): # Team Star
      setdata(player_id, "teams", "teamstar", None, [1])
    return
  if achieved == "released":
    setdata(player_id, "teams", "teamplasma", None, [released])

def getrarity(dex_number):
  if dex_number in commonpool:
    return 0
  if dex_number in uncommonpool:
    return 1
  if dex_number in rarepool:
    return 2
  if dex_number in rarerpool:
    return 3
  if dex_number in veryrarepool:
    return 4
  if dex_number in pseudolegendarypool:
    return 5
  if dex_number in legendarypool:
    return 6
  if dex_number in mythicalpool:
    return 7
  if dex_number in ultrabeastpool:
    return 8
  if dex_number in god:
    return 9
  if dex_number in egg:
    return 10
  return 11