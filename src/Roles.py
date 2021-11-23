from Votingsystem import VotingSystem

class Roles(object):

    game_logic = None
    text_channel = None
    werwolf = False
    werwolf_channel = None
    partner = None
    hauptmann = False
    
    def __init__(self, role_name, abilities):
        self.role_name = role_name
        self.abilities = abilities      # dict: {heal_posion: 1}

    async def start(self):
        print(self.role_name + " wacht auf und tut etwas.")
    # Werwölfe, Hexe, Jäger, Terrorist, Weißer-Werwolf, Wolfsbaby
    async def kill(self, victim, night):
        self.game_logic.playerStatus[victim.id] = 2

        if self.get_role_name() == 'Terrorist':
            terrorist_id = await self.game_logic.helper.get_id_of_role_name('Terrorist')
            self.game_logic.playerStatus[terrorist_id] = 2
            print(self.game_logic.playerStatus)
            if night:
                i = 0
                self.procedure_list_run_copy = self.game_logic.procedure_list_run.copy()
                for entry in self.procedure_list_run_copy:
                    if self.game_logic.character_assignment[victim.id].get_role_name() == entry:
                        await self.game_logic.procedure_list_run.pop(i)
                    i = i+1
                await self.game_logic.pre_kill()
            else:
                await self.game_logic.start_day()
        else:
            await self.next_role()

        
        # change 1 to 2

    # Leibwächter, Hexe
    async def safe(self, target):
        self.game_logic.playerStatus[target.id] = 3

        await self.next_role()


    # Nutte
    async def pimperLimpern(self, player):
        self.customer = player

        await self.next_role()

    # Richter
    def mute(self):
        pass

    # Kopierertyp, Magd
    async def copy(self, copy_ply, target):
        self.game_logic.character_assignment[copy_ply.id] = self.game_logic.character_assignment[target.id] # erzeugt eine Referenz
        role_name = self.game_logic.character_assignment[copy_ply.id].get_role_name()
        await self.game_logic.helper.send_a_message(copy_ply, self.game_logic.text.get_text_dict()[role_name.lower()])
        if role_name not in ['Baerenfuehrer', 'Engel', 'Jaeger', 'ReineSeele', 'Terrorist', 'Tetanusritter']:
            if "Werwolf" in role_name:
                self.text_channel = await self.game_logic.role_channels(copy_ply, role_name.lower())
            else:
                channel_name = role_name + " kopiert"
                self.text_channel = await self.game_logic.role_channels(copy_ply, channel_name.lower())

        try:
            pre_index = self.game_logic.procedure_list.index(role_name)
            self.game_logic.procedure_list.insert((pre_index + 1), role_name)
        except:
            pass


    # Seher, Fuchs, Bärenführer
    def discover(self):
        pass

    # Amor
    async def pair(self, one, two):
        print(str(one) + " " + str(two))
        self.game_logic.character_assignment[one.id].set_partner(two)
        self.game_logic.character_assignment[two.id].set_partner(one)

        one_name = await self.game_logic.helper.nick_name_module(user=one)
        two_name = await self.game_logic.helper.nick_name_module(user=two)

        print("partner from " + str(one_name) + " = " + str(self.game_logic.character_assignment[one.id].get_partner().name))
        print("partner from " + str(two_name) + " = " + str(self.game_logic.character_assignment[two.id].get_partner().name))
        await self.game_logic.helper.send_a_message(one, self.game_logic.text.get_text_dict()['liebespaar_1'])
        await self.game_logic.helper.send_a_message(one, self.game_logic.text.get_text_dict()['liebespaar_2'].format(two_name))
        await self.game_logic.helper.send_a_message(two, self.game_logic.text.get_text_dict()['liebespaar_1'])
        await self.game_logic.helper.send_a_message(two, self.game_logic.text.get_text_dict()['liebespaar_2'].format(one_name))

        await self.next_role()

    # WildesKind
    def idolize(self):
        pass


    # Ur-Wolf, 
    async def infest(self, victim):
        await self.next_role()
        pass 


    # Teternusritter
    def infest_teternusritter(self, own_id):
        is_victim = False
        sorted_voice_channel_members_alive = self.game_logic.helper.get_sorted_voice_channel_members_alive()
        for member in sorted_voice_channel_members_alive:
            if member.id == own_id:
                for member_above_index in range(sorted_voice_channel_members_alive.index(member), 0, -1):
                    if 'werwolf' in self.game_logic.character_assignment[sorted_voice_channel_members_alive[member_above_index].id].get_role_name().lower():
                        self.game_logic.playerStatus[sorted_voice_channel_members_alive[member_above_index].id] = 2
                        is_victim = True
                if not is_victim:
                    for member_above_index in range(len(sorted_voice_channel_members_alive), sorted_voice_channel_members_alive.index(member), -1):
                        if 'werwolf' in self.game_logic.character_assignment[sorted_voice_channel_members_alive[member_above_index].id].get_role_name().lower():
                            self.game_logic.playerStatus[sorted_voice_channel_members_alive[member_above_index].id] = 2
    

    # all
    def sleep(self):
        pass
    

    async def next_role(self):
        await self.game_logic.next_role()


    def get_role_name(self):
        return self.role_name
    
    def get_abilities(self):
        return self.abilities

    def get_partner(self):
        return self.partner

    def get_werwolf(self):
        return self.werwolf

    def get_text_channel(self):
        return self.text_channel
    
    def get_werwolf_channel(self):
        return self.werwolf_channel
    
    def get_isHauptmann(self):
        return self.hauptmann
    
    # setzt den Text-Kanal der Rolle
    def set_channel(self, channel):
        self.text_channel = channel

    def set_partner(self, partner):
        self.partner = partner
    
    def set_isHauptmann(self):
        self.hauptmann = True
    
    # hält alle Ereignisse fest, die die Figur macht
    def log(self):
        pass


