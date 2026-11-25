import json, requests, re, html, datetime, math, os, time
from typing import List, TypedDict
from enum import Enum

from reference.card_reference import *
from reference.request_reference import *
from reference.Card import *

# default size for image split
DEFAULT_IMAGE_SPLIT_AMOUNT = 1000
# default path to save the folders, files
DEFAULT_FOLDER_IMAGE = "card_image"
DEFAULT_FOLDER_FULL_IMAGE = "full"
DEFAULT_FOLDER_CROPPED_IMAGE = "cropped"

# official Yu-Gi-Oh database
# the root url for the database
YUGIOH_DATABASE_URL = "https://www.db.yugioh-card.com"
# the url for search action on the database
YUGIOH_DATABASE_SEARCH_URL = "https://www.db.yugioh-card.com/yugiohdb/card_search.action"

# YGO Pro Deck api for images
YGO_PRO_DECK_API = "https://db.ygoprodeck.com/api/v7/cardinfo.php"

# exponential waiting varible
# in case of sending multiple requests results in the request being blocked,
# wait for some time (exponentially) before sending another request
DELAY = 1

# for YGO Pro Deck api, the rate limit is 20 requests per second
# we only use the api for image
# we need two version of the image: full & cropped
# we also need to get the JSON of the card info to get the image link
# so to get the image(s) of a specific card, we need to send 3 requests
YGO_PRO_DECK_RATE = 20

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
        link_arrow: LinkArrows_db | List[LinkArrows_db] | None = None,
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
        release_year_to: int | None = None,
        page: int | None = 1
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

    # check for number of page to display (for continuous retrieving)
    if (type(page) is int):
        requestParameterDict["page"] = page

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
    if (type(link_arrow) is LinkArrows_db):
        requestDuplicateParameterDict["linkbtn"] = [(f"linkbtn{link_arrow.value}"), link_arrow.value]
    elif (type(link_arrow) is list):
        requestDuplicateParameterDict["linkbtn"] = [(f"linkbtn{item.value}", item.value) for item in link_arrow if type(item) is LinkArrows_db]


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
        url = YUGIOH_DATABASE_SEARCH_URL,
        params = requestParameterList
    )
    
    return request

# return the number of search results
# i.e. "Search Results: 41 - 50 of 14,068"
# i.e. {"current_start" : 41, "current_end" : 50, "total" : 14068}
# can be used at first request_search_card() and finding the amount of related cards
TypeSearchResultsDict = TypedDict("TypeSearchResultsDict", {"current_start" : int | None, "current_end" : int | None, "total" : int | None})
def request_search_results(
        response: requests.Response | None = None,
        response_text: str | None = None
    ) -> TypeSearchResultsDict:

    if (response is None and response_text is None):
        raise ValueError("The argument 'response' and 'response_text' cannot both be None at the same time.")

    if (type(response) is requests.Response):
        response_text = response.text

    # split the whole text into list of str, seperate by newline
    # reference: https://stackoverflow.com/a/15422155/21952784
    response_text_list = response_text.splitlines()
    # dictionary to be returned
    search_results_dict = {"current_start" : None, "current_end" : None, "total" : None}
    # placeholder list to store the value
    search_results_value = []

    for text in response_text_list:
        if "Search Results: " in text:
            # split the text by " "
            # e.g.  from " Search Results: 1 - 10 of 14,068"
            #       to ['\t\t\t\tSearch', 'Results:', '1', '-', '10', 'of', '14,068']
            text_list = text.split(' ')
            for item in text_list:
                try:
                    # replace the comma in the number, so that it can be converted to int
                    # reference: https://stackoverflow.com/a/2953756/21952784
                    item = item.replace(',', '')
                    search_results_value.append(int(item))
                except ValueError:
                    pass
            break

    if (len(search_results_dict.keys()) == len(search_results_value)):
        keys = list(search_results_dict.keys())
        for index in range(len(keys)):
            search_results_dict[keys[index]] = search_results_value[index]
    else:
        raise ValueError("Unexpected value error: The number of keys in search_results_dict is not equal to the number of search_results_value.")

    return search_results_dict

# get the list of card url (or related url) on the page
# i.e.  after searching, there should be "Search Results: <x amount> - <y amount> of <z amount>"
#       this function then return list of (x to y) cards that are displaying on the page
# 1. can be used at first request_search_card() to get the list of cards that fulfill the search condition
# 2. can be used to find the list of available set url of a card (need filter)
# 3. can be used to find the list of related card url of a card (need filter)
def request_card_url_list(
        response: requests.Response | None = None,
        response_text: str | None = None
    ) -> List[str]:

    if (response is None and response_text is None):
            raise ValueError("The argument 'response' and 'response_text' cannot both be None at the same time.")

    if (type(response) is requests.Response):
            response_text = response.text

    response_text_list = response_text.splitlines()
    card_url_list = []

    for text in response_text_list:
        if "class=\"link_value\"" in text:
            # if the text match, it should have a format like:
            # <input type="hidden" class="link_value" value="/yugiohdb/card_search.action?ope=2&amp;cid=21385&amp;iid=1">
            # remove the '<' and '>' at the front and back for easier splitting
            text = text[1:-1]
            # then, split the text by space, which gives a list of str
            # e.g.
            # ['input', 'type="hidden"', 'class="link_value"', 'value="/yugiohdb/card_search.action?ope=2&amp;cid=21385&amp;iid=1"']
            # take the last element (contain the card url link)
            text = text.split(' ')[-1]
            # remove the prefix "value="
            # remove the double quote
            text = text.removeprefix("value=").replace('"', '')
            # add the link to the list
            card_url_list.append(text)

    return card_url_list

