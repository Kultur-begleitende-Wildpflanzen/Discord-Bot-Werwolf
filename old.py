import random
import TexteundStuff
import discord


class GameLogic:
    # user
    erzaehlerId = 0  # ID des Erzählers
    erzaehler = None  # Erzähler user
    botuser = None  # user des Bots
    members_in_game = []  # Liste aller Mitspieler
    memberroledict = {}  # dictionary mit Rollen und user
    characterdict = {}

    # Channel

    werwolfchannel = None

    def __init__(self, *, loop=None, **options):
        self.variables = TexteundStuff.TexteUndStuff()
        self.characterdict = self.variables.characterdict
        self.func = Functions()
        pass  # Hier muessen die Klassen der Charaktere aufgerufen werden

    async def gamestart(self, user):
        if discord.utils.get(self.erzaehler.guild.text_channels, name="dorfversammlung"):
            pass
        else:
            overwrites = {self.erzaehler.guild.default_role: discord.PermissionOverwrite(send_messages=False),
                          self.erzaehler: discord.PermissionOverwrite(send_messages=True),
                          self.botuser: discord.PermissionOverwrite(send_messages=True)}

            self.werwolfchannel = await self.erzaehler.guild.create_text_channel(name="dorfversammlung",
                                                                                 overwrites=overwrites)

        for text in self.variables.texte:
            emoji = self.variables.emojis[self.variables.texte.index(text)]
            await self.textsending(self.werwolfchannel, text, emoji)

        await self.werwolfchannel.send("Bestätige deine Auswahl mit !OK")

    async def safetyquestion(self):
        tempcharacter = []
        count = 0
        for x in self.characterdict:
            if (self.characterdict[x] != 0) & (x != "werwolf") & (x != "dorfbewohner"):
                tempcharacter.append(self.variables.namedict[x])
                count = count + 1
            if (self.characterdict[x] != 0) & (x == "werwolf"):
                werwolfcount = "Werwölfe : " + str(self.characterdict[x])
                tempcharacter.append(werwolfcount)
                count = count + self.characterdict[x]
        characterstr = str(tempcharacter[0:])
        characterstr = characterstr.replace(",", "\n")
        characterstr = characterstr.replace("'", "").replace("[", "").replace("]", "")

        if count > len(self.members_in_game):
            await self.werwolfchannel.send("Du hast mehr Rollen ausgewählt als Mitspieler. \n Aktuell gibt es " + str(
                len(self.members_in_game)) + " Mitspieler. Bitte wähle erneut.")
            self.characterdict = self.variables.characterdict
            await self.gamestart(self.botuser)
        elif count == len(self.members_in_game):
            await self.werwolfchannel.send(
                "Folgende Rollen wurden ausgewählt: \n " + characterstr + "\n Bist du mit der Auswahl zufrieden? \n :white_check_mark: Ja \t :x: Nein")
            safemessage = await self.werwolfchannel.fetch_message(self.werwolfchannel.last_message_id)
            for emoji in self.variables.ynemojis:
                await safemessage.add_reaction(emoji)
        elif count < len(self.members_in_game):
            self.characterdict["dorfbewohner"] = ((len(self.members_in_game)) - count)
            await self.werwolfchannel.send(
                "Folgende Rollen wurden ausgewählt: \n " + characterstr + "\n Dorfbewohner : " + str(self.characterdict[
                                                                                                         "dorfbewohner"]) + " \n Bist du mit der Auswahl zufrieden? \n :white_check_mark: Ja \t :x: Nein")
            safemessage = await self.werwolfchannel.fetch_message(self.werwolfchannel.last_message_id)
            for emoji in self.variables.ynemojis:
                await safemessage.add_reaction(emoji)

    async def gameend(self):
        await self.werwolfchannel.send('Rollen werden gelöscht...')

        # Rollen Entfernung
        if discord.utils.get(self.erzaehler.guild.roles, name="Leiche"):
            role1 = discord.utils.get(self.erzaehler.guild.roles, name="Leiche")
            await role1.delete()

        if discord.utils.get(self.erzaehler.guild.roles, name="Lebendig"):
            role2 = discord.utils.get(self.erzaehler.guild.roles, name="Lebendig")
            await role2.delete()

        if discord.utils.get(self.erzaehler.guild.roles, name="Erzähler"):
            role3 = discord.utils.get(self.erzaehler.guild.roles, name="Erzähler")
            await role3.delete()

        # Kanäle löschen
        await self.werwolfchannel.send('Kanäle werden gelöscht...')
        if discord.utils.get(self.erzaehler.guild.text_channels, name="dorfversammlung"):
            await self.werwolfchannel.delete()
        for x in self.characterdict:
            if self.characterdict[x] != 0:
                delchannel = discord.utils.get(self.erzaehler.guild.text_channels, topic=x)
                await delchannel.delete()

        # Variablen clearen

        self.erzaehlerId = 0
        self.erzaehler = None
        for character in self.characterdict:
            self.characterdict[character] = 0
        self.members_in_game = []

    async def addreaction(self, reaction):
        # Zahlenreactions
        if reaction.message.content == self.variables.werwolftext:

            for emoji in self.variables.werwolfEmojis:
                if str(reaction.emoji) == emoji:
                    self.characterdict["werwolf"] = self.variables.werwolfEmojis.index(emoji) + 1
                    print(self.characterdict)

        # Charakter Reactions
        if reaction.message.content == self.variables.specialText:
            await self.reactioncalcup(reaction)

        if reaction.message.content == self.variables.seeingText:
            await self.reactioncalcup(reaction)

        if reaction.message.content == self.variables.dyingText:
            await self.reactioncalcup(reaction)

        if reaction.message.content == self.variables.oneHitText:
            await self.reactioncalcup(reaction)

        if reaction.message.content == self.variables.restText:
            await self.reactioncalcup(reaction)

        if reaction.emoji == self.variables.ynemojis[0]:
            await self.rollenzuweisung()
            await self.createchannel()
        if reaction.emoji == self.variables.ynemojis[1]:
            for character in self.characterdict:
                self.characterdict[character] = 0
            await reaction.message.channel.send("Bitte wiederhole deine Eingabe")
            await self.gamestart(self.botuser)


    async def rollenzuweisung(self):
        gamecharacter = []
        for x in self.characterdict:
            if (self.characterdict[x] != 0) & (x != "werwolf"):
                gamecharacter.append(x)
            if (self.characterdict[x] != 0) & (x == "werwolf"):
                for i in range(0, self.characterdict[x]):
                    gamecharacter.append(x)
            if (self.characterdict[x] != 0) & (x == "dorfbewohner"):
                for i in range(0, self.characterdict[x]):
                    gamecharacter.append(x)
        for member in self.members_in_game:
            temprole = random.choice(gamecharacter)
            self.memberroledict[member] = temprole
            await self.func.send_a_message(member, self.variables.textdict[temprole])
            gamecharacter.remove(temprole)
        print(self.memberroledict)

    async def textsending(self, channel, text, emojis):
        await channel.send(text)
        restmessage = await channel.fetch_message(channel.last_message_id)
        while restmessage.content != text:
            restmessage = await channel.fetch_message(channel.last_message_id)
        for emoji in emojis:
            await restmessage.add_reaction(emoji)

    async def reactioncalcup(self, reaction):
        for x in self.variables.emojidict:
            if str(reaction.emoji) == x:
                self.characterdict[self.variables.emojidict[x]] = 1

    async def reactioncalcdown(self, reaction):
        for x in self.variables.emojidict:
            if str(reaction.emoji) == x:
                self.characterdict[self.variables.emojidict[x]] = 0

    async def createroles(self, user):
        self.botuser = user
        # Rollen Erstellung

        color1 = discord.colour.Color(0xff0000)
        color2 = discord.colour.Color(0x33ff00)
        color3 = discord.colour.Color(0x4298f5)
        if discord.utils.get(self.erzaehler.guild.roles, name="Leiche"):
            pass
        else:
            await self.erzaehler.guild.create_role(name="Leiche", color=color1, hoist="true")

        if discord.utils.get(self.erzaehler.guild.roles, name="Lebendig"):
            pass
        else:
            await self.erzaehler.guild.create_role(name="Lebendig", color=color2, hoist="true")
        if discord.utils.get(self.erzaehler.guild.roles, name="Erzähler"):
            pass
        else:
            await self.erzaehler.guild.create_role(name="Erzähler", color=color3, hoist="true")

    async def createchannel(self):
        adminrole = discord.utils.get(self.erzaehler.guild.roles, name="Admin")
        for x in self.characterdict:
            if (self.characterdict[x] != 0) & (x != "dorfbewohner") & (not x.startswith('werwolf')):
                overwrites = {
                    self.erzaehler.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    self.botuser: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    self.erzaehler: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    adminrole: discord.PermissionOverwrite(read_messages=False)
                }
                for member in self.memberroledict:
                    if self.memberroledict[member] == x:
                        overwrites[member] = discord.PermissionOverwrite(send_messages=True, read_messages=True)
                await self.erzaehler.guild.create_text_channel(name=self.variables.namedict[x], overwrites=overwrites,
                                                               topic=x)
            elif x.startswith('werwolf'):
                if x.startswith("werwolf_"):
                    overwrites = {
                        self.erzaehler.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        self.botuser: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                        self.erzaehler: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                        adminrole: discord.PermissionOverwrite(read_messages=False)
                    }
                    for member in self.memberroledict:
                        if self.memberroledict[member] == x:
                            overwrites[member] = discord.PermissionOverwrite(send_messages=True, read_messages=True)
                    await self.erzaehler.guild.create_text_channel(name=self.variables.namedict[x],
                                                                   overwrites=overwrites,
                                                                   topic=x)
                    if discord.utils.get(self.erzaehler.guild.text_channels, topic="werwolf"):
                        pass
                    else:
                        overwrites = {
                            self.erzaehler.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                            self.botuser: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                            self.erzaehler: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                            adminrole: discord.PermissionOverwrite(read_messages=False)
                        }
                        for member in self.memberroledict:
                            if self.memberroledict[member] == x:
                                overwrites[member] = discord.PermissionOverwrite(send_messages=True, read_messages=True)
                        await self.erzaehler.guild.create_text_channel(name="werwoelfe", overwrites=overwrites,
                                                                       topic="werwolf")
                else:
                    if discord.utils.get(self.erzaehler.guild.text_channels, topic= "werwolf"):
                        pass
                    else:
                        overwrites = {
                            self.erzaehler.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                            self.botuser: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                            self.erzaehler: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                            adminrole: discord.PermissionOverwrite(read_messages=False)
                        }
                        for member in self.memberroledict:
                            if self.memberroledict[member] == x:
                                overwrites[member] = discord.PermissionOverwrite(send_messages=True, read_messages=True)
                        await self.erzaehler.guild.create_text_channel(name="werwoelfe", overwrites=overwrites,
                                                                       topic="werwolf")

class Functions:
    async def send_a_message(self, user, message):
        channel = await user.create_dm()
        await channel.send(message)

    async def channel_add_member(self, user, channelname):
        channel = discord.utils.get(user.guild.text_channels, topic=channelname)
        await channel.set_permissions(user, read_messages=True)
