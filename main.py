
#PyPixel! A project similar to SkyCrypt!

import requests
import json
#from pprint import *

# Setup functions

def getUsrProfInfo(uuid, api_key): # Get the profile information of the specified user
    r = requests.get(f"https://api.hypixel.net/player?key={api_key}&uuid={uuid}")
    data = r.json()
    return data['player']['stats']['SkyBlock']['profiles'] # Decode 'r' and return it in dictionary format

def getUUID(username):
    r = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{username}')
    data = r.json()
    return data['id']

def getNameFromUUID(uuid):
    r = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}")
    data = r.json()
    return data['name']


def getProfileData(profile_id, api_key):
    r = requests.get(f'https://api.hypixel.net/skyblock/profile?key={api_key}&profile={profile_id}')
    data = r.json()
    return data['profile']

def getSkillLevel(skill_xp, max_skill_level):
    skill_level = 0
    for i in range (1, max_skill_level):
        if skill_xp < level_boundaries[i]:
            skill_level = i - 1
            break
        elif skill_xp >= level_boundaries[max_skill_level - 1]:
            skill_level = max_skill_level
    return skill_level

def calculateSkillProgress(level, xp, cap, farming = "n"):
    if level != cap:
        total_for_next_level = level_boundaries[level + 1] - level_boundaries[level]
        amount_to_next_level = xp - level_boundaries[level]
        prog_display = f'{formatNumber(amount_to_next_level)}/{formatNumber(total_for_next_level)}'
    elif farming == "y" and cap != 60:
        prog_display = "You cannot level any further until you upgrade your cap!"
    else:
        prog_display = 'Max Level Reached'
    return prog_display

def formatNumber(number):
    digits = len(str(number))
    if digits >= 7:
        number = round(number / 100000) / 10
        number = remove0FromFloat(number)
        display = f'{number}M'
    elif digits <= 6 and digits >= 4:
        number = round(number / 100) / 10
        number = remove0FromFloat(number)
        display = f'{number}k'
    else:
        display = f'{number}'
    return display

def setSkillExp(skill):
    exp = 0
    try:
        exp = round(usr_prof_data[f'experience_skill_{skill}'])
    except KeyError:
        pass
    return exp

def remove0FromFloat(number):
    if str(number).endswith('.0'):
        number = int(number)
    return number

def getSlayerStats(slayer):
    claimed_levels = usr_prof_data["slayer_bosses"][slayer]["claimed_levels"]
    slayer_level = 0
    for i in range(1, 9):
        try:
            if claimed_levels[f"level_{i}"]:
                slayer_level = i
        except KeyError:
            pass
    return slayer_level

def calculateSKillAvg():
    total_skill_level = alchemy_level + carpentry_level + combat_level + enchanting_level + farming_level + fishing_level + foraging_level + mining_level + taming_level
    skill_average = (round((total_skill_level / 9) * 100)) / 100
    return skill_average

def getApiKey(config):
    f = open(config)
    data = json.load(f)
    api_key = data['api_key']
    return api_key

# Import API key and level boundaries

api_key = getApiKey('config.json')
level_boundaries = [0, 50, 175, 375, 675, 1175, 1925, 2925, 4425, 6425, 9925, 14925, 22425, 32425, 47425, 67425, 97425, 147425, 222425, 322425, 522425, 822425, 1222425, 1722425, 2322425, 3022425, 3822425, 4722025, 5722425, 6822425, 8022425, 9322425, 10722425, 12222425, 13822425, 15522425, 17322425, 19222425, 21222425, 23322425, 25522425, 27822425, 30222425, 32722425, 35322425, 38072425, 40972425, 44072425, 47472425, 51172425, 55172425, 59472425, 64072425, 68972425, 74172425, 79672425, 85472425, 91572425, 97972425, 104672425, 111672425]

# Get target username and find the UUID of it

target_player = input("Enter a Minecraft Username: ")
print("Fetching profile list.", end='')
target_uuid = getUUID(target_player)

player_name = getNameFromUUID(target_uuid)

# Get list of profiles and their IDs

