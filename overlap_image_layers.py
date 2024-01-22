from PIL import Image
import glob
import sys
import os
import random

OFFSET = 264
GENERATE_NUM = 30000
MAX_SUPPLY = 24000
ALLOWED_REDO_BY_DUPLICATION = 10

CHARACTER_NAME = [
    "Mikoto", "Ushiwaka", "Kagetora", "Hakuto", 
    "Ron", "Miroku", "Ema", "Mirai", 
    "Sasuke", "Asuka", "Yamato", "Takeru"
]

FIXED_PAIR_ITEMS = [
    "HotSpringMorningDuck",
    "HotSpringMorningCitron",
    "HotSpringNightDuck",
    "HotSpringNightCitron",
    "HanafudaAutumnLeaves",
    "HanafudaAwnMoon",
    "HanafudaLespedeza",
    "HanafudaMumCup",
    "HanafudaPaulowniaPhoenix",
    "HanafudaPeony",
    "HanafudaPine",
    "HanafudaSakuraCurtain",
    "HanafudaWillow"
]

ROOT_PATH = "./SSSGenerativeArt/"
LAYERS = sorted(os.listdir(path="./SSSGenerativeArt/"))
generated_dna = []

OUTPUT_PATH_MAIN = "./Output/draft-main/images/"
OUTPUT_PATH_SUB = "./Output/draft-sub/images/"

EXTENTION = ".png"

for num_nft in range(GENERATE_NUM - OFFSET):
    iteration_count = 0
    tmp_character_name = CHARACTER_NAME[(num_nft + OFFSET) % 12]

    while True:
        selected_items = []

        for layer in LAYERS:
            ###
            # Check predetermined combination
            ###            
            if layer != LAYERS[0]:
                if selected_items[0][1] in FIXED_PAIR_ITEMS:
                    if (layer == LAYERS[1]) or (layer == LAYERS[5]):
                        selected_items.append(
                            [
                                glob.glob(ROOT_PATH + layer + '/General#100/None*')[0],
                                'None'
                            ]
                        )
                        continue
                    elif layer == LAYERS[3]:
                        selected_items.append(
                            [
                                glob.glob(ROOT_PATH + layer + '/General#30/None*')[0],
                                'None'
                            ]
                        )
                        continue
                    elif layer == LAYERS[6]:
                        selected_items.append(
                            [
                                glob.glob(ROOT_PATH + layer + '/General#100/' + selected_items[0][1] + '*')[0],
                                selected_items[0][1].split('#')[0]
                            ]
                        )
                        continue


            ###
            # Extract directory name General and Character
            ###
            dirname_general_and_character = []
            dirname_general_and_character.append(glob.glob(ROOT_PATH + layer + '/General*')[0].split('/')[-1])
            dirname_general_and_character.append(glob.glob(ROOT_PATH + layer + '/' + tmp_character_name + '*')[0].split('/')[-1])


            ###
            # Select General or each Character by weights
            ###
            weights_general_and_character = []
            weights_general_and_character.append(int(dirname_general_and_character[0].split('#')[-1]))
            weights_general_and_character.append(int(dirname_general_and_character[1].split('#')[-1]))

            idx_selected_general_or_character = 0

            if (layer == LAYERS[3]) and (selected_items[2][1].startswith('Zen')):
                idx_selected_general_or_character = 0
            else:
                total_weight = sum(weights_general_and_character)
                rand = random.randint(1, total_weight)

                for idx in range(len(weights_general_and_character)):
                    rand -= weights_general_and_character[idx]
                    if rand <= 0:
                        idx_selected_general_or_character = idx
                        break


            ###
            # Select item by weights
            ###
            idx_selected_item = 0
            items = []

            if layer == LAYERS[5]:
                if selected_items[2][1].startswith('Zen'):
                    items = [os.path.basename(file) for file in glob.glob(ROOT_PATH + layer + '/General#100/Holding*')]
                else:
                    for item in glob.glob(ROOT_PATH + layer + '/General#100/*'):
                        if 'Holding' in item:
                            continue
                        else:
                            items.append(os.path.basename(item))
            else:
                items = os.listdir(ROOT_PATH + layer + '/' + dirname_general_and_character[idx_selected_general_or_character] + '/')

            weights_items = [int(item.split('#')[-1].split('.')[0]) for item in items]
            total_weight = sum(weights_items)
            rand = random.randint(1, total_weight)

            for idx in range(len(weights_items)):
                rand -= weights_items[idx]
                if rand <= 0:
                    idx_selected_item = idx
                    break

            selected_items.append(
                [
                    ROOT_PATH + layer + '/' + dirname_general_and_character[idx_selected_general_or_character] + '/' + items[idx_selected_item],
                    items[idx_selected_item].split('#')[0]
                ]
            )
        
        
        ###
        # Generate DNA and check duplication
        ###
        element_dna = []
        element_dna.append(tmp_character_name)

        for selected_item in selected_items:
            element_dna.append(selected_item[1])
        
        if '-'.join(element_dna) in generated_dna:
            iteration_count += 1
            if iteration_count > ALLOWED_REDO_BY_DUPLICATION:
                print('---------------------------------------------------')
                print('Reached ALLOWED_REDO_BY_DUPLICATION.')
                print('Force the application to stop.')
                sys.exit()
            else:
                print('#' + str((num_nft + OFFSET) + 1) + ': dna already exists(iteration_count: ' + str(iteration_count) + '/' + str(ALLOWED_REDO_BY_DUPLICATION) + ')')
                continue
        else:
            generated_dna.append('-'.join(element_dna))

            ###
            # Generate an overlapping picture
            ###
            overlapped_picture = Image.new("RGBA", (2048, 2048), (255, 255, 255, 0))

            for selected_item in selected_items:
                tmp_layer = Image.open(selected_item[0])

                # print('debug:')
                # print(selected_item)
                overlapped_picture = Image.alpha_composite(overlapped_picture, tmp_layer)
            
            if (num_nft + OFFSET) < MAX_SUPPLY: 
                overlapped_picture.save(OUTPUT_PATH_MAIN + str((num_nft + OFFSET) + 1) + "-" + "-".join(element_dna) + EXTENTION, format='PNG')
            else:
                overlapped_picture.save(OUTPUT_PATH_SUB + str((num_nft + OFFSET) + 1) + "-" + "-".join(element_dna) + EXTENTION, format='PNG')

            print('#' + str((num_nft + OFFSET) + 1) + ': generated ' + '-'.join(element_dna))

        break
    