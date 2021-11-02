import discord


class Helper(object):
    game_logic = None

    def __init__(self, game_logic):
        # super().__init__(loop=loop, **options)
        self.game_logic = game_logic
    

    async def nick_name_module(self, user=None, user_id=None):
        if user:
            if user.nick:
                user_name = user.nick
            else:
                user_name = user.name
            
            return str(user_name)
        elif user_id:
            user = await self.user_id_to_user(user_id)
            return await self.nick_name_module(user=user)
        else:
            print("Keinen User gefunden.")


    async def user_id_to_user(self, guild_id, user_id):
        guild = await self.guild_id_to_guild(guild_id)
        user = await guild.fetch_member(user_id)
        return user

    async def message_id_to_message(self, channel_id, message_id):
        channel = await self.channel_id_to_channel(channel_id)
        message = await channel.fetch_message(message_id)
        return message

    async def channel_id_to_channel(self, channel_id):
        channel = self.game_logic.client.get_channel(channel_id)
        return channel
    
    async def role_id_to_role(self, role_id, guild_id):
        guild = await self.guild_id_to_guild(guild_id)
        role = guild.get_role(role_id)
        return role

    async def guild_id_to_guild(self, guild_id):
        guild = self.game_logic.client.get_guild(guild_id)
        return guild
    
    async def get_spielID_by_guildID(self, guild_id):
        spiel_id = self.game_logic.sql_db.select_where_from_table('Spiel_ID', 'spiele', 'Server_ID', guild_id)[0][0]
        return spiel_id

    async def get_dorfversammlung_channel(self, guild_id, channel_type_inp):
        if channel_type_inp == 't' or channel_type_inp == 'text':
            channel_type = "Text"
        elif channel_type_inp == 'v' or channel_type_inp == 'voice':
            channel_type = "Voice"
        else:
            return None
        
        voice_text = 'Dorfversammlung_' + channel_type
        print("Get Dorfversammlung Channel: ", voice_text)

        channel = await self.channel_id_to_channel(self.game_logic.sql_db.select_where_from_table(voice_text, 'spiele', 'Server_ID', guild_id)[0][0])
        return channel

    async def get_erzaehler(self, guild_id):
        erzaehler_id = self.game_logic.sql_db.select_where_from_table('Erzaehler_ID', 'spiele', 'Server_ID', guild_id)[0][0]
        erzaehler = await self.user_id_to_user(guild_id, erzaehler_id)
        return erzaehler


    # Sendet eine persönliche Nachricht an den Spieler
    async def send_a_message(self, user, message):
        if user.dm_channel == None:
            channel = await user.create_dm()
        else:
            channel = user.dm_channel
        await channel.send(message)


    # Helfer Funktion um player ID einer Rolle zu bekommen
    async def get_id_of_role_name(self, role_name):
        for player_id in self.game_logic.character_assignment.keys():
            if self.game_logic.character_assignment[player_id].get_role_name() == role_name:
                return player_id
            

    # gibt alle lebenden Spielernamen wieder
    async def get_all_alive_names(self):
        all_alive_names = "*NickName -> UserName*\n"
        for user_id in self.game_logic.character_assignment.keys():
            user = await self.user_id_to_user(user_id)
            all_alive_names += (str(await self.nick_name_module(user=user)) + " -> " + str(user.name) + "\n")
        return all_alive_names
    
    #gibt alle zum töten markierten Spieler zurück
    async def get_all_lala(self):
        all_lala = "*NickName -> UserName*\n"
        for user_id in self.game_logic.character_assignment.keys():
            if self.game_logic.playerStatus[user_id] == 2:
                user = await self.user_id_to_user(user_id)
                all_lala += (str(await self.nick_name_module(user=user)) + " -> " + str(user.name) + "\n")
        return all_lala


    #gibt alle Member des Voice Channels in sortierter Reihenfolge zurück
    async def get_sorted_voice_channel_members(self, message=None):
        members_i_id_nick = []
        sorted_members = []
        if message:
            unsorted_members = message.author.voice.channel.members 
        else:
            unsorted_members = self.game_logic.prepgame.dorfversammlung_voice.members 

        for member_index in range(len(unsorted_members)):
            name = await self.nick_name_module(user=unsorted_members[member_index])
            
            members_i_id_nick.append([member_index, unsorted_members[member_index].id, name])
        pre_sorted_members = sorted(members_i_id_nick, key = lambda x: x[2])
        print(pre_sorted_members)

        for member in pre_sorted_members:
            sorted_members.append(unsorted_members[member[0]])
        return sorted_members

    #gibt die lebenden Member des Voicechannels in sortierter Reihenfolge wieder
    async def get_sorted_voice_channel_members_alive(self):
        sorted_voice_channel_members = self.get_sorted_voice_channel_members()

        for member in sorted_voice_channel_members:
            if self.game_logic.prepgame.d_rolle_tod in member.roles:
                sorted_voice_channel_members.remove(member)
        
        return sorted_voice_channel_members
    
    #gibt alle Werwölfe in sortierter Reihenfolge zurück
    async def get_sorted_voice_channel_members_werwolf(self):
        sorted_voice_channel_members_alive = self.get_sorted_voice_channel_members_alive()

        for member in sorted_voice_channel_members_alive:
            if 'werwolf' in self.game_logic.character_assignment[member.id].get_role_name().lower():
                pass
            else:
                sorted_voice_channel_members_alive.remove(member)
        
        return sorted_voice_channel_members_alive