# browse a specific card (with a link that direct you to the card page)
def request_browse_specific_card(
        card_url: str,
        result_per_page: ResultsPerPage | None = None,
        page: int | None = None,
        language: Language | None = None
    ) -> requests.Response:

    requestParameterDict = dict(REQUEST_BROWSING_PARAMETER_TEMPLATE)

    # note that the default result per page is 100 for browsing specific card
    # (easier to extract related cards information)
    if (type(result_per_page) is ResultsPerPage):
        requestParameterDict["rp"] = result_per_page.value

    if (type(page) is int):
        requestParameterDict["page"] = page

    if (type(language) is Language):
        requestParameterDict["request_locale"] = language.value

    request = requests.request(
        method = "GET",
        url = YUGIOH_DATABASE_URL + card_url,
        params = requestParameterDict
    )

    return request

# retrieve the information of the specific card, from the response
def extract_specific_card_information(
        card_url: str
    ) -> Card:

    # request the page of the specific card
    response = request_browse_specific_card(card_url)
    response_text = response.text

    # unescape html character
    # e.g. "&lt;" -> '<
    response_text = html.unescape(response_text)

    # split the response text by "<div id=\"CardSet\">"
    # the html elements between "<div id=\"CardSet\">" and "<!-- #CardSet -->"
    # contain the necessary information of the card
    # after splitting you will get a list with two elements,
    # [0] is the text before the split text,
    # [1] is the text after the split text
    cardInformationText = response_text.split("<div id=\"CardSet\">")[1]
    # the necessary card information is between:
    # 1. "<div id=\"CardSet\">"
    # 2. "<!-- #CardSet -->"
    cardInformationText = cardInformationText.split("<!-- #CardSet -->")[0]
    # split the text by lines to get a list
    cardInformationTextList = cardInformationText.splitlines()

    # count the html element with class "item_box_value"
    # with the format of yugioh database,
    # the number of element with this class hint the type of the card
    # 3: spell / trap
    # 6: non-pendulum monster
    # 7: pendulum monster
    mainValueCount = cardInformationText.count("class=\"item_box_value\"")

    # the line after the html element with class "item_box_value"
    # represents some value of the card,
    # 3 -> [icon of spell or trap]
    # 6 -> [attribute, (level / rank / link), attack, defence]
    # 7 -> [attribute, (level / rank / link), attack, defence, pendulum scale]
    # the last two elements with this class are always the language button (ocg/tcg)
    # thus, the amount of information you can retrieve from the mainValueCount is: mainValueCount - 2
    # e.g.  if there is 6 "class=\"item_box_value\"" from the text, that means the card is a non-pendulum monster,
    #       and the amount of information I can retrieve is: [attribute, (level / rank / link), attack, defence] (6-2=4)
    valueInformationList = []
    for index in range(len(cardInformationTextList)):
        if "class=\"item_box_value\"" in cardInformationTextList[index] and len(valueInformationList) < mainValueCount - 2:
            valueInformationList.append("")
            for index2 in range(index + 1, len(cardInformationTextList)):
                if "</span>" not in cardInformationTextList[index2]:
                    valueInformationList[len(valueInformationList) - 1] += cardInformationTextList[index2]
                else:
                    break;

        if (len(valueInformationList) >= mainValueCount - 2):
            break
    
    # put character '\t' and '\' as part of the regular expression format
    # https://stackoverflow.com/a/56206194/21952784
    reFormat = re.compile(r"(\\\t)|\\")
    # the text copy from html text contain the escape character '\t',
    # remove the escape character by using regular expression
    # reference: https://stackoverflow.com/a/4202559/21952784
    valueInformationList = [reFormat.sub('', re.escape(text)) for text in valueInformationList]

    # get the card name
    # tha card name is between <h1> tag,
    # the returned card name may contain multiple '\t', so filter is needed
    cardName: str = None
    for index in range(len(cardInformationTextList)):
        if "<h1>" in cardInformationTextList[index]:
            cardName = ""
            for index2 in range(index + 1, len(cardInformationTextList)):
                if "</h1>" not in cardInformationTextList[index2]:
                    cardName += cardInformationTextList[index2]
                else:
                    break
        if cardName is not None:
            cardName = reFormat.sub('', re.escape(cardName))
            break

    # check the number of item obtained for valueInformationList
    # 1: spell / trap card
    # 4: non-pendulum monster
    # 5: pendulum monster
    # if it is not a spell / trap, identify the monster type and monster card type
    if (len(valueInformationList) != 1):
        # for monster type list, the first array element is always the species (monster type),
        # the subsequent element would be the monster card type (effect, ritual)
        monsterTypeList: list = []
        # regular expression for monster type format
        # search for any character that is not alphabet or '-' or ' '
        # include space because "Sea Serpent" has space
        reMonsterTypeFormat = re.compile(r"[^a-zA-Z- ]")
        for index in range(len(cardInformationTextList)):
            # the monster type and monster card type is within the paragraph
            # <p class="species"> </p>
            if "class=\"species\"" in cardInformationTextList[index]:
                for index2 in range(index + 1, len(cardInformationTextList)):
                    if "</p>" not in cardInformationTextList[index2]:
                        # the html content in the paragraph contain '\t',
                        # thus use regular expression to escape the character and remove them
                        monsterTypes = reFormat.sub('', re.escape(cardInformationTextList[index2]))
                        # remove the html <span> tag in betweem
                        monsterTypes = monsterTypes.removeprefix("<span>").removesuffix("</span>")
                        # the website use a special slash character, 
                        # which is not in ascii to seperate the different monster type (probably slash in japanese input)
                        # check if the content is equal to empty string after all the filter
                        if (monsterTypes != ""):
                            # if not empty, replace the slash to normal comma
                            monsterTypes = reMonsterTypeFormat.sub(',', monsterTypes)
                            # split the results by comma (in case there are multiple types)
                            # e.g.  from: "Ritual／Effect"
                            #       to: "Ritual,Effect"
                            monsterTypes = monsterTypes.split(',')
                            # if there is a resulting list
                            if (type(monsterTypes) is list):
                                # check for empty string, as the website has a <span> with only slash,
                                # so after all the filter will result in an empty string for that <span>
                                monsterTypeList += [monsterType for monsterType in monsterTypes if monsterType != ""]
                            else: # else, it probably is a monster type (species) (instead of monster card type, i.e. effect, synchro)
                                monsterTypeList.append(monsterTypes)

                    # break if encounter "</p>", 
                    # it means the paragraph related to monster type has ended
                    else:
                        break

            # early break if we already added monster type value into the list
            if (len(monsterTypeList) > 1):
                break

    cardText: str = ""
    # search for the card text
    # within the cardInformationText, the card text is within the
    # <div class="text_linebreak"> </div>
    # the text is in a single line of the <div>
    # for pendulum monster, there can be 2 class="text_linebreak",
    # 1 for pendulum effect, another for normal card text
    # thus, we can have an additional filter (split) of:
    # 1. <!-- #CardTextSet -->
    # 2. class="CardText"
    cardTextText = cardInformationText.split("<!-- #CardTextSet -->")[1]
    cardTextText = cardTextText.split("class=\"CardText\"")[1]
    cardTextTextList = cardTextText.splitlines()
    for text in cardTextTextList:
        if "class=\"text_linebreak\"" in text:
            # remove the '\t' from the text
            cardText = reFormat.sub('', re.escape(text))
            # remove the prefix and suffix <div> to get the pure card text
            cardText = cardText.removeprefix("<div class=\"text_linebreak\">").removesuffix("</div>")
            # replace the <br> from the html text to escape character '\n'
            cardText = cardText.replace("<br>", '\n')
            break

    releaseDate: datetime.date | None = None
    releaseDateString: str = ""
    availableSet: list = []
    # check for release date and available set
    # the required body text is between:
    # 1. <div class="t_body">
    # 2. <!--#update_list-->
    cardReleaseInformationText = response_text.split("<div class=\"t_body\">")[1]
    cardReleaseInformationText = cardReleaseInformationText.split("<!--#update_list-->")[0]
    cardReleaseInformationTextList = cardReleaseInformationText.splitlines()

    # the release date is written in <div class="time"> </div>
    # thus, count the number of time "<div class="time">",
    # we can get the number of set the card is released on (though duplicate can happened due to different rarity, thus require filter)
    availableSetAmount = cardReleaseInformationText.count("<div class=\"time\">")
    
    # the oldest release date is in the last <div class="time">
    # the available set is in <div class="pack_name flex_1" > </div>
    traversedSet = 0
    for index in range(len(cardReleaseInformationTextList)):
        # read the available set of the card
        if "<div class=\"pack_name flex_1\" >" in cardReleaseInformationTextList[index]:
            availableSet.append("")
            for index2 in range(index + 1, len(cardReleaseInformationTextList)):
                if "</div>" not in cardReleaseInformationTextList[index2]:
                    availableSet[traversedSet] += cardReleaseInformationTextList[index2]
                else:
                    # remove the escape character '\t'
                    availableSet[traversedSet] = reFormat.sub('', re.escape(availableSet[traversedSet]))
                    traversedSet += 1
                    break

        # retrieve the date if it is the last set
        # traversedSet + 1 because in the website, the date comes before the set name
        # thus, we need to retrieve the date at second last iteration
        # HOWEVER
        # some cards' last available set does not have a release date
        # because they are from some tournament
        # SO NOW I NEED TO TRAVERSE AND RECORD THE EVERY DATE
        # until an exception which means there is no earlier date
        # BUT
        # WAIT A MINUTE
        # YOU THOUGHT IF THERE IS NO DATE
        # THEN THERE WOULDN'T BE A TIME CLASS?
        # YOU FUCKING DUMBASS
        # even if there is no actual date, there would still be a time class <div>
        # so you need to format yourself and see if there is actual date or it is empty time div
        # BUT WAIT
        # YOU THOUGHT THE CARD AT THE VERY LEAST MUST HAVE A DATE?
        # FUCKING DUMBASS
        # there is card(s) where release date is not on official record
        if "<div class=\"time\">" in cardReleaseInformationTextList[index]:
            # record new potential string
            potentialReleaseDateString = ""
            for index2 in range(index + 1, len(cardReleaseInformationTextList)):
                if "</div>" not in cardReleaseInformationTextList[index2]:
                    potentialReleaseDateString += cardReleaseInformationTextList[index2]
                else:
                    # remove the escape character '\t'
                    potentialReleaseDateString = reFormat.sub('', re.escape(potentialReleaseDateString))
                    # check if the potential release date string is real
                    # reference: https://stackoverflow.com/a/24476708/21952784
                    try:
                        datetime.datetime.strptime(potentialReleaseDateString, "%Y-%m-%d").date()
                        releaseDateString = potentialReleaseDateString
                    except:
                        pass
                    break

        # early break if traversedSet is equal to availableSetAmount
        if (traversedSet == availableSetAmount):
            # convert list to set to remove duplicate, then convert it back to list again for format
            # reference: https://stackoverflow.com/a/9841328/21952784
            # I was actually so drunk I searched "removed duplicate from string" instead of "remove duplicate from list" but it still work www
            availableSet = list(set(availableSet))
            # convert date string to list and convert it to datetime.date type
            releaseDateValueList = releaseDateString.split('-')
            # there are cards with no release date record, in this case, keep it as None
            try:
                releaseDate = datetime.date(int(releaseDateValueList[0]), int(releaseDateValueList[1]), int(releaseDateValueList[2]))
            except:
                releaseDate = None
            break

    # check for the related cards
    # the number of related cards can be get from "Search Results: 1 - 10 of 39"
    # (use request_search_results())
    # the content for related cards is between:
    # 1. <div class="list_style" id="relationCard">
    # 2. <!-- ///count  -->
    # note that for 1., from the website, it actually show:
    # <div id="relationCard" class="list_style">
    # (the order of class and id is reverse)
    # so just in case, only check for the id
    # some cards don't have related cards, so a try catch is needed
    hasRelatedCard = True
    relatedCardList: list = []
    try:
        relatedCardText = response_text.split("id=\"relationCard\"")[1]
        relatedCardText = relatedCardText.split("<!-- ///count  -->")[0]
        relatedCardTextList = relatedCardText.splitlines()
    except:
        hasRelatedCard = False

    if (hasRelatedCard):
        relatedCardSearchResults: TypeSearchResultsDict = {}
        relatedCardSearchResults = request_search_results(response_text = relatedCardText)
        # which page of the related card we are at
        currentRelatedCardPage = 1
        # how many results per page we want
        resultsPerPage = ResultsPerPage["100"]
        # get the maximum pages of related card (divide by resultsPerPage to calculate the maximum page, given we have x results per page)
        # some cards only have a page of related card, so "total" - "current_end" would be 0,
        # thus, the answer need to +1
        maxRelatedCardPage = math.ceil((relatedCardSearchResults["total"] - relatedCardSearchResults["current_end"]) / resultsPerPage.value) + 1
        for index in range(0, maxRelatedCardPage):
            # the card name of related card is within
            # <span class="card_name"> </span>
            for textIndex in range(len(relatedCardTextList)):
                if "class=\"card_name\"" in relatedCardTextList[textIndex]:
                    relatedCardList.append("")
                    for textIndex2 in range(textIndex + 1, len(relatedCardTextList)):
                        if "</span>" not in relatedCardTextList[textIndex2]:
                            relatedCardList[-1] += relatedCardTextList[textIndex2]
                        else:
                            # remove escape character
                            relatedCardList[-1] = reFormat.sub('', re.escape(relatedCardList[-1]))
                            break

                # early break if it reaches the current_end (current maximum related card that can be retrieved)
                if (len(relatedCardTextList) == relatedCardSearchResults["current_end"]):
                    break

            # after finishing the current page, retrieve the next page (if available)
            if (currentRelatedCardPage < maxRelatedCardPage):
                # request a new response (the subsequent page of related cards)
                newResponse = request_browse_specific_card(card_url, page = currentRelatedCardPage + 1)
                currentRelatedCardPage += 1
                # filter the response text and find the new related cards text section
                newResponseText = newResponse.text
                newResponseText = html.unescape(newResponseText)
                relatedCardText = newResponseText.split("id=\"relationCard\"")[1]
                relatedCardText = relatedCardText.split("<!-- ///count  -->")[0]
                relatedCardTextList = relatedCardText.splitlines()

    # extract the information from valueInformationList
    # array element : value
    # 1             : (spell / trap icon) || monster attribute
    # 2             : level / rank / link rating
    # 3             : attack
    # 4             : defence
    # 5             : pendulum scale
    cardType: CardTypes = None
    if (len(valueInformationList) == 1):
        # if the length of valueInformationList is 1, it is guarantee to be a spell or trap
        # split the value by ' ' to get the spell / trap icon and card type
        # e.g. "Counter Trap" -> ["Counter", "Trap"]
        valueInformationList = valueInformationList[0].split(' ')
        cardType = CardTypes[valueInformationList[-1]]
    else:
        # don't split the second element
        # i.e. keep "Rank 12" as it, since we need to differentiate level / rank later on
        cardType = CardTypes["Monster"]
        # convert the attack & defense into appropriate value (int || str)
        # str for '-' (link monster) or special case '?'
        try:
            valueInformationList[2] = int(valueInformationList[2])
        except ValueError:
            # keep it as str if can't be convert into int
            pass
        try:
            valueInformationList[3] = int(valueInformationList[3])
        except ValueError:
            # keep it as str if can't be convert into int
            pass
    
    if (len(valueInformationList) == 5):
        # if the length of valueInformationList is 5, it is a pendulum monster
        # process the last element of array to extract the pure number value
        # e.g. "Pendulum Scale 13" -> ["Pendulum", "Scale", "13"] -> "13"
        valueInformationList[-1] = int(valueInformationList[-1].split(' ')[-1])

    card: Card = None
    # create the Card object based on the length of valueInformationList after processing the value
    # length    : card type
    # 2         : spell / trap
    # 4         : non-pendulum monster
    # 5         : pendulum monster
    if (len(valueInformationList) == 2):
        # if it is a spell / trap, the array element would be:
        # [Icon, (Spell || Trap)]
        card = NonMonsterCard(
            name = cardName,
            card_text = cardText,
            release_date = releaseDate,
            available_set = availableSet,
            related_card = relatedCardList,
            spell_trap_type = SpellTrapTypes[valueInformationList[-1]],
            icon = SpellTrapIcons[valueInformationList[0]]
        )
    elif (len(valueInformationList) == 4):
        # if it is a non-pendulum monster
        # calculate the bit combination that represents the monster card type
        monsterCardType = 0
        # start from second element since the first element is monster species
        for monsterCardTypeValue in monsterTypeList[1:]:
            monsterCardType += MonsterCardTypes[monsterCardTypeValue].value

        # check the last array element (defence) to see if it is a link monster
        if (valueInformationList[-1] == '-'):
            # if defence is '-', then it is a link monster
            # calculate the bit combination that represents the link arrow direction
            # extract the text that contains information about link arrow,
            # which is inside <span class="icon_img_set link846" alt="Link" title="Link">
            # the key is the "link846", where 846 represents the link arrow direction
            # we can filter the text by finding the span that contains: alt="Link"
            linkArrow: int = 0
            for text in cardInformationTextList:
                if "alt=\"Link\"" in text:
                    # remove the escape character '\t'
                    text = reFormat.sub('', re.escape(text))
                    # split the text by '"', the "icon_img_set link846" would be the second element after the split
                    text = text.split('"')[1]
                    # split it again by "link"
                    # i.e. "link846" -> ["", "846"]
                    linkText = text.split("link")[-1]
                    # add all the value together (with respect to the bit representation)
                    for value in linkText:
                        linkArrow += LinkArrows_db[value].value
                    break
            
            card = LinkMonsterCard(
                name = cardName,
                card_text = cardText,
                release_date = releaseDate,
                available_set = availableSet,
                related_card = relatedCardList,
                attribute = MonsterAttributes[valueInformationList[0]],
                attack = valueInformationList[2],
                monster_type = MonsterTypes[monsterTypeList[0]],
                monster_card_type = monsterCardType,
                # split "Link x" to ["Link", "x"]
                link_rating = int(valueInformationList[1].split(' ')[-1]),
                link_arrow = linkArrow
            )
        else:
            # else, it is a non-link monster
            card = NonLinkMonsterCard(
                name = cardName,
                card_text = cardText,
                release_date = releaseDate,
                available_set = availableSet,
                related_card = relatedCardList,
                attribute = MonsterAttributes[valueInformationList[0]],
                attack = valueInformationList[2],
                defense = valueInformationList[3],
                monster_type = MonsterTypes[monsterTypeList[0]],
                monster_card_type = monsterCardType,
                # split "Level 4" to ["Level", "4"] to get level rank type and rating
                level_rank_type = LevelRankTypes[valueInformationList[1].split(' ')[0]],
                level_rank_rating = int(valueInformationList[1].split(' ')[-1])
            )
    elif (len(valueInformationList) == 5):
        # if it is a pendulum monster
        # calculate the bit combination that represents the monster card type
        monsterCardType = 0
        # start from second element since the first element is monster species
        for monsterCardTypeValue in monsterTypeList[1:]:
            monsterCardType += MonsterCardTypes[monsterCardTypeValue].value

        pendulumEffectText: str = ""
        # extract the pendulum effect, which is between:
        # 1. class="CardText pen"
        # 2. <!-- CardText -->
        pendulumEffectTextText = cardInformationText.split("class=\"CardText pen\"")[1]
        pendulumEffectTextText = pendulumEffectTextText.split("<!-- CardText -->")[0]
        pendulumEffectTextTextList = pendulumEffectTextText.splitlines()
        for text in pendulumEffectTextTextList:
            if "class=\"text_linebreak\"" in text:
                # remove the '\t' from the text
                pendulumEffectText = reFormat.sub('', re.escape(text))
                # remove the prefix and suffix <div> to get the pure card text
                pendulumEffectText = pendulumEffectText.removeprefix("<div class=\"text_linebreak\">").removesuffix("</div>")
                # replace the <br> from the html text to escape character '\n'
                pendulumEffectText = pendulumEffectText.replace("<br>", '\n')
                break

        card = PendulumMonsterCard(
            name = cardName,
            card_text = cardText,
            release_date = releaseDate,
            available_set = availableSet,
            related_card = relatedCardList,
            attribute = MonsterAttributes[valueInformationList[0]],
            attack = valueInformationList[2],
            defense = valueInformationList[3],
            monster_type = MonsterTypes[monsterTypeList[0]],
            monster_card_type = monsterCardType,
            # split "Level 4" to ["Level", "4"] to get level rank type and rating
            level_rank_type = LevelRankTypes[valueInformationList[1].split(' ')[0]],
            level_rank_rating = int(valueInformationList[1].split(' ')[-1]),
            pendulum_effect = pendulumEffectText,
            pendulum_scale = int(valueInformationList[4])
        )

    return card

