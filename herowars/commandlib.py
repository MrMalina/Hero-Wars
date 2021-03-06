# ======================================================================
# >> IMPORTS
# ======================================================================

# Hero Wars
from herowars.player import get_player

# Python 3
from collections import defaultdict

# Source.Python
from messages import SayText2

from listeners.tick import tick_delays

from filters.players import PlayerIter

from mathlib import Vector


# ======================================================================
# >> ALL DECLARATION
# ======================================================================

__all__ = (
    'burn', 'freeze', 'noclip', 'jetpack',
    'push', 'push_to', 'boost_velocity', 'set_property',
    'player_nearest_vector', 'player_near_vector'
)


# ======================================================================
# >> GLOBALS
# ======================================================================

_effects = {key: defaultdict(set) for key in __all__[:4]}


# ======================================================================
# >> FUNCTIONS
# ======================================================================

def tell(player, message):
    """Sends a message to a player through the chat."""

    SayText2(message=message).send(player.index)


def shiftprop(player, prop, shift, duration=0):
    """Shifts player's property's value for a duration.

    Args:
        player: Player whose property to shift
        prop: Name of the property to shift
        shift: Shift to make, can be negative
        duration: Duration until the effect is reverted, 0 for infinite
    """

    setattr(player, prop, getattr(player, prop) + shift)
    if duration:
        tick_delays.delay(duration, shiftprop, player, prop, -shift)()


def burn(player, duration):
    """Sets a player on fire."""

    player.call_input('Ignite')
    delay = tick_delays.delay(duration, _unburn)
    delay.args = (player, delay)
    _effects['burn'][player.index].add(delay)
    delay()


def _unburn(player, delay):
    """Extinguishes a player."""

    _effects['burn'][player.index].discard(delay)
    if not _effects['burn'][player.index]:
        player.call_input('IgniteLifetime', 0)


def freeze(player, duration):
    """Freezes a player."""

    player.freeze = True
    delay = tick_delays.delay(duration, _unfreeze)
    delay.args = (player, delay)
    _effects['freeze'][player.index].add(delay)
    delay()


def _unfreeze(player, delay):
    """Unfreezes a player."""

    _effects['freeze'][player.index].discard(delay)
    if not _effects['freeze'][player.index]:
        player.freeze = False


def noclip(player, duration):
    """Noclips a player."""

    player.noclip = True
    delay = tick_delays.delay(duration, _unnoclip)
    delay.args = (player, delay)
    _effects['noclip'][player.index].add(delay)


def _unnoclip(player, delay):
    """Unnoclips a player."""

    _effects['noclip'][player.index].discard(delay)
    if not _effects['noclip'][player.index]:
        player.noclip = False


def jetpack(player, duration):
    """Jetpacks a player."""

    player.jetpack = True
    delay = tick_delays.delay(duration, _unjetpack)
    delay.args = (player, delay)
    _effects['jetpack'][player.index].add(delay)


def _unjetpack(player, delay):
    """Unjetpacks a player."""

    _effects['jetpack'][player.index].discard(delay)
    if not _effects['jetpack'][player.index]:
        player.jetpack = False
        

def boost_velocity(player, x_mul=1.0, y_mul=1.0, z_mul=1.0):
    """Boosts player's velocity."""

    base_string = 'CBasePlayer.localdata.m_vecBaseVelocity'
    velocity = player.get_property_vector(base_string)
    velocity.x *= x_mul
    velocity.y *= y_mul
    velocity.z *= z_mul
    player.set_property_vector(base_string, vector)


def get_nearby_players(point, radius, is_filters='alive', not_filters=''):
    """Gets players near a point sorted by their distance to the point.

    Args:
        point: (x, y, z) coordinates of a 3D point
        radius: Radius to look for the players
        is_filters: PlayerIter's is_filters
        not_filters: PlayerIter's not_filters

    Returns:
        A list of players within the given radius from the given point,
        sorted by their distance of the point.
    """

    vector = Vector(point)
    players = set()
    for userid in PlayerIter(
            is_filters=is_filters,
            not_filters=not_filters,
            return_types='userid'):
        player = get_player(userid)
        if vector.get_distance(player.location) <= radius:
            players.add(player)
    return sorted(players, key=lambda p: vector.get_distance(p.location))


def push(player, vector):
    """Pushes player along given vector

    Pushes player along given vector (x,y,z).
    """

    player.set_property_string(
        'CBasePlayer.localdata.m_vecBaseVelocity', ','.join(vector)
    )


def push_to(player, vector, force):
    """Pushes player towards given point

    Pushes player towards given vector point (x,y,z)
    with given force.
    """

    push(player, (vector - player.location) * force)
