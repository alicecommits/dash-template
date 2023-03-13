# importing libraries ----------------------------------------------------
import ast # to evaluate dict-like str --> dict
import pandas as pd
pd.options.display.max_columns # display all df columns when printing

DEBUG_file_parsing = False # for debug prints

'''
This file demos 2 different ways of parsing a file for further analysis with python,
depending on the way the data of interest was generated and stored.
- typical example of data being written to a .csv file
- less typical example of parsing a .db file - in this example, we divert from the
primary use of the .db file, as we treat it like a line-by-line .txt file.
This can be useful when the server-client structure of an web-based analytical app
is not yet set, but the data is ready to be previewed / parsed.
Note: for each example, a random db/data generator script has been used to create
dummy data. The scripts are available in the nested folders of the input_data folder.
'''


# -------------------------- .csv  --> formatted dataframe -------------------------- #
# if your data of interest is in a .csv file, straight-forward parsing with
# pandas method pd.read_csv()

#TODO code


# ----------------------------------------------------------------------------------- #
# -------------------------- neDB .db  --> formatted dataframe ---------------------- #

# Python program to read line by line from .db file
filepath = './input_data/js-nedb-example/myRandomData.db'

L = []
if DEBUG_file_parsing:
    count = 0
with open(filepath) as file:
    for item in file:
        result = ast.literal_eval(item) # to turn into dict
        L.append(result)
        if DEBUG_file_parsing:
            print(f'item number {count}: {item}')
            count += 1
if DEBUG_file_parsing:
    print(L)

df = pd.DataFrame(data = L)
if DEBUG_file_parsing:
    print('df right after parsing list from .db file: ', df)