
#PyPixel! A project similar to SkyCrypt!

from pypixel_functions import *

# Get target username and find the UUID of it

target_name = input("Enter a Minecraft Username: ")
target = Player(target_name)
target_uuid = target.uuid
player_name = target.name

profiles = target.getUsrProfInfo()
profile_list = [profile for profile in profiles.values()]
target.getProfileSelection(profile_list)

alch = Skill(target, 'alchemy', 50)
carp = Skill(target, 'carpentry', 50)
combat = Skill(target, 'combat', 60)
ench = Skill(target, 'enchanting', 60)
farm = Skill(target, 'farming')
fish = Skill(target, 'fishing', 50)
forage = Skill(target, 'foraging', 50)
mine = Skill(target, 'mining', 60)
tame = Skill(target, 'taming', 50)

skill_average = calculateSkillAvg(alch, carp, combat, ench, farm, fish, forage, mine, tame)

rev = Slayer('zombie', 'Revenant Horror', target)
tara = Slayer('spider', 'Tarantula Broodfather', target)
sven = Slayer('wolf', 'Sven Packmaster', target)
eman = Slayer('enderman', 'Voidgloom Seraph', target)
blaze = Slayer('blaze', 'Inferno Demonlord', target)

print(f'''
                        {target.displayName}'s Stats on {target.chosen_profile_cute}

                            Skills ({skill_average} average):

Taming {tame}    Farming {farm}    Mining {mine}
Combat {combat}    Foraging {forage}    Fishing {fish}
Enchanting {ench}    Alchemy {alch}    Carpentry {carp}

                            Slayers ({rev.lvl}/{tara.lvl}/{sven.lvl}/{eman.lvl}/{blaze.lvl}):
INDIVIDUAL SLAYER STATS SUCH AS TIER KILLS, LEVEL PROGRESS AND TOTAL XP COMING SOON''')