''' This code converts the annotation outputs of Encord tool to 
yolo format. Encord annotation tool puts all annptations (i.e. for multiple images)
into a singl Json file. yolo need annotations in a text format. also each image 
should have a corresponding text file with the same name.
encord produces the BB info as x_start, y_start, h, w
yolo format needs the BB info as, x_center, y_center, h, w
instructions: export annotations by Encord as a Json file, decompress 
the file and provided to this code.
'''

import json

DICTIONARY = {
    "acceptable_orange_tape": 101,
    "unacceptable_orange_tape": 102,
    "acceptable_blake_tape": 103,
    "unacceptable_black_tape": 104,
    "acceptable_cloth_tape": 105,
    "unacceptable_cloth_tape": 106,
}

def split_annotations(input_json: str):
    '''
    This function gets the name/path of the output json file
    from encord and produces the txt files for each image.
    '''
    with open(input_json, "r", encoding="utf-8") as f:
        data = json.load(f)
    for item in data[0]["data_units"]:
        name = data[0]["data_units"][item]["data_title"].split(".")[0]
        output_filename = "lbls/" + f"{name}.txt".format(name)
        with open(output_filename, "w", encoding="utf-8") as outfile:
            for j in data[0]["data_units"][item]["labels"]["objects"]:
                label = DICTIONARY[j["name"]]
                h, w, x, y = (
                    j["boundingBox"]["h"],
                    j["boundingBox"]["w"],
                    j["boundingBox"]["x"],
                    j["boundingBox"]["y"],
                )
                x = x + w / 2
                y = y + h / 2
                new_line = (
                    str(label)
                    + " "
                    + str(x)
                    + " "
                    + str(y)
                    + " "
                    + str(w)
                    + " "
                    + str(h)
                )
                outfile.writelines(new_line + "\n")

INPUT_JSON_FILE = "ZS9H0198-R0A.json"
split_annotations(INPUT_JSON_FILE)
