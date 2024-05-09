from pathlib import Path
import argparse
import urllib.request
import glob
import json
import os
import re


def download(arguments):
    style_counter = {} # Created an empty dictionary key value pair work kare
    input_dir = arguments.input_dir
    output_dir = arguments.output_dir

    for file in os.listdir(input_dir): # For loop  to iterate through each file in the directory listdir=all files in dir
        with open(os.path.join(input_dir, file)) as json_file: # Opening JSON file -> json_file.close()
            spitted = Path(file).stem.split("_")  # Splitting filename into list based on "_"
            key = spitted[0] #bohemian_0_win ["bohemian", "0", "win"]

            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            if not hasattr(style_counter, key): # 
                list_of_files = glob.glob(output_dir + "/*") # C://Downloads/output_dir/filename1.jpg glob=files 

                if len(list_of_files) == 0: # a = [2,4,6,8] -> len(a) -> 4
                    count_from = 0
                else:
                    latest_file = max(list_of_files, key=os.path.getctime) # Returns  the most recently modified file
                    digits = re.findall('\d+', Path(latest_file).stem) # We used re to find all the expressions
                    if digits:
                        last_file_index = int(digits[0]) # digits is a string so we need to convert it to integer
                        count_from = last_file_index + 1
                    else:
                        count_from = 0

            style_counter[key] = count_from # a = [1, 2, 3, 4] -> 1  a[0]    style_counter = {"key": count_from}

            data = json.load(json_file)

            uniq_folder = os.path.join(output_dir, key)

            if not os.path.exists(uniq_folder):
                os.makedirs(uniq_folder)

            for item in data[count_from:]: # It will access all the data starting from count_from
                full_file_name = os.path.join(output_dir, key, key + str(style_counter[key]) + ".jpg") #  Creating a name of the new image file

                try:
                    urllib.request.urlretrieve(item['imageURL'], full_file_name)
                    style_counter[key] = style_counter[key] + 1 #  Adding one to the counter of that particular key
                except Exception as e:
                    print("ITEM DOESN'T HAVE imageURL")


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input-dir',
        type=str,
        required=True,
        help='input dir')
    parser.add_argument(
        '--output-dir',
        type=str,
        required=True,
        help='output dir')
    a, _ = parser.parse_known_args() # ["nishank", "neel"]
    return a


if __name__ == '__main__':
    args = get_args()
    download(args)

# example:
# python data.py --input-dir ./sources/pinterest --output-dir ./data/train
