import discord
import time


class PrepareGame():

    game_category = None
    gameLogic = None
    character_list =[]
    msg_confirm_selection = None
    last_reaction = None

    def __init__(self, logic):
        # Konstrucktor Teil
        self.game_logic = logic
        self.guild = self.game_logic.guild


    #Erstellt Main-Channel und Rollen und setzt den Erzaehler
    async def join_game(self, guild_id):
        erzaehler = await self.game_logic.helper.get_erzaehler(guild_id)
        print("Get Erzaehler: ", erzaehler)
        
        #dorfversammlung_voice = await self.game_logic.helper.get_dorfversammlung_channel(guild_id, "v")

        await self.create_discord_roles(guild_id)
        await self.create_discord_channels(guild_id)

        dorfversammlung_text = await self.game_logic.helper.get_dorfversammlung_channel(guild_id, "text")
        print("Dorfversammlung_text: ", dorfversammlung_text)

        # weist dem Erzaehler seine Rolle zu
        self.erzaehler_for_role = await self.game_logic.helper.user_id_to_user(guild_id, erzaehler.id)
        await self.erzaehler_for_role.add_roles(await self.game_logic.helper.role_id_to_role(self.game_logic.sql_db.select_where_from_table('DC_Rolle_Erzaehler_ID', "spiele", 'Server_ID', guild_id)[0][0], guild_id))

        

        if erzaehler.voice != None:
            # self.game_logic.previous_voice_channel[self.game_logic.erzaehler.id] = self.game_logic.erzaehler.voice.channel
            tempvar = self.game_logic.sql_db.update_where_from_table('spiele', 'Erzaehler_Previous_Channel', erzaehler.voice.channel.id, 'Erzaehler_ID', erzaehler.id)
            print("Set Erzaehler Previous Channel: ", tempvar)
            temp_voice = await self.game_logic.helper.get_dorfversammlung_channel(guild_id, "voice")
            print("Get VoiceChannel: ", temp_voice)
            await erzaehler.move_to(temp_voice)

		
        # join message
        self.msg_join_game = await dorfversammlung_text.send(self.game_logic.text.get_game_join_text())
        await self.msg_join_game.add_reaction("👍")
        await self.msg_join_game.add_reaction("🤔")



    # erstellt alle nötigen Discord-Rollen
    async def create_discord_roles(self, guild_id):
        guild = await self.game_logic.helper.guild_id_to_guild(guild_id)
        d_rolle_erzaehler = await guild.create_role(
            name='erzaehler', color=discord.colour.Color(0xffffff))

        d_rolle_lebendig = await guild.create_role(
            name='lebendig', color=discord.colour.Color(0x2ecc71))
        d_rolle_tot = await guild.create_role(
            name='tot', color=discord.colour.Color(0xe74c3c))
        
        self.d_rolle_everyone = guild.roles[0]

        tempvar = self.game_logic.sql_db.update_where_from_table('spiele', 'DC_Rolle_Lebendig_ID', d_rolle_lebendig.id, 'Server_ID', guild_id)
        print("Set DC_Rolle_Lebendig_ID: ", tempvar)
        tempvar = self.game_logic.sql_db.update_where_from_table('spiele', 'DC_Rolle_Tot_ID', d_rolle_tot.id, 'Server_ID', guild_id)
        print("Set DC_Rolle_Tot_ID: ", tempvar)
        tempvar = self.game_logic.sql_db.update_where_from_table('spiele', 'DC_Rolle_Erzaehler_ID', d_rolle_erzaehler.id, 'Server_ID', guild_id)
        print("Set DC_Rolle_Erzaehler_ID: ", tempvar)
    


    async def create_discord_channels(self, guild_id):
        guild = await self.game_logic.helper.guild_id_to_guild(guild_id)
        category_id = self.game_logic.sql_db.select_where_from_table('Discord_Kategorie', 'spiele', 'Server_ID', guild_id)[0][0]
        game_category = discord.utils.get(guild.categories, id=category_id)
        print(game_category)

        # erstellt Text-Channel der Dorfversammlung
        dorfversammlung_text = await guild.create_text_channel('dorfversammlung', category=game_category)
        self.game_logic.sql_db.update_where_from_table('spiele', 'Dorfversammlung_Text', dorfversammlung_text.id, 'Server_ID', guild_id)
        d_rolle_erzaehler = await self.game_logic.helper.role_id_to_role(self.game_logic.sql_db.select_where_from_table('DC_Rolle_Erzaehler_ID', "spiele", 'Server_ID', guild_id)[0][0], guild_id)
        d_rolle_lebendig = await self.game_logic.helper.role_id_to_role(self.game_logic.sql_db.select_where_from_table('DC_Rolle_Lebendig_ID', "spiele", 'Server_ID', guild_id)[0][0], guild_id)
        d_rolle_tot = await self.game_logic.helper.role_id_to_role(self.game_logic.sql_db.select_where_from_table('DC_Rolle_Tot_ID', "spiele", 'Server_ID', guild_id)[0][0], guild_id)
        d_rolle_everyone = (await self.game_logic.helper.guild_id_to_guild(guild_id)).roles[0]

        await dorfversammlung_text.set_permissions(d_rolle_erzaehler, read_messages=True, send_messages=True)
        await dorfversammlung_text.set_permissions(d_rolle_lebendig, read_messages=True, send_messages=False)
        await dorfversammlung_text.set_permissions(d_rolle_tot, read_messages=True, send_messages=False)
        await dorfversammlung_text.set_permissions(d_rolle_everyone, read_messages=True, send_messages=False)
        
        # erstellt Voice-Channel des Dorfversammlung
        dorfversammlung_voice = await guild.create_voice_channel('Dorf', category=game_category)
        self.game_logic.sql_db.update_where_from_table('spiele', 'Dorfversammlung_Voice', dorfversammlung_voice.id, 'Server_ID', guild_id)
        await dorfversammlung_voice.set_permissions(d_rolle_erzaehler, connect=True, speak=True)
        await dorfversammlung_voice.set_permissions(d_rolle_lebendig, connect=True, speak=True)
        await dorfversammlung_voice.set_permissions(d_rolle_tot, connect=True, speak=False)
        await dorfversammlung_voice.set_permissions(d_rolle_everyone, connect=False)
        
        # erstellt Text-Channel für den Erzähler
        erzaehler_text = await guild.create_text_channel('erzaehler', category=game_category)
        self.game_logic.sql_db.update_where_from_table('spiele', 'Erzaehler_Channel', erzaehler_text.id, 'Server_ID', guild_id)
        await erzaehler_text.set_permissions(d_rolle_erzaehler, read_messages=True, send_messages=True)
        await erzaehler_text.set_permissions(d_rolle_everyone, read_messages=False, send_messages=False)

        # await self.create_how_to_play_channel(guild_id)



    async def create_how_to_play_channel(self, guild_id):
        guild = await self.game_logic.helper.guild_id_to_guild(guild_id)
        category_id = self.game_logic.sql_db.select_where_from_table('Discord_Kategorie', 'spiele', 'Server_ID', guild_id)
        game_category = await discord.utils.get(guild.categories, id=category_id)
        
        self.how_to_play_text = await guild.create_text_channel('how_to_play', category=game_category)
        await self.how_to_play_text.set_permissions(self.d_rolle_everyone, read_messages=True, send_messages=False)

        self.common_text_dict = self.game_logic.text.get_common_text_dict()
        for text in self.common_text_dict:
            await self.how_to_play_text.send(self.common_text_dict[text])


    # Fuegt Spieler als lebendig zur Spielerliste hinzu
    async def add_player(self, user, guild_id):
        spiel_id = self.game_logic.sql_db.select_where_from_table("Spiel_ID","spiele", "Server_ID", guild_id)[0][0]
        
        # self.game_logic.playerStatus[user.id] = 1
        temp_sql_return_val = self.game_logic.sql_db.insert("spieler", spiel_id, user.id, await self.game_logic.helper.nick_name_module(user=user), user.voice.channel.id)
        print("Add new player to db + game: ", temp_sql_return_val)
        await user.add_roles(await self.game_logic.helper.role_id_to_role(self.game_logic.sql_db.select_where_from_table('DC_Rolle_Lebendig_ID', "spiele", 'Server_ID', guild_id)[0][0], guild_id))


    # Entfernt Spieler von der Spielerliste
    async def remove_player(self, user, guild_id):
        # spiel_id = self.game_logic.sql_db.select_where_from_table("Spiel_ID","spiele", "Server_ID", guild_id)[0][0]

        # self.game_logic.playerStatus.pop(user.id, None)
        self.game_logic.sql_db.delete_where_from_table('spieler', 'Discord_ID', user.id)
        await user.remove_roles(await self.game_logic.helper.role_id_to_role(self.game_logic.sql_db.select_where_from_table('DC_Rolle_Lebendig_ID', "spiele", 'Server_ID', guild_id)[0][0], guild_id))


    # Sendet Texte und Reaktionen fuer die Charakterauswahl
    async def character_menu(self, guild_id):
        # self.player_count = 17
        player_count = self.game_logic.sql_db.count_entries_from_table("Discord_ID", "spieler", "Spiel_ID", self.game_logic.sql_db.select_where_from_table("Spiel_ID", "spiele","Server_ID", guild_id)[0][0])
        print(player_count)
        werwolf_count_advice = self.calculate_werwolf_count_advice(player_count)
        dorfversammlung_text = await self.game_logic.helper.get_dorfversammlung_channel(guild_id, "text")
        msg_player_role_count_text_content = self.game_logic.text.get_game_player_role_count_text()
        msg_player_role_count_text = await dorfversammlung_text.send(msg_player_role_count_text_content.format(player_count, self.game_logic.sql_db.count_entries_from_table("Rollen_ID", "temp_rollen_im_spiel", "Spiel_ID", self.game_logic.sql_db.select_where_from_table("Spiel_ID", "spiele","Server_ID", guild_id)[0][0])))
        self.game_logic.sql_db.insert("temp_tabelle",self.game_logic.sql_db.select_where_from_table("Spiel_ID", "spiele","Server_ID", guild_id)[0][0], "msg_player_role_count_text_content", msg_player_role_count_text_content  )
        self.game_logic.sql_db.insert("temp_tabelle",self.game_logic.sql_db.select_where_from_table("Spiel_ID", "spiele","Server_ID", guild_id)[0][0], "msg_player_role_count_text_ID", msg_player_role_count_text.id)

        character_menu_text = self.game_logic.text.get_character_menu_text()
        for text in character_menu_text:
            emojis = self.game_logic.text.get_character_menu_emojis(text)
            if text == character_menu_text[0]:
                message = await dorfversammlung_text.send(text.format(werwolf_count_advice))
                self.game_logic.sql_db.insert("temp_tabelle",self.game_logic.sql_db.select_where_from_table("Spiel_ID", "spiele","Server_ID", guild_id)[0][0], "msg_werwolf_text_ID", message.id  )
                self.game_logic.sql_db.insert("temp_tabelle",self.game_logic.sql_db.select_where_from_table("Spiel_ID", "spiele","Server_ID", guild_id)[0][0], "msg_werwolf_text_content", text)
            else:
                message = await dorfversammlung_text.send(text)
            for emoji in emojis:
                await message.add_reaction(emoji)
    

    # Berechnet einen groben Vorschlag der Werwolfanzahl
    def calculate_werwolf_count_advice(self, player_count):
        if player_count <= 4:
            return 1
        elif player_count <= 8:
            return 2
        elif player_count <= 12:
            return 3
        elif player_count <= 16:
            return 4
        else:
            return 5
        
    #Erstellen der Rollenliste bei hinzufuegen einere Reaktion im character_menu
    async def character_selection(self, reaction):
        guild_id = reaction.guild_id
        spiel_id = self.game_logic.sql_db.select_where_from_table("Spiel_ID", "spiele","Server_ID", guild_id)[0][0]
        player_count = self.game_logic.sql_db.count_entries_from_table("Discord_ID", "spieler", "Spiel_ID", self.game_logic.sql_db.select_where_from_table("Spiel_ID", "spiele","Server_ID", guild_id)[0][0])
        msg_werwolf_text = await self.game_logic.helper.message_id_to_message(reaction.channel_id, self.game_logic.sql_db.select_where_from_table("Wert", "temp_tabelle", "Beschreibung","msg_werwolf_text_ID","Spiel_ID", spiel_id)[0][0])
        msg_werwolf_text_content = self.game_logic.sql_db.select_where_from_table("Wert", "temp_tabelle", "Beschreibung","msg_werwolf_text_content","Spiel_ID", spiel_id)[0][0]
        msg_player_role_count_text = await self.game_logic.helper.message_id_to_message(reaction.channel_id, self.game_logic.sql_db.select_where_from_table("Wert", "temp_tabelle", "Beschreibung","msg_player_role_count_text_ID","Spiel_ID", spiel_id)[0][0])
        msg_player_role_count_text_content = self.game_logic.sql_db.select_where_from_table("Wert", "temp_tabelle", "Beschreibung","msg_player_role_count_text_content","Spiel_ID", spiel_id)[0][0]
        edict = self.game_logic.text.get_emojidict()

        # Geht alle Emojis in der Emojiliste durch und prüft, ob das Emoji der Reaktion gleich ist
        for emoji in edict:
            if emoji == str(reaction.emoji):
                # Wenn an der Stelle Emoji eine Liste als Wert hinterlegt ist, handelt es sich um die Werwölfe und die Liste  wird dementsprechend angepasst
                if type(edict[emoji]) == list:
                    
                    # Wenn es eine letzte Reaktion gab, soll diese entfernt werden
                    if self.last_reaction != None:
                        await msg_werwolf_text.remove_reaction(self.last_reaction, await self.game_logic.helper.get_erzaehler(guild_id))
                        self.last_reaction = emoji
                    else:
                        self.last_reaction = emoji
                    #Sucht alle Einträge in der Charakterliste die werwolf sind, entfernt diese und setzt an Hand der neuen Reaktion diese neu
                    self.game_logic.sql_db.delete_where_from_table("temp_rollen_im_spiel", "Spiel_ID", spiel_id, "Rollen_ID", 1 )
                    for rollen_id in edict[emoji]:
                        self.game_logic.sql_db.insert('temp_rollen_im_spiel', spiel_id, rollen_id)

                    #Aktualisiert die Anzahl an ausgewählten Werwölfen im character_menu
                    werwolf_count = self.game_logic.sql_db.count_entries_from_table("Discord_ID", "spieler", "Spiel_ID", spiel_id, "Rollen_ID", 1)
                    await msg_werwolf_text.edit(content=(msg_werwolf_text_content + '\nAnzahl der Werwölfe: ' + str(werwolf_count)))

                else:
                    # Fügt den nicht Werwolf Charakter zur character_list hinzu
                    self.game_logic.sql_db.insert('temp_rollen_im_spiel', spiel_id, edict[emoji])

        #Dynamische Anzeige der Anzahl der bisher gewählten Rollen
        rollen_count = self.game_logic.sql_db.count_entries_from_table("Rollen_ID", "temp_rollen_im_spiel", "Spiel_ID", spiel_id)
        await msg_player_role_count_text.edit(content=(msg_player_role_count_text_content.format(player_count, rollen_count)))
        print(rollen_count)
        # msg_player_role_count_text_content

    # Entfernen von Rollen aus der Rollenliste bei entfernen einer Reaktion im character_menu
    async def character_selection_remove(self, reaction):
        guild_id = reaction.guild_id
        spiel_id = self.game_logic.sql_db.select_where_from_table("Spiel_ID", "spiele","Server_ID", guild_id)[0][0]
        player_count = self.game_logic.sql_db.count_entries_from_table("Discord_ID", "spieler", "Spiel_ID", self.game_logic.sql_db.select_where_from_table("Spiel_ID", "spiele","Server_ID", guild_id)[0][0])
        msg_player_role_count_text = await self.game_logic.helper.message_id_to_message(reaction.channel_id,self.game_logic.sql_db.select_where_from_table("Wert", "temp_tabelle", "Beschreibung","msg_player_role_count_text_ID","Spiel_ID", spiel_id)[0][0])
        msg_player_role_count_text_content = self.game_logic.sql_db.select_where_from_table("Wert", "temp_tabelle", "Beschreibung","msg_player_role_count_text_content","Spiel_ID", spiel_id)[0][0]
        edict = self.game_logic.text.get_emojidict()
        print("Nach Variablen Abfrage")

        # guckt alle emojies durch
        for emoji in edict:
            # print("In For-Schleife | Emoji: ", emoji)
            if emoji == str(reaction.emoji):
                # wenn Eintrag keine Liste, entferne diesen Eintrag
                if type(edict[emoji]) == list:
                    pass
                else:
                    self.game_logic.sql_db.delete_where_from_table("temp_rollen_im_spiel", "Spiel_ID", spiel_id, "Rollen_ID", edict[emoji] )

                    
            # verändert die gezeigte Anzahl der ausgewählten Rollen
        rollen_count = self.game_logic.sql_db.count_entries_from_table("Rollen_ID", "temp_rollen_im_spiel", "Spiel_ID", spiel_id)
        await msg_player_role_count_text.edit(content=(msg_player_role_count_text_content.format(player_count, rollen_count)))
        print(rollen_count)
    
    #Charakterauswahl zusammenfassen
    async def confirm_selection(self, guild_id):
        spiel_id = self.game_logic.sql_db.select_where_from_table("Spiel_ID", "spiele","Server_ID", guild_id)[0][0]
        # kopiert die character Liste um diese manipulieren zu können
        temp_character_list = self.game_logic.sql_db.select_where_from_table("r.Rollen_Name", "temp_rollen_im_spiel tris,rollen r", "tris.Spiel_ID", spiel_id,"tris.Rollen_ID","r.Rollen_ID" )
        # ersetzt die Rollenbezeichnungen durch richtige Namen
        for entry in temp_character_list:
            namedict = self.game_logic.text.get_name_dict()
            if entry in namedict:
                temp_character_list[temp_character_list.index(entry)] = namedict[entry]
        
        # Ersetzt die werwolf Einträge durch einen Einzelnen Eintrag mit Anzahl der ausgewählten Werwölfe
        werwolf = 'werwolf'
        if self.count_werwolf > 0:
            indexes = [i for i, x in enumerate(temp_character_list) if x == werwolf]
            for index in reversed(indexes):
                temp_character_list.pop(index)
            temp_character_list.append(("Werwölfe: " + str(self.count_werwolf)))

        characterstr = ""
        # Erstellt aus der Liste der Rollen einen String
        for role in temp_character_list:
            characterstr += role + "\n"
        
        self.count_members = len(self.game_logic.playerStatus)
        self.count_roles = len(self.character_list)
        confirm_menu_dict = self.game_logic.text.get_confirm_menu_dict()
        dorfversammlung_text = await self.game_logic.helper.get_dorfversammlung_channel(guild_id, "text")
        #Wenn es weniger Spieler als Rollen gibt soll die Auswahl wiederholt werden
        if self.count_members < self.count_roles:
            await dorfversammlung_text.send(confirm_menu_dict['many'].format(self.count_members, self.count_roles) + characterstr + confirm_menu_dict['divider'] )
            self.character_list = []
            self.count_werwolf = 0
            time.sleep(5)
            await self.character_menu()
        # Wenn es mehr Spieler als Rollen gibt, werden Dorfbewohner hinzugefuegt. Der Spielleiter kann sich entscheiden, ob er mit der Auswahl zufrieden ist
        elif self.count_members > self.count_roles:
            diffrence = self.count_members - self.count_roles
            for i in range(diffrence):
                self.character_list.append('dorfbewohner')
            characterstr += ("Dorfbewohner: " + str(diffrence))
            self.msg_confirm_selection = await dorfversammlung_text.send((confirm_menu_dict['less'] + characterstr))
            for emoji in self.game_logic.text.get_ynemojis():
                await self.msg_confirm_selection.add_reaction(emoji)
        # Wenn es die gleiche Anzahl Spieler und Rollen gibt, werden diese Zusammengefasst. Der Spielleiter kann sich entscheiden, ob er mit der Auswahl zufrieden ist
        else:
            self.msg_confirm_selection = await dorfversammlung_text.send((confirm_menu_dict['perfect'] + characterstr))
            for emoji in self.game_logic.text.get_ynemojis():
                await self.msg_confirm_selection.add_reaction(emoji)

        
    async def send_erzaehler_commands(self):
        await self.erzaehler_text.send(self.game_logic.text.get_erzaehler_commands_text())