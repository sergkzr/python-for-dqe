# assumptions:
#   - whitespace is exactly what defined in string module
#   - sentence is string, which ends with '.' OR ':', thats why first row in source string is sentence

import pprint as pp
import string as st

ws = st.whitespace

# source string

s = """homEwork:

  tHis iz your homeWork, copy these Text to variable.

 

  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

 

  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.

 

  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
"""
# print('Source string:')
# print(s)
# print()


# 'normalize' string

def get_normalized_list(source_text, split_symbol):
    """
    Given source_text (which is string),
    Split it on the sentences (separate line of text, as list element), in wich:
    - all the symbols are in lower case, except the first symbol of the sentence
    - there are no leading whitespaces
    - each sentence starts from capital letter
    - each sentence ends with split symbol, e.g. '.', wich is the end symbol of the sentence
    - there are no empty lines
    """
  
    source = source_text.lower()
    
    normalized_text =  []
    sentences = source.split(split_symbol)

    for sent in sentences:
        if len(sent.strip()) != 0:
            ss = sent.strip()
            normalized_text.append(ss[0].upper() + ss[1:] + split_symbol)

    return normalized_text


# treat source text as sequence: [header to ':', text with sentences ater ':' to the end]

splitted_colon = s.split(':')
splitted_list = []


# process string before ':'

# get part before ':'
ss = splitted_colon[0].strip().lower()

# first letter of first word in the sentence --> to upper case
splitted_list.append(ss[0].upper() + ss[1:] + ':')


# process string after ':'

normalized = get_normalized_list(splitted_colon[1], '.')
splitted_list.extend(normalized)


print(splitted_list)
print("------")


#  make string from sentences in the list

norm_string = '\n'.join(splitted_list)
print(norm_string)


# calculate amount of white spaces,

def whitespaces_count(str):

    ws_count = 0

    for c in str:
        if c in ws:
            ws_count = ws_count + 1

    return ws_count


ws_count = whitespaces_count(norm_string)

print(f'whitespace_count: {ws_count}')
  

#
# prepare list of last words in each sentence
# add them to the source normalized string
#

def get_last_word_list(sent_list):
    """
    iterate through list of sentences
    get last word in the sentence
    make list of last words
    """
    last_word_list = []

    for sent in sent_list:
        words = sent.split()
        last_word_list.append(words[-1][:-1])

    return last_word_list


last_word_list = get_last_word_list(splitted_list)

print('Word list of last words in each sentence:')
print(last_word_list)
print()

# construct new sentence from the list of last words
# capitalize first word in the sentence

norm_plusnew = norm_string +  \
            '\n' +            \
            last_word_list[0][0].upper() +  \
            last_word_list[0][1:] +         \
            ' ' +                           \
            ' '.join(last_word_list[1:]) +  \
            '.\n'

print('Normalized string with new sentence added:')
print(norm_plusnew)
print()


# iz misspelling: --> is
# find ' iz ' and change it to ' is '

sss = norm_plusnew.replace(' iz ', ' is ')
print('Result string:')
print(sss)