class Amor(Roles):


    def __init__(self):
        self.abilities = {}
        Roles.__init__(self, self.__class__.__name__, self.abilities)
        
    def set_channel(self, channel):
        self.text_channel = channel
    
    async def start(self):
        print(self.role_name + " wacht auf und tut etwas.")
        await self.text_channel.send(await Roles.game_logic.helper.get_all_alive_names())
        await self.text_channel.send('Schreibe *!verkuppeln @[**Username 1**] @[**Username 2**]*')


# kein extra channel
class Baerenfuehrer(Roles):


    def __init__(self):
        self.abilities = {}
        Roles.__init__(self, self.__class__.__name__, self.abilities)

    # kein extra channel


# kein extra channel
class Engel(Roles):

    engel_count = 0
    engel_limit = 2

    def __init__(self):
        self.abilities = {}
        Roles.__init__(self, self.__class__.__name__, self.abilities)

    async def engel_whatever(self):
        if self.engel_count < self.engel_limit:
            self.engel_count = self.engel_count + 1
        elif self.engel_count == self.engel_limit: # != -eq
            await self.game_logic.prepgame.erzaehler_text.send('Der Engel kann nicht mehr gewinnen!')
    
    def set_engel_limit(self, newLimit):
        self.engel_limit  = newLimit

# kein extra channel

class Fuchs(Roles):


    def __init__(self):
        self.abilities = {}
        Roles.__init__(self, self.__class__.__name__, self.abilities)

    def set_channel(self, channel):
        self.text_channel = channel


class Hexe(Roles):


    def __init__(self):
        self.abilities = {
            'heilungs_trank': True,
            'vergiftungs_trank': True
        }
        Roles.__init__(self, self.__class__.__name__, self.abilities)

    def set_channel(self, channel):
        self.text_channel = channel
    
    async def start(self):
        print(self.role_name + " wacht auf und tut etwas.")
        await self.text_channel.send('Schreibe *!toeten @[**Username**]*\nSchreibe *!heilen @[**Username**]*\ngefährdete Menschen:')
        await self.text_channel.send(await self.game_logic.helper.get_all_lala())
    

# kein extra channel
class Jaeger(Roles):


    def __init__(self):
        self.abilities = {}
        Roles.__init__(self, self.__class__.__name__, self.abilities)

    # kein extra channel


class Kopierertyp(Roles):


    def __init__(self):
        self.abilities = {}
        Roles.__init__(self, self.__class__.__name__, self.abilities)

    def set_channel(self, channel):
        self.text_channel = channel
    
    async def start(self):
        print(self.role_name + " wacht auf und tut etwas.")
        await self.text_channel.send(await Roles.game_logic.helper.get_all_alive_names())
        await self.text_channel.send('Schreibe *!kopieren @[**Username 1**]*')


class Leibwaechter(Roles):


    def __init__(self):
        self.abilities = {}
        Roles.__init__(self, self.__class__.__name__, self.abilities)
        
    def set_channel(self, channel):
        self.text_channel = channel


class Magd(Roles):


    def __init__(self):
        self.abilities = {
            'rolle_uebernommen': False
        }
        Roles.__init__(self, self.__class__.__name__, self.abilities)
        
    def set_channel(self, channel):
        self.text_channel = channel
    
    async def start(self, victim_id):
        print("Die ergebene Magd entscheidet ob Sie die Rolle übernehmen will.")
        victim = await self.game_logic.helper.user_id_to_user(victim_id)
        victim_name = await self.game_logic.helper.nick_name_module(user=victim)
        await self.text_channel.send('Schreibe *!fortfuehren* um die Rolle von {} zu übernehmen.\nSchreibe *!weiter* um nichts zu tun'.format(victim_name))
    


