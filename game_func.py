from datetime import datetime
import discord
import sqlite3
from game_data import *

def init_data():
  data = sqlite3.connect('data.db')
  cursor = data.cursor()
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS players(
       id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
       name TEXT,
       age INTERGER
  )
  """)
  data.commit()
  data.close()
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
      db[data] = newdatas

def setlanguage(id):
  keys = db.prefix("option")
  if "option"+str(id) in keys:
    return db["option"+str(id)][3]
  else:
    return 0

def setoption(id):
  keys = db.prefix("option")
  if "option"+str(id) in keys:
    return db["option"+str(id)]
  else:
    db["option"+str(id)] = defaultoption
    return defaultoption

def setdata(id, name, create = False):
  keys = db.prefix("player_data")
  id = str(id)
  if "player_data"+id in keys:
    for i in range(len(database)):
      if id == database[i][0]:
        return database[i][1]
    datas = db["player_data"+id]
    database.append([id, datas])
    return database[-1][1]
  else:
    if create:
      datas = [str(name), 2, [False for _ in range(len(dex))], [0 for _ in range(len(dex))], [0 for _ in range(len(dex))], [False for _ in range(len(dex))], [None, None, None, None, None, None], [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] for _ in range(len(dex))], 2, 1000, [20, 10, 5]+[0 for _ in range(997)], 0, 0, [0 for _ in range(len(dex))], 1000, False, [0 for _ in range(len(dex))], 0, [1, 1, 1], [None, None], [], [False, 0, 0], [0, 0, 0], [0 for _ in range(15)], 0    ]
      db["player_data"+id] = datas
      return datas

def additems(item, amount, id, name):
  try:
    item = int(item) -1
    if item < len(buyableitems) and amount > 0:
      datas = setdata(id, name)
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
    return False, False, 51

def getdex(list_name, found_types, stats, sprite, language, options, number, id, name, shiny):
  datas = setdata(id, name)
  if number is None:
    embed = discord.Embed(title = "Pokédex", description = list_name[language].capitalize(), colour = [0xA8A878, 0xC03028, 0xA890F0, 0xA040A0, 0xE0C068, 0xB8A038, 0xA8B820, 0x705898, 0xB8B8D0, 0xF08030, 0x6890F0, 0x78C850, 0xF8D030, 0xF85888, 0x98D8D8, 0x7038F8, 0x705848, 0xEE99AC][types[0]], timestamp = datetime.utcnow())
  else:
    embed = discord.Embed(title = "Pokédex", description = list_name[language].capitalize()+" #"+str(int(number)+1)+" "+rarityname[getrarity(number+1)], colour = [0xA8A878, 0xC03028, 0xA890F0, 0xA040A0, 0xE0C068, 0xB8A038, 0xA8B820, 0x705898, 0xB8B8D0, 0xF08030, 0x6890F0, 0x78C850, 0xF8D030, 0xF85888, 0x98D8D8, 0x7038F8, 0x705848, 0xEE99AC][found_types[0]], timestamp = datetime.utcnow())
  embed.set_footer(text = "SHAdOw")
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
  if options[0]: #View other languages.
    embed.add_field(name = ["`Name in other languages`", "`Noms dans d'autres langues`", "`Namen in anderen Sprachen`", "`用其他語言命名`", "`다른 언어로 된 이름`", "`Hoka no gengo no namae`", "`他の言語の名前`"][language], value = ["English", "Anglais", "Englische Sprache", "英文", "영어", "Eigo", "英語"][language]+" : "+list_name[0].capitalize()+"\n"+["French", "Français", "Französisch Sprache", "法文", "프랑스 국민", "Furansugo", "フランス語"][language]+" : "+list_name[1].capitalize()+"\n"+["Japanese", "Japonais", "Japanisch Sprache", "日文", "일본어", "Hifumi", "日本語"][language]+" : "+list_name[6]+" / "+list_name[5].capitalize()+"\n"+["Chinese", "Chinois", "Chinesische Sprache", "中文", "중국어", "Chūgokugo", "中国語"][language]+" : "+list_name[3]+"\n"+["German", "Allemand", "Deutsche Sprache", "德國的語言", "독일어", "Doitsugo", "ドイツ語"][language]+" : "+list_name[2].capitalize()+"\n"+["Korean", "Coréen", "Koreanische Sprache", "朝鮮語", "한국어", "Kankoku-go", "韓国語"][language]+" : "+list_name[4], inline = False)
  if options[5]: #View links
    embed.add_field(name = ["`Link`", "`Lien`", "`Link`", "`網站`", "`사이트 링크`", "`Saito rinku`", "`サイトリンク`"][language], value = ["https://bulbapedia.bulbagarden.net/wiki/"+list_name[language]+"_(Pok%C3%A9mon)", "https://www.pokepedia.fr/"+list_name[language], "https://www.pokewiki.de/"+list_name[language], "https://wiki.52poke.com/wiki/"+list_name[language], "https://pokemonkorea.co.kr/pokedex", "https://wiki.xn--rckteqa2e.com/wiki/"+list_name[language], "https://wiki.xn--rckteqa2e.com/wiki/"+list_name[language]][language], inline = True)
  if options[6]: #View game stats
    embed.add_field(name = ["`Caught`", "`Capturé`", "`Erfassung`", "`捕獲`", "`포착`", "`Kyapuchā`", "`キャプチャー`"][language], value = datas[13+3*int(shiny)][number], inline = True)
    embed.add_field(name = ["`Inbox`", "`Dans la boîte`", "`Erfassung`", "`捕獲`", "`포착`", "`Kyapuchā`", "`キャプチャー`"][language], value = datas[7][number][int(shiny)], inline = True)
    embed.add_field(name = ["`IVs (Hp/Atk/Def/Spa/Spd/Spe)`", "`IVs (Pv/Att/Def/ASp/DSp/Vit)`", "`IVs (Kra/Ang/Ver/SpA/SpV/Ini)`", "`IVs (Hp/攻击/防御/特攻/特防/速度)`", "`IVs (Hp/공격/방어/특수공격/특수방어/스피드)`", "`IVs (Kō geki/Bōgyo/Toku kō/Toku bō/Subaya-sa)`", "`IVs (Hp/こうげき/ぼうぎょ/とくこう/とくぼう/すばやさ)`"][language], value = "{}/{}/{}/{}/{}/{}".format(datas[7][number][2], datas[7][number][3], datas[7][number][4], datas[7][number][5], datas[7][number][6], datas[7][number][7]), inline = True)
  return embed

def add_pokemon(player_id, dex_number, datas, shiny, updateiv = False):
  iv = [randint(0,31) for i in range(6)]
  if sum(iv) > datas[7][dex_number][2]+datas[7][dex_number][3]+datas[7][dex_number][4]+datas[7][dex_number][5]+datas[7][dex_number][6]+datas[7][dex_number][7] and updateiv:
    for i in range(6):
      datas[7][dex_number][i+2] = iv[i]
  datas[7][dex_number][int(shiny)] += 1
  if updateiv: #Real catch
    datas[13+3*int(shiny)][dex_number] += 1
    datas[12] += 1
  return datas

def getrarity(number):
  if number in commonpool:
    return 0
  if number in uncommonpool:
    return 1
  if number in rarepool:
    return 2
  if number in rarerpool:
    return 3
  if number in veryrarepool:
    return 4
  if number in pseudolegendarypool:
    return 5
  if number in legendarypool:
    return 6
  if number in mythicalpool:
    return 7
  if number in ultrabeastpool:
    return 8
  if number in god:
    return 9
  if number in egg:
    return 10
  return 11