# parsing the card information into dict
def parse_card_information(card: Card, bin: bool = False) -> dict:
    # convert object to dictionary for parsing as JSON
    # reference: https://stackoverflow.com/a/10252138/21952784
    card_dict = card.__dict__
    # convert value to string type for storing
    for key in card_dict.keys():
        # check if the value is an Enum
        if (isinstance(card_dict[key], Enum)):
            # take the string representation
            card_dict[key] = card_dict[key].name
        # check if the value is datetime
        if (type(card_dict[key]) is datetime.date):
            # convert date to string format
            card_dict[key] = str(card_dict[key])

    # if don't want binary conversion (for monster card type and link arrow direction)
    # TODO: add code to output JSON file that doesn't have monster card type and link arrow direction as binary representation by default
    if not bin:
        pass

    return card_dict

# convert card information into JSON and write it to a file
def write_card_information(
        card_dict: dict,
        folder_path: str | None = None,
        file_name: str | None = None,
        bin: bool = False
    ):

    if (folder_path is None):
        folder_path = "individual_card/"

    if (file_name is None):
        file_name = f"{card_dict['filename']}.json"

    if not (os.path.exists(folder_path)):
        os.makedirs(folder_path)

    jsonString = json.dumps(card_dict, indent = 4)
    file = open(os.path.join(folder_path, file_name), mode = "w", encoding = "utf-8")
    file.write(jsonString)
    file.close()
    print(f"Created file: {file_name}")

