import discord
import time
import random

class VotingSystem(object):
    text_channel = None

    nominated_players = []
    vote_embed = None

    vote_one = []
    vote_two = []
    vote_three = []

    start_time = None
    end_time = None

    voting_time = 30
    remaining_time = voting_time

    pro_start = 0
    werwolf_voter_id = None
    

    def __init__(self, game_logic, text_channel):
        self.game_logic = game_logic
        self.text_channel = text_channel


    # nominiert einen lebendigen Spieler, wenn nicht schon 3 Spieler angeklagt sind
    async def nominate_player(self, player, voter_id):
        print("nominate_player " + str(self.nominated_players))
        # nick-name module
        player_name = await self.game_logic.helper.nick_name_module(user=player)
        if len(self.nominated_players) < 3:
            if self.game_logic.prepgame.d_rolle_lebendig in player.roles:
                if player not in self.nominated_players:
                    self.nominated_players.append(player)

                    await self.text_channel.send("Nominierter Spieler: " + str(player_name))
                    # check if author of message is Werwolf and if it's night
                    if 'Werwolf' in self.game_logic.character_assignment[voter_id].role_name and self.game_logic.client.game_night_started:
                        self.werwolf_voter_id = voter_id
                        await self.start_question()
            else:
                await self.text_channel.send(str(player_name) + " ist nicht mehr im Spiel.")
        else:
            await self.text_channel.send("Es sind schon drei Spieler nominiert.")
        

    # Fragt die Werwölfe ob alle ausgewaehlt wurden
    async def start_question(self):
        self.pro_start_question = await self.text_channel.send("Sind das alle zur Auswahl?")
        await self.pro_start_question.add_reaction("👍") 

    
    # aktiviert das Voting, wenn über die Hälfte der Werwölfe dafür sind
    async def count_pros(self):
        active_werwolf_count = len([i for i in self.game_logic.character_assignment if 'Werwolf' in self.game_logic.character_assignment[i].get_role_name()])
        # print(active_werwolf_count)

        self.pro_start += 1
        if self.pro_start >= active_werwolf_count/2: # die, die die Rolle lebendig haben
            self.pro_start = 0
            await self.start_voting()


    # startet das Voting
    async def start_voting(self):
        # zeigt alle ausgewählten Spieler an
        await self.create_voting_embed()

        # zeigt die verbleibende Zeit an
        msg_remaining_time_text = "Verbleibende Zeit: {}s"
        msg_remaining_time = await self.text_channel.send(msg_remaining_time_text.format(str(self.remaining_time)))
        
        # erneuert jede 5 Sekunden die verbleibende Zeit
        self.start_time = time.time()
        while (time.time() - self.start_time) < self.voting_time:
            self.remaining_time = round(self.voting_time - (time.time() - self.start_time), 0)
            if (self.remaining_time % 5) == 0:
                await msg_remaining_time.edit(content=(msg_remaining_time_text.format(str(self.remaining_time))))
        # starte die Auswertung
        await self.confirm_vote()
    

    # organisiert die Votes der Users
    async def vote_player(self, user_id, vote):
        # checkt ob die Person schon jemanden anderen gevoted hat und entfernt den falls nötig
        if user_id in self.vote_one or user_id in self.vote_two or user_id in self.vote_three:
            try:
                self.vote_one.remove(user_id)
                await self.vote_embed.remove_reaction("1️⃣", await self.game_logic.helper.user_id_to_user(user_id))
            except:
                pass
            try:
                self.vote_two.remove(user_id)
                await self.vote_embed.remove_reaction("2️⃣", await self.game_logic.helper.user_id_to_user(user_id))
            except:
                pass
            try:
                self.vote_three.remove(user_id)
                await self.vote_embed.remove_reaction("3️⃣", await self.game_logic.helper.user_id_to_user(user_id))
            except:
                pass

        # fügt die Person zur neuen Liste hinzu
        if vote == 1:
            self.vote_one.append(user_id)
        elif vote == 2:
            self.vote_two.append(user_id)
        elif vote == 3:
            self.vote_three.append(user_id)
        # print(self.vote_one, self.vote_two, self.vote_three)


    # Erstellt eine Voting Übersicht für den Erzähler
    async def create_voting_embed(self):
        embed = discord.Embed(
            title = 'Voting'
        )
        emojirange = []
        
        # fügt die Felder zum Embed hinzu, sodass man weis welche Reaktion man drücken muss
        for player in self.nominated_players:
            # nick-name module
            player_name = await self.game_logic.helper.nick_name_module(user=player)
            embed.add_field(name=player_name, value=self.game_logic.text.get_numbered_emojis()[self.nominated_players.index(player)], inline=True)
            emojirange.append(self.nominated_players.index(player))
            # print(emojirange)

        # schreibt das embed in eine Nachricht, sodass darauf automatisch reagiert werden kann
        self.vote_embed = await self.text_channel.send(embed=embed)

        # reagiert mit den emojies für: 1,2,3
        for number in emojirange:
            await self.vote_embed.add_reaction(self.game_logic.text.get_numbered_emojis()[number])

    # bestimmt das Opfer
    async def calc_victim(self):
        all_votes = [self.vote_one, self.vote_two, self.vote_three]
        all_votes_lengh = [len(self.vote_one), len(self.vote_two), len(self.vote_three)]
        number_winner = max(all_votes_lengh)
        indexes_winner = [i for i, value in enumerate(all_votes_lengh) if value == number_winner]

        # wenn Unentschieden herscht
        if len(indexes_winner) > 1:
            if not self.game_logic.client.game_night_started:
                for list_number in indexes_winner:
                    for player_id in all_votes[list_number]:
                        if self.game_logic.character_assignment[player_id].get_hauptmann():
                            winner_person = self.nominated_players[indexes_winner[0]]
                            return winner_person
                return None
            else:
                return None
        else:
            # wenn es ein direktes Opfer gibt
            winner_person = self.nominated_players[indexes_winner[0]]
            return winner_person



    async def confirm_vote(self):
        # keiner darf mehr schreiben
        await self.text_channel.set_permissions(self.game_logic.prepgame.d_rolle_lebendig, send_messages=False)
        print("Das Voting wurde beendet")

        victim = await self.calc_victim()

        # nick-name module
        victim_name = await self.game_logic.helper.nick_name_module(user=victim)
        print(victim_name)

        if victim:
            print("Es gibt ein Opfer")
            # wenn das Opfer von den Werwölfen getötet wurde
            if self.werwolf_voter_id and self.text_channel == self.game_logic.character_assignment[self.werwolf_voter_id].text_channel:
                self.game_logic.playerStatus[victim.id] = 2
                await self.game_logic.character_assignment[self.werwolf_voter_id].text_channel.send(str(victim_name) + " wurde auserwählt.")
                
                await self.clear_all_var()
                print("Werwolf Opfer beendet")

                await self.game_logic.next_role()
            else:
                # Wenn das Opfer am Tag getötet wurde
                self.game_logic.prepgame.game_voting_started = False

                if self.game_logic.client.hauptmann_voting_started == True:
                    self.game_logic.character_assignment[victim.id].set_isHauptmann()
                    self.game_logic.client.hauptmann_voting_started = False
                    self.game_logic.hauptmann_name = victim_name
                    await self.game_logic.prepgame.dorfversammlung_text.send(str(victim_name) + " ist das neue Oberhaupt des Dorfes.")
                    await victim.edit(nick ="Mächtiger Elch" , reason="Wurde als Bürgermeister gewählt")
                    
                    await self.clear_all_var()
                    print("Hauptmann-Voting vorbei")
                else: # wenn Abstimmung am Tag
                    # Wenn Magd
                    if "Magd" in self.game_logic.procedure_list:
                        self.game_logic.character_assignment[self.game_logic.helper.get_id_of_role_name("Magd")].start()
                    else:
                        await self.game_logic.send_death_text(victim)

                    self.game_logic.playerStatus[victim.id] = 2
                    await self.game_logic.pre_kill()
                    
                    await self.clear_all_var()
                    print("Wenn Magd vorbei")
         
        

    # cleared alle wichtigen Variablen
    async def clear_all_var(self):
        print("clear_all_var")
        self.nominated_players.clear()
        print("Cleared nominated_players " + str(self.nominated_players))
        self.vote_embed = None

        self.vote_one.clear()
        self.vote_two.clear()
        self.vote_three.clear()