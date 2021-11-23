import discord

class Narrator():
    game_logic = None

    def __init__(self, game_logic):
        self.game_logic = game_logic

    
    # Erstellt eine Zusammenfassung für den Erzähler
    async def create_summary_embed(self):
        embed = discord.Embed(
            title = 'Zusammenfassung - Tag: ' + self.game_logic.anzahl_der_Tage
        )

        person_values = ""
        for user_id in self.playerStatus:
            if self.playerStatus[user_id] == 1:
                person_values += str(await self.game_logic.helper.nick_name_module(user_id=user_id) + "\n")
        
        rolle_values = ""
        for user_id in self.character_assignment:
            rolle_values += (str(self.character_assignment[user_id].get_role_name()) + "\n")

        faehigkeiten_values = ""
        for user_id in self.character_assignment:
            if str(self.character_assignment[user_id].get_abilities()) == "{}":
                faehigkeiten_values += "-\n"
            else:
                faehigkeiten_values += (str(self.character_assignment[user_id].get_abilities()).replace("{", "").replace("'", "").replace("}", "") + "\n")

        embed.add_field(name='Spielername', value=person_values, inline=True)
        embed.add_field(name='Rolle', value=rolle_values, inline=True)
        embed.add_field(name='Fähigkeiten', value=faehigkeiten_values, inline=True)

        await self.game_logic.prepgame.erzaehler_text.send(embed=embed)

    async def send_msg_to_narrator(self, msg):
        await self.game_logic.prepgame.erzaehler_text.send(msg)