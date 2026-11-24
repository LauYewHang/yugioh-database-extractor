# Yu-Gi-Oh database extractor
A simple Python program that helps to extract card information (TCG, English) from the [official Yu-Gi-Oh! database](https://www.db.yugioh-card.com/yugiohdb/card_search.action?wname=CardSearch). The program retrieves the card information and save each card in an individual JSON files.  
Additionally, the program can help download the card images from [YGOPRODeck website](https://ygoprodeck.com/) with its API. Some images may be missing due to the image not available from the website, or different display name between official database and said website. (available images: 14009/14068 as of 24/11/2026)  

## Downloading zip
You can download the extracted cards' JSON files with the zip:
- [Default version](cards/individual_card.zip)
- [With integer representation](cards/individual_card_bin.zip)  

The zip file will extract into a folder containing a list of JSON files that represent each individual cards. E.g. "Sky_Striker_Ace___Azalea_Temperance.json", "Arahime_the_Manifested_Mikanko.json", ...  
Visit the [section below](#different-versions) to see what is the difference between the two versions.

## Card images
The card images are available in the following directory:
- [Full version](card_image/full/)  
- [Cropped version](card_image/cropped/)  

Unfortunately currently directly downloading a zip file for images is not possible due to the file size. (even after splitting 15 fold)

## Different versions
There exists two version of the output:  
- `individual_card/`
- `indiviual_card_bin/`  
The difference between the two versions is how they store some card information for better optimization. (mostly useful if you would like to do use the data in your own program)  
### `individual_card`
**individual_card** is the default version where it stores cards' information in a way that it is easily comprehensible by reading directly.  
E.g.  

<details open>
<summary> <strong> Maliss &lt;Q&gt; White Binder </strong> </summary>  

```json
{
    "name": "Maliss <Q> White Binder",
    "filename": "Maliss__Q__White_Binder",
    "card_text": "2+ monsters, including a \"Maliss\" monster\nIf this card is Special Summoned: You can target up to 3 cards in any GY(s); banish them. During your Main Phase: You can Set 1 \"Maliss\" Trap from your Deck or GY. If this card is banished: You can pay 900 LP; Special Summon it, then you can draw 1 card. You can only use each effect of \"Maliss <Q> White Binder\" once per turn.",
    "release_date": "2024-12-06",
    "available_set": [
        "2025 MEGA-PACK TIN",
        "CROSSOVER BREAKERS"
    ],
    "related_card": [
        "Maliss <C> GWC-06",
        "Maliss <C> MTP-07",
        "Maliss <C> TB-11",
        "Maliss <P> Chessy Cat",
        "Maliss <P> Dormouse",
        "Maliss <P> March Hare",
        "Maliss <P> White Rabbit",
        "Maliss <Q> Hearts Crypter",
        "Maliss <Q> Red Ransom",
        "Maliss in the Mirror",
        "Maliss in Underground"
    ],
    "attribute": "DARK",
    "attack": 2300,
    "defense": null,
    "monster_type": "Cyberse",
    "monster_card_type": [
        "Link",
        "Effect"
    ],
    "link_rating": 3,
    "link_arrow": [
        "Top-Center",
        "Middle-Right",
        "Middle-Left"
    ]
}
```
</details>

### `individual_card_bin`
**individual_card_bin** version stores card information such as `link arrow direction` and `monster card type` with integer representation in a way that they can be easily compared / check equality during the programming process. For more details explanation, kindly visit the [documentation](docs/) for extra info.  
E.g.  

<details open>
<summary> <strong> Zenna's Deceiving Doll Maidens </strong> </summary>

```json
{
    "name": "Zenna's Deceiving Doll Maidens",
    "filename": "Zenna_s_Deceiving_Doll_Maidens",
    "card_text": "2+ Effect Monsters\nYou can also use 1 monster in your hand as material to Link Summon this card. You can only use each of the following effects of \"Zenna's Deceiving Doll Maidens\" once per turn. If this card is Link Summoned: You can send 1 monster from your Deck to the GY, or if all materials used for its Link Summon were monsters you controlled, you can send 1 monster from your Extra Deck instead. During your next Standby Phase after this card was sent from the field to the GY: You can add 1 monster from your GY to your hand.",
    "release_date": "2026-07-03",
    "available_set": [
        "CHAOS ORIGINS"
    ],
    "related_card": [],
    "attribute": "DARK",
    "attack": 0,
    "defense": null,
    "monster_type": "Machine",
    "monster_card_type": 8194,
    "link_rating": 5,
    "link_arrow": 94
}
```

And the `monster_card_type` has value `8194` instead of a list of string: `["Link", "Effect"]`.  
Notice how the `link_arrow` has value `94` instead of a list of string: `["Middle-Right", "Middle-Left", "Bottom-Right", "Bottom-Center", "Bottom-Left"]`.  

</details>

<details>  
<summary> <strong> Patissciel Couverture </strong> </summary>

```json
{
    "name": "Patissciel Couverture",
    "filename": "Patissciel_Couverture",
    "card_text": "2 Pendulum Monsters\nIf this card in the Monster Zone is destroyed: You can place this card in your Pendulum Zone.",
    "release_date": "2022-05-20",
    "available_set": [
        "25TH ANNIVERSARY TIN: DUELING HEROES MEGA PACK",
        "DIMENSION FORCE"
    ],
    "related_card": [
        "Concours de Cuisine (Culinary Confrontation)"
    ],
    "attribute": "DARK",
    "attack": 1700,
    "defense": 700,
    "monster_type": "Fairy",
    "monster_card_type": 4106,
    "level_rank_type": "Level",
    "level_rank_rating": 5,
    "pendulum_effect": "If you have no card in your other Pendulum Zone: You can place 1 face-up Pendulum Monster from your Extra Deck in your Pendulum Zone. You can only use this effect of \"Patissciel Couverture\" once per turn.",
    "pendulum_scale": 1
}
```

Notice how the `monster_card_type` has value `4106` instead of a list of string: `["Fusion", "Pendulum", "Effect"]`.

</details>

If you only wish to retrieve the card information and use the information directly, using [individual_card](cards/individual_card.zip)'s version should suit you the best.  

## Manually running the code
You can manually download the repository and run the Python code yourself by:  
`pip install -r requirements.txt`   - install all the necessary library  
`python3 extractor.py`              - run the [extractor.py](extractor.py) main program  
The program should manually extract the information from the [official Yu-Gi-Oh! database](https://www.db.yugioh-card.com/yugiohdb/card_search.action?wname=CardSearch) and write the results into the a folder `individual_card`.  

## Author's note
Any poor performance and unoptimization of this program is all due to I am too stupid, or too tired to change the stuff when I only realized I should not be doing that after I wrote 500 lines of code. Also I wrote this thingy in the heat of passion, when I should be doing my school assignments.  
For any suggestions, questions, or anything else, feel free to contact me on:  
- [Discord](https://discord.com/users/1225424004630974496): sunshinetsu0411 (let me know you come from GitHub)
- [Email](yewhang2004@gmail.com): yewhang2004@gmail.com  
Thanks for stopping by to visit this hot mess <3
