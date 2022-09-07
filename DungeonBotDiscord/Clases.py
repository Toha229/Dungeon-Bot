import os
import discord
from discord.ext import commands
from discord import utils
from colorama import init
from colorama import Fore, Back, Style

from random import seed
from random import randint



class Item:
    name = str;
    sellprice = int;
    weight = float;
    quantity = int;
    picture = str;
    description = str;


    def __init__(self, n, p, w, q, pict, desc):
        self.name = n
        self.sellprice = p
        self.weight = w
        self.quantity = q
        self.picture = pict
        self.description = desc
    
    def get(self):
        emb = discord.Embed( title = 'Item', colour = discord.Color.green())
        emb.add_field(name = str(self.name) + ' :', value = str(self.description) + "\nКількість: \t" + str(self.quantity) + "\nВага: \t" + str(self.weight) + "кг\nЦіна: \t" + str(self.sellprice), inline = True )
        emb.set_thumbnail(url = str(self.picture))
        #print(self.description)
        #emb = discord.Embed( title = 'Item', colour = discord.Color.green())
        #emb.add_field(name ='zxc :', value = "asd", inline = True )
        return emb

class Skill:
    name = str
    mana = int
    kd = int
    damage = int
    range = int
    radius = int
    preview = str
    
    def __init__(self, name, mana, kd, damage, range, radius, preview):
        self.name = name
        self.mana = mana
        self.kd = kd
        self.damage = damage
        self.range = range
        self.radius = radius
        self.preview = preview

    def atack(self):
        return

    def previewF(self):
        return (str(self.preview) + "\n" + ("\nНаносить шкоду: " + str(self.damage) if self.damage > 0 else "")
               + ("\nВідновлює HP: " + str(-self.damage) if self.damage < 0 else "")
               + ("\nВ радіусі: " + str(self.radius) if self.radius > 0 else "")
               + ("\nДальність: " + str(self.range) if self.range < 0 else ""))

    def show(self):
        return




class Weapon(Item):
    minDamage = int
    maxDamage = int
    criticalDamage = int
    critChance = int
    skill1 = Skill
    skill2 = Skill
    skill3 = Skill

    def __init__(self, n, p, w, q, pict, desc, min, max, crit, chance, s1 = Skill("",0,0,0,0,0,""), s2 = Skill("",0,0,0,0,0,""), s3 = Skill("",0,0,0,0,0,"")):
        self.name = n
        self.sellprice = p
        self.weight = w
        self.quantity = q
        self.picture = pict
        self.description = desc
        self.minDamage = min
        self.maxDamage = max
        self.criticalDamage = crit
        self.critChance = chance
        self.skill1 = s1
        self.skill2 = s2
        self.skill3 = s3

class Sword(Weapon):
    def get(self):
        emb = discord.Embed( title = 'Sword', colour = discord.Color.green())
        emb.add_field(name = str(self.name) + ' :', value = str(self.description)
                     + "\n\nШкода:   " + str(self.minDamage) + (" - " + str(self.maxDamage) if self.minDamage != self.maxDamage else "")
                     + "\nКрит:   " + str(self.criticalDamage) + "        Шанс крита:   " + str(self.critChance)
                     + "\nВага:     " + str(self.weight) + "кг\nЦіна: " + str(self.sellprice), inline = False )
        if self.skill1.name != "":
            emb.add_field(name = str(self.skill1.name) + ' :', value = str(self.skill1.previewF()), inline = True )
        if self.skill2.name != "":
            emb.add_field(name = str(self.skill2.name) + ' :', value = str(self.skill2.previewF()), inline = True )
        if self.skill3.name != "":
            emb.add_field(name = str(self.skill3.name) + ' :', value = str(self.skill3.previewF()), inline = True )

        emb.set_thumbnail(url = str(self.picture))
        return emb

class Staff(Weapon):
    rangeA = int

    def __init__(self, name, sellPrice, weight, quantity, picture, description, min, max, crit, critChance, range, s1 = Skill("",0,0,0,0,0,""), s2 = Skill("",0,0,0,0,0,""), s3 = Skill("",0,0,0,0,0,"")):
        self.name = name
        self.sellprice = sellPrice
        self.weight = weight
        self.quantity = quantity
        self.picture = picture
        self.description = description
        self.minDamage = min
        self.maxDamage = max
        self.criticalDamage = crit
        self.critChance = critChance
        self.skill1 = s1
        self.skill2 = s2
        self.skill3 = s3
        self.rangeA = range

    def get(self):
        emb = discord.Embed( title = 'Staff', colour = discord.Color.green())
        emb.add_field(name = str(self.name) + ' :', value = str(self.description)
                     + "\n\nШкода:   " + str(self.minDamage) + (" - " + str(self.maxDamage) if self.minDamage != self.maxDamage else "")
                     + "\nКрит:   " + str(self.criticalDamage) + "        Шанс крита:   " + str(self.critChance)
                     + "\nДальність: " + str(self.rangeA) + "\nВага:     " + str(self.weight)
                     + "кг\nЦіна: " + str(self.sellprice), inline = False )
        if self.skill1.name != "":
            emb.add_field(name = str(self.skill1.name) + ' :', value = str(self.skill1.previewF()), inline = True )
        if self.skill2.name != "":
            emb.add_field(name = str(self.skill2.name) + ' :', value = str(self.skill2.previewF()), inline = True )
        if self.skill3.name != "":
            emb.add_field(name = str(self.skill3.name) + ' :', value = str(self.skill3.previewF()), inline = True )
        emb.set_thumbnail(url = str(self.picture))
        return emb