profiles = getUsrProfInfo(target_uuid, api_key)
print(".", end='')
profile_list = [profile for profile in profiles.values()]
print(".")

# Print list of profiles to choose from
for i, profile in enumerate(profile_list):
    print(f"{i + 1}: {profile['cute_name']}")

# Get the user's selection

prof_index = input("Select profile: ")
print("Fetching skill levels.", end='')
chosen_profile = profile_list[int(prof_index) - 1]['profile_id']
chosen_profile_cute = profile_list[int(prof_index) - 1]["cute_name"]
prof_data = getProfileData(chosen_profile, api_key)
print('..')
usr_prof_data = prof_data['members'][str(target_uuid)]

farming_lvl_cap_upgrades = 0
try:
    farming_lvl_cap_upgrades = usr_prof_data['jacob2']['perks']['farming_level_cap']
except KeyError:
    pass
farming_lvl_cap = farming_lvl_cap_upgrades + 50

usr_exp_alchemy = setSkillExp('alchemy')
usr_exp_carpentry = setSkillExp('carpentry')
usr_exp_combat = setSkillExp('combat')
usr_exp_enchanting = setSkillExp('enchanting')
usr_exp_farming = setSkillExp('farming')
usr_exp_fishing = setSkillExp('fishing')
usr_exp_foraging = setSkillExp('foraging')
usr_exp_mining = setSkillExp('mining')
usr_exp_taming = setSkillExp('taming')

alchemy_level = getSkillLevel(usr_exp_alchemy, 50)
carpentry_level = getSkillLevel(usr_exp_carpentry, 50)
combat_level = getSkillLevel(usr_exp_combat, 60)
enchanting_level = getSkillLevel(usr_exp_enchanting, 60)
farming_level = getSkillLevel(usr_exp_farming, farming_lvl_cap)
fishing_level = getSkillLevel(usr_exp_fishing, 50)
foraging_level = getSkillLevel(usr_exp_foraging, 50)
mining_level = getSkillLevel(usr_exp_mining, 60)
taming_level = getSkillLevel(usr_exp_taming, 50)

alchemy_progress = calculateSkillProgress(alchemy_level, usr_exp_alchemy, 50)
carpentry_progress = calculateSkillProgress(carpentry_level, usr_exp_carpentry, 50)
combat_progress = calculateSkillProgress(combat_level, usr_exp_combat, 60)
enchanting_progress = calculateSkillProgress(enchanting_level, usr_exp_enchanting, 60)
farming_progress = calculateSkillProgress(farming_level, usr_exp_farming, farming_lvl_cap, "y")
fishing_progress = calculateSkillProgress(fishing_level, usr_exp_fishing, 50)
foraging_progress = calculateSkillProgress(foraging_level, usr_exp_foraging, 50)
mining_progress = calculateSkillProgress(mining_level, usr_exp_mining, 60)
taming_progress = calculateSkillProgress(taming_level, usr_exp_taming, 50)

skill_average = calculateSKillAvg()

rev_slayer = getSlayerStats("zombie")
tara_slayer = getSlayerStats("spider")
sven_slayer = getSlayerStats("wolf")
eman_slayer = getSlayerStats("enderman")
blaze_slayer = getSlayerStats("blaze")

#pprint(usr_prof_data)

print(f'''
                        {player_name}'s Stats on {chosen_profile_cute}

                            Skills ({skill_average} average):

Taming {taming_level} ({taming_progress})    Farming {farming_level} ({farming_progress})    Mining {mining_level} ({mining_progress})
Combat {combat_level} ({combat_progress})    Foraging {foraging_level} ({foraging_progress})    Fishing {fishing_level} ({fishing_progress})
Enchanting {enchanting_level} ({enchanting_progress})    Alchemy {alchemy_level} ({alchemy_progress})    Carpentry {carpentry_level} ({carpentry_progress})

                            Slayers ({rev_slayer}/{tara_slayer}/{sven_slayer}/{eman_slayer}/{blaze_slayer}):
INDIVIDUAL SLAYER STATS SUCH AS TIER KILLS, LEVEL PROGRESS AND TOTAL XP COMING SOON''')