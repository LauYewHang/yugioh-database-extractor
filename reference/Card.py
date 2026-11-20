import datetime

from reference.card_reference import *

# generic card class
class Card:
    def __init__(
        self,
        name: str,
        card_text: str,
        release_date: datetime.date,
        available_set: list,
        related_card: list
    ):
        self.name = name
        self.card_text = card_text
        self.release_date = release_date
        self.available_set = available_set
        self.related_card = related_card

# monster card type
class MonsterCard(Card):
    def __init__(
        self,
        # inherited
        name: str,
        card_text: str,
        release_date: datetime.date,
        available_set: list,
        related_card: list,
        # extended
        attribute: MonsterAttributes,
        attack: int,
        defense: int | None,
        monster_type: MonsterTypes,
        monster_card_type: int # the bit combination that represents the monster card types
    ):
        super().__init__(
            name = name,
            card_text = card_text,
            release_date = release_date,
            available_set = available_set,
            related_card = related_card
        )
        self.attribute = attribute
        self.attack = attack
        self.defense = defense
        self.monster_type = monster_type
        self.monster_card_type = monster_card_type

class NonLinkMonsterCard(Card):
    def __init__(
        self,
        # inherited
        name: str,
        card_text: str,
        release_date: datetime.date,
        available_set: list,
        related_card: list,
        attribute: MonsterAttributes,
        attack: int,
        defense: int,
        monster_type: MonsterTypes,
        monster_card_type: int, # the bit combination that represents the monster card types
        # extended
        level_rank_type: LevelRankTypes,
        level_rank_rating: int
    ):
        super().__init__(
            name = name,
            card_text = card_text,
            release_date = release_date,
            available_set = available_set,
            related_card = related_card,
            attribute = attribute,
            attack = attack,
            defense = defense,
            monster_type = monster_type,
            monster_card_type = monster_card_type
        )
        self.level_rank_type = level_rank_type
        self.level_rank_rating = level_rank_rating

class LinkMonsterCard(MonsterCard):
    def __init__(
        self,
        # inherited
        name: str,
        card_text: str,
        release_date: datetime.date,
        available_set: list,
        related_card: list,
        attribute: MonsterAttributes,
        attack: int,
        # link monster don't have defense
        # defense: int | None,
        monster_type: MonsterTypes,
        monster_card_type: int, # the bit combination that represents the monster card types
        # extended
        link_rating: int,
        link_arrow: int # the bit combination that represents the link arrows direction
    ):
        super().__init__(
            name = name,
            card_text = card_text,
            release_date = release_date,
            available_set = available_set,
            related_card = related_card,
            attribute = attribute,
            attack = attack,
            defense = None,
            monster_type = monster_type,
            monster_card_type = monster_card_type
        )
        self.link_rating = link_rating
        self.link_arrow = link_arrow

class PendulumMonsterCard(NonLinkMonsterCard):
    def __init__(
        self,
        # inherited
        name: str,
        card_text: str,
        release_date: datetime.date,
        available_set: list,
        related_card: list,
        attribute: MonsterAttributes,
        attack: int,
        defense: int,
        monster_type: MonsterTypes,
        monster_card_type: int, # the bit combination that represents the monster card types
        level_rank_type: LevelRankTypes,
        level_rank_rating: int,
        # extended
        pendulum_effect: str,
        pendulum_scale: int
    ):
        super().__init__(
            name = name,
            card_text = card_text,
            release_date = release_date,
            available_set = available_set,
            related_card = related_card,
            attribute = attribute,
            attack = attack,
            defense = defense,
            monster_type = monster_type,
            monster_card_type = monster_card_type,
            level_rank_type = level_rank_type,
            level_rank_rating = level_rank_rating
        )
        self.pendulum_effect = pendulum_effect
        self.pendulum_scale = pendulum_scale

# spell & trap card
class NonMonsterCard(Card):
    def __init__(
        self,
        # inherited
        name: str,
        card_text: str,
        release_date: datetime.date,
        available_set: list,
        related_card: list,
        # extended
        spell_trap_type: SpellTrapTypes,
        icon: SpellTrapIcons
    ):
        super().__init__(
            name = name,
            card_text = card_text,
            release_date = release_date,
            available_set = available_set,
            related_card = related_card
        )
        self.spell_trap_type = spell_trap_type
        self.icon = icon
