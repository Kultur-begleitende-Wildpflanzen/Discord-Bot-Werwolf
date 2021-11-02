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
        
        self.result_magd_available = threading.Event()
    
    # returns the DB table of the relevant gamestates
    def get_mysql_table_spiele(self):
        temp_sql_return_val = self.game_logic.sql_db.select_all_from_table('*', 'spiele')
        print("Get all from 'Spiele': ", temp_sql_return_val)
        return temp_sql_return_val

    def is_game_running(self, guild_id):
        try:
            if guild_id in self.game_logic.sql_db.select_all_from_table('Server_ID', 'spiele')[0]: # Can raise IndexError
                return True
            else:
                return False
        except:
            return False


    # Einloggen
    async def on_ready(self):
        print("Eingeloggt als user: " + str(self.user))
        await self.change_presence(activity=discord.Game(name=f"{self.prefix}help für mehr Informationen"))

    # Wenn Nachricht gepostet wird
    async def on_message(self, message):
        # Ignoriert Nachricht vom Bot
        if message.author == self.user:
            return

        guild_id = message.channel.guild.id

        # Wenn die Nachricht mit dem vorher bestimmten Prefix beginnt
        if message.content.startswith(self.prefix):
            split_msg = message.content[1:].lower().split(' ')

            if self.is_game_running(guild_id):
                # if split_msg[0] == 'start' and split_msg[1] == 'game':
                #     await message.delete(delay=4)
                #     await message.channel.send('Auf diesem Server läuft bereits ein Werwolfspiel!', delete_after=5)

                # Befehle die nur im Dorfversammlungschannel geschrieben werden können
                if message.channel == await self.game_logic.helper.get_dorfversammlung_channel(message.channel.guild.id, "text"):
                    # Erzählerbefehle
                    if message.author == await self.game_logic.helper.get_erzaehler(guild_id):
                        # Befehl zum starten der Charakter Auswahl
                        if split_msg[0] == 'start' and split_msg[1] == 'menu':
                            self.game_logic.sql_db.update_where_from_table("spiele", "Is_Menu", True, "Server_ID", guild_id)
                            await self.game_logic.prepgame.character_menu(guild_id)
                        # Befehl zum beenden des Spiels
                        if split_msg[0] == 'end' and split_msg[1] == 'game':
                            # Sicherheitsfrage
                            dorfversammlung_text = await self.game_logic.helper.get_dorfversammlung_channel(message.channel.guild.id, "text")
                            msg_end_safety_question = await dorfversammlung_text.send(self.text.get_game_end_safety_question_text())
                            self.game_logic.sql_db.update_where_from_table('temp_tabelle', 'Beschreibung', msg_end_safety_question.id, 'msg_end_safety_question', 'None')
                            for emoji in self.game_logic.text.get_ynemojis():
                                await self.msg_end_safety_question.add_reaction(emoji)
            
            # Befehle die ausgeführt werden können, wenn kein Spiel gestartet ist
            else:
                # Hilfebefehl
                if split_msg[0] == 'help':
                    await message.channel.send(self.text.get_help_text())
                    
                # Befehl zum starten eines Spiels
                if split_msg[0] == 'start' and split_msg[1] == 'game':
                        await message.delete(delay=4)
                        await message.channel.send('Neues Werwolfspiel wird gestartet.', delete_after=5)

                        temp_sql_return_val = self.game_logic.sql_db.insert('spiele', message.channel.guild.id, message.author.id)
                        print("Insert new Spiel in 'Spiele': ", temp_sql_return_val)
                        
                        await self.game_logic.new_game(guild_id)
    



    # Wenn eine Reaktion hinzugeuegt wird
    async def on_raw_reaction_add(self, payload):
        #Ignoriert Reaktionen vom Bot
        if payload.user_id == self.user.id:
            return
                
        guild_id = payload.guild_id

        if self.is_game_running(guild_id):
            guild = await self.game_logic.helper.guild_id_to_guild(guild_id)
            channel = await self.game_logic.helper.channel_id_to_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            user = await self.game_logic.helper.user_id_to_user(guild_id, payload.user_id)
            erzaehler = await self.game_logic.helper.get_erzaehler(guild_id)
    
            
            if payload.user_id == erzaehler.id:
                #Reaktionen im Dorfversammlungschannel
                if channel.id == (await self.game_logic.helper.get_dorfversammlung_channel(payload.guild_id, "text")).id:
                    if str(payload.emoji) == "✅":
                        if message == self.game_logic.helper.message_id_to_message((await self.game_logic.helper.get_dorfversammlung_channel(payload.guild_id, "text")).id, (self.game_logic.sql_db.select_where_from_table('Wert', 'temp_tabelle', 'Spiel_ID', self.game_logic.helper.get_spielID_by_guildID(guild_id), 'Beschreibung', 'msg_end_safety_question')[0][0])):
                                await message.channel.send('Das Werwolfspiel wird beendet. Alle Kanäle und Rollen werden entfernt', delete_after=3)
                                await self.game_logic.end_game(guild_id)
                        elif message == self.game_logic.prepgame.msg_confirm_selection:
                            self.roles_confirmed = True
                            await self.game_logic.prepgame.send_erzaehler_commands()
                            await self.game_logic.create_role_objects()

                    elif str(payload.emoji) == "❌":
                        if message == self.msg_end_safety_question:
                            await message.channel.send("Das Spiel wird NICHT beendet.", delete_after=5)
                            await self.msg_end_safety_question.delete()
                        elif message == self.game_logic.prepgame.msg_confirm_selection:
                                await message.channel.send(self.game_logic.text.get_confirm_menu_dict()['divider'] + "\nBitte wiederhole deine Auswahl")
                                self.game_logic.prepgame.character_list = []
                                self.game_logic.prepgame.count_werwolf = 0
                                await self.game_logic.prepgame.character_menu()

                    #elif message == self.game_logic.voting_system.vote_embed:
                    #    await self.game_logic.voting_system.vote_embed.remove_reaction(str(payload.emoji),  self.game_logic.erzaehler)

                    elif str(payload.emoji) == "👍":
                        await message.remove_reaction(str(payload.emoji), self.game_logic.erzaehler)
                        
                    else:
                        await self.game_logic.prepgame.character_selection(payload)
                else:
                    await message.remove_reaction(str(payload.emoji),self.game_logic.erzaehler)
            # Wenn nicht der Erzähler die Reaktion hinzugefügt hat:
            else:
                #Reaktionen im Dorfversammlungschannel
                if payload.channel_id == (await self.game_logic.helper.get_dorfversammlung_channel(guild_id, "text")).id:
                    if message == self.game_logic.prepgame.msg_join_game:
                        #Thumbsup Reaktion von Mitspielern
                        if str(payload.emoji) == "👍" and not (self.game_logic.sql_db.select_where_from_table("Is_Menu", "spiele","Server_ID", guild_id)[0][0]):
                                await self.game_logic.prepgame.add_player(user, payload.guild_id)
                                if user.voice.channel != None:
                                    await user.move_to(await self.game_logic.helper.get_dorfversammlung_channel(payload.guild_id, "voice"))
                        elif str(payload.emoji) == "🤔":
                            text_dict = self.game_logic.text.get_text_dict()
                            for text in text_dict:
                                await self.game_logic.helper.send_a_message(user, text_dict[text])


    # Wenn eine Reaktion entfernt wird
    async def on_raw_reaction_remove(self, payload):

        guild_id = payload.guild_id
        dorfversammlung_text = await self.game_logic.helper.get_dorfversammlung_channel(guild_id, "text")
        message = await dorfversammlung_text.fetch_message(payload.message_id)
        user = await self.game_logic.helper.user_id_to_user(guild_id, payload.user_id)
        erzaehler = await self.game_logic.helper.get_erzaehler(guild_id)

        #Ignoriert Reaktionen vom Bot
        if payload.user_id == self.user.id:
            return
        
        if payload.user_id == erzaehler.id:
            #Reaktionen im Dorfversammlungschannel
            if payload.channel_id == dorfversammlung_text.id:
                #if message != self.game_logic.voting_system.vote_embed:
                await self.game_logic.prepgame.character_selection_remove(payload)

                
        else: # Mitspieler
            if payload.channel_id == dorfversammlung_text.id:
                if not (self.game_logic.sql_db.select_where_from_table("Is_Menu", "spiele","Server_ID", guild_id)[0][0]):
                    if str(payload.emoji) == "👍":
                        if user.voice.channel == await self.game_logic.helper.get_dorfversammlung_channel(payload.guild_id, "voice"):
                            previous_channel_id = self.game_logic.sql_db.select_where_from_table('Previous_Voice_Channel', 'spieler','Discord_ID', user.id)[0][0]
                            print("Get previous_channel_id: ", previous_channel_id)
                            previous_channel = await self.game_logic.helper.channel_id_to_channel(previous_channel_id)
                            await user.move_to(previous_channel)
                            await user.edit(mute = False, reason = "Der Spieler hat das Werwolfspiel verlassen")
                            await self.game_logic.prepgame.remove_player(user, payload.guild_id)        	
                