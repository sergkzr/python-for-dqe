import os
from time import sleep

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

 

def get_obj_prop(obj_type: str, obj_keys: dict, obj_lines: list, skipped: str) -> dict:
    """
Get object (type) properties -> dic

    obj_type  : like "News" | "Book"
    obj_keys  : dict with the object (type) pproperties names
    obj_lines : list of object lines (represantation)
    skipped   : in-out string with skipped lines (during parsing of object lines)
"""

    #lines = obj_string.splitlines()  ??
    lines = obj_lines
    
    prop_dict = {}

    key = "Obj_type"
    value = obj_type
    
    skipped = ''
    multy_line = True

    for line in lines:

        # print('--->', line)

        if line.find(':') >= 0:
      
            prop_dict |= {key: value} 
            
            key, value = line.split(':')
            key = key.strip().lower().title()
            
            multy_line = True
            if key in obj_keys:
                multy_line = True if obj_keys[key] > 1 else False

        elif key == 'Obj_type':
            pass
        elif key in obj_keys and multy_line:
            value += '\n'.join([value, line])
        elif key in obj_keys:      # one line
            prop_dict |= {key: value}
            skipped = '\n'.join([skipped, line])
        else:
            # print(f'{key=}, {value=}')
            value = '\n'.join([value, line])    
        # print(f'{key=}')
        # print(f'{value=}')
        # print(f'{prop_dict=}')
        # print(f'{skipped=}')                  

    prop_dict |= {key: value} 

    return {k: v  for k, v in prop_dict.items() if k in obj_keys}


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

    skipped = ''
    obj_type = 'News'

    pr_dict = get_prop(obj_type, news_keys, s, skipped)

    print(f'{obj_type} Result:')
    print(news_keys)
    for key, value in pr_dict.items():
        print(f'{key}: {value}')

 
    pr_dict = get_prop(obj_type, ad_keys, s, skipped)

    print(f'{obj_type} Result:')
    print(ad_keys)
    for key, value in pr_dict.items():
        print(f'{key}: {value}')

    skipped = ''
    obj_type = 'Book'
    
    pr_dict = get_prop(obj_type, book_keys, s, skipped)
  
    print(f'{obj_type} Result:')
    print(book_keys)          
    for key, value in pr_dict.items():
        print(f'{key}: {value}')
