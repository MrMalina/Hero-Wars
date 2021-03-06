# ======================================================================
# >> IMPORTS
# ======================================================================

# Python
import os


# ======================================================================
# >> CONFIGURATIONS
# ======================================================================

# Default language key for translations
default_lang_key = 'en'


# Prefix needed for chat commands
chat_command_prefix = '!'


# (Relative) path to database file used by Hero Wars
database_path = os.path.dirname(__file__) + '/herowars.db'


# Amounts of experience points gained from objectives
exp_values = dict(

    # Kill values
    kill = 30,
    headshot = 15,
    assist = 15,
    weapon_knife = 30,

    # Round values
    round_win = 30,
    round_lose = 15,

    # Bomb values
    bomb_plant = 15,
    bomb_plant_team = 5,
    bomb_explode = 25,
    bomb_explode_team = 10,
    bomb_defuse = 30,
    bomb_defuse_team = 15,

    # Hostage values
    hostage_pick_up = 5,
    hostage_pick_up_team = 0,
    hostage_rescue = 25,
    hostage_rescue_team = 10,
)


# Amounts of gold gained from objectives
gold_values = dict(

    # Kill values
    kill = 2,
    assist = 1,

    # Round values
    round_win = 3,
    round_lose = 2
)


# Show messages for gold gain
show_gold_messages = True


# Starting heroes for when a player joins the server for the first time
# > Use class names for identifying the Hero classes
starting_heroes = (
    'TestHero1',
)


# Hero category used when the category is not defined
default_hero_category = 'Others'


# Item category used when the category is not defined
default_item_category = 'Others'


# Items' default sell value's multiplier
item_sell_value_multiplier = 0.5


# Exp algorithm for required exp to level up
def exp_algorithm(level):
    return 100 + level * 20
