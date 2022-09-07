import Items
import Clases
from Clases import Item, Skill, Sword, Staff
from Items import item, iceButcher, sb, forestStaff, bloodBow, fireBook
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


db = sqlite3.connect('databases/profile.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS profiles (
    login TEXT,
    clan TEXT,
    class TEXT,
    money INT,
    xp INT
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


def profileTest(author):
    sql.execute("SELECT * FROM profiles WHERE login = '"+ str(author) + "'")
    try:
        prof = sql.fetchone()
        if prof[0] != "":
            return 1
    except:
        return 0



def moneyTest(author, money):
    if profileTest(author) == 1:
        sql.execute("SELECT money FROM profiles WHERE login = '"+ str(author) + "'")
        prof = sql.fetchone()
        if(prof[0] > money):
            return 1
    return 0


def moneyPay(author, money):
    sql.execute("SELECT money FROM profiles WHERE login = '"+ str(author) + "'")
    prof = sql.fetchone()
    moneys = prof[0] - money
    sql.execute("UPDATE profiles SET money = " + str(moneys) + " WHERE login = '"+ str(author) + "'")
    db.commit()



def clanTest(author):
    if profileTest(author) == 1:
        sql.execute("SELECT clan FROM profiles WHERE login = '"+ str(author) + "'")
        prof = sql.fetchone()
        if prof[0] != 'none':
            return 1
    return 0


item.get()

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
    moneyPay(ctx.author, -100000)
    await ctx.send("халявщік)))))))))")



@bot.command()
async def profile(ctx, *, arg = ""):
    #profile
    if arg == "":
        sql.execute(f"SELECT * FROM profiles WHERE login = '{ctx.author}'")
        try:
            prof = sql.fetchone()
            if prof[0] == f"{ctx.author}":
                emb = discord.Embed( title = 'Profile', colour = discord.Color.orange())
                emb.add_field(name = f'{ctx.author}:', value = '\nclan: ' + prof[1] + '\nclass: ' + prof[2] + '\nmoney: ' + str(prof[3]) + " " + valute + 'level: ' + "тимчасово прибрано" + '\nxp: ' + str(prof[4]), inline = True)
                emb.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/910219499985330199/910596641868902471/8489841ce19d1edcf84237ae9c49ecdb.jpeg')
                await ctx.send(embed=emb)
        except:
            await ctx.send('у вас нет профиля')
        return
    #profile create
    if arg == 'create':
        sql.execute("SELECT * FROM profiles WHERE login = '{0.author}'".format(ctx))
        try:
            prof = sql.fetchone()
            if prof[0] == '{0.author}'.format(ctx):
                await ctx.channel.send('У вас уже есть профиль')
        except:
            sql.execute("INSERT INTO profiles VALUES ('{0.author}', 'none', 'none', 0, 0)".format(ctx))
            db.commit()
            await ctx.send('Профиль было создано')
            print("{0.author}: create a profile".format(ctx))
        return
    #other profile
    arg_list = list(arg)
    if arg_list[1] == '@':
        i = 2
        othU = 0
        while i < len(arg_list) - 1:
            othU *= 10
            othU += int(arg_list[i])
            i += 1
        try:
            user = await bot.fetch_user(othU)
            sql.execute(f"SELECT * FROM profiles WHERE login = '{user}'")
            prof = sql.fetchone()
            if prof[0] != "":
                emb = discord.Embed( title = 'Profile', colour = discord.Color.orange())
                emb.add_field(name = prof[0], value = '\nclan: ' + prof[1] + '\nclass: ' + prof[2] + '\nmoney: ' + str(prof[3]) + " " + valute + 'level: ' + "тимчасово прибрано" + '\nxp: ' + str(prof[4]), inline = True)
                emb.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/910219499985330199/910596641868902471/8489841ce19d1edcf84237ae9c49ecdb.jpeg')
                await ctx.send(embed=emb)
        except:
            await ctx.send('У этого пользователя нет профиля')
        return

@bot.command()
async def clan(ctx, param = "", *, name = ""):
    #clan - просмотреть профиль клана
    if param == "" or param == 'profile':
        if clanTest(ctx.author) == 1:
            sql.execute("SELECT clan FROM profiles WHERE login = '"+ str(ctx.author) + "'")
            prof = sql.fetchone()
            sql.execute("SELECT * FROM clans WHERE name = '"+ str(prof[0]) + "'")
            clan = sql.fetchone()

            emb = discord.Embed( title = 'Clan', colour = discord.Color.orange())
            emb.add_field(name = clan[0] + ':', value = "уровень: тимчасово прибрано \nопыт: " + str(clan[3]) + "\nадмин клана: " + clan[2], inline = True )
            emb.set_thumbnail(url = clan[1])
            await ctx.send(embed=emb)
            return
        else:
            await ctx.send('У вас нет клана:(')
        return

    #clan create - создать клан
    if param == 'create':
        if name == "":
            await ctx.send('Имя клана не может быть пустым!')
        else:
            if profileTest(ctx.author) == 1:
                if moneyTest(ctx.author, 1000) == 0:
                    await ctx.send('Чтобы создать клан нужно 1000 ' + valute)
                    return
                if clanTest(ctx.author) == 1:
                    await ctx.send('Вы уже находитесь в клане\nЧтоб покинуть клан, введите ' + prefix + ' clan leave')
                    return

                sql.execute("UPDATE profiles SET clan = '" + str(name) + "' WHERE login = '"+ str(ctx.author) + "'")
                sql.execute("INSERT INTO clans VALUES ('" + str(name) + "', 'https://cdn.discordapp.com/attachments/910219499985330199/910596641868902471/8489841ce19d1edcf84237ae9c49ecdb.jpeg', '{0.author}', 0)".format(ctx))
                db.commit()
                await ctx.send('Клан успешно создан!')
                return
            else:
                await ctx.send('У вас нет профиля:(')
                return
    #clan join - присоеденится в клан
    if param == 'join':
        if profileTest(ctx.author) == 0:
            await ctx.send("У вас нет профиля:(")
            return
        if clanTest(ctx.author) == 1:
            await ctx.send("Вы уже находитесь в клане!")
            return
        for invs in sql.execute(f"SELECT * FROM claninv WHERE name = '{name}'"):
            if invs[1] == str(ctx.author):
                if invs[2] == 1:
                    sql.execute(f"UPDATE profiles SET clan = '{name}' WHERE login = '{ctx.author}'")
                    sql.execute(f"DELETE FROM claninv WHERE invuser = '{ctx.author}'")
                    db.commit()
                    await ctx.send("Вы вступили в клан!")
                    return
                else:
                    await ctx.send("Вы уже отправили заявку на вступление!")
                    return
        sql.execute(f"INSERT INTO claninv VALUES ('{name}', '{ctx.author}', 0, 1)")
        db.commit()
        await ctx.send("Вы отправили заявку на вступление!\nДля принятия, админ клана должен написать ***" + prefix + "clan invite <имя_пользователя>***")
        return
    #clan invite - пригласить пользователя в клан
    if param == 'invite':
        arg_list = list(name)
        if arg_list[1] == '@':
            i = 2
            othU = 0
            while i < len(arg_list) - 1:
                othU *= 10
                othU += int(arg_list[i])
                i += 1
        try:
            user = await bot.fetch_user(othU)
            sql.execute(f"SELECT * FROM profiles WHERE login = '{user}'")
            prof = sql.fetchone()
            if not prof:
                await ctx.send('У этого пользователя нет профиля')
                return
        except:
            await ctx.send('У этого пользователя нет профиля')
            return



        sql.execute(f"SELECT name FROM clans WHERE admin = '{ctx.author}'")
        clan = sql.fetchone()
        if clan:
            if clanTest(str(user)):
                await ctx.send("Этот пользователь уже в клане!")
                return
            for invs in sql.execute(f"SELECT * FROM claninv WHERE name = '{clan[0]}'"):
                if invs[1] == str(user):
                    if invs[3] == 1:
                        sql.execute(f"UPDATE profiles SET clan = '{clan[0]}' WHERE login = '{user}'")
                        sql.execute(f"DELETE FROM claninv WHERE invuser = '{user}'")
                        db.commit()
                        await ctx.send("Пользователь вступил в ваш клан!")
                        return
                    else:
                        await ctx.send("Вы уже пригласили этого пользователя!")
                        return

            sql.execute(f"INSERT INTO claninv VALUES ('{clan[0]}', '{user}', 1, 0)")
            db.commit()
            await ctx.send("Пользователь приглашён в клан!\nЧтобы принять заявку, он должен написать ***" + prefix + "clan join <имя_клана>***")
        else:
            await ctx.send("У вас нету клана, или вы не являетесь его админом!")
        return

    #clan leave - выйти из клана
    if param == 'leave':
        if clanTest(ctx.author) == 1:
            sql.execute(f"SELECT name FROM clans WHERE admin = '{ctx.author}'")
            clan = sql.fetchone()
            if clan:
                pass
            else:
                sql.execute(f"UPDATE profiles SET clan = 'none' WHERE login = '{ctx.author}'")
                db.commit()
                await ctx.send("Вы покинули клан!")
        else:
            await ctx.send("Вы не находитесь в клане")
    #clan delete - удалить клан



@bot.command()
async def getmyid2(ctx):
    await ctx.send(discord.utils.get(ctx.guild.members, name='{Оплот 229}').id)
    
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
            
#        if message.content.startswith(";;play"):
#            await message.channel.send('''♫ ɴᴏᴡ ᴘʟᴀʏɪɴɢ: Gay porn
#            ───────────⚪──────────────────────────────────
#            ◄◄⠀▐▐ ⠀►►⠀⠀　　⠀ ₁:₃₂ / ₃:₃₂　　　　🔇 ───○ 🔊⠀　　　ᴴᴰ ⚙ ❐''')
#            return

#        if message.content.startswith("Db! rate ?"):
#            emb = discord.Embed( title = 'Оцініть бота', colour = discord.Color.orange())
#            emb.add_field(name = 'Db! rate *<1-10> <reason>*', value = 'ваш відгук буде надіслано автору')
#            await message.channel.send(embed=emb)
#            return

#        if message.content.startswith("Db! rate 10"):
#            rates = open('rate/rate.txt', 'a')
#            rates.write("{0.author}: {0.content}\n".format(message))
#            rates.close()
#            emb = discord.Embed( title = 'Дякую за відгук!', colour = discord.Color.orange())
#            emb.add_field(name = 'ваш відгук надіслано автору', value = 'ми зробимо все можливе для найкращого користування!')
#            await message.channel.send(embed=emb)
#            await message.channel.send("https://cdn.discordapp.com/attachments/753910983637991505/956981595615690782/anime-hug-84.png")
#            return

#        if message.content.startswith("Db! rate 1"):
#            rates = open('rate/rate.txt', 'a')
#            rates.write("{0.author}: {0.content}\n".format(message))
#            rates.close()
#            emb = discord.Embed( title = 'Дякую за відгук!', colour = discord.Color.orange())
#            emb.add_field(name = 'Вам послання від автора:', value = 'ТИ ЩО АХУЇВ?')
#            await message.channel.send(embed=emb)
#            return

#        if message.content.startswith("Db! rate "):
#            rates = open('rate/rate.txt', 'a')
#            rates.write("{0.author}: {0.content}\n".format(message))
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
#        if message.content.startswith("хто саня?"):
#            emb = discord.Embed( title = 'Гей їбаний', colour = discord.Color.orange())
#            await message.channel.send(embed=emb)
#            return
#        if message.content.startswith("хто тоха?"):
#            emb = discord.Embed( title = 'Топ чел лутший разраб в світі', colour = discord.Color.orange())
#            await message.channel.send(embed=emb)
#            return



bot.run(TOKEN)
