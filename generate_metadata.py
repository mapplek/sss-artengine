from natsort import natsorted

import json
import numpy as np
import os

MAX_SUPPLY = 24000

JSON_PATH = "./Output/prod/json/"
IMAGES_PATH = "./Output/draft-main/images/"

# AWS_IMAGE_URL = "https://sattva-soul-supporters.mapplek.xyz/gene/images/animal/"
AWS_IMAGE_URL = "https://gene.sattva-soul-supporters.com/images/animal/"

DESC_FOR_EACH_CHARACTER = [
    [
        "Mikoto who is one of the SattvaSoulSupporters guardian of Sattva, the Mouse",
        "Ushiwaka who is one of the SattvaSoulSupporters guardian of Sattva, the Ox",
        "Kagetora who is one of the SattvaSoulSupporters guardian of Sattva, the Tiger",
        "Hakuto who is one of the SattvaSoulSupporters guardian of Sattva, the Rabbit",
        "Ron who is one of the SattvaSoulSupporters guardian of Sattva, the Dragon",
        "Miroku who is one of the SattvaSoulSupporters guardian of Sattva, the Snake",
        "Ema who is one of the SattvaSoulSupporters guardian of Sattva, the Horse",
        "Mirai who is one of the SattvaSoulSupporters guardian of Sattva, the Sheep",
        "Sasuke who is one of the SattvaSoulSupporters guardian of Sattva, the Monkey",
        "Asuka who is one of the SattvaSoulSupporters guardian of Sattva, the Rooster",
        "Yamato who is one of the SattvaSoulSupporters guardian of Sattva, the Dog",
        "Takeru who is one of the SattvaSoulSupporters guardian of Sattva, the Boar"
    ],
    [
        "「子：ねずみ」のミコト",
        "「丑：うし」のウシワカ",
        "「寅：とら」のカゲトラ",
        "「卯：うさぎ」のハクト",
        "「辰：りゅう」のロン",
        "「巳：へび」のミロク",
        "「午：うま」のエマ",
        "「未：ひつじ」のミライ",
        "「申：さる」のサスケ",
        "「酉：とり」のアスカ",
        "「戌：いぬ」のヤマト",
        "「亥：いのしし」のタケル"
    ]
]

images = os.listdir(IMAGES_PATH)
images = natsorted(images)

for num_nft in range(MAX_SUPPLY):
    ###
    # Prepare for character name
    ###
    cosplay_name = ''
    layer_items = images[num_nft].split('-')

    if layer_items[4] != 'None':
        cosplay_name = '-' + layer_items[4]
    

    ###
    # Prepare description
    ###
    description = "He is " + DESC_FOR_EACH_CHARACTER[0][num_nft % 12] + " of the twelve signs of the Japanese Zodiac.  \n" + \
        "After undergoing rigorous training, he descended to earth to bestow Sattva's blessings on people!  \n  \n" + \
        "サットヴァ様を護衛するSattvaSoulSupporters一柱・十二支" + DESC_FOR_EACH_CHARACTER[1][num_nft % 12] + "。  \n" + \
        "厳しい修行を経てサットヴァ様の御加護を人々に与えるため、地上に降り立たちました！"


    ###
    # Dicision parameters by normal distribution
    ###
    norm_dist = np.clip(np.round(np.random.randn(6) * 2 + 5.5), 1, 10)


    ###
    # Generate metadata
    ###
    metadata = {
        "name": layer_items[1] + cosplay_name + " #" + str(num_nft + 1).zfill(5),
        "description": description,
        "image": AWS_IMAGE_URL + str(num_nft + 1) + ".png",
        "edition": (num_nft + 1),
        "attributes": [
            {
                "trait_type": "Character",
                "value": layer_items[1]
            },
            {
                "trait_type": "Body",
                "value": layer_items[4]
            },
            {
                "trait_type": "Cosplay",
                "value": layer_items[5]
            },
            {
                "trait_type": "Accessory(Body)",
                "value": layer_items[7]
            },
            {
                "trait_type": "Accessory(Head)",
                "value": layer_items[6]
            },
            {
                "trait_type": "Accessory(Back)",
                "value": layer_items[3]
            },
            {
                "trait_type": "Foreground",
                "value": layer_items[8].split('.')[0]
            },
            {
                "trait_type": "Background",
                "value": layer_items[2]
            },
            {
                "trait_type": "PsychicPower",
                "value": int(norm_dist[0])
            },
            {
                "trait_type": "Spirituality",
                "value": int(norm_dist[1])
            },
            {
                "trait_type": "Cleverness",
                "value": int(norm_dist[2])
            },
            {
                "trait_type": "Belief",
                "value": int(norm_dist[3])
            },
            {
                "trait_type": "Fortune",
                "value": int(norm_dist[4])
            },
            {
                "trait_type": "Perseverance",
                "value": int(norm_dist[5])
            }
        ]
    }


    ###
    # Write metadata as json file
    ###
    with open(JSON_PATH + str(num_nft + 1) + '.json', 'w') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)