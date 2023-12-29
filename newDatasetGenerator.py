''' 
This python code is designed to pick special classses from the main dataset 
and create a new dataset (folder) with chosen class numbers. also for the new
dataset the class numbers are respectively changed (starting from zero to the 
max number of classes in the new dataset.

instructions:
all you need to do is to change the source dataset path, total class numbers, 
the destination dataset path and also the mapping dictionary, based on your project targets.
'''

import shutil
import os
from glob import glob

IMGS_ROOTS = {}
CLS_NUMS = {}
IMG_LIST = []



TOTAL_CLASS_NUMBER = 110  #  TO CHANGE -- Maximum class number in the dataset.
TEXT_LIST = glob(
    "/data/for_hafizurr/konnectai/megaone/shyft_main/*.txt"
)  # TO CHANGE -- The path of the directory containing the labels (text files) and IMAGEs.


for i in range(0, TOTAL_CLASS_NUMBER):
    CLS_NUMS[str(i)] = 0
    IMGS_ROOTS[str(i)] = []

# extracting the roots of the IMAGEs which have their corresponding text file in the same root.
for i in TEXT_LIST:
    IMG_JPG = i.split(".")[0] + ".jpg"
    IMG_PNG = i.split(".")[0] + ".png"
    IMAGE_EXISTS = False
    if os.path.exists(IMG_JPG):
        IMAGE = IMG_JPG
        IMAGE_EXISTS = True
    elif os.path.exists(IMG_PNG):
        IMAGE = IMG_PNG
        IMAGE_EXISTS = True
    if IMAGE_EXISTS:
        IMG_LIST.append(IMAGE)
        with open(i, "r", encoding='utf-8') as file:
            FILEDATA = file.readlines()
            for line in FILEDATA:
                CLS = line.split()[0]
                if CLS in CLS_NUMS:
                    CLS_NUMS[CLS] += 1
                    IMGS_ROOTS[CLS].append(IMAGE)

#  TO CHANGE -- the destination path to save the new labels.
DESTINATION_ROOT = "/data/for_hafizurr/konnectai/megaone/shyft_augmented/"

#  TO CHANGE -- converting class#Xto class#Y
MAPPING_DICT = {
    14: 0,
    15: 1,
    74: 2,
    75: 3,
    78: 4,
    79: 5,
    80: 6,
    81: 7,
    82: 8,
    83: 9,
    98: 10,
    99: 11,
    48: 2,
    101: 12,
    102: 13,
    103: 14,
    104: 15,
    105: 16,
    106: 17,
}

DESIED_CLASS = list(MAPPING_DICT.keys())
DESIRRED_IMGS = []

for i in DESIED_CLASS:
    for j in IMGS_ROOTS[str(i)]:
        DESIRRED_IMGS.append(j)

# changing the labels to have new class numbers and saving them in the new path (destination path).
for img in IMG_LIST:
    TXT = img.split(".")[0] + ".txt"
    IMG_NAME = img.split("/")[-1]
    TXT_NAME = TXT.split("/")[-1]
    NEW_TXT = DESTINATION_ROOT + TXT_NAME
    NEW_IMG = DESTINATION_ROOT + IMG_NAME
    if not os.path.exists(TXT):
        continue
    if img in DESIRRED_IMGS:
        if os.path.exists(NEW_IMG):
            continue
        shutil.copy(img, NEW_IMG)
        with open(NEW_TXT, "w", encoding='utf-8') as output:
            with open(TXT, "r", encoding='utf-8') as file:
                FILEDATA = file.readlines()
                for line in FILEDATA:
                    CLS = line.split()[0]
                    try:
                        NEW_CLS = MAPPING_DICT[int(CLS)]
                    except ValueError:
                        continue
                    NEW_LINE = [str(NEW_CLS)] + line.split()[1:]
                    print(line)
                    k = ""
                    for l in NEW_LINE:
                        k = k + l + " "
                    NEW_LINE = k[:-1]
                    output.writelines(NEW_LINE + "\n")
