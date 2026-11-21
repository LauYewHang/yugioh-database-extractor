import json, requests, re, html, datetime, math
from typing import List, TypedDict

from reference.card_reference import *
from reference.request_reference import *
from reference.Card import *

# the root url for the database
YUGIOH_DATABASE_URL = "https://www.db.yugioh-card.com"
# the url for search action on the database
YUGIOH_DATABASE_SEARCH_URL = "https://www.db.yugioh-card.com/yugiohdb/card_search.action"

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
        monsterTypeList = []
        # regular expression for monster type format
        # search for any character that is not alphabet or '-'
        reMonsterTypeFormat = re.compile(r"[^a-zA-Z-]")
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
    for text in cardInformationTextList:
        if "class=\"text_linebreak\"" in text:
            # remove the '\t' from the text
            cardText = reFormat.sub('', re.escape(text))
            # remove the prefix and suffix <div> to get the pure card text
            cardText = cardText.removeprefix("<div class=\"text_linebreak\">").removesuffix("</div>")
            break

    releaseDate: datetime.date = None
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
        if (traversedSet + 1 == availableSetAmount):
            if "<div class=\"time\">" in cardReleaseInformationTextList[index]:
                for index2 in range(index + 1, len(cardReleaseInformationTextList)):
                    if "</div>" not in cardReleaseInformationTextList[index2]:
                        releaseDateString += cardReleaseInformationTextList[index2]
                    else:
                        # remove the escape character '\t'
                        releaseDateString = reFormat.sub('', re.escape(releaseDateString))
                        break

        # early break if traversedSet is equal to availableSetAmount
        if (traversedSet == availableSetAmount):
            # convert list to set to remove duplicate, then convert it back to list again for format
            # reference: https://stackoverflow.com/a/9841328/21952784
            # I was actually so drunk I searched "removed duplicate from string" instead of "remove duplicate from list" but it still work www
            availableSet = list(set(availableSet))
            # convert date string to list and convert it to datetime.date type
            releaseDateValueList = releaseDateString.split('-')
            releaseDate = datetime.date(int(releaseDateValueList[0]), int(releaseDateValueList[1]), int(releaseDateValueList[2]))
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
                            relatedCardTextList[-1] += relatedCardTextList[textIndex2]
                        else:
                            # remove escape character
                            relatedCardTextList[-1] = reFormat.sub('', re.escape(relatedCardTextList[-1]))
                            break

                # early break if it reaches the current_end (current maximum related card that can be retrieved)
                if (len(relatedCardTextList) == relatedCardSearchResults["current_end"]):
                    break

            # after finishing the current page, retrieve the next page (if available)
            # if (currentRelatedCardPage < maxRelatedCardPage):
            #     print(response.request.url)
            #     currentRelatedCardPage += 1
                #nextResponseText = request_browse_specific_card()
        print(relatedCardList)

# search the card and write to a file
def retrieve_card_information(filepath: str = "cards.json"):
    file = open(filepath, mode = "w", encoding = "utf-8")
    pass

if __name__ == "__main__":
    None
