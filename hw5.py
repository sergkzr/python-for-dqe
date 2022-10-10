# 1.News – text and city as input. Date is calculated during publishing.
#
# 2.Privat ad – text and expiration date as input. Day left is calculated during publishing.
#
# 3.Your unique one with unique publish rules: text and 


import datetime as dt
import os
from time import sleep


class Constants:
    FILE_PATH = './data/feed_data'
    OBJECTS_PER_SCREEN = 3


class Messages:
    def __init__(self, file_name):
        self.file_name = file_name
        self.lines_list = []
        self.object_index_list = []
        self.n_objects = 0
        self.current_position = 0
        self.pred_position = 0
        self.file_is_read = False

    def __make_object_index(self):

        if not self.file_is_read:

            lines_list = []
            object_index_list = []
            n_objects = 0
            object_index_list = []
            lines_list = []

            with open(self.file_name, 'r') as file:
                
                lines = file.read().split('\n')
                
                for i, line in enumerate(lines):
                    lines_list.append(line)
                    if line.startswith('<----------'):
                        object_index_list.append(i) 
                        n_objects += 1

            self.n_objects = n_objects        
            self.lines_list = lines_list
            self.object_index_list = object_index_list
            self.current_position = 0
            self.pred_position = 0

            self.file_is_read = True

    def __show_page(self):

        page_len = Constants.OBJECTS_PER_SCREEN

        if (self.current_position >= 0) and (self.current_position < self.n_objects):
            from_ind = self.current_position
        else:
            from_ind = self.pred_position
            self.current_position = self.pred_position

        rest_len = self.n_objects - from_ind
        if rest_len >= page_len:
            to_ind = from_ind + page_len - 1
        else:
            to_ind = from_ind + rest_len - 1
        
        for obj_ind in self.object_index_list[from_ind:to_ind+1]:

            for line in self.lines_list[obj_ind:]:

                print(line)
                if line.strip() == '---------->': 
                    break

        return self.current_position + to_ind - from_ind + 1

    def show_first_page(self):

        self.__make_object_index()

        self.current_position = 0
        back = self.current_position
        self.current_position = self.__show_page()
        self.pred_position = back  

        return 'Wait'
    
    def show_last_page(self):
        
        self.__make_object_index()

        back = self.current_position
        self.current_position = self.n_objects - Constants.OBJECTS_PER_SCREEN
        self.current_position = self.__show_page()
        self.pred_position = back

        return 'Wait'

    def show_next_page(self):
       
        self.__make_object_index()

        back = self.current_position
        self.current_position = self.__show_page()
        self.pred_position = back

        return 'Wait'

    def show_prev_page(self):

        self.__make_object_index()

        back = self.current_position
        self.current_position -= Constants.OBJECTS_PER_SCREEN
        self.current_position = self.__show_page()  
        self.pred_position = back

        return 'Wait'


class Message:
   
    def __init__(self, msg='NoMessage'):
        self.msg = msg

    def put_message(self):

        with open(Constants.FILE_PATH, 'a') as file:
            file.write(self.make_obj_string())

    def show(self):
        print(self.make_obj_string())
       

class News_message(Message):
    def __init__(self, msg='NoMessage', city='NoCity'):
        super().__init__(msg)
        self.city = city

    def make(self):
        self.msg = input('News message: ')
        self.city = input('City: ')
        return self

    def make_obj_string(self):
        return f"""<----------
News
text: {self.msg}
city: {self.city}
----------> 
"""


class Private_ad__message(Message):

    def __init__(self, ad='NoAd', expiration_date='NoDate'):
        super().__init__(ad)
        self.expiration_date = expiration_date

    def __expire_days(self):

        now_date = dt.date.today()

        sy, sm, sd = self.expiration_date.split('-')
        y = int(sy)
        m = int(sm)
        d = int(sd)
        exp_date = dt.date(y, m, d)

        exp_days = exp_date - now_date

        return f'{exp_days}'

    def make(self):
        self.msg = input('New Private Ad: ')
        self.expiration_date = input('Expiration_date: ')
        return self

    def make_obj_string(self):
        return f"""<----------
Private Ad
text: {self.msg}
city: {self.expiration_date}
days left: {self.__expire_days()}
---------->
"""


class Book_message(Message):

    def __init__(self, book_name='NoBookName', isbn='NoISBN', publish_year='NoYear'):
        super().__init__(book_name)
        self.isbn = isbn
        self.publish_year = publish_year

    def make(self):
        self.msg = input('New Book title: ')
        self.isbn = input('ISBN: ')    
        self.publish_year = input('Publish_year: ')   
        return self 

    def make_obj_string(self):
        return f"""<----------
Book_anounce
Title: {self.msg}
ISBN: {self.isbn}
publish_year: {self.publish_year}
----------> 
"""

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
                        _ = input('Press any key')
                    else:
                        print(res)
                        sleep(2)

                elif self.objct is None:

                    res.show()
                    res.put_message()
                    print('Written.')
                    sleep(2)


# obj := Messages(Constants.FILE_PATH)

MENU_SHOW_ALL = {
    '__init__': ('init object', obj := Messages(Constants.FILE_PATH)),
    'F': ('show First page', obj.show_first_page),
    'P': ('show Previous page', obj.show_prev_page),
    'N': ('show Next page', obj.show_next_page),
    'L': ('show Last page', obj.show_last_page),
    'E': ('Exit', lambda: 'Exit')
}

MENU = {
    '__init__': ('init object', None),    
    '1': ('Make News  message',       News_message().make),
    '2': ('Make Private Add message', Private_ad__message().make),
    '3': ('Make_Book_message',        Book_message().make),
    '4': ('Show all the messages',    Menu(MENU_SHOW_ALL, 'SHOW FILE MENU --------------').run),
    '0': ('Exit programm',            lambda: 'Exit')
}


if __name__ == '__main__':

    # create file if not exists
    try:
        with open(Constants.FILE_PATH, 'r') as file:
            pass
    except FileNotFoundError:
        with open(Constants.FILE_PATH, 'w') as file:
            pass
    
    news0 = News_message("We are waiting for Pope's visit", 'Napoly')
    print(news0.make_obj_string())

    ad0 = Private_ad__message('Be ready to see new slippers in owr stories!', '2022-12-25')
    print(ad0.make_obj_string())
    
    book0 = Book_message('PySpark and Big Data', 'ISBN: 23456123', '2010')
    print(book0.make_obj_string())

    menu = Menu(MENU, 'Main menu')
    menu_res = menu.run()
    
    print(menu_res)




    
