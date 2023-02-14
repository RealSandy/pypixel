
#PyPixel! A project similar to SkyCrypt!

import requests
import json
#from pprint import *

class Player:
    def __init__(self, name):
        self.name = name
        self.uuid = self.getUUID(self.name)
        self.displayName = self.getNameFromUUID(self.uuid)

    def getUUID(self, username):
        r = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{username}')
        data = r.json()
        return data['id']

    def getNameFromUUID(self, uuid):
        r = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}")
        data = r.json()
        return data['name']

    def getUsrProfInfo(self, api_key):
        r = requests.get(f"https://api.hypixel.net/player?key={api_key}&uuid={self.uuid}")
        data = r.json()
        return data['player']['stats']['SkyBlock']['profiles']

    def getProfileSelection(self, profile_list):
        print(f'{self.displayName}\'s profiles:')
        for i, profile in enumerate(profile_list):
            print(f"{i + 1}: {profile['cute_name']}")
        prof_index = input("Select profile: ")
        chosen_profile = profile_list[int(prof_index) - 1]['profile_id']
        self.chosen_profile_cute = profile_list[int(prof_index) - 1]["cute_name"]
        prof_data = self.getProfileData(chosen_profile, api_key)
        self.prof_data = prof_data['members'][str(target_uuid)]
    def getProfileData(self, profile_id, api_key):
        r = requests.get(f'https://api.hypixel.net/skyblock/profile?key={api_key}&profile={profile_id}')
        data = r.json()
        return data['profile']


class Skill:
    def __init__(self, name, cap=0):
        self.name = name
        self.setCap(cap)
        self.setSkillExp()
        self.getLevel()
        self.calculateSkillProgress()

    def setCap(self, cap):
        if self.name == 'farming':
            farming_lvl_cap_upgrades = 0
            try:
                farming_lvl_cap_upgrades = target.prof_data['jacob2']['perks']['farming_level_cap']
            except KeyError:
                pass
            self.cap = farming_lvl_cap_upgrades + 50
        else:
            self.cap = cap

    def setSkillExp(self):
        exp = 0
        try:
            exp = round(target.prof_data[f'experience_skill_{self.name}'])
        except KeyError:
            pass
        self.xp = exp

    def getLevel(self):
        skill_level = 0
        for i in range(1, self.cap):
            if self.xp < level_boundaries[i]:
                skill_level = i - 1
                break
            elif self.xp >= level_boundaries[self.cap - 1]:
                skill_level = self.cap
        self.lvl = skill_level

    def calculateSkillProgress(self):
        if self.lvl != self.cap:
            total_for_next_level = level_boundaries[self.lvl + 1] - level_boundaries[self.lvl]
            amount_to_next_level = self.xp - level_boundaries[self.lvl]
            prog_display = f'{formatNumber(amount_to_next_level)}/{formatNumber(total_for_next_level)}'
        elif self.name == 'farming' and self.cap != 60:
            prog_display = "You cannot level any further until you upgrade your cap!"
        else:
            prog_display = 'Max Level Reached'
        self.prog = prog_display

    def __str__(self):
        return f"{self.lvl} ({self.prog})"


class Slayer:
    def __init__(self, mob_type, name):
        self.type = mob_type
        self.name = name
        self.dat = target.prof_data["slayer_bosses"][self.type]
        self.getSlayerLevel()

    def getSlayerLevel(self):
        claimed_levels = self.dat["claimed_levels"]
        slayer_level = 0
        for i in range(1, 9):
            try:
                if claimed_levels[f"level_{i}"]:
                    slayer_level = i
            except KeyError:
                pass
        self.lvl = slayer_level


# Setup functions

def formatNumber(number):
    digits = len(str(number))
    if digits >= 7:
        number = round(number / 100000) / 10
        number = remove0FromFloat(number)
        display = f'{number}M'
    elif 6 >= digits >= 4:
        number = round(number / 100) / 10
        number = remove0FromFloat(number)
        display = f'{number}k'
    else:
        display = f'{number}'
    return display


def remove0FromFloat(number):
    if str(number).endswith('.0'):
        number = int(number)
    return number


def calculateSkillAvg():
    total_skill_level = alch.lvl + carp.lvl + combat.lvl + ench.lvl + farm.lvl + fish.lvl + forage.lvl + mine.lvl + tame.lvl
    skill_average = (round((total_skill_level / 9) * 100)) / 100
    return skill_average


def getApiKey(config):
    f = open(config)
    data = json.load(f)
    api_key = data['api_key']
    return api_key


# Import API key and level boundaries

api_key = getApiKey('config.json')
level_boundaries = (0, 50, 175, 375, 675, 1175, 1925, 2925, 4425, 6425, 9925, 14925, 22425, 32425, 47425, 67425, 97425, 147425, 222425, 322425, 522425, 822425, 1222425, 1722425, 2322425, 3022425, 3822425, 4722025, 5722425, 6822425, 8022425, 9322425, 10722425, 12222425, 13822425, 15522425, 17322425, 19222425, 21222425, 23322425, 25522425, 27822425, 30222425, 32722425, 35322425, 38072425, 40972425, 44072425, 47472425, 51172425, 55172425, 59472425, 64072425, 68972425, 74172425, 79672425, 85472425, 91572425, 97972425, 104672425, 111672425)

# Get target username and find the UUID of it

target = Player(input("Enter a Minecraft Username: "))
target_uuid = target.uuid
player_name = target.name

profiles = target.getUsrProfInfo(api_key)
profile_list = [profile for profile in profiles.values()]
target.getProfileSelection(profile_list)

alch = Skill('alchemy', 50)
carp = Skill('carpentry', 50)
combat = Skill('combat', 60)
ench = Skill('enchanting', 60)
farm = Skill('farming')
fish = Skill('fishing', 50)
forage = Skill('foraging', 50)
mine = Skill('mining', 60)
tame = Skill('taming', 50)

skill_average = calculateSkillAvg()

rev = Slayer('zombie', 'Revenant Horror')
tara = Slayer('spider', 'Tarantula Broodfather')
sven = Slayer('wolf', 'Sven Packmaster')
eman = Slayer('enderman', 'Voidgloom Seraph')
blaze = Slayer('blaze', 'Inferno Demonlord')

#pprint(usr_prof_data)

print(f'''
                        {target.displayName}'s Stats on {target.chosen_profile_cute}

                            Skills ({skill_average} average):

Taming {tame}    Farming {farm}    Mining {mine}
Combat {combat}    Foraging {forage}    Fishing {fish}
Enchanting {ench}    Alchemy {alch}    Carpentry {carp}

                            Slayers ({rev.lvl}/{tara.lvl}/{sven.lvl}/{eman.lvl}/{blaze.lvl}):
INDIVIDUAL SLAYER STATS SUCH AS TIER KILLS, LEVEL PROGRESS AND TOTAL XP COMING SOON''')