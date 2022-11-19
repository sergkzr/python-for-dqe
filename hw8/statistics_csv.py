# calculate statistics for feed_data db file:
# number of words and letters from previous Homeworks 5/6 output test file.
# Two csv:
# 1. word-count (all words are preprocessed in lowercase)
# 2. letter, cout_all, count_uppercase, percentage (add header, spacecharacters are not included)
# CSVs should be recreated each time new record added.
# 

import string as st
import csv

WS = st.whitespace
# LTall = st.ascii_letters
LTlower_lat = 'abcdefghijklmnopqrstuvwxyz'
LTupper_lat = LTlower_lat.upper()
LTlower_cyr = 'абвгґдеєжзиіїыклмнопрстуфхцчшщьъэюя'
LTupper_cyr = LTlower_cyr.upper()
LTall = ''.join([LTlower_lat, LTupper_lat, LTlower_cyr, LTupper_cyr])
LTlower = ''.join([LTlower_lat, LTlower_cyr])
LTupper = ''.join([LTupper_lat, LTupper_cyr])


def get_text_from_feed_data(file_path):

    with open(file_path, 'r', encoding='UTF-8') as file:
        lines = file.readlines()

    # filter lines where we will seek for words
    text = '' 
    line_ = ''
    accumulate = False

    for line in lines:

        line_ = line.lower()

        if line_ == '<----------\n':
            continue

        if line_ == '---------->\n':
            accumulate = False
            continue

        if line_.startswith('news,') or line_.startswith('private ad,') or line_.startswith('book,'):
            continue
        
        if line.find(':') > 0:

            h_, t = line.split(':', 1)
            h = h_.strip().lower()
            
            if h in ('text', 'city', 'title'):
                text += t
                accumulate = True
            else:
                continue
        elif accumulate:
            text += line

    return text  


def word_count(string):
    counts = dict()
    words = string.split()

    for word in words:
        if (len(word) > 0) and word[-1] in '.,;?!-+=^*':
            word = word[:-1]
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return counts


def letters_count(string):

    letters_ = { smb:0 for smb in LTlower}
    letters = { smb:0 for smb in LTlower}
    others = dict()

    percentage = dict()

    smb_count = 0
    smb_notWS_count = 0

    for smb in string:

        smb_count += 1
        if smb in WS:
            continue
        smb_notWS_count += 1

        if smb in LTall:
            letters_[smb.lower()] += 1        
            if smb in LTupper:
                letters[smb.lower()] += 1
        else:
            if smb in others:
                others[smb] += 1
            else:
                others[smb] = 1

    return letters_, letters, others


def write_stat_wordcount(word_count_dict, file_to_write, silent=True):

    with open(file_to_write, 'w', encoding='UTF-8', newline='') as ftw:

        writer = csv.writer(ftw, delimiter='-')

        for word, count in word_count_dict.items():
            if not silent:
                print('csv-writer:', word, count)
            writer.writerow([word, count])


def write_stat_lettercount(lett_dict, lett_upper_dict, file_to_write, silent=True):

    total_letters_count = 0
    for _, v in lett_dict.items():
        total_letters_count += v

    with open(file_to_write, 'w', encoding='UTF-8', newline='') as ftw:

        header = ('letter', 'letter_count', 'letter_upper_count', 'letter_percent')
        writer = csv.DictWriter(ftw, fieldnames=header)

        writer.writeheader()
    
        for symb in LTlower:
        
            # write row from dict
            
            if not silent:
                print('dict-writer:', symb, lett_dict[symb], lett_upper_dict[symb], lett_dict[symb]/total_letters_count*100)

            writer.writerow({'letter': symb, 
                            'letter_count': lett_dict[symb], 
                            'letter_upper_count': lett_upper_dict[symb], 
                            'letter_percent': f'{lett_dict[symb]/total_letters_count*100:.3}'})



if __name__ == '__main__':

    FILE_PATH = './data/feed_data'
    FILE_STAT_LETTERS_PATH = './data/lettercount'
    FILE_STAT_WORDS_PATH = './data/wordcount'

    txt = get_text_from_feed_data(FILE_PATH)
    
    word_count = word_count(txt.lower())
    print(word_count)

    d1, d2, d3 = letters_count(txt)

    print(d1)
    print(d2)
    print(d3)

    write_stat_wordcount(word_count, FILE_STAT_WORDS_PATH)
    
    write_stat_lettercount(d1, d2, FILE_STAT_LETTERS_PATH)