    async def on_raw_reaction_add(self, payload):
        if self.game_started:
            message = await self.game_logic.prepgame.dorfversammlung_text.fetch_message(payload.message_id)
    
            #Ignoriert Reaktionen vom Bot
            if payload.user_id == self.user.id:
                return
            
            
            #Reaktionen im Dorfversammlungschannel
            if payload.channel_id == self.game_logic.prepgame.dorfversammlung_text.id:
                
                if message == self.game_logic.prepgame.msg_join_game:
                    #Thumbsup Reaktion von Mitspielern
                    if str(payload.emoji) == "👍" and not self.game_started_menu:
                        if payload.user_id != self.game_logic.erzaehler.id:
                            await self.game_logic.prepgame.add_player(payload.user_id)
                            user = await self.game_logic.guild.fetch_member(payload.user_id)
                            if user.voice.channel != None:
                                self.game_logic.previous_voice_channel[payload.user_id] = user.voice.channel
                                await user.move_to(self.game_logic.prepgame.dorfversammlung_voice)
                    elif str(payload.emoji) == "🤔" :
                        self.text_dict = self.game_logic.text.get_text_dict()
                        for text in self.text_dict:
                            await self.game_logic.send_a_message(await self.game_logic.guild.fetch_member(payload.user_id), self.text_dict[text])
                if self.game_voting_started:
                    if message == self.game_logic.voting_system.vote_embed:
                        if payload.user_id != self.game_logic.erzaehler.id:
                            if str(payload.emoji) == "1️⃣":
                                await self.game_logic.voting_system.vote_player(payload.user_id, 1)
                            elif str(payload.emoji) == "2️⃣":
                                await self.game_logic.voting_system.vote_player(payload.user_id, 2)
                            elif str(payload.emoji) == "3️⃣":
                                await self.game_logic.voting_system.vote_player(payload.user_id, 3)
                        else:
                            await self.game_logic.voting_system.vote_embed.remove_reaction(str(payload.emoji),self.game_logic.erzaehler)

                # Reaktionen des Erzaehlers
                elif payload.user_id == self.game_logic.erzaehler.id and str(payload.emoji) != "👍":
                    if message == self.msg_end_safety_question:
                        if str(payload.emoji) == "✅" :
                            await message.channel.send(self.text.get_game_end_text(), delete_after=3)
                            await self.game_logic.end_game()
                            self.game_started = False
                        if str(payload.emoji) == "❌" :
                            await message.channel.send("Das Spiel wird NICHT beendet.", delete_after=5)
                            await self.msg_end_safety_question.delete()
                    elif message == self.game_logic.prepgame.msg_confirm_selection:
                        if str(payload.emoji) == "✅" :
                            self.roles_confirmed = True
                            await self.game_logic.prepgame.send_erzaehler_commands()
                            await self.game_logic.create_role_objects()
                        if str(payload.emoji) == "❌" :
                            await message.channel.send(self.game_logic.text.get_confirm_menu_dict()['divider'] + "\nBitte   wiederhole deine Auswahl")
                            self.game_logic_prepgame.character_list = []
                            self.game_logic.prepgame.count_werwolf = 0
                            await self.game_logic.prepgame.character_menu()
                    elif message == self.game_logic.voting_system.vote_embed:
                        await self.game_logic.voting_system.vote_embed.remove_reaction(str(payload.emoji),self.game_logic.erzaehler)
                    else:
                        await self.game_logic.prepgame.character_selection(payload.emoji)
        









# Wenn eine Reaktion entfernt wird
    async def on_raw_reaction_remove(self, payload):
        message = await self.game_logic.prepgame.dorfversammlung_text.fetch_message(payload.message_id)
        #Ignoriert Reaktionen vom Bot
        if payload.user_id == self.user.id:
            return

        #Reaktionen im Dorfversammlungschannel
        elif payload.channel_id == self.game_logic.prepgame.dorfversammlung_text.id:
			
            # Reaktionen des Erzaehlers
            if payload.user_id == self.game_logic.erzaehler.id and str(payload.emoji) != "👍":
                if message == self.game_logic.voting_system.vote_embed:
                    await self.game_logic.voting_system.vote_embed.remove_reaction(str(payload.emoji), self.game_logic.erzaehler)
                else:
                    await self.game_logic.prepgame.character_selection_remove(payload.emoji)

            #Thumbsup Reaktion von Mitspielern
            if str(payload.emoji) == "👍" and not self.game_started_menu:
                if payload.user_id != self.game_logic.erzaehler.id:
                    await self.game_logic.prepgame.remove_player(payload.user_id)
            if self.game_voting_started:
                if message == self.game_logic.voting_system.vote_embed:
                    if payload.user_id != self.game_logic.erzaehler.id:
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