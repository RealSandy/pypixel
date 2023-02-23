
import os
import time
import requests
import json
from math import *

skill_levels = []


class Player:
    def __init__(self, name=None):
        if not name:
            raise RuntimeError('You need to provide a name')
        self.name = name
        self.uuid = get_uuid_from_name(self.name)
        self.displayName = get_name_from_uuid(self.uuid)
        self.api_key = get_api_key('config.json')
        self.profiles = self.get_usr_prof_info()
        self.profiles_list = [profile for profile in self.profiles.values()]
        self.chosen_profile_cute, self.prof_data = self.get_profile_selection(self.profiles_list)
        clear_screen()

    def get_usr_prof_info(self):
        r = requests.get(f"https://api.hypixel.net/player?key={self.api_key}&uuid={self.uuid}")
        data = r.json()
        return data['player']['stats']['SkyBlock']['profiles']

    def get_profile_selection(self, profile_list):
        print(f'{self.displayName}\'s profiles:')
        for i, profile in enumerate(profile_list):
            print(f"{i + 1}: {profile['cute_name']}")
        prof_index = input("Select profile: ")
        chosen_profile = profile_list[int(prof_index) - 1]['profile_id']
        prof_cute_name = profile_list[int(prof_index) - 1]["cute_name"]
        prof_data = self.get_profile_data(chosen_profile)
        prof_data = prof_data['members'][str(self.uuid)]
        return prof_cute_name, prof_data

    def get_profile_data(self, profile_id):
        r = requests.get(f'https://api.hypixel.net/skyblock/profile?key={self.api_key}&profile={profile_id}')
        data = r.json()
        return data['profile']


class Skill:
    def __init__(self, target, name='', cap=0):
        self.lvl_bounds = (0, 50, 175, 375, 675, 1175, 1925, 2925, 4425, 6425, 9925, 14925, 22425, 32425, 47425, 67425,
                           97425, 147425, 222425, 322425, 522425, 822425, 1222425, 1722425, 2322425, 3022425, 3822425,
                           4722025, 5722425, 6822425, 8022425, 9322425, 10722425, 12222425, 13822425, 15522425,
                           17322425, 19222425, 21222425, 23322425, 25522425, 27822425, 30222425, 32722425, 35322425,
                           38072425, 40972425, 44072425, 47472425, 51172425, 55172425, 59472425, 64072425, 68972425,
                           74172425, 79672425, 85472425, 91572425, 97972425, 104672425, 111672425)
        self.name = name
        self.target = target
        self.cap = self.set_cap(cap)
        self.xp = self.set_skill_xp()
        self.lvl = self.get_level()
        self.prog = self.calculate_skill_progress()
        skill_levels.append(self.lvl)

    def set_cap(self, cap):
        if self.name == 'farming':
            farming_lvl_cap_upgrades = 0
            try:
                farming_lvl_cap_upgrades = self.target.prof_data['jacob2']['perks']['farming_level_cap']
            except KeyError:
                pass
            return farming_lvl_cap_upgrades + 50
        else:
            return cap

    def set_skill_xp(self):
        xp = 0
        try:
            xp = round(self.target.prof_data[f'experience_skill_{self.name}'])
        except KeyError:
            pass
        return xp

    def get_level(self):
        skill_level = 0
        for i in range(1, self.cap):
            if self.xp < self.lvl_bounds[i]:
                skill_level = i - 1
                break
            elif self.xp >= self.lvl_bounds[self.cap - 1]:
                skill_level = self.cap
        return skill_level

    def calculate_skill_progress(self):
        level_boundaries = self.lvl_bounds
        if self.lvl != self.cap:
            total_for_next_level = level_boundaries[self.lvl + 1] - level_boundaries[self.lvl]
            amount_to_next_level = self.xp - level_boundaries[self.lvl]
            prog_display = f'{format_number(amount_to_next_level)}/{format_number(total_for_next_level)}'
        elif self.name == 'farming' and self.cap != 60:
            prog_display = "You cannot level any further until you upgrade your cap!"
        else:
            prog_display = 'Max Level Reached'
        return prog_display

    def __str__(self):
        return pad_string(f"{self.name.capitalize()} {self.lvl} ({self.prog})", 34)


