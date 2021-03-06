# ======================================================================
# >> IMPORTS
# ======================================================================

# Hero Wars
from herowars.entities import Hero, Skill

from herowars.tools import chance, chancef
from herowars.tools import cooldown, cooldownf

from herowars.player import get_player

import herowars.commandlib as cmdlib

# Source.Python
from filters.players import PlayerIter


# ======================================================================
# >> Test Hero #1
# ======================================================================

class TestHero1(Hero):
    name = 'Test Hero #1'
    description = 'First testing hero, limited alpha release edition.'
    authors = ('Mahi', 'Kamiqawa')


@TestHero1.passive
class HealthSpeed(Skill):
    name = 'Speed&Health Passive'
    description = 'Gain speed on spawn and health on attack.'

    def on_spawn(self, player, **eargs):
        player.set_property_float('m_flLaggedMovementValue', 1.3)
        cmdlib.tell(player, '+30% speed from Passive.')

    @chance(33)
    def on_attack(self, attacker, **eargs):
        attacker.health += 5
        cmdlib.tell(attacker, '+5 health from Passive.')

        
@TestHero1.skill
class Damage(Skill):
    name = 'Damage'
    description = 'Deal 2x damage with attacks.'
    max_level = 1

    def on_attack(self, attacker, defender, **eargs):
        #attacker.damage(defender, eargs['damage'])  # disabled temporarily
        cmdlib.tell(defender, 'You dealt 2x damage!')


@TestHero1.skill
class Ignite(Skill):
    name = 'Ignite'
    description = 'Ignite all enemies for 3-4 seconds when you spawn.'
    max_level = 2

    def on_spawn(self, player, **eargs):
        target_team = player.team == 2 and 'ct' or 't'
        for userid in PlayerIter(
                is_filters=('alive', target_team), return_types='userid'):
            target = get_player(userid)
            if target:
                cmdlib.burn(target, 2 + self.level)
                cmdlib.tell(target, 'You were burned!')
        cmdlib.tell(player, 'You burned your enemies!')


@TestHero1.skill
class Noclip(Skill):
    name = 'Noclip'
    description = 'Ultimate: Get noclip for 2-4 seconds'
    max_level = 3
    cost = 2
    required_level = 5

    @cooldownf(lambda self, **eargs: 20 - self.level * 2)
    def on_ultimate(self, player, **eargs):
        cmdlib.noclip(player, 1 + self.level)
        cmdlib.tell(player, 'You got noclip for {duration} seconds!'
            .format(duration=1 + self.level))
