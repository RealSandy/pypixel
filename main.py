
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

{tame}{farm}{mine}
{combat}{forage}{fish}
{ench}{alch}{carp}

                            Slayers ({rev.lvl}/{tara.lvl}/{sven.lvl}/{eman.lvl}/{blaze.lvl}):


Slayer Kills:
    T1: {rev.kills_t1}{tara.kills_t1}{sven.kills_t1}{eman.kills_t1}{blaze.kills_t1}
    T2: {rev.kills_t2}{tara.kills_t2}{sven.kills_t2}{eman.kills_t2}{blaze.kills_t2}
    T3: {rev.kills_t3}{tara.kills_t3}{sven.kills_t3}{eman.kills_t3}{blaze.kills_t3}
    T4: {rev.kills_t4}{tara.kills_t4}{sven.kills_t4}{eman.kills_t4}{blaze.kills_t4}
    T5: {rev.kills_t5}{tara.kills_t5}{sven.kills_t5}{eman.kills_t5}{blaze.kills_t5}

Slayer Tiers:
    {rev.tier}
    {tara.tier}
    {sven.tier}
    {eman.tier}
    {blaze.tier}
''')
