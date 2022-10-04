# assumptions:
#   - whitespace is exactly what defined in string module
#   - sentence is string, which ends with '.' OR ':', thats why first row in source string is centence

import string as st
ws = st.whitespace

s = """homEwork:

  tHis iz your homeWork, copy these Text to variable.

 

  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

 

  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.

 

  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
"""
# print('Source string:')
# print(s)
# print()


# 'normalize' string - transform it to lower case
sl = s.lower()


# calculate amount of white spaces,
# prepare new string with capital letter in each first word of the sentence
# by parsing normalized string symbol by symbol 

ss = ''
ws_count = 0
new_sentence = True 

for i, c in enumerate(sl):

    # calculate whitespaces in the normalized string
    if c in ws:
        ws_count = ws_count + 1
        # print(f'index: {i}, ws_count: {ws_count}, symb:"{c}"')

    # move input symbol to output string
    # change first letter in the first word of the sentence to upper case
    if c in ':.' :
        ss = ss + c 
        new_sentence = True
    elif new_sentence and (c in ws):
        ss = ss + c
    elif new_sentence:
        ss = ss + c.upper()
        new_sentence = False
    else:
        ss = ss + c

print(f'whitespace_count: {ws_count}')
print('Updated string (normalized and with capital letter in the start of the sentence):')
print(ss) 
print()  

#
# prepare list of last words in each sentence
# add them to the source normalized string
#

last_sentence_word_list = []

# first sentence is ended with ':'

s1 = ss.split(':')
last_sentence_word_list.append(s1[0].split()[0])

# other sentences are ended with '.'

s2 = s1[1]
# split into sentences
sent_list = s2.split('.')

# split each sentence to words
# get last word of the sentence
for sent in sent_list:
    word_list = sent.split()
    if len(word_list) != 0 :
        last_sentence_word_list.append(word_list[-1])

print('Word list of last words in each sentence:')
print(last_sentence_word_list)
print()

# add new string
ss_plusnew = ss + ' '.join(last_sentence_word_list) + '.\n'
print('Normalized string with new sentence added:')
print(ss_plusnew)
print()


# iz misspelling: --> is
# find ' iz ' and change it to ' is '

sss = ss_plusnew.replace(' iz ', ' is ')
print('Result string:')
print(sss)