# retrieve all the cards from the database and write to files
def retrieve_all_cards(
        folder_path: str | None = "individual_card/",
        from_page: int = 1,
        results_per_page: ResultsPerPage = ResultsPerPage["10"],
        bin: bool = False
    ):

    try:
        # record the current and total page
        currentPage = from_page
        totalPage = 0
        # the total yugioh card dict
        retrievingCard = 0
        totalCard = 0

        response = request_search_card(page = currentPage, result_per_page = results_per_page)
        searchResults = request_search_results(response)

        # total page is the amount of total cards divide by results per page
        # no +1 like the code above since it doesn't account (deduct) current page
        # and we have totalPage + 1 at the below
        totalPage = math.ceil(searchResults["total"] / results_per_page.value)
        retrievingCard = searchResults["current_start"]
        totalCard = searchResults["total"]

        # totalPage + 1 because range is exclusive
        for page in range(currentPage, totalPage + 1):
            print("#" * 40)
            print(f"Page: {currentPage} of {totalPage}")
            print("#" * 40)
            cardUrlList = request_card_url_list(response)
            for url in cardUrlList:
                print(f"Retrieving card: {retrievingCard} of {totalCard}", end = "\t\t\t")
                card = extract_specific_card_information(url)
                cardDict = parse_card_information(card)
                write_card_information(cardDict, folder_path = folder_path)
                # log into the file to record card retrieved
                file = open(os.path.join(folder_path, "log.txt"), mode = "a", encoding = "utf-8")
                file.write(f"log: #{retrievingCard}\t\t\t{cardDict['name']}\n")
                file.close()
                retrievingCard += 1
                print("done")

            response = request_search_card(page = page + 1, result_per_page = results_per_page)
            currentPage += 1
    
    # if requests exception, start again from the nearest checkpoint
    except (requests.RequestException, requests.ConnectionError, requests.ConnectTimeout, requests.ReadTimeout, requests.Timeout) as e:
        print("\nRequests exception... trying again...")
        file = open(os.path.join(folder_path, "log.txt"), mode = "a", encoding = "utf-8")
        file.write(f"log: exception occured - {e}\n##############################\n")
        file.close()
        retrieve_all_cards(from_page = currentPage, results_per_page = results_per_page)