class Slayer:
    def __init__(self, mob_type, name, target):
        self.boss_xp = [0, 5, 25, 100, 500, 1500]
        self.type = mob_type
        self.name = name
        self.dat = target.prof_data["slayer_bosses"][self.type]
        self.xp = self.set_xp()
        self.bounds = self.set_bounds()
        self.max_tier = self.set_max_tier()
        self.lvl = self.get_level()
        self.pad_length = self.get_pad_length()
        self.kills_t1, self.kills_t2, self.kills_t3, self.kills_t4, self.kills_t5, self.t1, self.t2, self.t3, self.t4, \
            self.t5 = self.get_kills()
        self.highest_killed = self.get_highest_kill()
        self.kills_to_next = self.get_kills_to_next()
        self.tier = self.get_level_progress()

    def get_level(self):
        slayer_level = 0
        for i in range(1, 9):
            if self.xp < self.bounds[i]:
                slayer_level = i
                break
            elif self.xp >= self.bounds[8]:
                slayer_level = 9
        return slayer_level

    def set_xp(self):
        xp = 0
        try:
            xp = self.dat['xp']
        except KeyError:
            pass
        return xp

    def set_bounds(self):
        bounds = {'zombie': [5, 15, 200, 1000, 5000, 20000, 100000, 400000, 1000000],
                  'spider': [10, 25, 200, 1000, 5000, 20000, 100000, 400000, 1000000],
                  'wolf': [10, 30, 250, 1500, 5000, 20000, 100000, 400000, 1000000],
                  'enderman': [10, 30, 250, 1500, 5000, 20000, 100000, 400000, 1000000],
                  'blaze': [10, 30, 250, 1500, 5000, 20000, 100000, 400000, 1000000]}
        return bounds[self.type]

    def set_max_tier(self):
        max_tiers = {'zombie': 5, 'spider': 4, 'wolf': 4, 'enderman': 4, 'blaze': 4}
        return max_tiers[self.type]

    def get_kills(self):
        name = self.type.capitalize()
        kills = []
        kills_raw = []
        for i in range(5):
            tier_kills = 0
            try:
                tier_kills = self.dat[f'boss_kills_tier_{i}']
            except KeyError:
                pass
            kills.append(pad_string(f'{name} - x{tier_kills}', self.pad_length))
            kills_raw.append(tier_kills)
        if self.max_tier != 5:
            kills[4] = pad_string(f'{name} - N/A', self.pad_length)
            kills_raw[4] = 'N/A'
        return kills[0], kills[1], kills[2], kills[3], kills[4], kills_raw[0], kills_raw[1], kills_raw[2], \
            kills_raw[3], kills_raw[4]

    def get_pad_length(self):
        pad_length = len(self.type) + 9
        return pad_length

    def get_level_progress(self):
        level_boundaries = self.bounds
        if self.lvl != 9:
            prog_display = f'{format_number(self.xp)}/{format_number(level_boundaries[self.lvl])}'
        else:
            prog_display = 'Max Level Reached'
        level_display = pad_string(f'{self.name} {self.lvl}', 24)
        level_display += pad_string(f'({prog_display})', 14)
        if self.lvl != 9:
            level_display += f'- T{self.highest_killed} x{self.kills_to_next} to next level'
        return level_display

    def get_highest_kill(self):
        kills = [self.t1, self.t2, self.t3, self.t4, self.t5]
        highest_killed = 0
        for i in range(len(kills)):
            if str(kills[i]) != 'N/A':
                if int(kills[i]) < 1:
                    highest_killed = i
                    break
                elif i == 4 and int(kills[i]) > 1:
                    highest_killed = 5
            else:
                highest_killed = i
        if highest_killed == 0:
            highest_killed = 1
        return highest_killed

    def get_kills_to_next(self):
        if self.lvl != 9:
            xp_to_next = self.bounds[self.lvl] - self.xp
            xp_per_boss = self.boss_xp[self.highest_killed]
            number_to_kill = xp_to_next / xp_per_boss
            number_to_kill = ceil(number_to_kill)
            return number_to_kill


# Setup functions

def format_number(number):
    digits = len(str(number))
    if digits >= 7:
        number = round(number / 100000) / 10
        number = remove_float_trail(number)
        display = f'{number}M'
    elif 6 >= digits >= 4:
        number = round(number / 100) / 10
        number = remove_float_trail(number)
        display = f'{number}k'
    else:
        display = f'{number}'
    return display


def remove_float_trail(number):
    if str(number).endswith('.0'):
        number = int(number)
    return number


def calculate_skill_avg():
    skill_total = 0
    for i in range(len(skill_levels)):
        skill_total += skill_levels[i]
    skill_average = (round((skill_total / 9) * 100)) / 100
    return skill_average


def get_api_key(config):
    f = open(config)
    data = json.load(f)
    api_key = data['api_key']
    return api_key


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def startup_screen(screen):
    clear_screen()
    start_screen = open(screen)
    for lines in start_screen:
        print(lines, end='')
    time.sleep(2.5)
    clear_screen()


def get_uuid_from_name(username):
    r = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{username}')
    data = r.json()
    return data['id']


def get_name_from_uuid(uuid):
    r = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}")
    data = r.json()
    return data['name']


def pad_string(string, target_length):
    current_length = len(string)
    spaces_to_add = target_length - current_length
    return string + (' ' * spaces_to_add)
