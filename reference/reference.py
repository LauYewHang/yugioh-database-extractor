from enum import Enum

# available filters for the cards
CARD_TYPES = [
    "Monster",
    "Spell",
    "Trap"
]

# monster card
MONSTER_ATTRIBUTES = [
    "DARK",
    "LIGHT",
    "EARTH",
    "WATER",
    "FIRE",
    "WIND",
    "DIVINE"
]

MONSTER_TYPES = [
    "Spellcaster",
    "Dragon",
    "Zombie",
    "Warrior",
    "Beast-Warrior",
    "Beast",
    "Winged Beast",
    "Fiend",
    "Fairy",
    "Insect",
    "Dinosaur",
    "Reptile",
    "Fish",
    "Sea Serphent",
    "Aqua",
    "Pyro",
    "Thunder",
    "Rock",
    "Plant",
    "Machine",
    "Psychic",
    "Divine-Beast",
    "Wyrm",
    "Cyberse",
    "Illusion"
]

MONSTER_CARD_TYPES = [
    "Normal",
    "Effect",
    "Ritual",
    "Fusion",
    "Synchro",
    "Xyz",
    "Toon",
    "Spirit",
    "Union",
    "Gemini",
    "Tuner",
    "Flip",
    "Pendulum",
    "Link"
]

MINIMUM_LEVEL_RANK = 0
MAXIMUM_LEVEL_RANK = 13

MINIMUM_PENDULUM_SCALE = 0
MAXIMUM_PENDULUM_SCALE = 13

MINIMUM_LINK = 0
MAXIMUM_LINK = 6

# spell card
SPELL_ICONS = [
    "Equip",
    "Field",
    "Quick-Play",
    "Ritual",
    "Continuous",
    "Normal"
]

# trap card
TRAP_ICONS = [
    "Continuous",
    "Counter",
    "Normal"
]

###########################################################################
# create enum for each filter
CardTypes = Enum("CardTypes", CARD_TYPES)
MonsterAttributes = Enum("MonsterAttributes", MONSTER_ATTRIBUTES)
MonsterTypes = Enum("MonsterTypes", MONSTER_TYPES)
SpellIcons = Enum("SpellIcons", SPELL_ICONS)
TrapIcons = Enum("TrapIcons", TRAP_ICONS)

# for monster card type, there can be multiple: e.g. Synchro + Pendulum + Effect
# thus, instead of making a list, gives each enum a binary representation
# e.g.  normal = 0b00001    (decimal 1)
#       effect = 0b00010    (decimal 2)
#       ritual = 0b00100    (decimal 4)
#       fusion = 0b01000    (decimal 8)
# so for a ritual effect monster, can do bitwise or operator: effect | ritual = 0b00110
MonsterCardTypes = Enum("MonsterCardTypes", [(MONSTER_CARD_TYPES[index], 2**index) for index in range(len(MONSTER_CARD_TYPES))])
