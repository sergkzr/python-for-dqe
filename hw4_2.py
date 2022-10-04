# 1. create a list of random number of dicts (from 2 to 10)
#
# dict's random numbers of keys should be letter,
# dict's values should be a number (0-100),
# example: [{'a': 5, 'b': 7, 'g': 11}, {'a': 3, 'c': 35, 'g': 42}]
#
# 2. get previously generated list of dicts and create one common dict:
#
# if dicts have same key, we will take max value, and rename key with dict number with max value
# if key is only in one dict - take it as is,
# example: {'a_1': 5, 'b': 7, 'c': 35, 'g_2': 42}
#
# Each line of code should be commented with description.
#
# Commit script to git repository and provide link as home task result.

import random as rnd
import pprint as pp

rnd.seed(44)                            # to get the same results for each run
letters = "abcdefghijklmnopqrstuvwxyz"  # letters to choose from randomly


# 1. create a list of random number of dicts (from 2 to 10)

n_dict = rnd.randint(2, 10)   # number of dict to be generated
dict_list = []                # initial list of dictionaries


# generate list of n_dict dictionaries
# each new dictionary will be appended to dict_list

def generate_dicts(dict_list, n_dict, max_length_dict):

    for i in range(1, n_dict + 1):

        l_dict = rnd.randint(1, 10)   # random length of dict to be generated
        d = {}                        # starting from empty dictionary

        # generate l_dict elements of the dictionary
        
        for j in range(l_dict):     
            
            letter = rnd.choice(letters)   # in case new randomly generated letter is the letter which is in the dictionary
            while letter in d:
                letter = rnd.choice(letters)

            d[letter] = rnd.randint(0, 100) # add new element to dictionary

        # print(f'#: {i}, {d}')
        dict_list.append(d)   # add generated dictionary to dict_list


generate_dicts(dict_list, n_dict, 10)

print('Source dictionaries:')
pp.pprint(dict_list)


# 2. get previously generated list of dicts and create one common dict
# intermediate dictionary structure: { key: (max_value_for_key, index_of_dictionary_with_max_value, OneValueOnly) }

union_dict = {}

def prepare_intermediate_dict(source_dict_list, interm_dict):

    for i, d in enumerate(dict_list):   # process previously generated dictionaries 

        for k, v in d.items():  # iterate through dictionary
        
            if k not in interm_dict:
                # new key, add it to dict as is, set flag 'OneValueOnly' to True
                interm_dict[k] = (v, i+1, True)
            elif interm_dict[k][0] < v:
                # new value is bigger than current value: change key and value and set flag 'OneValueOnly' to False
                interm_dict[k] = (v, i+1, False)
            else:
                # new value is less than current value: change flag 'OneValueOnly' to False
                uv, ui, _ = union_dict[k]
                interm_dict[k] = (uv, ui, False)


prepare_intermediate_dict(dict_list, union_dict)


# transformation of intermediate dictionary into result dictionary

def result_dict(union_dict):

    udict = {}
    for k, (v, i, OneValueOnly) in union_dict.items():  # unpack dict element into variables
        if OneValueOnly:
            udict[k] = v 
        else:
            # there are some values in different dictionaries, we use maximum and indicate index in the dictionary key
            udict[f'{k}_{i}'] = v
    
    return udict

ud = result_dict(union_dict)

# show result
print('Transformed dictionary as the result:')
pp.pprint(ud)
