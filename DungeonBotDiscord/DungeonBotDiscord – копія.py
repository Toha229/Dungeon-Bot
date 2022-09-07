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

db.commit()

def addUserToClan(admin, user):
    clanfile = open("clans/" + clan + ".txt", "r")
    tmp = list(clanfile.readline())
    tmp = list(clanfile.readline())
    tmp = list(clanfile.readline())
    tmp = list(clanfile.readline())

item.get()

class MyClient(discord.Client):

    

    async def on_ready(self):
        print(Fore.GREEN)
        print('Logged on as {0}!'.format(self.user))
        print('prefix is: ' + prefix)
        print(Fore.WHITE)
        game = discord.Game("Захват Кубані!")
        await client.change_presence(activity=game, status=discord.Status.online, afk=False)


    async def on_message(self, message):

        if message.author != self.user:
            if message.content.startswith("Db! Профіль"):
                await message.channel.send('ДАЛБАЙОБ?????????')
                return
            
            if message.content.startswith(";;play"):
                await message.channel.send('''♫ ɴᴏᴡ ᴘʟᴀʏɪɴɢ: Gay porn
               ───────────⚪──────────────────────────────────
               ◄◄⠀▐▐ ⠀►►⠀⠀　　⠀ ₁:₃₂ / ₃:₃₂　　　　🔇 ───○ 🔊⠀　　　ᴴᴰ ⚙ ❐''')
                return

            if message.content.startswith("Db! rate ?"):
                emb = discord.Embed( title = 'Оцініть бота', colour = discord.Color.orange())
                emb.add_field(name = 'Db! rate *<1-10> <reason>*', value = 'ваш відгук буде надіслано автору')
                await message.channel.send(embed=emb)
                return

            if message.content.startswith("Db! rate 10"):
                rates = open('rate/rate.txt', 'a')
                rates.write("{0.author}: {0.content}\n".format(message))
                rates.close()
                emb = discord.Embed( title = 'Дякую за відгук!', colour = discord.Color.orange())
                emb.add_field(name = 'ваш відгук надіслано автору', value = 'ми зробимо все можливе для найкращого користування!')
                await message.channel.send(embed=emb)
                await message.channel.send("https://cdn.discordapp.com/attachments/753910983637991505/956981595615690782/anime-hug-84.png")
                return

            if message.content.startswith("Db! rate 1"):
                rates = open('rate/rate.txt', 'a')
                rates.write("{0.author}: {0.content}\n".format(message))
                rates.close()
                emb = discord.Embed( title = 'Дякую за відгук!', colour = discord.Color.orange())
                emb.add_field(name = 'Вам послання від автора:', value = 'ТИ ЩО АХУЇВ?')
                await message.channel.send(embed=emb)
                return

            if message.content.startswith("Db! rate "):
                rates = open('rate/rate.txt', 'a')
                rates.write("{0.author}: {0.content}\n".format(message))
                rates.close()
                emb = discord.Embed( title = 'Дякую за відгук!', colour = discord.Color.orange())
                emb.add_field(name = 'ваш відгук надіслано автору', value = 'ми зробимо все можливе для найкращого користування!')
                await message.channel.send(embed=emb)
                await message.channel.send("https://cdn.discordapp.com/attachments/753910983637991505/956981595615690782/anime-hug-84.png")
                return

            if message.content.startswith("Слава Україні!"):
                emb = discord.Embed( title = 'Героям Слава!', colour = discord.Color.orange())
                await message.channel.send(embed=emb)
                return
            if message.content.startswith("Слава Нації!"):
                emb = discord.Embed( title = 'Смерть ворогам!', colour = discord.Color.orange())
                await message.channel.send(embed=emb)
                return
            if message.content.startswith("Україна"):
                emb = discord.Embed( title = 'Понад усе!', colour = discord.Color.orange())
                await message.channel.send(embed=emb)
                return
            if message.content.startswith("Путін"):
                emb = discord.Embed( title = 'Хуйло!!! ЛАЛАЛЛАЛЛАЛАЛАЛЛАЛАЛЛАЛАЛЛАЛАЛЛАЛЛАЛЛАЛЛААЛАЛАЛЛАЛАЛЛАЛЛАЛЛААЛАЛАЛЛАЛЛАЛ!', colour = discord.Color.orange())
                await message.channel.send(embed=emb)
                return
            if message.content.startswith("путін"):
                emb = discord.Embed( title = 'Хуйло!!! ЛАЛАЛЛАЛЛАЛАЛАЛЛАЛАЛЛАЛАЛЛАЛАЛЛАЛЛАЛЛАЛЛААЛАЛАЛЛАЛАЛЛАЛЛАЛЛААЛАЛАЛЛАЛЛАЛ!', colour = discord.Color.orange())
                await message.channel.send(embed=emb)
                return
            if message.content.startswith("хто саня?"):
                emb = discord.Embed( title = 'Гей їбаний', colour = discord.Color.orange())
                await message.channel.send(embed=emb)
                return
            if message.content.startswith("хто тоха?"):
                emb = discord.Embed( title = 'Топ чел лутший разраб в світі', colour = discord.Color.orange())
                await message.channel.send(embed=emb)
                return

            if message.content.startswith(prefix + ' profile create'):
                
                sql.execute("SELECT * FROM profiles WHERE login = '{0.author}'".format(message))
                try:
                    prof = sql.fetchone()
                    if prof[0] == '{0.author}'.format(message):
                        await message.channel.send('У вас уже есть профиль')
                except:
                    sql.execute("INSERT INTO profiles VALUES ('{0.author}', 'none', 'none', 0, 0)".format(message))
                    db.commit()
                    await message.channel.send('Профиль было создано')
                    print("{0.author}: create a profile".format(message))
                return



            if message.content.startswith(prefix + " help"):
                emb = discord.Embed( title = 'Help', colour = discord.Color.orange())

                emb.add_field(name = 'profile', value = 'profile create - регистрация\nprofile - просмотреть профиль\nprofile delete - удалить профиль', inline = True)
                emb.add_field(name = 'clan', value = 'clan - просмотреть профиль клана\nclan create - создать клан\nclan delete - удалить клан\nclan join - присоеденится в клан', inline = True)
                emb.add_field(name = 'team', value = 'team - просмотреть список учасников команды\nteam create - создать команду\nteam delete - удалить команду\nteam join - присоеденится в команду\nteam kick - исключить члена команды', inline = False)
                await message.channel.send(embed=emb)
                return



            if message.content.startswith(prefix + " profile"):
                sql.execute("SELECT * FROM profiles WHERE login = '{0.author}'".format(message))
                try:
                    prof = sql.fetchone()
                    if prof[0] == "{0.author}".format(message):
                        emb = discord.Embed( title = 'Profile', colour = discord.Color.orange())
                        emb.add_field(name = '{0.author}:'.format(message), value = '\nclan: ' + prof[1] + '\nclass:' + prof[2] + '\nmoney: ' + str(prof[3]) + " " + valute + 'level: ' + "тимчасово прибрано" + '\nxp: ' + str(prof[4]), inline = True)
                        emb.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/910219499985330199/910596641868902471/8489841ce19d1edcf84237ae9c49ecdb.jpeg')
                        await message.channel.send(embed=emb)
                except:
                    await message.channel.send('у вас нет профиля')
                return



            if message.content.startswith(prefix + " clan create"):
                try:
                    user.readProfile('{0.author}'.format(message))
                except:
                    await message.channel.send('У вас нет профиля:(')
                    return
                if moneyTest(1000) == 0:
                    await message.channel.send('Чтобы создать клан нужно 1000 ' + valute)
                    return
                if clanTest() == 1:
                    await message.channel.send('Вы уже находитесь в клане\nЧтоб покинуть клан, введите ' + prefix + ' clan leave')
                    return
                moneyPay(1000)
                clanl = list("{0.content}".format(message))
                profileSetClan(clanl)
                writeProfile('{0.author}'.format(message))

                clan = open("clans/" + str(clan) + ".txt", "w")
                clan.write("0\n")
                clan.write("0\n")
                clan.write("https://cdn.discordapp.com/attachments/910219499985330199/910596641868902471/8489841ce19d1edcf84237ae9c49ecdb.jpeg \n")
                clan.write("{0.author}\n".format(message))
                clan.write("end")
                clan.close()

                await message.channel.send('клан создан')
                return



            #if message.content.startswith(prefix + " clan invite"):
            #    try:
            #        readProfile('{0.author}'.format(message))
            #        try:
            #            readClan(clan) 
            #            if(clanadmin != '{0.author}'.format(message)):
            #                await message.channel.send('Вы не являетесь администратором клана:(')
            #        except:
            #            await message.channel.send('У вас нет клана:(')
            #    except:
            #        await message.channel.send('У вас нет профиля:(')
            #    addUserToClan()
            #    return



            if message.content.startswith(prefix + " clan"):
                try:
                    user.readProfile('{0.author}'.format(message))
                    try:
                        readClan(clan) 
                        emb = discord.Embed( title = 'Clan', colour = discord.Color.orange())
                        emb.add_field(name = clan + ':', value = 'уровень: ' + str(clanlvl) + "\nопыт: " + str(clanxp) + "\nадмин клана: @" + clanadmin, inline = True )
                        emb.set_thumbnail(url = clanavatar)
                        await message.channel.send(embed=emb)
                    except:
                        await message.channel.send('У вас нет клана:(')
                except:
                    await message.channel.send('У вас нет профиля:(')
                return



            if message.content.startswith(prefix + " item2"):
                await message.channel.send(embed=iceButcher.get())
                return
            if message.content.startswith(prefix + " items"):
                await message.channel.send(embed=sb.get())
                await message.channel.send(embed=iceButcher.get())
                await message.channel.send(embed=fireBook.get())
                await message.channel.send(embed=bloodBow.get())
                await message.channel.send(embed=forestStaff.get())
                return
            if message.content.startswith(prefix + " item"):
                await message.channel.send(embed=sb.get())
                return
            
            if message.content.startswith(""):
                ms = list('{0.content}'.format(message))
                i = 0
                try:
                    while ms[i] != '\n':
                        if ms[i] == 'ы' or ms[i] == 'э' or ms[i] == 'ё' or ms[i] == 'ъ':
                            emb = discord.Embed( title = 'СЛАВА УКРАЇНІ!', colour = discord.Color.orange())
                            emb.add_field(name = 'Русский военный корабль иди нахуй!', value = 'Москалі підараси')
                            await message.channel.send(embed=emb)
                            return
                        i += 1
                except:
                    return
            else: 
                return



                
                


bot = MyClient(command_prefix='Db!')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

bot.run(TOKEN)


        #if deleteUser != "fff":
        #    if deleteUser == "{0.author}".format(message):
        #        if message.content.startswith(prefix + ' yes'):
        #            try:
        #                os.system("del 'profiles/{0.author}.txt'".format(message))
        #                print("{0.author}: deleted profile".format(message))
        #                await message.channel.send('Профиль удален')
        #            except:
        #                await message.channel.send('У вас нет профиля:(')
        #            deleteUser = "fff"
        #            return
        #        else: deleteUser = "fff"


            #if message.content.startswith(prefix + " profile delete"):
            #    deleteUser = "{0.author}".format(message)
            #    await message.channel.send('Вы уверены?\nнапишыте "db! yes" чтоб подтвердить операцию')
            #    return