class Nutte(Roles):


    def __init__(self):
        self.abilities = {}
        self.customer = None
        Roles.__init__(self, self.__class__.__name__, self.abilities)

    def set_channel(self, channel):
        self.text_channel = channel

    async def start(self):
        print(self.role_name + " wacht auf und tut etwas.")
        await self.text_channel.send(await Roles.game_logic.helper.get_all_alive_names())
        await self.text_channel.send('Schreibe *!pimperlimpern @[**Username**]*')


# kein extra channel
class ReineSeele(Roles):


    def __init__(self):
        self.abilities = {}
        Roles.__init__(self, self.__class__.__name__, self.abilities)

    # kein extra channel


class Richter(Roles):


    def __init__(self):
        self.abilities = {}
        Roles.__init__(self, self.__class__.__name__, self.abilities)

    def set_channel(self, channel):
        self.text_channel = channel


class Seherin(Roles):


    def __init__(self):
        self.abilities = {}
        Roles.__init__(self, self.__class__.__name__, self.abilities)

    
    def set_channel(self, channel):
        self.text_channel = channel

    async def start(self):
        print(self.role_name + " wacht auf und tut etwas.")
        await self.text_channel.send(await Roles.game_logic.helper.get_all_alive_names())
        await self.text_channel.send('Schreibe *!offenbaren @[**Username**]*')
    
    async def discover(self, target):
        await self.text_channel.send(self.game_logic.character_assignment[target.id].get_role_name())

        await self.next_role()
        

# extra channel!!!!!!
class Terrorist(Roles):


    def __init__(self):
        self.abilities = {}
        Roles.__init__(self, self.__class__.__name__, self.abilities)

    def set_channel(self, channel):
        self.text_channel = channel
    
    #async def kill(self, victim,night):
#
    #    if night:
    #       pass
    #    else:
    #        #wenn tag ist
#
    #        pass    
    #    #victim_name = await self.game_logic.helper.nick_name_module(user=victim)
    #    #await self.game_logic.prepgame.dorfversammlung_text.send("Der Terrorist  hat eine Sauerei veranstalltet. Dabei hat er {} mitgenommen.".format(victim_name))
    
    async def send_msg(self):
        await self.text_channel.send(await Roles.game_logic.helper.get_all_alive_names())
        await self.text_channel.send(self.game_logic.text.get_text_dict()[self.get_role_name().lower()])
    
    
    # kein extra channel


# kein extra channel
class Tetanusritter(Roles):


    def __init__(self):
        self.abilities = {}
        Roles.__init__(self, self.__class__.__name__, self.abilities)
    
    # kein extra channel


class Werwolf(Roles):
    voting_system = None

    def __init__(self, game_logic):
        self.abilities = {}
        Roles.__init__(self, self.__class__.__name__, self.abilities)
        Roles.game_logic = game_logic
        Roles.werwolf = True

    def set_channel(self, channel):
        self.text_channel = channel
        Roles.werwolf_channel = channel
        self.voting_system = VotingSystem(self.game_logic, self.text_channel)
        
    async def start(self):
        print(self.role_name + " wacht auf und tut etwas.")
        await self.text_channel.send(await Roles.game_logic.helper.get_all_alive_names())
        await self.text_channel.send('Schreibe *!vorschlagen @[**Username**]*')


# kein extra channel
class WerwolfBaby(Roles):


    def __init__(self):
        self.abilities = {}
        Roles.__init__(self, self.__class__.__name__, self.abilities)
        Roles.werwolf = True
    # kein extra 


class WerwolfUr(Roles):


    def __init__(self):
        self.abilities = {}
        Roles.__init__(self, self.__class__.__name__, self.abilities)
        Roles.werwolf = True
    
    # werwolf_channel = Roles.Werwolf.text_channel
    def set_channel(self, channel):
        self.text_channel = channel


class WerwolfWeisser(Roles):
    #Nutte beachten

    def __init__(self):
        self.abilities = {}
        Roles.__init__(self, self.__class__.__name__, self.abilities)
        Roles.werwolf = True
    
    
    def set_channel(self, channel):
        self.text_channel = channel


class WildesKind(Roles):


    def __init__(self):
        self.abilities = {
            'verwandeln': True
        }
        Roles.__init__(self, self.__class__.__name__, self.abilities)

    
    def set_channel(self, channel):
        self.text_channel = channel


class Dorfbewohner(Roles):

    def __init__(self):
        self.abilities = {}
        Roles.__init__(self, self.__class__.__name__, self.abilities)
