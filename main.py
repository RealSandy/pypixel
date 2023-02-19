
# PyPixel! A project by RealSandy!

from pypixel_functions import *

# Print the startup screen

startup_screen('start_screen')

target = Player(input("Enter a Minecraft Username: "))

alch = Skill(target, 'alchemy', 50)
carp = Skill(target, 'carpentry', 50)
combat = Skill(target, 'combat', 60)
ench = Skill(target, 'enchanting', 60)
farm = Skill(target, 'farming')
fish = Skill(target, 'fishing', 50)
forage = Skill(target, 'foraging', 50)
mine = Skill(target, 'mining', 60)
tame = Skill(target, 'taming', 50)

skill_average = calculate_skill_avg()

rev = Slayer('zombie', 'Revenant Horror', target)
tara = Slayer('spider', 'Tarantula Broodfather', target)
sven = Slayer('wolf', 'Sven Packmaster', target)
eman = Slayer('enderman', 'Voidgloom Seraph', target)
blaze = Slayer('blaze', 'Inferno Demonlord', target)

clear_screen()
print(f'''
                        {target.displayName}'s Stats on {target.chosen_profile_cute}

                            Skills ({skill_average} average):

Taming {tame}    Farming {farm}    Mining {mine}
Combat {combat}    Foraging {forage}    Fishing {fish}
Enchanting {ench}    Alchemy {alch}    Carpentry {carp}

                            Slayers ({rev.lvl}/{tara.lvl}/{sven.lvl}/{eman.lvl}/{blaze.lvl}):
INDIVIDUAL SLAYER STATS SUCH AS TIER KILLS, LEVEL PROGRESS AND TOTAL XP COMING SOON''')

print(rev.dat)
