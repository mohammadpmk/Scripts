""" This script reads all the availble images/labels
and automatically creat train.txt, test.txt and val.txt
files for YOLO
"""
from glob import glob
import os
import numpy as np


SOURCE_ROOT = "/data/for_hafizurr/konnectai/megaone/shyft/"
IMGS_ROOTS = {}
CLS_NUMS = {}
DICT_VAL = {}
DICT_TEST = {}
DICT_TRAIN = {}
IMG_LIST = []
VAL = []
TEST = []
TRAIN = []
MAX_CLASS_ID = 120
TEXT_LIST = glob(SOURCE_ROOT + "*.txt")

for x in range(0, MAX_CLASS_ID):
    CLS_NUMS[str(x)] = 0
    IMGS_ROOTS[str(x)] = []

for i in TEXT_LIST:  # Old data root: old_data and for new: data
    if i == SOURCE_ROOT + "classes.txt":
        continue
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
        with open(i, "r", encoding="utf-8") as file:
            FILEDATA = file.readlines()
            for line in FILEDATA:
                CLS = line.split()[0]
                if CLS in CLS_NUMS:
                    CLS_NUMS[CLS] += 1
                    IMGS_ROOTS[CLS].append(IMAGE)


for i in range(0, MAX_CLASS_ID):
    NUM = CLS_NUMS[str(i)]
    TEST_NUM = NUM // 8
    VAL_NUM = NUM // 8
    SET = IMGS_ROOTS[str(i)]
    np.random.shuffle(SET)

    DICT_VAL[str(i)] = SET[:VAL_NUM]
    VAL.extend(SET[:VAL_NUM])

    DICT_TEST[str(i)] = SET[VAL_NUM : TEST_NUM + VAL_NUM]
    TEST.extend(SET[VAL_NUM : TEST_NUM + VAL_NUM])

    DICT_TRAIN[str(i)] = SET[TEST_NUM + VAL_NUM :]
    TRAIN.extend(SET[TEST_NUM + VAL_NUM :])


with open(SOURCE_ROOT + "val.txt", "w", encoding='utf-8') as output:
    for j in VAL:
        output.writelines(str(j) + "\n")

with open(SOURCE_ROOT + "test.txt", "w", encoding='utf-8') as output:
    for j in TEST:
        output.writelines(str(j) + "\n")

with open(SOURCE_ROOT + "train.txt", "w", encoding='utf-8') as output:
    for j in TRAIN:
        output.writelines(str(j) + "\n")

print(
    "---------------------------------------------\n---------------------------------------------\n"
)
print(CLS_NUMS)
print(
    "---------------------------------------------\n---------------------------------------------\n"
)

print("Number of the samples for TRAIN dataset:", len(TRAIN))
print("Number of the samples for VAL dataset:", len(VAL))
print("Number of the samples for TEST dataset:", len(TEST))

print("done!")
