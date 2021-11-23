# Klasse um mit Discord zu komunizieren

import discord
import threading

class Listener(discord.Client):



    prefix = '!'

    def __init__(self, game_logic, text, *, loop=None, **options):
        super().__init__(loop=loop, **options)
        self.game_logic = game_logic
        self.text = text

        # Variablen fuer den Ablauf
        self.game_started = False
        self.game_started_menu = False
        self.game_night_started = False
        self.game_voting_started = False
        self.game_day_started = False
        self.roles_confirmed = False
        self.hauptmann_voting_started = False

        self.msg_end_safety_question = None
        
        self.result_magd = None
        self.result_magd_available = threading.Event()
    

    # returns the DB table of the relevant gamestates
    def get_mysql_table_spiele(self):
        temp_sql_return_val = self.game_logic.sql_db.select_all_from_table('*', 'spiele')
        print("Get all from 'Spiele': ", temp_sql_return_val)
        return temp_sql_return_val


    # Einloggen
    async def on_ready(self):
        print("Eingeloggt als user: " + str(self.user))
        await self.change_presence(activity=discord.Game(name="!help für mehr Informationen"))


    # Wenn Nachricht gepostet wird
    async def on_message(self, message):
        # Ignoriert Nachricht vom Bot
        if message.author == self.user:
            return

        # Wenn die Nachricht mit dem vorher bestimmten Prefix beginnt
        if message.content.startswith(self.prefix):
            split_msg = message.content[1:].lower().split(' ')
            
            # Wenn das Game gestartet ist
            if self.game_started:
                if message.author != self.game_logic.erzaehler:
                    author_role = self.game_logic.character_assignment[message.author.id]
                

                # Befehle die nur im Dorfversammlungschannel geschrieben werden können
                if message.channel == await self.game_logic.helper.get_dorfversammlung_channel(message.channel.guild.id, "text"):
                    # Erzählerbefehle
                    if message.author == self.game_logic.erzaehler:
                        # Befehl zum beenden des Spiels
                        if split_msg[0] == 'end' and split_msg[1] == 'game':
                            # Sicherheitsfrage
                            dorfversammlung_text = await self.game_logic.helper.get_dorfversammlung_channel(message.channel.guild.id, "text")
                            self.msg_end_safety_question = await dorfversammlung_text.send(self.text.get_game_end_safety_question_text())
                            for emoji in self.game_logic.text.get_ynemojis():
                                await self.msg_end_safety_question.add_reaction(emoji)
                        # Befehl zum öffnen der Charakter Auswahl
                        if split_msg[0] == 'start' and split_msg[1] == 'menu':
                            self.game_started_menu = True
                            self.game_logic.prepgame.werwolf_count_advice = 0
                            await self.game_logic.prepgame.character_menu(message.channel.guild)
                        #Auswahl bestätigen
                        if split_msg[0]== 'confirm' and split_msg[1] == 'menu':
                            await self.game_logic.prepgame.confirm_selection(message.channel.guild)
                        # Wenn Rollen verteilt wurden
                        if self.roles_confirmed:
                            try:
                                # Befehl zum starten der Nacht ohne muten
                                if split_msg[0] == 'nacht' and split_msg[1] == 'unmute':
                                    await self.game_logic.prepgame.dorfversammlung_text.set_permissions(self.game_logic.prepgame.d_rolle_lebendig, read_messages=True, send_messages= False)
                                    self.game_night_started = True
                                    self.game_day_started = False
                                    await self.game_logic.start_night()
                            except:
                                # Befehl zum starten der Nacht
                                if split_msg[0] == 'nacht':
                                    await self.game_logic.prepgame.dorfversammlung_text.set_permissions(self.game_logic.prepgame.d_rolle_lebendig, read_messages=True, send_messages= False)
                                    self.game_night_started = True
                                    self.game_day_started = False
                                    for member in self.game_logic.prepgame.dorfversammlung_voice.members:
                                        if member != self.game_logic.erzaehler:
                                            # if player schon gemutet dann net
                                            await member.edit(mute = True, reason= "Die Nacht hat im Werwolfchannel begonnen.")
                                    await self.game_logic.start_night()
                            #Befehl zum starten des Tages
                            if split_msg[0] == 'tag':
                                self.game_night_started = False
                                self.game_day_started = True
                                await self.game_logic.start_day()                             
                            if split_msg[0] == 'start' and split_msg[1] == 'vote':
                                self.game_voting_started = True
                                await self.game_logic.voting_system.start_voting()
                            if split_msg[0] =='hauptmann' and self.hauptmann_voting_started == True:
                                await self.game_logic.vote_for_hauptmann()
                                # self.hauptmann = False
                    else: # wenn Spieler schreibt
                        if self.game_day_started:
                            if split_msg[0] =='nachfolger' and self.author_role.get_isHauptmann == True:
                                nachfolger = await self.game_logic.helper.user_id_to_user(split_msg[1][3:-1])
                                try:
                                    self.game_logic.character_assignment[nachfolger.id].set_isHauptmann()
                                    nachfolger_name = await self.game_logic.helper.nick_name_module(user=nachfolger)
                                    self.game_logic.hauptmann_name = nachfolger_name
                                    await nachfolger.edit(nick ="Häuptling Mächtiger Elch" , reason= "Wurde als Bürgermeister gewählt")
                                except:
                                    await self.prepgame.dorfversammlung_text.send("{}, ist nicht mehr im Spiel!\nWähle bitte eine andere Person.")
                            if split_msg[0] == "anklagen":
                                #!anklagen @samu
                                player = await self.game_logic.helper.user_id_to_user(split_msg[1][3:-1])
                                await self.game_logic.voting_system.nominate_player(player, message.author.id)
                                                
                        else: #Fuer die Nominierung des Hauptmanns
                            if split_msg[0] == "nominieren" and self.hauptmann_voting_started:
                                player = await self.game_logic.helper.user_id_to_user(split_msg[1][3:-1])
                                await self.game_logic.hauptmann_vote.nominate_player(player, message.author.id)
                # Befehle die im Erzaehler Channel ausgefuehrt werden
                elif message.channel == self.game_logic.prepgame.erzaehler_text:
                    if message.author == self.game_logic.erzaehler:
                        # Sendet eine Zusammenfassung des Spiels
                        if split_msg[0] == 'zusammenfassung':
                            await self.game_logic.Narrator.create_summary_embed()
                        # Methode um einen Textvorschlag zu erhalten
                        if split_msg[0] == 'vorschlag':
                            pass
                        # Ruft die naechste Rolle auf
                        if split_msg[0] == 'weiter':
                            await self.game_logic.next_role()
                # Wenn Channel Werwolf-Channel ist und Author Werwolf ist
                elif message.channel == author_role.get_werwolf_channel() and author_role.get_werwolf():
                    if 'Werwolf' in author_role.get_role_name():
                        if self.game_night_started:
                            #Methode zum vorschlagen eines Opfers
                            if split_msg[0] == "vorschlagen":
                                #!vorschlagen @samu
                                player = await self.game_logic.helper.user_id_to_user(split_msg[1][3:-1])
                                await author_role.voting_system.nominate_player(player, message.author.id)
                # Befehle für die Hexe
                elif author_role.get_role_name() == 'Hexe' and author_role.get_text_channel() == message.channel:
                    if self.game_night_started:
                        player = await self.game_logic.helper.user_id_to_user(split_msg[1][3:-1])
                        # toetet einen Spieler
                        if split_msg[0] == "toeten":
                            author_role.kill(player, self.game_night_started)
                            author_role.abilities['vergiftungs_trank'] = False
                        # heilt einen Spieler
                        elif split_msg[0] == "heilen":
                            author_role.safe(player)
                            author_role.abilities['heilungs_trank'] = False
                # Befehle für die Seherin
                elif author_role.get_role_name() == 'Seherin' and author_role.get_text_channel() == message.channel:
                    if self.game_night_started and author_role.get_role_name() == self.game_logic.current_role_procedure_list:
                        player = await self.game_logic.helper.user_id_to_user(split_msg[1][3:-1])
                        if split_msg[0] == "offenbaren":
                            await author_role.discover(player)
                # Befehle für die Nutte
                elif author_role.get_role_name() == 'Nutte' and author_role.get_text_channel() == message.channel:
                    if self.game_night_started and author_role.get_role_name() == self.game_logic.current_role_procedure_list:
                        player = await self.game_logic.helper.user_id_to_user(split_msg[1][3:-1])
                        if split_msg[0] == "pimperlimpern":
                            if player == message.author:
                                await message.channel.send("Leider ist das Internet im Dorf zu schlecht um mit Webcam zu streamen. Bitte such dir einen Kunden in deiner Nähe aus.")
                            else:
                                await author_role.pimperLimpern(player)
                #Befehle für Amor
                elif author_role.get_role_name() == 'Amor' and author_role.get_text_channel() == message.channel:
                    print("procedure_list_run[0] = " + str(self.game_logic.procedure_list_run[0]))
                    print("author_role = " + str(author_role.get_role_name()))
                    if self.game_night_started and author_role.get_role_name() == self.game_logic.current_role_procedure_list:
                        player1 = await self.game_logic.helper.user_id_to_user(split_msg[1][3:-1])
                        player2 = await self.game_logic.helper.user_id_to_user(split_msg[2][3:-1])
                        if split_msg[0] == "verkuppeln":
                            await author_role.pair(player1, player2)
                            self.game_logic.procedure_list.remove('Amor')
                #Befehle für den Kopierertypi
                elif author_role.get_role_name() == 'Kopierertyp' and author_role.get_text_channel() == message.channel:
                    if self.game_night_started and author_role.get_role_name() == self.game_logic.current_role_procedure_list:
                        player = await self.game_logic.helper.user_id_to_user(split_msg[1][3:-1])
                        if split_msg[0] == "kopieren":
                            await author_role.copy(message.author, player)
                # Befehle für den Terroristen
                elif author_role.get_role_name() == 'Terrorist' and message.channel == author_role.get_text_channel():
                    player = await self.game_logic.helper.user_id_to_user(split_msg[1][3:-1])
                    if split_msg[0] == "boom":
                        await author_role.kill(player, self.game_night_started)
                #Befehle für die Magd
                elif author_role.get_role_name() == 'Magd' and author_role.get_text_channel() == message.channel:
                    #für die Magd
                    self.magd_weiter = True
                    def check(m):
                        if m.content == '!fortfuehren':
                            self.magd_weiter = False
                        elif m.content == "!weiter":
                            self.magd_weiter = True

                        return m.content == '!fortfuehren' or m.content == '!weiter' and m.channel == self.game_logic.character_assignment[self.game_logic.helper.get_id_of_role_name("Magd")].get_channel()

                    await self.wait_for('message', check=check)
                    self.result_magd_available.set()
                    
                    if self.magd_weiter == False:
                        author_role.copy(message.author, self.game_logic.kill_list[0])

            # Befehle die ausgeführt werden können, wenn kein Spiel gestartet ist
            else:
                # Hilfebefehl
                if split_msg[0] == 'help':
                    await message.channel.send(self.text.get_help_text())
                # Befehl zum starten eines Spiels
                if split_msg[0] == 'start' and split_msg[1] == 'game':

                    if len(self.game_logic.sql_db.select_all_from_table('Server_ID', 'spiele')) == 0:
                        await message.channel.send(self.text.get_game_start_text(), delete_after=5)

                        # Wert in Datenbank aendern
                        self.game_logic.erzaehler = message.author
                        self.game_logic.guild = message.channel.guild
                        await message.delete(delay=3)
                        temp_sql_return_val = self.game_logic.sql_db.insert('spiele', message.channel.guild.id, False, False, False, False, False, True, False, message.author.id, 0, 0)
                        print("Insert new Spiel in 'Spiele': ", temp_sql_return_val)
                        print(self.get_mysql_table_spiele())
                        self.game_started = True
                        await self.game_logic.new_game(message.channel.guild.id)
                    elif message.channel.guild.id in self.game_logic.sql_db.select_all_from_table('Server_ID', 'spiele')[0]:
                        await message.channel.send('Auf diesem Server läuft bereits ein Werwolfspiel!', delete_after=5)
                    else:
                        await message.channel.send(self.text.get_game_start_text(), delete_after=5)

                        # Wert in Datenbank aendern
                        self.game_logic.erzaehler = message.author
                        self.game_logic.guild = message.channel.guild
                        await message.delete(delay=3)
                        temp_sql_return_val = self.game_logic.sql_db.insert('spiele', message.channel.guild.id, False, False, False, False, False, True, False, message.author.id, 0, 0)
                        print("Insert new Spiel in 'Spiele': ", temp_sql_return_val)
                        print(self.get_mysql_table_spiele())
                        self.game_started = True
                        await self.game_logic.new_game(message.channel.guild.id)
                if split_msg[0] == 'memberlist':
                    members = await self.game_logic.helper.get_sorted_voice_channel_members(message)
                    await message.delete(delay=3)
                    print(members)
                    

            # await message.channel.send("Hi, möchtest du was von mir?")


	# Wenn eine Reaktion hinzugeuegt wird
    async def on_raw_reaction_add(self, payload):
        if self.game_started:
            channel = self.game_logic.guild.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            user = await self.game_logic.helper.user_id_to_user(payload.user_id)
    
            #Ignoriert Reaktionen vom Bot
            if payload.user_id == self.user.id:
                return
            
            if payload.user_id == self.game_logic.erzaehler.id:
                #Reaktionen im Dorfversammlungschannel
                if payload.channel_id == (await self.game_logic.helper.get_dorfversammlung_channel(payload.guild_id, "text")).id:
                    if str(payload.emoji) == "✅" :
                        if message == self.msg_end_safety_question:
                                await message.channel.send(self.text.get_game_end_text(), delete_after=3)
                                await self.game_logic.end_game(payload.guild_id)
                                self.game_started = False
                        elif message == self.game_logic.prepgame.msg_confirm_selection:
                            self.roles_confirmed = True
                            await self.game_logic.prepgame.send_erzaehler_commands()
                            await self.game_logic.create_role_objects()
                    elif str(payload.emoji) == "❌" :
                        if message == self.msg_end_safety_question:
                            await message.channel.send("Das Spiel wird NICHT beendet.", delete_after=5)
                            await self.msg_end_safety_question.delete()
                        elif message == self.game_logic.prepgame.msg_confirm_selection:
                                await message.channel.send(self.game_logic.text.get_confirm_menu_dict()['divider'] + "\nBitte wiederhole deine Auswahl")
                                self.game_logic.prepgame.character_list = []
                                self.game_logic.prepgame.count_werwolf = 0
                                await self.game_logic.prepgame.character_menu()


                    elif message == self.game_logic.voting_system.vote_embed:
                        await self.game_logic.voting_system.vote_embed.remove_reaction(str(payload.emoji),  self.game_logic.erzaehler)
                    elif str(payload.emoji) == "👍":
                        await message.remove_reaction(str(payload.emoji), self.game_logic.erzaehler)
                    else:
                        await self.game_logic.prepgame.character_selection(payload.emoji)
                else:
                    await message.remove_reaction(str(payload.emoji),self.game_logic.erzaehler)
            else:
                #Reaktionen im Dorfversammlungschannel
                if payload.channel_id == (await self.game_logic.helper.get_dorfversammlung_channel(payload.guild_id, "text")).id:

                    if message == self.game_logic.prepgame.msg_join_game:
                        #Thumbsup Reaktion von Mitspielern
                        if str(payload.emoji) == "👍" and not self.game_started_menu:
                                await self.game_logic.prepgame.add_player(user, payload.guild_id)
                                if user.voice.channel != None:
                                    # temp_sql_return_val = self.game_logic.sql_db.update_where_from_table("spieler", "Previous_Voice_Channel", user.voice.channel.id,'Discord_ID', user.id)
                                    # print("Set Previous_Voice_Channel by spieler: ", temp_sql_return_val)
                                    # self.game_logic.previous_voice_channel[payload.user_id] = user.voice.channel
                                    await user.move_to(await self.game_logic.helper.get_dorfversammlung_channel(payload.guild_id, "voice"))
                        elif str(payload.emoji) == "🤔":
                            text_dict = self.game_logic.text.get_text_dict()
                            for text in text_dict:
                                await self.game_logic.helper.send_a_message(user, text_dict[text])
                
                    
                    if self.game_voting_started:
                        if message == self.game_logic.voting_system.vote_embed:
                                if str(payload.emoji) == "1️⃣":
                                    await self.game_logic.voting_system.vote_player(payload.user_id, 1)
                                elif str(payload.emoji) == "2️⃣":
                                    await self.game_logic.voting_system.vote_player(payload.user_id, 2)
                                elif str(payload.emoji) == "3️⃣":
                                    await self.game_logic.voting_system.vote_player(payload.user_id, 3)
                # Reactions von Werwölfen                    
                elif 'Werwolf' in self.game_logic.character_assignment[payload.user_id].role_name:
                    if message == self.game_logic.character_assignment[payload.user_id].voting_system.pro_start_question:
                        #Thumbsup Reaktion von Mitspielern
                        if str(payload.emoji) == "👍" and self.game_night_started:
                            await self.game_logic.character_assignment[payload.user_id].voting_system.count_pros()
                    if message == self.game_logic.character_assignment[payload.user_id].voting_system.vote_embed:
                            if str(payload.emoji) == "1️⃣":
                                await self.game_logic.character_assignment[payload.user_id].voting_system.vote_player(payload.user_id, 1)
                            elif str(payload.emoji) == "2️⃣":
                                await self.game_logic.character_assignment[payload.user_id].voting_system.vote_player(payload.user_id, 2)
                            elif str(payload.emoji) == "3️⃣":
                                await self.game_logic.character_assignment[payload.user_id].voting_system.vote_player(payload.user_id, 3)
                                # else:
                            #     await self.game_logic.voting_system.vote_embed.remove_reaction(str(payload.emoji),  self.game_logic.erzaehler)

                    
        
                

    # Wenn eine Reaktion entfernt wird
    async def on_raw_reaction_remove(self, payload):
        dorfversammlung_text = await self.game_logic.helper.get_dorfversammlung_channel(payload.guild_id, "text")
        message = await dorfversammlung_text.fetch_message(payload.message_id)
        user = await self.game_logic.helper.user_id_to_user(payload.user_id)

        #Ignoriert Reaktionen vom Bot
        if payload.user_id == self.user.id:
            return
        
        if payload.user_id == self.game_logic.erzaehler.id:
            #Reaktionen im Dorfversammlungschannel
            if payload.channel_id == self.game_logic.prepgame.dorfversammlung_text.id:
                if message != self.game_logic.voting_system.vote_embed:
                    await self.game_logic.prepgame.character_selection_remove(payload.emoji)
                
        else: # Mitspieler
            if payload.channel_id == dorfversammlung_text.id:
                if not self.game_started_menu:
                    if str(payload.emoji) == "👍":
                        if user.voice.channel == await self.game_logic.helper.get_dorfversammlung_channel(payload.guild_id, "voice"):
                            previous_channel_id = self.game_logic.sql_db.select_where_from_table('Previous_Voice_Channel', 'spieler','Discord_ID', user.id)
                            print("Get previous_channel_id: ", previous_channel_id)
                            previous_channel = await self.game_logic.helper.channel_id_to_channel(previous_channel_id)
                            await user.move_to(previous_channel)
                            await user.edit(mute = False, reason = "Das Werwolfspiel wurde beendet")
                            await self.game_logic.prepgame.remove_player(user, payload.guild_id)
                if self.game_voting_started:
                    if message == self.game_logic.voting_system.vote_embed:
                            if str(payload.emoji) == "1️⃣":
                                try:
                                    await self.game_logic.voting_system.unvote_player(payload.user_id, 1)
                                except:
                                    pass
                            elif str(payload.emoji) == "2️⃣":
                                try:
                                    await self.game_logic.voting_system.unvote_player(payload.user_id, 2)
                                except:
                                    pass
                            elif str(payload.emoji) == "3️⃣":
                                try:
                                    await self.game_logic.voting_system.unvote_player(payload.user_id, 3)
                                except:
                                    pass
            # Reactions von Werwölfen                        
            elif 'Werwolf' in self.game_logic.character_assignment[message.author.id].role_name:    
                if message == self.game_logic.character_assignment[payload.user_id].voting_system.vote_embed:
                            if str(payload.emoji) == "1️⃣":
                                try:
                                    await self.game_logic.character_assignment[payload.user_id].voting_system.unvote_player(payload.user_id, 1)
                                except:
                                    pass
                            elif str(payload.emoji) == "2️⃣":
                                try:
                                    await self.game_logic.character_assignment[payload.user_id].voting_system.unvote_player(payload.user_id, 2)
                                except:
                                    pass
                            elif str(payload.emoji) == "3️⃣":
                                try:
                                    await self.game_logic.character_assignment[payload.user_id].voting_system.unvote_player(payload.user_id, 3)
                                except:
                                    pass            	
                        

    #async def on_disconnect(self):
    #    self.game_logic.end_game()
    


    # async def on_voice_state_update(self,member,before,after):
    #    if self.game_night_started:
    #        if after.channel == self.game_logic.prepgame.dorfversammlung_voice and member != self.game_logic.erzaehler and before.mute == False:
    #            await member.edit(mute = True, reason = "Werwolfchannel während der Nacht betreten.")
    #    if before.channel == self.game_logic.prepgame.dorfversammlung_voice and before.mute == True:
    #        await member.edit(mute = False, reason = "Der Werwolfchannel wurde verlassen.")