from enum import Enum

from reference.reference import *

# available parameter for the query string
# parameter template: template to show what are the possible parameter (that does not have duplicate)
REQUEST_PARAMETER_TEMPLATE = {
    "rp" : 10, # number of results per page
    "sort" : 1, # sort by
    "keyword" : None, # search with specific word
    "stype" : 1, # search type for keyword (card name, card text, pendulum effect, card number)
    "ctype" : None, # card type (monster, spell, trap)
    "othercon" : 2, # and || or for the monster card type
    "starfr" : None, # monster card from this level / rank (inclusive)
    "starto" : None, # monster card to this level / rank (inclusive)
    "pscalefr" : None, # pendulum scale from this value (inclusive)
    "pscaleto" : None, # pendulum scale to this value (inclusive)
    "atkfr" : None, # monster attack from this value
    "atkto" : None, # monster attack to this value
    "deffr" : None, # monster defense from this value
    "defto" : None, # monster defense to this value
    "linkmarkerfr" : None, # link rating from this value
    "linkmarkerto" : None, # link rating to this value
    "link_m" : 2, # and || or for the link arrows position
    "releaseDStart" : None, # release day from this value
    "releaseMStart" : None, # release month from this value
    "releaseYStart" : None, # release year from this value
    "releaseDEnd" : None, # release day to this value
    "releaseMEnd" : None, # release month to this value
    "releaseYEnd" : None, # release year to this value
}

# the list of parameter that allows duplicate value
REQUEST_DUPLICATE_PARAMETER_TEMPLATE = {
    "attr" : None, # the list of monster attributes to search for
    "effe" : None, # the list of spell / trap icons to search for
    "species" : None, # the list of monster type to search for
    "other" : None, # list of monster card type to search for
    "jogai" : None, # list of monster card type to exclude (除外ですか？ ww)
    "level" : None, # list of level to search for
    "Pscale" : None, # list of pendulum scale to search for
    "Link" : None, # list of link rating to seach for
    "linkbtn" : None, # list of link arrows to search for
}

###########################################################################
# supporting data
SORT_BY = [
    "Sort by Name",
    "Sort by Level/Rank (Desc.)",
    "Sort by Level/Rank (Asc.)",
    "Sort by ATK (Desc.)",
    "Sort by ATK (Asc.)",
    "Sort by DEF (Desc.)",
    "Sort by DEF (Asc.)",
    "Sort by Pendulum Scale (Desc.)",
    "Sort by Pendulum Scale (Asc.)",
    "Sort by Link Rating (Desc.)",
    "Sort by Link Rating (Asc.)",
    "Sort by Release Date (Desc.)",
    "Sort by Release Date (Asc.)",
]

###########################################################################

# supporting enum or list for query parameter (the possible value)
ResultsPerPage = Enum("ResultsPerPage", [("10", 10), ("50", 50), ("100", 100)])
SortBy = Enum("SortBy", SORT_BY)
SearchBy = Enum("SearchBy", ["Card Name", "Card Text", "Pendulum Effect", "Card Number"])
SearchCondition = Enum("SearchCondition", ["And", "Or"])