# convert the card JSON list into a single JSON file
def convert_single_json(folder_path: str):
    jsonFiles = [file for file in os.listdir(folder_path) if file.endswith(".json")]
    jsonFiles.sort()
    cardInformationList = []
    for jsonFile in jsonFiles:
        jsonFile = open(os.path.join(folder_path, jsonFile), mode = "r", encoding = "utf-8")
        cardInformationList.append(json.loads(jsonFile.read()))
        jsonFile.close()

    newJSONstring = json.dumps(cardInformationList, indent = 4)
    newFile = open("card_information.json", mode = "w", encoding = "utf-8")
    newFile.write(newJSONstring)
    newFile.close()

# TODO: make the retrieve image doesn't require preexisting individual card JSON files
# retrieve images
def retrieve_images(
        full: bool = True,
        cropped: bool = True,
        card_json_folder: str = "individual_card/",
        save_to_folder: str = "card_image/"
    ):

    # check if folder to save to exist
    if (not os.path.exists(save_to_folder)):
        os.makedirs(save_to_folder)
    # check for folder to save full / cropped to, and create log file
    if (full):
        if (not os.path.exists(os.path.join(save_to_folder, "full"))):
            os.makedirs(os.path.join(save_to_folder, "full"))
        fullLogFile = open(f"{os.path.join(save_to_folder, 'full', 'log.txt')}", mode = "w", encoding = "utf-8")
    if (cropped):
        if (not os.path.exists(os.path.join(save_to_folder, "cropped"))):
            os.makedirs(os.path.join(save_to_folder, "cropped"))
        croppedLogFile = open(f"{os.path.join(save_to_folder, 'cropped', 'log.txt')}", mode = "w", encoding = "utf-8")

    imageTypeAmount = full + cropped
    fileList = []

    # open JSON files in the folder to read the card name
    fileList = [file for file in os.listdir(card_json_folder) if file.endswith(".json")]
    fileList.sort()
    # keep track of how many image to download and how many total card there is
    downloadedImage = 0
    totalCard = len(fileList)

    # iterate fileList to read the card JSON
    while (len(fileList) > 0):
        cardFile = open(os.path.join(card_json_folder, fileList.pop()), mode = "r", encoding = "utf-8")
        cardJSON = cardFile.read()
        cardFile.close()
        cardDict = json.loads(cardJSON)

        ygoProDeckRequest = requests.request(
            url = YGO_PRO_DECK_API,
            method = "GET",
            params = {"name" : cardDict["name"]}
        )

        requestJSON = ygoProDeckRequest.json()
        # check to download full image and cropped image
        try:
            # check if the image has already exists or not,
            # and if the file not exist, download the file
            if (full and not os.path.exists(os.path.join(save_to_folder, "full", f"{cardDict['filename']}.jpg"))):
                # get the full image link
                fullImageLink = requestJSON["data"][0]["card_images"][0]["image_url"]
                imageResponse = requests.get(fullImageLink)
                # write to the file with binary
                # refference: https://stackoverflow.com/a/63978199/21952784 (write image to file with requests)
                # refference: https://stackoverflow.com/a/2665873/21952784 (what is "wb")
                fullImage = open(f"{os.path.join(save_to_folder, 'full', cardDict['filename'])}.jpg", mode = "wb")
                fullImage.write(imageResponse.content) # content is bytes type
                fullImage.close()
                fullLogFile.write(f"Downloaded full image of: {cardDict['name']}\n")
                print(f"Downloaded full image of: {cardDict['name']}")
        except Exception as e:
            fullLogFile.write(f"##############################\n")
            fullLogFile.write(f"Exception occured for full image of: {cardDict['name']}\t\t{e}\n")
            fullLogFile.write(f"##############################\n")

        # TODO: manually process the images that cannot be retrieved from YGO Pro deck
        try:
            if (cropped and not os.path.exists(os.path.join(save_to_folder, "cropped", f"{cardDict['filename']}.jpg"))):
                croppedImageLink = requestJSON["data"][0]["card_images"][0]["image_url_cropped"]
                imageResponse = requests.get(croppedImageLink)
                croppedImage = open(f"{os.path.join(save_to_folder, 'cropped', cardDict['filename'])}.jpg", mode = "wb")
                croppedImage.write(imageResponse.content)
                croppedImage.close()
                croppedLogFile.write(f"Downloaded cropped image of: {cardDict['name']}\n")
                print(f"Downloaded cropped image of: {cardDict['name']}")
        except Exception as e:
            croppedLogFile.write(f"##############################\n")
            croppedLogFile.write(f"Exception occured for cropped image of: {cardDict['name']}\t\t{e}\n")
            croppedLogFile.write(f"##############################\n")

        downloadedImage += 1
        print(f"Progress: downloaded {downloadedImage} of {totalCard}\n")
        # sleep to prevent reaching rate limit
        time.sleep(1 / (YGO_PRO_DECK_RATE / (imageTypeAmount + 1)))

    if (full):
        fullLogFile.close()
    if (cropped):
        croppedLogFile.close()

