import Clases
from Clases import Chest
import os
import sqlite3
import discord
from discord.ext import commands
from discord import utils
from colorama import init
from colorama import Fore, Back, Style



init()

#загрузка токена префікса і тд
print("Loading settings/bot.conf")

config = open("settings/bot.txt", "r")
lprefix = list(config.readline())
valute = config.readline()
TOKEN = config.readline()
config.close()

prefix = ""
i = 0
while lprefix[i] != "\n":
    prefix += str(lprefix[i])
    i += 1

#загрузка налаштувань гри

print("Loading settings/dungeons.conf")
config = open("settings/dungeons.txt", "r")
skyCastle = int(config.readline())
mushroomValley = int(config.readline())
snowyMountans = int(config.readline())
underwaterTemple= int(config.readline())
xz = int(config.readline())
config.close()

if skyCastle + mushroomValley + snowyMountans + underwaterTemple + xz != 100:
    print(Fore.RED)
    print("\n\nCHANCES ERROR! The sum of the odds must be 100\n\n")
    exit(0)


#підготовка бази данних


print("Loading DataBases")

db = sqlite3.connect('databases/profile.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS profiles (
    id TEXT,
    clan TEXT,
    class TEXT,
    money INT,
    xp INT,
    party TEXT
)""")
sql.execute("""CREATE TABLE IF NOT EXISTS clans (
    name TEXT,
    ava TEXT,
    admin TEXT,
    xp INT
)""")
sql.execute("""CREATE TABLE IF NOT EXISTS claninv (
    name TEXT,
    invuser TEXT,
    admin BOOL,
    user BOOL
)""")

db.commit()





partiesDB = sqlite3.connect('databases/parties.db')
pdb = partiesDB.cursor()

pdb.execute("""CREATE TABLE IF NOT EXISTS parties (
    type TEXT,
    admin TEXT,
    user1 TEXT,
    user2 TEXT,
    user3 TEXT,
    user4 TEXT
)""")

pdb.execute("""CREATE TABLE IF NOT EXISTS inventory (
    name TEXT,
    shield TEXT,
    weapon TEXT,
    ring TEXT,
    slot1 TEXT,
    slot2 TEXT,
    slot3 TEXT
)""")

partiesDB.commit()


def profileTest(author):
    sql.execute("SELECT * FROM profiles WHERE id = '"+ str(author) + "'")
    try:
        prof = sql.fetchone()
        if prof[0] != "":
            return 1
    except:
        return 0



def moneyTest(author, money):
    if profileTest(author) == 1:
        sql.execute("SELECT money FROM profiles WHERE id = '"+ str(author) + "'")
        prof = sql.fetchone()
        if(prof[0] > money):
            return 1
    return 0


def moneyPay(author, money):
    sql.execute("SELECT money FROM profiles WHERE id = '"+ str(author) + "'")
    prof = sql.fetchone()
    moneys = prof[0] - money
    sql.execute("UPDATE profiles SET money = " + str(moneys) + " WHERE id = '"+ str(author) + "'")
    db.commit()



def clanTest(author):
    if profileTest(author) == 1:
        sql.execute("SELECT clan FROM profiles WHERE id = '"+ str(author) + "'")
        prof = sql.fetchone()
        if prof[0] != 'none':
            return 1
    return 0



#А ось і сам бот
bot = commands.Bot(command_prefix='Db!')

    
@bot.event
async def on_ready():
    print(Fore.GREEN)
    print('Logged on as {0}!'.format(bot.user))
    print('prefix is: ' + prefix)
    print(Fore.WHITE)
    game = discord.Game("Захват Кубані!")
    await bot.change_presence(activity=game, status=discord.Status.online, afk=False)

@bot.event
async def on_user_update(before, after):
    channel = await bot.fetch_channel(910219789908180992)
    await channel.send(before.name)
    await channel.send(after.name)
    return

@bot.command()
async def getmyid(ctx):
    await ctx.send(ctx.author.id)

@bot.command()
async def FREE_MONEY(ctx):
    moneyPay(ctx.author.id, -100000)
    await ctx.send("халявщік)))))))))")



@bot.group(invoke_without_command=True)
async def profile(ctx, *, otherUser=''):
    #other profile
    if len(otherUser) > 2:
        arg_list = list(otherUser)
        if arg_list[1] == '@':
            i = 2
            othU = 0
            while i < len(arg_list) - 1:
                othU *= 10
                othU += int(arg_list[i])
                i += 1
            try:
                user = await bot.fetch_user(othU)
                sql.execute(f"SELECT * FROM profiles WHERE id = '{othU}'")
                prof = sql.fetchone()
                if prof[0] != "":
                    emb = discord.Embed( title = 'Profile', colour = discord.Color.orange())
                    emb.add_field(name = user.name, value = '\nclan: ' + prof[1] + '\nclass: ' + prof[2] + '\nmoney: ' + str(prof[3]) + " " + valute + 'level: ' + "тимчасово прибрано" + '\nxp: ' + str(prof[4]), inline = True)
                    emb.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/910219499985330199/910596641868902471/8489841ce19d1edcf84237ae9c49ecdb.jpeg')
                    await ctx.send(embed=emb)
            except:
                await ctx.send('У цього користувача немає профілю')
            return
    #profile
    sql.execute(f"SELECT * FROM profiles WHERE id = '{ctx.author.id}'")
    try:
        prof = sql.fetchone()
        if prof[0] == f"{ctx.author.id}":
            emb = discord.Embed( title = 'Profile', colour = discord.Color.orange())
            emb.add_field(name = f'{ctx.author}:', value = '\nclan: ' + prof[1] + '\nclass: ' + prof[2] + '\nmoney: ' + str(prof[3]) + " " + valute + 'level: ' + "тимчасово прибрано" + '\nxp: ' + str(prof[4]), inline = True)
            emb.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/910219499985330199/910596641868902471/8489841ce19d1edcf84237ae9c49ecdb.jpeg')
            await ctx.send(embed=emb)
    except:
        await ctx.send('У вас немає профіля')
    return
    #profile create
@profile.command()
async def create(ctx):
    sql.execute("SELECT * FROM profiles WHERE id = '{0.author.id}'".format(ctx))
    try:
        prof = sql.fetchone()
        if prof[0] == '{0.author.id}'.format(ctx):
            await ctx.channel.send('У вас вже є профіль')
    except:
        sql.execute("INSERT INTO profiles VALUES ('{0.author.id}', 'none', 'none', 0, 0, '')".format(ctx))
        db.commit()
        await ctx.send('Профіль створено')
        print("{0.author.id} {0.author}: create a profile".format(ctx))
    return
    


@bot.group(invoke_without_command=True)
async def clan(ctx):
    #clan - переглянути профіль клану
    if clanTest(ctx.author.id) == 1:
        sql.execute("SELECT clan FROM profiles WHERE id = '"+ str(ctx.author.id) + "'")
        prof = sql.fetchone()
        sql.execute("SELECT * FROM clans WHERE name = '"+ str(prof[0]) + "'")
        clan = sql.fetchone()

        emb = discord.Embed( title = 'Clan', colour = discord.Color.orange())
        emb.add_field(name = clan[0] + ':', value = "Рівень: тимчасово прибрано \nопыт: " + str(clan[3]) + "\nАдмін клану: " + str(await bot.fetch_user(clan[2])), inline = True )
        emb.set_thumbnail(url = clan[1])
        await ctx.send(embed=emb)
        return
    else:
        await ctx.send('У вас немає клану:(')
    return



@clan.command()
async def profile(ctx):
    await clan(ctx)

#clan create - створити клан
@clan.command()
async def create(ctx, *, name = ""):
    if name == "":
        await ctx.send('Імя клану не може бути пустим')
    else:
        if profileTest(ctx.author.id) == 1:
            if moneyTest(ctx.author.id, 1000) == 0:
                await ctx.send('Щоб створити клан потрібно 1000 ' + valute)
                return

            if clanTest(ctx.author.id) == 1:
                await ctx.send('Ви вже вступили в клан\nщоб вийти з нього введіть ' + prefix + ' clan leave')
                return

            sql.execute("SELECT name FROM clans WHERE name = '" + name + "'")
            namePlaced = sql.fetchone()
            if namePlaced:
                await ctx.send('Такий клан вже існує!')
                return

            moneyPay(ctx.author.id, 1000)
            sql.execute("UPDATE profiles SET clan = '" + str(name) + "' WHERE id = '"+ str(ctx.author.id) + "'")
            sql.execute("INSERT INTO clans VALUES ('" + str(name) + "', 'https://cdn.discordapp.com/attachments/910219499985330199/910596641868902471/8489841ce19d1edcf84237ae9c49ecdb.jpeg', '{0.author.id}', 0)".format(ctx))
            db.commit()
            await ctx.send('Клан успішно створено!')
            return
        else:
            await ctx.send('У вас немає профілю:(')
            return
        
        

#clan join - приєднатися в клан
@clan.command()
async def join(ctx, *, name = ""):
    if profileTest(ctx.author.id) == 0:
        await ctx.send('У вас немає профілю:(')
        return
    if clanTest(ctx.author.id) == 1:
        await ctx.send("Ви вже вступили в клан\nщоб вийти з нього введіть ' + prefix + ' clan leave")
        return
    sql.execute(f"SELECT * FROM clans WHERE name = '{name}'")
    if not sql.fetchone():
        await ctx.send("Такий клан не існує")
        return
    for invs in sql.execute(f"SELECT * FROM claninv WHERE name = '{name}'"):
        if invs[1] == str(ctx.author.id):
            if invs[2] == 1:
                sql.execute(f"UPDATE profiles SET clan = '{name}' WHERE id = '{ctx.author.id}'")
                sql.execute(f"DELETE FROM claninv WHERE invuser = '{ctx.author.id}'")
                db.commit()
                await ctx.send("Ви приєдналися до клану!")
                return
            else:
                await ctx.send("Ви вже відправили заявку на вступ!")
                return
    sql.execute(f"INSERT INTO claninv VALUES ('{name}', '{ctx.author.id}', 0, 1)")
    db.commit()
    await ctx.send("Ви відправили заявку на вступ!\nДля прийняття, адмін клана повинен написати ***" + prefix + "clan invite <имя_пользователя>***")
    return



#clan invite - пригласить пользователя в клан
@clan.command()
async def invite(ctx, *, user = ""):
    if len(user) > 2:
        arg_list = list(user)
        if arg_list[1] == '@':
            i = 2
            othU = 0
            while i < len(arg_list) - 1:
                othU *= 10
                othU += int(arg_list[i])
                i += 1
        try:
            sql.execute(f"SELECT * FROM profiles WHERE id = '{othU}'")
            prof = sql.fetchone()
            if not prof:
                await ctx.send('У цього користувача немає профілю')
                return
        except:
            await ctx.send('У цього користувача немає профілю')
            return


        sql.execute(f"SELECT name FROM clans WHERE admin = '{ctx.author.id}'")
        clan = sql.fetchone()
        if clan:
            if clanTest(str(othU)):
                await ctx.send("Цей користувач уже в клані!")
                return
            for invs in sql.execute(f"SELECT * FROM claninv WHERE name = '{clan[0]}'"):
                if invs[1] == str(othU):
                    if invs[3] == 1:
                        sql.execute(f"UPDATE profiles SET clan = '{clan[0]}' WHERE id = '{othU}'")
                        sql.execute(f"DELETE FROM claninv WHERE invuser = '{othU}'")
                        db.commit()
                        await ctx.send("Користувач вступив у ваш клан!")
                        return
                    else:
                        await ctx.send("Ви вже запросили цього користувача!")
                        return

            sql.execute(f"INSERT INTO claninv VALUES ('{clan[0]}', '{othU}', 1, 0)")
            db.commit()
            await ctx.send("Користувача запрошено в клан!\nДля прийняття запрошення він повинен написати ***" + prefix + "clan join <имя_клана>***")
        else:
            await ctx.send("У вас неає клану, або ви не є його адміном!")
        return



#clan leave - выйти из клана
@clan.command()
async def leave(ctx):
        if clanTest(ctx.author.id) == 1:
            sql.execute(f"SELECT name FROM clans WHERE admin = '{ctx.author.id}'")
            clan = sql.fetchone()
            if clan:
                pass
            else:
                sql.execute(f"UPDATE profiles SET clan = 'none' WHERE id = '{ctx.author.id}'")
                db.commit()
                await ctx.send("Ви вийшли з клану!")
        else:
            await ctx.send("Ви не знаходитесь в клані")
#clan delete - удалить клан
#@clan.command()
#async def delete(ctx):
#    sql.execute(f"DELETE FROM clans WHERE admin = '{ctx.author.id}'")
#    sql.execute(f"UPDATE profiles SET clan = 'none' WHERE id = '{ctx.author.id}'")
#    db.commit()

@bot.group(invoke_without_command=True)
async def ah(ctx):
    await ctx.send("oh");

@ah.command()
async def ahaha(ctx):
    await ctx.send("ahahhahahahhah");



    #parties (
    #type TEXT,
    #admin TEXT,
    #user1 TEXT,
    #user2 TEXT,
    #user3 TEXT,
    #user4 TEXT


 #   inventory (
 #   name TEXT,
 #   shield TEXT,
 #   weapon TEXT,
 #   ring TEXT,
 #   slot1 TEXT,
 #   slot2 TEXT,
 #   slot3 TEXT

@bot.group(invoke_without_command=True)
async def party(ctx):
    pass

@party.command()
async def start(ctx, difficulty='1'):
    pass



@party.command()
async def public(ctx):
    sql.execute("UPDATE profiles SET party = '" + str(ctx.author.id) + "' WHERE id = '" + str(ctx.author.id) + "'")
    db.commit()
    pdb.execute("INSERT INTO parties VALUES ('public', '" + str(ctx.author.id) + "', '', '', '', '')")
    partiesDB.commit()

@party.command()
async def clan(ctx):
    pass

@party.command()
async def private(ctx):
    pass



@party.command()
async def leave(ctx):
    pass

@party.command()
async def kick(ctx, user='', *, reason=''):
    pass

@party.command()
async def delete(ctx):
    pass








@bot.command()
async def chest(ctx, mimikChance = 25):
    chest = Chest(False, mimikChance)
    await ctx.send(embed = chest.Loot())









#bot.remove_command(help)

#@bot.command()
#async def help(ctx, param = ""):
#    emb = discord.Embed( title = 'Help', colour = discord.Color.orange())

#    emb.add_field(name = 'profile', value = 'profile create - регистрация\nprofile - просмотреть профиль\nprofile delete - удалить профиль', inline = True)
#    emb.add_field(name = 'clan', value = 'clan - просмотреть профиль клана\nclan create - создать клан\nclan delete - удалить клан\nclan join - присоеденится в клан\nclan invite - пригласить пользователя в клан', inline = True)
#    emb.add_field(name = 'team', value = 'team - просмотреть список учасников команды\nteam create - создать команду\nteam delete - удалить команду\nteam join - присоеденится в команду\nteam kick - исключить члена команды', inline = False)
#    await message.channel.send(embed=emb)
#    return

















#@bot.event
#async def on_message(message): 

#    if message.author != bot.user:
#        #if message.content.startswith("Db! Профіль"):
#        #    await message.channel.send('ДАЛБАЙОБ?????????')
#        #    return

#        if message.content.startswith("Db! rate ?"):
#            emb = discord.Embed( title = 'Оцініть бота', colour = discord.Color.orange())
#            emb.add_field(name = 'Db! rate *<1-10> <reason>*', value = 'ваш відгук буде надіслано автору')
#            await message.channel.send(embed=emb)
#            return

#        if message.content.startswith("Db! rate 10"):
#            rates = open('rate/rate.txt', 'a')
#            rates.write("{0.author.id}: {0.content}\n".format(message))
#            rates.close()
#            emb = discord.Embed( title = 'Дякую за відгук!', colour = discord.Color.orange())
#            emb.add_field(name = 'ваш відгук надіслано автору', value = 'ми зробимо все можливе для найкращого користування!')
#            await message.channel.send(embed=emb)
#            await message.channel.send("https://cdn.discordapp.com/attachments/753910983637991505/956981595615690782/anime-hug-84.png")
#            return

#        if message.content.startswith("Db! rate 1"):
#            rates = open('rate/rate.txt', 'a')
#            rates.write("{0.author.id}: {0.content}\n".format(message))
#            rates.close()
#            emb = discord.Embed( title = 'Дякую за відгук!', colour = discord.Color.orange())
#            emb.add_field(name = 'Вам послання від автора:', value = 'ТИ ЩО КАБАН?')
#            await message.channel.send(embed=emb)
#            return

#        if message.content.startswith("Db! rate "):
#            rates = open('rate/rate.txt', 'a')
#            rates.write("{0.author.id}: {0.content}\n".format(message))
#            rates.close()
#            emb = discord.Embed( title = 'Дякую за відгук!', colour = discord.Color.orange())
#            emb.add_field(name = 'ваш відгук надіслано автору', value = 'ми зробимо все можливе для найкращого користування!')
#            await message.channel.send(embed=emb)
#            await message.channel.send("https://cdn.discordapp.com/attachments/753910983637991505/956981595615690782/anime-hug-84.png")
#            return

#        if message.content.startswith("Слава Україні!"):
#            emb = discord.Embed( title = 'Героям Слава!', colour = discord.Color.orange())
#            await message.channel.send(embed=emb)
#            return
#        if message.content.startswith("Слава Нації!"):
#            emb = discord.Embed( title = 'Смерть ворогам!', colour = discord.Color.orange())
#            await message.channel.send(embed=emb)
#            return
#        if message.content.startswith("Україна"):
#            emb = discord.Embed( title = 'Понад усе!', colour = discord.Color.orange())
#            await message.channel.send(embed=emb)
#            return
#        if message.content.startswith("Путін"):
#            emb = discord.Embed( title = 'Хуйло!!! ЛАЛАЛЛАЛЛАЛАЛАЛЛАЛАЛЛАЛАЛЛАЛАЛЛАЛЛАЛЛАЛЛААЛАЛАЛЛАЛАЛЛАЛЛАЛЛААЛАЛАЛЛАЛЛАЛ!', colour = discord.Color.orange())
#            await message.channel.send(embed=emb)
#            return
#        if message.content.startswith("путін"):
#            emb = discord.Embed( title = 'Хуйло!!! ЛАЛАЛЛАЛЛАЛАЛАЛЛАЛАЛЛАЛАЛЛАЛАЛЛАЛЛАЛЛАЛЛААЛАЛАЛЛАЛАЛЛАЛЛАЛЛААЛАЛАЛЛАЛЛАЛ!', colour = discord.Color.orange())
#            await message.channel.send(embed=emb)
#            return
#        if message.content.startswith("хто тоха?"):
#            emb = discord.Embed( title = 'Топ чел лутший разраб в світі', colour = discord.Color.orange())
#            await message.channel.send(embed=emb)
#            return



bot.run(TOKEN)
