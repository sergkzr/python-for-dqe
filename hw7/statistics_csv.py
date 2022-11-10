# calculate sttatistics for feed_data db file:
# number of words and letters from previous Homeworks 5/6 output test file.
# Two csv:
# 1. word-count (all words are preprocessed in lowercase)
# 2. letter, cout_all, count_uppercase, percentage (add header, spacecharacters are not included)
# CSVs should be recreated each time new record added.
# 

import string as st

WS = st.whitespace
LTall = st.ascii_letters
LTlower = st.ascii_lowercase
LTupper = st.ascii_uppercase


def get_text_from_feed_data(file_path):

    with open(file_path, 'r') as file:
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
        if (len(word) > 0) and word[-1] in '.,;?!':
            word = word[:-1]
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return counts


def letters_count(string):

    letters_ = { smb:0 for smb in LTlower}
    letters = { smb:0 for smb in LTupper}
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
                letters[smb] += 1
        else:
            if smb in others:
                others[smb] += 1
            else:
                others[smb] = 1

    return letters_, letters, others


FILE_PATH = './data/feed_data'



if __name__ == '__main__':
    
    txt = get_text_from_feed_data(FILE_PATH)
    
    word_count = word_count(txt.lower())
    print(word_count)

    d1, d2, d3 = letters_count(txt)
    print(d1)
    print(d2)
    print(d3)