# split the card images into smaller folder (batch) for easier transfer
def split_card_images(
        full: bool = True,
        cropped: bool = True,
        full_folder: str = os.path.join(DEFAULT_FOLDER_IMAGE, DEFAULT_FOLDER_FULL_IMAGE),
        cropped_folder: str = os.path.join(DEFAULT_FOLDER_IMAGE, DEFAULT_FOLDER_CROPPED_IMAGE)
    ):

    if (full):
        # list the image files and sort by name
        fullImageFiles = [file for file in os.listdir(full_folder) if file.endswith(".jpg")]
        fullImageFiles.sort()

        # calculate how many time to split the image to batch
        # ceiling because 1200 / 1000 -> 1.2, which should be 2 batch
        splitCount = math.ceil(len(fullImageFiles) / DEFAULT_IMAGE_SPLIT_AMOUNT)

        if (not os.path.exists("card_image_split/full")):
            os.makedirs("card_image_split/full")

        for index in range(splitCount):
            imageBatch = []
            # if not the last batch
            if (index != splitCount - 1):
                # add the split amount into the batch
                for i in range(DEFAULT_IMAGE_SPLIT_AMOUNT):
                    # add the first image to the image batch list
                    imageBatch.append(fullImageFiles.pop(0))
            # else, add the remaining image files into the batch
            else:
                while (len(fullImageFiles) > 0):
                    imageBatch.append(fullImageFiles.pop(0))
            
            # save the files to a new folder
            # name: batch_<current index>_<max index>
            savePath = f"card_image_split/full/batch_{index + 1}_{splitCount}"
            if (not os.path.exists(savePath)):
                os.makedirs(savePath)
            
            # copy the file to the save path by reading and writing binary
            while (len(imageBatch) > 0):
                imageFileName = imageBatch.pop(0)
                readImageFile = open(os.path.join(full_folder, imageFileName), mode = "rb")
                imageFile = readImageFile.read()
                readImageFile.close()
                writeImageFile = open(os.path.join(savePath, imageFileName), mode = "wb")
                writeImageFile.write(imageFile)
                writeImageFile.close()

    if (cropped):
        # list the image files and sort by name
        croppedImageFiles = [file for file in os.listdir(cropped_folder) if file.endswith(".jpg")]
        croppedImageFiles.sort()

        # calculate how many time to split the image to batch
        # ceiling because 1200 / 1000 -> 1.2, which should be 2 batch
        splitCount = math.ceil(len(croppedImageFiles) / DEFAULT_IMAGE_SPLIT_AMOUNT)

        if (not os.path.exists("card_image_split/cropped")):
            os.makedirs("card_image_split/cropped")

        for index in range(splitCount):
            imageBatch = []
            # if not the last batch
            if (index != splitCount - 1):
                # add the split amount into the batch
                for i in range(DEFAULT_IMAGE_SPLIT_AMOUNT):
                    # add the first image to the image batch list
                    imageBatch.append(croppedImageFiles.pop(0))
            # else, add the remaining image files into the batch
            else:
                while (len(croppedImageFiles) > 0):
                    imageBatch.append(croppedImageFiles.pop(0))
            
            # save the files to a new folder
            # name: batch_<current index>_<max index>
            savePath = f"card_image_split/cropped/batch_{index + 1}_{splitCount}"
            if (not os.path.exists(savePath)):
                os.makedirs(savePath)
            
            # copy the file to the save path by reading and writing binary
            while (len(imageBatch) > 0):
                imageFileName = imageBatch.pop(0)
                readImageFile = open(os.path.join(cropped_folder, imageFileName), mode = "rb")
                imageFile = readImageFile.read()
                readImageFile.close()
                writeImageFile = open(os.path.join(savePath, imageFileName), mode = "wb")
                writeImageFile.write(imageFile)
                writeImageFile.close()

