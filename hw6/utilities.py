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

 
def parse_objects_from_text(ing_file, message_types):
    """
    Text file format:

    ***<ObjType1>
    <Key1>: <value - 1 or some lines
    ...
    <KeyN>: <valueN - 1 or some lines
    ***<OBjType2>
    <Key1>: <value - 1 or some lines
    ...
    <KeyN>: <valueN - 1 or some lines
    --<end-of-file>

    Example:

    ***News
    Message: Any text - without ':', It's possible to
    have sentences (wich are ended by dot symbol '.'.
    one line or more than one line of text
    Date: 2013-10-12



    Result:
       objects_lines_list : text to  lines, source linex except skipped lines
       obj_index_list     : list with indexes of the first row of the object in objects_lines_list
       skipped_lines_list : list of skipped lines in the source text
    """

    error_result = ([], [], [])

    try:

        with open(ing_file, 'r') as file:
            lines = file.readlines()
        
        if not lines:
            # empty source file
            print(f'Empty file:: {ing_file}')
            return error_result 

    except:

        # No file or invalid path
        print(f'-parse_objects_from_text: {ing_file}')
        return error_result

    objects_lines = []
    obj_index = []
    skipped_lines = []

    skip = True
    index = 0

    for i, line in enumerate(lines):
        # print(i, line, end='')
           
        if line.startswith('***') and len(line) > 3:

            obj_type_curr =  line[3:].strip().lower().title()

            if obj_type_curr not in message_types:
                skipped_lines.append(line)
                skip = True
                continue

            objects_lines.append(line)
            obj_index.append(index)
            index += 1 
            skip = False
                                
        elif skip:
            skipped_lines.append(line)

        else:  
            objects_lines.append(line)
            index += 1 
       
    return (objects_lines, obj_index, skipped_lines)


def get_obj_prop(obj_type: str, obj_keys: dict, obj_lines: list, skipped: list) -> dict:
    """
Get object (type) properties -> dic with object properties

    obj_type  : like "News" | "Book"
    obj_keys  : dict with the object (type) pproperties names
    obj_lines : list of object lines (represantation)
    skipped   : in-out string with skipped lines (during parsing of object lines)
"""

    #lines = obj_string.splitlines()  ??
    lines = obj_lines
    
    prop_dict = {}

    key = "Skipped"
    value = obj_type
    skipped = []
    multy_line = True

    for line in lines:

        if line.find(':') >= 0:
      
            prop_dict |= {key: value} 
            
            key, value = line.split(':')
            key = key.strip().lower().title()
            
            multy_line = True
            if key in obj_keys:
                multy_line = True if obj_keys[key] > 1 else False

            if not multy_line:
                prop_dict |= {key: value}
                key = 'Skipped'

        elif key = 'Skipped':
            skipped.append(line)
        elif (key in obj_keys) and multy_line:
            value = '\n'.join([value, line])
        else:  # key not in obj_keys
            value = '\n'.join([value, line])    
        # print(f'{key=}')
        # print(f'{value=}')
        # print(f'{prop_dict=}')
        # print(f'{skipped=}')                  

    prop_dict |= {key: value} 

    return {k: v  for k, v in prop_dict.items() if k in obj_keys}


def json_get(js: str, key: str, default_value: str = 'NoValue') -> str:
    """
      get value for given key(s) in json string
      js  : json string to be parsed
      key : key which value requested, e.x. 'device.MacId'
      default return value - in case json is bad or there are no keys requested in json provided
    """

    res = default_value
    
    keys = key.split('.')
    if len(keys) == 0: 
        return default_value
    
    try:
      js_obj = json.loads(js)
    except:
      return default_value

    interm = js_obj
    for k in keys:
        if type(interm) is not dict: 
            return default_value
        interm = interm.get(k, default_value)

    return str(interm)


if __name__ == '__main__':

    news_keys = {'Message': 2, 'City': 1}
    ad_keys = {'Private Ad': 2, 'Expiration Date': 1}
    book_keys = {'Title': 2, 'Isbn': 1, 'Publish Year':1}

    s = """  aaa aaa aaa
Message: bbb1 bbb2 bbb3
bbb4 bbb5 bbb6
bbb7
Message1: cccc1 cccc2 cccc3
Date: 2022-05-09
City: Pula/Pola

Expiration Date: 2022-101-30
Private Ad: mess1
mess 2

fdsf 
dsasdg
MMM : m1 m2 m3
   Finish : Finish
: Empty key
Title: SVE za vozila
ISBN : 123456789
Publish Year: 2020
Key: ''
:
ogogo1
ogogo2
"""

    # skipped = ''
    # obj_type = 'News'

    # pr_dict = get_prop(obj_type, news_keys, s, skipped)

    # print(f'{obj_type} Result:')
    # print(news_keys)
    # for key, value in pr_dict.items():
    #     print(f'{key}: {value}')

 
    # pr_dict = get_prop(obj_type, ad_keys, s, skipped)

    # print(f'{obj_type} Result:')
    # print(ad_keys)
    # for key, value in pr_dict.items():
    #     print(f'{key}: {value}')

    # skipped = ''
    # obj_type = 'Book'
    
    # pr_dict = get_prop(obj_type, book_keys, s, skipped)
  
    # print(f'{obj_type} Result:')
    # print(book_keys)          
    # for key, value in pr_dict.items():
    #     print(f'{key}: {value}')
