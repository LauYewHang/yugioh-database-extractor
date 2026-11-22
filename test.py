from extractor import *

url_list = [
    "/yugiohdb/card_search.action?ope=2&cid=13570&iid=1",
    "/yugiohdb/card_search.action?ope=2&cid=21349&iid=1",
    "/yugiohdb/card_search.action?ope=2&cid=20607&iid=1",
    "/yugiohdb/card_search.action?ope=2&cid=16471&iid=1",
    "/yugiohdb/card_search.action?ope=2&cid=20586&iid=1",
    "/yugiohdb/card_search.action?ope=2&cid=19172&iid=1",
    "/yugiohdb/card_search.action?ope=2&cid=4861&iid=1",
    "/yugiohdb/card_search.action?ope=2&cid=22692&iid=1"
]

for i in range(len(url_list)):
    r = request_browse_specific_card(url_list[i])
    f = open(f"t_{i}.txt", mode="w", encoding="utf-8")
    f.write(r.text)
    f.close()
    write_card_information(parse_card_information(extract_specific_card_information(url_list[i])))