# convert existing JSON from bin to non-bin or vise versa
def convert_bin_format(
        folder_path: str = "individual_card_bin/",
        new_folder_path: str = "individual_card/",
        bin_to_nonbin: bool = True
    ):

    # TODO: implement bin_to_nonbin (non binary representation to binary representation)

    # get the list of JSON files
    jsonFileList = [file for file in os.listdir(folder_path) if file.endswith(".json")]

    # iterate and change the content, then write to new file
    for fileName in jsonFileList:
        file = open(os.path.join(folder_path, fileName), mode = "r", encoding = "utf-8")
        fileString = file.read()
        file.close()

        # parse card JSON to dictionary
        cardDict: dict = json.loads(fileString)

        monsterCardTypeList = []
        linkArrowList = []
        for key in cardDict.keys():
            # the idea of converting from binary representation to list of values is,
            # assume: ["left", "right", "front", "back"] corresponds to [1, 2, 4, 8]
            # for int value, each value is equal to: 2**index
            # then ["left", "front"] can be represented by: 1 + 4 = 5 = 0b0101
            # we try deduct from the largest value first, since if the largest value help make up for the int value,
            # it will be able to deduct, otherwise no
            # e.g. 5 - 8 -> -3
            # a negative value means the the enum doesn't help building the int value
            # however, 5 - 4 -> 1
            # when the value is deductable, we know the enum add up to this int
            # we always start from the largest first, since starting from the smallest create ambiguaty,
            # e.g.  5 - 1 = 4
            #       4 - 2 = 2
            # we will mistaken the value is made from "left" & "right" instead of the real "left" & "front"
            # convert the monster card type int to list of string
            if (key == "monster_card_type"):
                monsterCardTypeInt = cardDict[key]
                for value in range(len(MONSTER_CARD_TYPES), 0, -1):
                    if (monsterCardTypeInt - (2 ** (value - 1)) >= 0):
                        monsterCardTypeList.append(MonsterCardTypes[MONSTER_CARD_TYPES[value - 1]].name)
                        monsterCardTypeInt -= (2 ** (value - 1))
                cardDict[key] = monsterCardTypeList
                continue
            
            # convert the link arrow int to list of string
            if (key == "link_arrow"):
                linkArrowInt = cardDict[key]
                for value in range(len(availableLinkIndex), 0, -1):
                    # for the link arrow, we cannot directly use:
                    # 2 ** (value - 1)
                    # like monster types
                    # since link arrow representation is: [1, 2, 3, 4, 6, 7, 8, 9]
                    # 5 is missing from the list, so we need to take the availableLinkIndex[value - 1]
                    # in binary representation, 0b111101111
                    # the position to represent 5 will always be empty (0)
                    if (linkArrowInt - (2 ** (availableLinkIndex[value - 1])) >= 0):
                        linkArrowList.append(LinkArrows[LINK_ARROW_DIRECTION[value - 1]].name)
                        linkArrowInt -= (2 ** (availableLinkIndex[value - 1]))
                cardDict[key] = linkArrowList
                continue

            # early break if both list is not empty
            if (monsterCardTypeList != [] and linkArrowList != []):
                break

        # write to file
        if (not os.path.exists(new_folder_path)):
            os.makedirs(new_folder_path)

        jsonSrting = json.dumps(cardDict, indent = 4)
        writeFile = open(os.path.join(new_folder_path, f"{cardDict['filename']}.json"), mode = "w", encoding = "utf-8")
        writeFile.write(jsonSrting)
        writeFile.close()
                
if __name__ == "__main__":
    retrieve_all_cards()
    retrieve_images()
    None
