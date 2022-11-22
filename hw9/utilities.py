import os
from time import sleep
import string as st

ws = st.whitespace

def get_normalized_list(source_text, split_symbol):
    """
    Given source_text (which is string),
    Split it on the sentences (separate line of text, as list element), in wich:
    - all the symbols are in lower case, except the first symbol of the sentence
    - there are no leading whitespaces
    - each sentence starts from capital letter
    - each sentence ends with split symbol, e.g. '.', wich is the end symbol of the sentence
    - there are no empty lines
    --->> normalized text, lenes are separated by symbol '\n' 
    """
  
    source = source_text.lower()
    
    normalized_text =  []
    sentences = source.split(split_symbol)

    for sent in sentences:
        if len(sent.strip()) != 0:
            ss = sent.strip()
            normalized_text.append(ss[0].upper() + ss[1:] + split_symbol)

    return '\n'.join(normalized_text)

##
## properties checks
##
##

def check_date(date_str):

    date_valid = True

    # check date
    try:
        y, m, d = date_str.split('-')
    except:
        return False
    
    y = int(y)
    m = int(m)
    d = int(d)

    if not ((y >= 1945) and (y <= 2030)):
        date_valid = False
    elif not ((m >= 1) and (m <= 12)):
        date_valid = False
    elif not ( (d >= 1) and (d <= (31 if m in [1, 3, 5, 7, 8, 10, 12] else (30 if m in [4, 6, 9, 11] else 29))) ):
        date_valid = False

    return date_valid


def check_year(year_str):
    
    year_valid = True
    
    # check year
    try:
        y = int(year_str)
    except:
        return False

    if not ((y >= 1900) and (y <= 2030)):
        year_valid = False

    return year_valid


def check_message(message_str_list):
    message_valid = True
    # check message
    return message_valid


def check_ISBN(isbn, year=2008):

    isbn_valid = True
    isbn = str(isbn)

    # check isbn
    if not isbn.isdigit():
        return False

    # 13 digits after 2007
    # 10 digits before year 2008
    if year < 2008:
        if len(isbn) != 10:
            isbn_valid = False
    else:
        if len(isbn) != 13:
            isbn_valid = False
    
    return isbn_valid

##
## MENU execution
##

class Menu:
    def __init__(self, menu, title):
        self.title = title
        init_param = menu.get('__init__', None)
        if init_param:
            self.objct = init_param[1]
            menu.pop('__init__')
            self.MENU = menu
        else:   
            self.objct = None 
            self.MENU = menu
        
    def __show(self):

       # clear screen
        _ = os.system('cls') if os.name == 'nt' else os.system('clear')
    
        # show title
        print(f'{self.title:<20}')
        print('Choose option:')
 
        # show menu 
        for menu_point, (menu_message, _) in self.MENU.items():
            print(f'\t{menu_point:2}: {menu_message}')

        # prompt
        print('> ', end='')

    def run(self):
        
        while True:

            self.__show()
            
            input_str = input()
            if input_str == '':
                pass

            # menu_mf - Menu Message Function
            elif ( menu_mf := self.MENU.get(input_str, None) ) is None:
                
                print('Not valid menu point. Please repeat.')
                sleep(2)
                                
            else:

                res = menu_mf[1]()

                if type(res) is str:

                    if res == 'Exit':
                        return 'Done'
                    elif res == 'Wait':
                        _ = input('Press ENTER key')
                    else:
                        print(res)
                        sleep(2)

 