class Bow(Weapon):
    rangeA = int

    def __init__(self, n, p, w, q, pict, desc, min, max, crit, chance, range, s1 = Skill("",0,0,0,0,0,""), s2 = Skill("",0,0,0,0,0,""), s3 = Skill("",0,0,0,0,0,"")):
        self.name = n
        self.sellprice = p
        self.weight = w
        self.quantity = q
        self.picture = pict
        self.description = desc
        self.minDamage = min
        self.maxDamage = max
        self.criticalDamage = crit
        self.critChance = chance
        self.skill1 = s1
        self.skill2 = s2
        self.skill3 = s3
        self.rangeA = range

    def get(self):
        emb = discord.Embed( title = 'Bow', colour = discord.Color.green())
        emb.add_field(name = str(self.name) + ' :', value = str(self.description)
                     + "\n\nШкода:   " + str(self.minDamage) + (" - " + str(self.maxDamage) if self.minDamage != self.maxDamage else "")
                     + "\nКрит:   " + str(self.criticalDamage) + "        Шанс крита:   " + str(self.critChance)
                     + "\nДальність: " + str(self.rangeA) + "\nВага:     " + str(self.weight)
                     + "кг\nЦіна: " + str(self.sellprice), inline = False )
        if self.skill1.name != "":
            emb.add_field(name = str(self.skill1.name) + ' :', value = str(self.skill1.previewF()), inline = True )
        if self.skill2.name != "":
            emb.add_field(name = str(self.skill2.name) + ' :', value = str(self.skill2.previewF()), inline = True )
        if self.skill3.name != "":
            emb.add_field(name = str(self.skill3.name) + ' :', value = str(self.skill3.previewF()), inline = True )
        emb.set_thumbnail(url = str(self.picture))
        return emb

class Book(Weapon):
    rangeA = int

    def __init__(self, n, p, w, q, pict, desc, min, max, crit, chance, range, s1 = Skill("",0,0,0,0,0,""), s2 = Skill("",0,0,0,0,0,""), s3 = Skill("",0,0,0,0,0,"")):
        #Weapon(n,p,w,q,pict,desc,min,max,crit,chance,s1,s2,s3)
        self.name = n
        self.sellprice = p
        self.weight = w
        self.quantity = q
        self.picture = pict
        self.description = desc
        self.minDamage = min
        self.maxDamage = max
        self.criticalDamage = crit
        self.critChance = chance
        self.skill1 = s1
        self.skill2 = s2
        self.skill3 = s3
        self.rangeA = range


    def get(self):
        emb = discord.Embed( title = 'Book', colour = discord.Color.green())
        emb.add_field(name = str(self.name) + ' :', value = str(self.description)
                     + "\n\nШкода:   " + str(self.minDamage) + (" - " + str(self.maxDamage) if self.minDamage != self.maxDamage else "")
                     + "\nКрит:   " + str(self.criticalDamage) + "        Шанс крита:   " + str(self.critChance)
                     + "\nДальність: " + str(self.rangeA) + "\nВага:     " + str(self.weight)
                     + "кг\nЦіна: " + str(self.sellprice), inline = False )
        if self.skill1.name != "":
            emb.add_field(name = str(self.skill1.name) + ' :', value = str(self.skill1.previewF()), inline = True )
        if self.skill2.name != "":
            emb.add_field(name = str(self.skill2.name) + ' :', value = str(self.skill2.previewF()), inline = True )
        if self.skill3.name != "":
            emb.add_field(name = str(self.skill3.name) + ' :', value = str(self.skill3.previewF()), inline = True )
        emb.set_thumbnail(url = str(self.picture))
        return emb



















class Chest:
    item = Item
    money = int
    mimik = bool
    looted = False


    def __init__(self, moneyChest = False, mimikChance = 25):
        if randint(0,100) <= mimikChance:
            self.mimik = True
        else:
            self.mimik = False

        if moneyChest:
            self.money = randint(100, 300)
        else:
            self.money = randint(50, 150)


    def Loot(self):
        emb = discord.Embed(title = 'Сундук', colour = discord.Color.orange())
        if self.mimik:
            emb.add_field(name = 'Мімік', value = 'На вас напав мімік')
            emb.set_image(url="https://cdn.discordapp.com/attachments/910219916811046972/910242037880741938/ee5c1e2bf682b2faef43e63a77292fa6.png")
        else:
            config = open("settings/bot.txt", "r")
            valute = config.readline()
            valute = config.readline()
            config.close()
            emb.add_field(name = 'Вы отримуєте', value = 'тут буув предмет\nбуде*\n\nГроші: ' + str(self.money) + ' ' + valute, inline = True)
            emb.set_image(url="https://cdn.discordapp.com/attachments/910219916811046972/910242157250613308/d5cb98e6cfafed0e47e5168a58283077.png")
        return emb
            


class Room:
    chest = Chest
    mob = int


class BossRoom:
    chest = Chest
    boss = int



class Dungeon:
    rooms = Room