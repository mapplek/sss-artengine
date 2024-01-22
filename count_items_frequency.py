import collections
import csv
import glob
import os
import pprint

ROOT_PARTS = "./SSSGenerativeArt/"
ROOT_OUTPUT = "./Output/"

LAYERS = sorted(os.listdir(path=ROOT_PARTS))
GENE_ART = os.listdir(path=ROOT_OUTPUT+"draft-main/images/")
# GENE_ART = os.listdir(path=ROOT_OUTPUT+"draft-sub/images/")

CHARACTER_NAME = [
    "Mikoto", "Ushiwaka", "Kagetora", "Hakuto", 
    "Ron", "Miroku", "Ema", "Mirai", 
    "Sasuke", "Asuka", "Yamato", "Takeru"
]

COMMON_COSPLAY_ITEM = [
    "None", "FairyRobe", "Cloak"
]


###
# Collect parts each layer in material
##
'''
parts_each_layer_material
  [0] -> Character + Body
  [1] -> Character + Cosplay
  [2] -> Accessory(Body)
  [3] -> Accessory(Head)
  [4] -> Accessory(Back)
  [5] -> Foreground
  [6] -> Background
'''
parts_each_layer_material = [[],[],[],[],[],[],[]]
for layer in LAYERS:
    if layer == LAYERS[0]:
        for file  in glob.glob(ROOT_PARTS + layer + '/*/*.png', recursive=True):
            parts_each_layer_material[6].append(os.path.basename(file).split('#')[0])
    if layer == LAYERS[1]:
        for file  in glob.glob(ROOT_PARTS + layer + '/*/*.png', recursive=True):
            parts_each_layer_material[4].append(os.path.basename(file).split('#')[0])
    if layer == LAYERS[2]:
        for file  in glob.glob(ROOT_PARTS + layer + '/*/*.png', recursive=True):
            parts_each_layer_material[0].append(
                file.split('/')[-2].split('#')[0] + os.path.basename(file).split('#')[0]
            )
    if layer == LAYERS[3]:
        for file  in glob.glob(ROOT_PARTS + layer + '/*/*.png', recursive=True):
            if os.path.basename(file).split('#')[0] in COMMON_COSPLAY_ITEM:
                for character in CHARACTER_NAME:
                    parts_each_layer_material[1].append(
                        character + os.path.basename(file).split('#')[0]
                    )
            else: 
                parts_each_layer_material[1].append(
                    file.split('/')[-2].split('#')[0]
                    + os.path.basename(file).split('#')[0]
                )
    if layer == LAYERS[4]:
        for file  in glob.glob(ROOT_PARTS + layer + '/*/*.png', recursive=True):
            parts_each_layer_material[3].append(os.path.basename(file).split('#')[0])
    if layer == LAYERS[5]:
        for file  in glob.glob(ROOT_PARTS + layer + '/*/*.png', recursive=True):
            parts_each_layer_material[2].append(os.path.basename(file).split('#')[0])
    if layer == LAYERS[6]:
        for file  in glob.glob(ROOT_PARTS + layer + '/*/*.png', recursive=True):
            parts_each_layer_material[5].append(os.path.basename(file).split('#')[0])

# pprint.pprint(parts_each_layer_material)


###
# Collect parts each layer in output arts
###
'''
parts_each_layer_output_arts
  [0] -> Character + Body
  [1] -> Character + Cosplay
  [2] -> Accessory(Body)
  [3] -> Accessory(Head)
  [4] -> Accessory(Back)
  [5] -> Foreground
  [6] -> Background
'''
parts_each_layer_output_arts = [[],[],[],[],[],[],[]]

for art in GENE_ART:
    parts = art.split('-')
    parts_each_layer_output_arts[0].append(parts[1] + parts[4])
    parts_each_layer_output_arts[1].append(parts[1] + parts[5])
    parts_each_layer_output_arts[2].append(parts[7])
    parts_each_layer_output_arts[3].append(parts[6])
    parts_each_layer_output_arts[4].append(parts[3])
    parts_each_layer_output_arts[5].append(parts[8].split('.')[0])
    parts_each_layer_output_arts[6].append(parts[2])

# pprint.pprint(parts_each_layer_output_arts)


###
# Count frequency parts each layer
###
table_frequency_items = []

for layer in LAYERS:
    if layer == LAYERS[0]:
        array_freq = collections.Counter(parts_each_layer_output_arts[6])

        for item in parts_each_layer_material[6]:
            table_frequency_items.append([layer, item, array_freq[item]])

    if layer == LAYERS[1]:
        array_freq = collections.Counter(parts_each_layer_output_arts[4])

        for item in parts_each_layer_material[4]:
            table_frequency_items.append([layer, item, array_freq[item]])

    if layer == LAYERS[2]:
        array_freq = collections.Counter(parts_each_layer_output_arts[0])

        for item in parts_each_layer_material[0]:
            table_frequency_items.append([layer, item, array_freq[item]])

    if layer == LAYERS[3]:
        array_freq = collections.Counter(parts_each_layer_output_arts[1])

        for item in parts_each_layer_material[1]:
            table_frequency_items.append([layer, item, array_freq[item]])

    if layer == LAYERS[4]:
        array_freq = collections.Counter(parts_each_layer_output_arts[3])

        for item in parts_each_layer_material[3]:
            table_frequency_items.append([layer, item, array_freq[item]])

    if layer == LAYERS[5]:
        array_freq = collections.Counter(parts_each_layer_output_arts[2])

        for item in parts_each_layer_material[2]:
            table_frequency_items.append([layer, item, array_freq[item]])

    if layer == LAYERS[6]:
        array_freq = collections.Counter(parts_each_layer_output_arts[5])

        for item in parts_each_layer_material[5]:
            table_frequency_items.append([layer, item, array_freq[item]])

pprint.pprint(table_frequency_items)

with open('count_items_frequency.csv', 'w') as file:
    writer = csv.writer(file, lineterminator='\n')
    writer.writerows(table_frequency_items)