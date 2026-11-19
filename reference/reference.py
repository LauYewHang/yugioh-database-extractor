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

# spell and trap card
SPELL_TRAP_ICONS = [
    "Equip",
    "Field",
    "Quick-Play",
    "Ritual",
    "Continuous",
    "Counter",
    "Normal"
]

###########################################################################
# supporting data
# some information, such as the "DARK" attribute is referenced as value 12 in the yugioh database
# this section create list that help map enum name with their respective value
MONSTER_ATTRIBUTES_VALUE = [
    12,
    11,
    15,
    13,
    14,
    16,
    17
]

MONSTER_TYPES_VALUE = [
    18,
    1,
    2,
    15,
    12,
    11,
    16,
    3,
    17,
    10,
    9,
    20,
    8,
    5,
    14,
    4,
    19,
    6,
    13,
    7,
    21,
    22,
    26,
    27,
    34
]

MONSTER_CARD_TYPES_VALUE = [
    0,
    1,
    3,
    2,
    9,
    10,
    4,
    5,
    6,
    7,
    8,
    14,
    15,
    17
]

SPELL_TRAP_ICONS_VALUE = [
    23,
    22,
    25,
    26,
    24,
    21,
    20
]

###########################################################################
# create enum for each filter
CardTypes = Enum("CardTypes", CARD_TYPES)

# enum with the name repect to the value used by yugioh database
MonsterAttributes = Enum("MonsterAttributes", [(MONSTER_ATTRIBUTES[index], MONSTER_ATTRIBUTES_VALUE[index]) for index in range(len(MONSTER_ATTRIBUTES))])
MonsterTypes = Enum("MonsterTypes", [(MONSTER_TYPES[index], MONSTER_TYPES_VALUE[index]) for index in range(len(MONSTER_TYPES))])
SpellTrapIcons = Enum("SpellTrapIcons", [(SPELL_TRAP_ICONS[index], SPELL_TRAP_ICONS_VALUE[index]) for index in range(len(SPELL_TRAP_ICONS))])

# for monster card type, there can be multiple: e.g. Synchro + Pendulum + Effect
# thus, instead of making a list, gives each enum a binary representation
# e.g.  normal = 0b00001    (decimal 1)
#       effect = 0b00010    (decimal 2)
#       ritual = 0b00100    (decimal 4)
#       fusion = 0b01000    (decimal 8)
# so for a ritual effect monster, can do bitwise or operator: effect | ritual = 0b00110
MonsterCardTypes = Enum("MonsterCardTypes", [(MONSTER_CARD_TYPES[index], 2**index) for index in range(len(MONSTER_CARD_TYPES))])

# map the enum name with the value used in the official database
MonsterCardTypes_db = Enum("MonsterCardTypes_db" [(MONSTER_CARD_TYPES[index], MONSTER_CARD_TYPES_VALUE[index])] for index in range(len(MONSTER_CARD_TYPES)))

###########################################################################
# miscellaneous enum for easier classify
# level or rank enum
LevelRankTypes = Enum("LevelRankType", ["Level", "Rank"])

# link arrow enum, also apply bitwise operator
# according to the yugioh database, link arrow classify as following direction:
#   7   8   9
#   4   -   6
#   1   2   3
availableLinkIndex = [index for index in range(1, 10) if index != 5]
# the link arrow has bit start with integer 2 instead of 1
# i.e. first value is 0b10 instead of 0b1 since the lowest link is 1 (2**1 = 2)
LinkArrows = Enum("LinkArrows", [(str(index), 2**(index)) for index in availableLinkIndex])

# spell or trap enum
SpellTrapTypes = Enum("SpellTrapTypes", ["Spell", "Trap"])
