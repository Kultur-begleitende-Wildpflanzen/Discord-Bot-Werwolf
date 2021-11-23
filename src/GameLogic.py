from Listener import Listener
from Texte import Texte
from PrepareGame import PrepareGame
#from Token import samu_token
import Roles
from Votingsystem import VotingSystem
from Helper import Helper
from Narrator import Narrator

import random
import discord
import threading
import os
# from operator import attrgetter


class GameLogic(object):
    helper = None
    text = Texte()
    prepgame = None
    voting_system = None
    narrator = None

    previous_voice_channel = {}

    guild = None

    character_assignment = {}
    playerStatus = {}
    procedure_list = ["Kopierertyp", "Amor", "Leibwaechter", "Nutte", "Fuchs", "Seherin", "WildesKind", "Werwolf", "WerwolfUr", "WerwolfWeisser", "Hexe", "Richter"]

    #in Datenbank
    objectdict = {
        'werwolf': None,
        'werwolf_weißer': Roles.WerwolfWeisser(),
        'wildes_kind': Roles.WildesKind(),
        'werwolf_baby': Roles.WerwolfBaby(),
        'werwolf_ur': Roles.WerwolfUr(), 
        'bärenführer': Roles.Baerenfuehrer(), 
        'fuchs': Roles.Fuchs(),
        'seherin': Roles.Seherin(),
        'jäger': Roles.Jaeger(),
        'tetanusritter': Roles.Tetanusritter(),
        'terrorist': Roles.Terrorist(),
        'amor': Roles.Amor(),
        'kopierertyp': Roles.Kopierertyp(),
        'magd': Roles.Magd(),
        'nutte': Roles.Nutte(),
        'leibwächter': Roles.Leibwaechter(),
        'reine_seele': Roles.ReineSeele(), 
        'richter': Roles.Richter(),
        'engel': Roles.Engel(),
        'hexe': Roles.Hexe(),
        'dorfbewohner': Roles.Dorfbewohner()
    }

    hauptmann_name = None
    hauptmann_vote = None
    reine_seele_name = None


    def __init__(self, sql_db):
        self.sql_db = sql_db

        self.helper = Helper(self)
        self.narrator = Narrator(self)
        
        self.objectdict['werwolf'] = Roles.Werwolf(self)
        
        intents = discord.Intents().default()
        intents.members = True

        self.client = Listener(self, self.text, intents = intents)
        self.client.run(os.environ.get('TOKEN_SAMU'))


    # Erstellt beim Start des Spiels eine entsprechende Kategorie und ruft die join_game Methode auf
    async def new_game(self, guild_id):
        self.anzahl_der_Tage = 0
        guild = await self.helper.guild_id_to_guild(guild_id)
        spiel_id = await self.helper.get_spielID_by_guildID(guild_id)

        self.sql_db.insert('temp_tabelle', spiel_id, 'msg_end_safety_question', 'None')
        self.sql_db.insert('temp_tabelle', spiel_id, 'result_magd', 'None')

        game_category = await guild.create_category('Werwolf-Spiel')
        
        tempvar= self.sql_db.update_where_from_table('spiele','Discord_Kategorie', game_category.id, 'Server_ID', guild_id)
        print("Set Discord Category: ", tempvar)

        self.prepgame = PrepareGame(self)

        await self.prepgame.join_game(guild_id)

        # self.voting_system = VotingSystem(self, await self.game_logic.helper.get_dorfversammlung_channel(guild_id, "text"))
    

    # Zuordnung der Rollen und Erstellung der Objekte
    async def create_role_objects(self):
        self.character_assignment = self.playerStatus.copy()
        helpchannel = await self.guild.create_text_channel("Rollen-Übersicht", category = self.game_category)
        # ordnet jedem User eine Zufallsrolle zu
        temp_character_list = self.prepgame.character_list.copy()
        for player in self.character_assignment:
            temprole = random.choice(temp_character_list)
            self.character_assignment[player] = temprole
            temp_character_list.remove(temprole)
    
        # ordnet jedem User ein Rollen-Objekt zu
        for role_object in self.objectdict:
            for player_id in self.character_assignment:
                if self.character_assignment[player_id] == role_object:
                    await self.helper.send_a_message((await self.helper.user_id_to_user(player_id)), self.text.get_text_dict()[role_object])
                    await helpchannel.send(self.text.get_common_text_dict()[role_object])
                    self.character_assignment[player_id] = self.objectdict[role_object]
                    if role_object not in ['bärenführer', 'engel', 'jäger', 'reine_seele', 'tetanusritter', 'dorfbewohner']:
                        await self.role_channels((await self.helper.user_id_to_user(player_id)) , role_object)
                    elif role_object == 'reine_seele':
                        self.reine_seele_name = await self.helper.nick_name_module(user_id=player_id)
                        reine_seele = await self.helper.user_id_to_user(player_id)
                        await reine_seele.edit(nick ="Reine Seele" , reason="Der Spieler ist die Reine Seele")
        print(self.character_assignment)

        # Ermöglicht das Hauptmann Voting und fragt ob einer gewählt werden soll
        self.client.hauptmann_voting_started = True
        await self.prepgame.dorfversammlung_text.send("Wenn jetzt ein Hauptmann gewählt werden soll schreibe !hauptmann in den Chat.")

    #Funktion zum erstellen von Channels und der Zuordnung von Berechtigungen
    async def role_channels(self, user, channel_name):
        if channel_name == 'werwolf':
            temp_text_channel = await self.create_role_channels(user, channel_name)
        elif 'werwolf' in channel_name:
            temp_text_channel = await self.create_role_channels(user, 'werwolf')
            if channel_name != 'werwolf_baby':
                temp_text_channel_two = await self.create_role_channels(user, channel_name)
                self.character_assignment[user.id].set_channel(temp_text_channel_two)
        else:
            temp_text_channel = await self.create_role_channels(user, channel_name)
    
        self.character_assignment[user.id].set_channel(temp_text_channel)

        if channel_name == 'terrorist':
            await self.character_assignment[user.id].send_msg()
    
    #Erstellt Text Channel für die verschiedenen Rollen und gibt den Usern Berechtigungen in dem Rollen Channel
    async def create_role_channels(self,user,channel_name):      
        temp_text_channel = discord.utils.get(self.guild.text_channels, name=channel_name)
        if temp_text_channel == None:
            temp_text_channel = await self.guild.create_text_channel(channel_name, category=self.game_category)
            await temp_text_channel.set_permissions(self.prepgame.d_rolle_erzaehler, read_messages=False, send_messages=False)
            await temp_text_channel.set_permissions(self.prepgame.d_rolle_everyone, read_messages=False, send_messages=False)
            await temp_text_channel.set_permissions(self.prepgame.d_rolle_lebendig, read_messages=False, send_messages=False)
            await temp_text_channel.set_permissions(self.prepgame.d_rolle_tod, read_messages=True, send_messages=False)
        await temp_text_channel.set_permissions(user, read_messages=True, send_messages=True)
        return temp_text_channel


    #Methode für den Day-Night Zyklus
    async def start_day(self):
        # Mute
        self.anzahl_der_Tage += 1
        await self.prepgame.dorfversammlung_text.set_permissions(self.prepgame.d_rolle_lebendig, read_messages=True, send_messages=True)
        for member in self.prepgame.dorfversammlung_voice.members:
            if member != self.erzaehler:
                # if player schon gemutet dann net
                await member.edit(mute = False, reason= "Der Tag hat im Werwolfchannel begonnen.")

        # Kill procedure
        await self.pre_kill()

    # KILL
    # ------------------------------------------------------------------------------------------------------------------------
    async def pre_kill(self):
        magd = None 
        magd_id = None 
        nutte = None 
        nutte_id = None
        try:
            nutte_id = await self.helper.get_id_of_role_name("Nutte")
            nutte = self.character_assignment[nutte_id]
        except:
            print('Keine Nutte vorhanden.')

        try:
            magd_id = await self.helper.get_id_of_role_name("Magd")
            magd = self.character_assignment[magd_id]
        except:
            print('Keine Magd vorhanden.')

        self.kill_list = []

        for user_id in self.playerStatus:
            user = await self.helper.user_id_to_user(user_id=user_id)

            if self.playerStatus[user_id] == 2:
                self.kill_list.append(user)

            #geschützte werden lebendig gesetzt
            elif self.playerStatus[user_id] == 3:
                self.playerStatus[user_id] = 1

            #Nutte wird überprüft
            if self.character_assignment[user_id].get_role_name() == 'Nutte':
                try:
                    if self.playerStatus[nutte.customer.id] == 2:
                        self.kill_list.append(user_id)
                except:
                    print("Nuttenfehler")

        if self.kill_list != []:
            print(self.kill_list)
            for player in self.kill_list:
                if magd and self.playerStatus[magd_id] != 2:
                    await magd.start(self.kill_list[0])
                    thread = threading.Thread(target=self.client.on_message())
                    thread.start()
                    self.client.result_magd_available.wait()

                if self.character_assignment[self.kill_list[0].id].get_isHauptmann():
                    await self.prepgame.dorfversammlung_text.send("Bestimme mit *!nachfolger @[**Username**]* den nächsten Hauptmann")
                    await self.kill_list[0].edit(nick = self.hauptmann_name, reason= "Der Hauptmann wurde getötet")
                #Wenn Tetanusritter getötet wird
                if self.character_assignment[self.kill_list[0].id].get_role_name() == 'Tetanusritter':
                    self.character_assignment[self.kill_list[0].id].infest_teternusritter(self.kill_list[0].id)
                if self.character_assignment[self.kill_list[0].id].get_role_name() == "ReineSeele":
                    await user.edit(nick = self.reine_seele_name, reason= "Die Reine Seele wurde getötet.")
                #Abfrage für das Liebespaar
                partner = self.character_assignment[self.kill_list[0].id].get_partner()
                if partner:
                    current_victim = partner
                    await self.kill(current_victim)
                current_victim = self.kill_list[0]
                await self.kill(current_victim)
                self.kill_list.pop(0)
        else:
            await self.prepgame.erzaehler_text.send("Alle Rollen wurden getötet! \n-> *!tag*")
            #await self.start_day()
            await self.prepgame.dorfversammlung_text.send("Gebe !anklagen ein um einen Mitspieler anzuklagen.") # ?
        
        await self.Narrator.create_summary_embed()


    #Spieler werden getötet, es werden neue Rechte vergeben und ggf. wird der entsprechende Rollenkanal entfernt
    async def kill(self, victim):
        text_channel = self.character_assignment[victim.id].get_text_channel()
        if text_channel:
            await text_channel.set_permissions(victim, read_messages=True, send_messages=False)

        await self.send_death_text(victim)

        self.playerStatus[victim.id] = 0
        await victim.add_roles(self.prepgame.d_rolle_tod)
        await victim.remove_roles(self.prepgame.d_rolle_lebendig)
        
        role = self.character_assignment[victim.id]
        self.character_assignment.pop(victim.id)
        rolelist = self.character_assignment.values()
        if role not in rolelist and text_channel:
           await text_channel.delete(reason = 'Die Rolle ist ausgestorben.')
    
    # ------------------------------------------------------------------------------------------------------------------------


    #Methode für den Day-Night Zyklus
    async def start_night(self):
        self.client.hauptmann_voting_started = False
        # print(self.procedure_list)
        temp = []
        for player in self.character_assignment.keys():
            temp.append(self.character_assignment[player].get_role_name())
        for i in range((len(self.procedure_list)-1), -1, -1):
            if self.procedure_list[i] not in temp:
                self.procedure_list.pop(i)
        # self.procedure_list.reverse()
        print("Ablauf: " + str(self.procedure_list))
        self.procedure_list_run = self.procedure_list.copy()
        
        await self.next_role()

        '''
        Roles.Klassenname.start()
        d.keys()[i]
        first_key = list(colors)[0]
        
        '''
    
    async def next_role(self):
        # if minimum one role in the current queue
        if self.procedure_list_run != []:
            self.current_role_procedure_list = self.procedure_list_run[0]
            await self.narrator.send_msg_to_narrator(self.current_role_procedure_list)
            for player in self.character_assignment:
                    if self.character_assignment[player].get_role_name() == self.procedure_list_run[0]:
                        await self.character_assignment[player].start()
            self.procedure_list_run.pop(0)
        else:
            await self.prepgame.erzaehler_text.send("Alle Rollen wurden ausgeführt! \n-> *!tag*")
            #await self.start_day()
        
    # sendet den Todestext
    async def send_death_text(self, victim):

        #Nickname Module
        victim_name = await self.helper.nick_name_module(user=victim)

        #Todestexte für den Tag
        if self.client.game_day_started:
            death_dict_day = self.text.get_death_text_dict_day()
            deathtext_day = random.choice(list(death_dict_day.values()))
            await self.prepgame.dorfversammlung_text.send(deathtext_day.format(Playername=victim_name, Role=self.character_assignment[victim.id].get_role_name()))
        #Todestexte für die Nacht
        else:
            death_dict_night = self.text.get_death_text_dict_night()
            deathtext_night = random.choice(list(death_dict_night.values()))
            await self.prepgame.dorfversammlung_text.send(deathtext_night.format(Playername=victim_name, Role=self.character_assignment[victim.id].get_role_name()))
        
        #Todestexte für Liebespaar
        if self.character_assignment[victim.id].get_partner():
            death_dict_pair = self.text.get_death_text_dict_pair()
            deathtext_pair = random.choice(list(death_dict_pair.values()))
            await self.text_channel.send(deathtext_pair.format(victim=victim_name, partner= self.character_assignment[victim.id].get_partner() ,Role=self.character_assignment[self.character_assignment[victim.id].get_partner()].get_role_name())) # dorfversammlung

    #Hauptmannvoting
    async def vote_for_hauptmann(self):
        await self.prepgame.dorfversammlung_text.set_permissions(self.prepgame.d_rolle_lebendig, send_messages=True)
        self.hauptmann_vote = VotingSystem(self, self.prepgame.dorfversammlung_text)
        await self.prepgame.dorfversammlung_text.send("Kandidaten für den Posten des Hauptmann´s können mit *!nominieren* nominiert werden.")

    #Aufraeumen am Ende des Spiels
    async def end_game(self, guild_id):
        print("Spiel wird beendet")
        dorfversammlung_voice = await self.helper.get_dorfversammlung_channel(guild_id, "voice")
        spieler_sql = self.sql_db.select_where_from_table("Discord_ID","spieler","Spiel_ID", self.sql_db.select_where_from_table("Spiel_ID","spiele","Server_ID", guild_id)[0][0])
        if spieler_sql and len(spieler_sql) != 0:
            spieler_ids = spieler_sql
            print(spieler_ids)

            # verschiebe alle Spieler wieder zurück
            for user_id in spieler_ids:
                user = await self.helper.user_id_to_user(guild_id, user_id[0])
            #    try:
            #        if self.character_assignment[user_id].get_isHauptmann():
            #            await user.edit(nick = self.hauptmann_name, reason= "Das Werwolfspiel wurde beendet")
            #    except:
            #        pass
            #    try:
            #        if self.character_assignment[user_id].get_role_name() == "ReineSeele":
            #            await user.edit(nick = self.reine_seele_name, reason= "Das Werwolfspiel wurde beendet")
            #    except:
            #        pass
                # Verschiebung der Spieler
                try:
                    if user.voice.channel == dorfversammlung_voice:
                        await user.move_to(await self.helper.channel_id_to_channel(self.sql_db.select_where_from_table("Previous_Voice_Channel","spieler","Discord_ID", user.id)[0][0]))
                        await user.edit(mute = False, reason = "Das Werwolfspiel wurde beendet")
                except:
                    print("Keine Verschiebung des Users moeglich!")


        else:
            print("[INFO] Keine Spieler vorhanden.")
        
        # Verschiebung des Erzaehlers
        try:
            erzaehler = await self.helper.user_id_to_user(guild_id, self.sql_db.select_where_from_table('Erzaehler_ID', 'spiele', 'Server_ID', guild_id)[0][0])
            if erzaehler.voice.channel == dorfversammlung_voice:
                await erzaehler.move_to(await self.helper.channel_id_to_channel(self.sql_db.select_where_from_table("Erzaehler_Previous_Channel","spiele","Erzaehler_ID", erzaehler.id)[0][0]))
                await erzaehler.edit(mute = False, reason = "Das Werwolfspiel wurde beendet")
        except:
            print("[ERROR] Keine Verschiebung des Erzaehlers moeglich!")



        # Entferne alle Channel in der Kategorie Werwolf-Spiel
        guild = await self.helper.guild_id_to_guild(guild_id)
        category_id = self.sql_db.select_where_from_table('Discord_Kategorie', 'spiele', 'Server_ID', guild_id)[0][0]
        game_category = discord.utils.get(guild.categories, id=category_id)
        for channel in game_category.channels:
            await channel.delete()
        #Rollen entfernen
        await (await self.helper.role_id_to_role(self.sql_db.select_where_from_table("DC_Rolle_Lebendig_ID","spiele","Server_ID",guild_id)[0][0],guild_id)).delete()
        await (await self.helper.role_id_to_role(self.sql_db.select_where_from_table("DC_Rolle_Tot_ID","spiele","Server_ID",guild_id)[0][0], guild_id)).delete()
        await (await self.helper.role_id_to_role(self.sql_db.select_where_from_table("DC_Rolle_Erzaehler_ID","spiele","Server_ID",guild_id)[0][0], guild_id)).delete()
        # Entferne Kategorie Werwolf-Spiel
        await game_category.delete()

        self.sql_db.clear_all_tables(guild_id)

        print("Spiel beendet")

        # To-Do Variablen clearen?