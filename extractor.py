import json, requests
from typing import List

from reference.card_reference import *
from reference.request_reference import *

# the url for search from the database
YUGIOH_DATABASE_URL = "https://www.db.yugioh-card.com/yugiohdb/card_search.action"

# exponential waiting varible
# in case of sending multiple requests results in the request being blocked,
# wait for some time (exponentially) before sending another request
DELAY = 1

# default parameter: the default / compulsory parameter for the request
# "ope" should stand for operation type? not so sure,
# but got the conclusion that it is necessary by trying the searching
DEFAULT_REQUEST_PARAMETER = {
    "ope" : "1"
}

# search card(s) from the database
def request_search_card(
        keyword: str | None = None,
        attribute: MonsterAttributes | List[MonsterAttributes] | None = None,
        icon: SpellTrapIcons | List[SpellTrapIcons] | None = None,
        monster_type: MonsterTypes | List[MonsterTypes] | None = None,
        monster_card_type: MonsterCardTypes_db | List[MonsterCardTypes_db] | None = None,
        exclude_monster_card_type: MonsterCardTypes_db | List[MonsterCardTypes_db] | None = None,
        level: int | List[int] | None = None,
        pendulum_scale: int | List[int] | None = None,
        link_rating: int | List[int] | None = None,
        link_arrow: LinkArrows | List[LinkArrows] | None = None,
        result_per_page: ResultsPerPage = ResultsPerPage["10"],
        sort_by: SortBy = SortBy["Sort by Name"],
        search_by: SearchBy = SearchBy["Card Name"],
        card_type: CardTypes | None = None,
        monster_card_type_condition: SearchCondition = SearchCondition["Or"],
        level_from: int | None = None,
        level_to: int | None = None,
        pendulum_scale_from: int | None = None,
        pendulum_scale_to: int | None = None,
        attack_from: int | None = None,
        attack_to: int | None = None,
        defence_from: int | None = None,
        defence_to: int | None = None,
        link_rating_from: int | None = None,
        link_rating_to: int | None = None,
        link_arrow_condition: SearchCondition = SearchCondition["Or"],
        release_day_from: int | None = None,
        release_month_from: int | None = None,
        release_year_from: int | None = None,
        release_day_to: int | None = None,
        release_month_to: int | None = None,
        release_year_to: int | None = None
    ) -> requests.Response:

    # get the necessary query parameter
    requestParameterDict = dict(DEFAULT_REQUEST_PARAMETER)
    # get the rest of the query parameter
    requestParameterDict.update(REQUEST_PARAMETER_TEMPLATE)

    # dictionary for storing potential duplicate query parameter
    requestDuplicateParameterDict = dict(REQUEST_DUPLICATE_PARAMETER_TEMPLATE)

    # check for keyword
    if (type(keyword) is str):
        requestParameterDict["keyword"] = keyword

    # check for result per page
    if (type(result_per_page) is ResultsPerPage):
        requestParameterDict["rp"] = result_per_page.value

    # check for sort by
    if (type(sort_by) is SortBy):
        requestParameterDict["sort"] = sort_by.value

    # check for search by
    if (type(search_by) is SearchBy):
        requestParameterDict["stype"] = search_by.value

    # check for card type
    if (type(card_type) is CardTypes):
        requestParameterDict["ctype"] = card_type.value

    # check for monster card type search condition
    if (type(monster_card_type_condition) is SearchCondition):
        requestParameterDict["othercon"] = monster_card_type_condition.value

    # check for level from & level to
    if (type(level_from) is int):
        requestParameterDict["starfr"] = level_from
    if (type(level_to) is int):
        requestParameterDict["starto"] = level_to

    # check for pendulum scale from & pendulum scale to
    if (type(pendulum_scale_from) is int):
        requestParameterDict["pscalefr"] = pendulum_scale_from
    if (type(pendulum_scale_to) is int):
        requestParameterDict["pscaleto"] = pendulum_scale_to

    # check for attack & defence range
    if (type(attack_from) is int):
        requestParameterDict["atkfr"] = attack_from
    if (type(attack_to) is int):
        requestParameterDict["atkto"] = attack_to
    if (type(defence_from) is int):
        requestParameterDict["deffr"] = defence_from
    if (type(defence_to) is int):
        requestParameterDict["defto"] = defence_to

    # check for link rating range
    if (type(link_rating_from) is int):
        requestParameterDict["linkmarkerfr"] = link_rating_from
    if (type(link_rating_to) is int):
        requestParameterDict["linkmarkerto"] = link_rating_to

    # check for link arrow search condition
    if (type(link_arrow_condition) is SearchCondition):
        requestParameterDict["link_m"] = link_arrow_condition.value

    # check for date range
    if (type(release_day_from) is int):
        requestParameterDict["releaseDStart"] = release_day_from
    if (type(release_month_from) is int):
        requestParameterDict["releaseMStart"] = release_month_from
    if (type(release_year_from) is int):
        requestParameterDict["releaseYStart"] = release_year_from
    if (type(release_day_to) is int):
        requestParameterDict["releaseDEnd"] = release_day_to
    if (type(release_month_to) is int):
        requestParameterDict["releaseMEnd"] = release_month_to
    if (type(release_year_to) is int):
        requestParameterDict["releaseYEnd"] = release_year_to

    # check for the parameter that can have duplicate value
    # check for attribute
    if (type(attribute) is MonsterAttributes):
        requestDuplicateParameterDict["attr"] = [("attr", attribute.value)]
    elif (type(attribute) is list):
        requestDuplicateParameterDict["attr"] = [("attr", item.value) for item in attribute if type(item) is MonsterAttributes]

    # check for spell / trap icons
    if (type(icon) is SpellTrapIcons):
        requestDuplicateParameterDict["effe"] = [("effe", icon.value)]
    elif (type(icon) is list):
        requestDuplicateParameterDict["effe"] = [("effe", item.value) for item in icon if type(item) is SpellTrapIcons]

    # check for monster type
    if (type(monster_type) is MonsterTypes):
        requestDuplicateParameterDict["species"] = [("species", monster_type.value)]
    elif (type(monster_type) is list):
        requestDuplicateParameterDict["species"] = [("species", item.value) for item in monster_type if type(item) is MonsterTypes]

    # check for monster card type
    if (type(monster_card_type) is MonsterCardTypes_db):
        requestDuplicateParameterDict["other"] = [("other", monster_card_type.value)]
    elif (type(monster_card_type) is list):
        requestDuplicateParameterDict["other"] = [("other", item.value) for item in monster_card_type if type(item) is MonsterCardTypes_db]

    # check for exclude monster card type
    if (type(exclude_monster_card_type) is MonsterCardTypes_db):
        requestDuplicateParameterDict["jogai"] = [("jogai", exclude_monster_card_type.value)]
    elif (type(exclude_monster_card_type) is list):
        requestDuplicateParameterDict["jogai"] = [("jogai", item.value) for item in exclude_monster_card_type if type(item) is MonsterCardTypes_db]

    # check for monster level
    if (type(level) is int):
        requestDuplicateParameterDict["level"] = [(f"level{level}", "on")]
    elif (type(level) is list):
        requestDuplicateParameterDict["level"] = [(f"level{item}", "on") for item in level if type(item) is int]

    # check for pendulum scale
    if (type(pendulum_scale) is int):
        requestDuplicateParameterDict["Pscale"] = [(f"Pscale{pendulum_scale}", "on")]
    elif (type(pendulum_scale) is list):
        requestDuplicateParameterDict["Pscale"] = [(f"Pscale{item}", "on") for item in pendulum_scale if type(item) is int]

    # check for link rating
    if (type(link_rating) is int):
        requestDuplicateParameterDict["Link"] = [(f"Link{link_rating}", "on")]
    elif (type(link_rating) is list):
        requestDuplicateParameterDict["Link"] = [(f"Link{item}", "on") for item in link_rating if type(item) is int]

    # check for link arrow
    if (type(link_arrow) is LinkArrows):
        requestDuplicateParameterDict["linkbtn"] = [(f"linkbtn{link_arrow.value}"), link_arrow.value]
    elif (type(link_arrow) is list):
        requestDuplicateParameterDict["linkbtn"] = [(f"linkbtn{item.value}", item.value) for item in link_arrow if type(item) is LinkArrows]


    # combine the dictionaries and make a list of tuple
    # i.e. ("<search_parameter>", <value>)
    # e.g. [("keyword", "mikanko"), ("starfr", 4), ...]
    requestParameterList = list(requestParameterDict.items())
    # each value in requestDuplicateParameterDict is definitely a list of tuple, if it is not None
    for item in requestDuplicateParameterDict.values():
        if item is not None:
            requestParameterList += item

    request = requests.request(
        method = "GET",
        url = YUGIOH_DATABASE_URL,
        params = requestParameterList
    )
    
    return request

if __name__ == "__main__":
    None
