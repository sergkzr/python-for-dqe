# HW6: files and modules

import datetime as dt
import os
# from time import sleep

import utilities as U

class Constants:

    FILE_PATH = './data/feed_data'   # like internal DB file path
    OBJECTS_PER_SCREEN = 3

    INGEST_FILE_PATH_DEFAULT = './data/for_ingest'
    INGEST_FILE_NAME_DEFAULT = 'for_ingest.txt'

    ARCHIVE_FILE_PATH_DEFAULT = './data/archive'
    ARCHIVE_ERRFILE_DEFAULT = 'ingest_err'
    ARCHIVE_SUCCFILE_DEFAULT = 'ingest_succ'


class Empty_object:
    def __init__(self):
        self.message = 'Empty object'

    def show(self):
        print(self.message)

empty_object = Empty_object()


class Messages:
    def __init__(self, file_name):
        self.file_name = file_name
        self.lines_list = []
        self.object_index_list = []
        self.n_objects = 0
        self.last_page_lengh = 0
        self.current_page = 0
        self.file_is_read = False

    def __make_object_index(self):

        if not self.file_is_read:

            page_length = Constants.OBJECTS_PER_SCREEN

            lines_list = []
            object_index_list = []

            with open(self.file_name, 'r') as file:
                
                lines = file.read().split('\n')
                
                for i, line in enumerate(lines):
                    lines_list.append(line)
                    if line.startswith('<----------'):
                        object_index_list.append(i) 

            self.lines_list = lines_list
            self.n_objects = len(object_index_list)        
            self.object_index_list = object_index_list

            last_page_length = self.n_objects % page_length
            
            self.pages_num = self.n_objects // page_length + (1 if  last_page_length > 0 else 0)
            self.last_page_length = page_length if last_page_length == 0 else last_page_length

            self.current_page = 0
            self.file_is_read = True


    def __show_page(self, page_numb, page_objects):

        start_index = page_numb * Constants.OBJECTS_PER_SCREEN
        end_index = start_index + page_objects

        for obj_ind in self.object_index_list[start_index : end_index]:
            
            for line in self.lines_list[obj_ind:]:

                print(line)
                if line.strip() == '---------->': 
                    break

        return None

    def show_first_page(self):

        self.__make_object_index()

        page_length_default = Constants.OBJECTS_PER_SCREEN
        self.current_page = 0

        page = 0
        page_objects = self.last_page_length if (page + 1) == self.pages_num  else page_length_default
        self.__show_page(page, page_objects) 

        return 'Wait'
    
    def show_last_page(self):

        self.__make_object_index()
        
        page_length_default = Constants.OBJECTS_PER_SCREEN
        
        page = self.pages_num - 1
        self.current_page = page
        page_length = self.last_page_length 

        self.__show_page(page, page_length)

        return 'Wait'

    def show_next_page(self):
       
        self.__make_object_index()

        if self.current_page >= self.pages_num - 1 :     # last page and after 

            self.show_last_page()   # show last shown page

        else:

            self.current_page += 1
           
            page_length_default = Constants.OBJECTS_PER_SCREEN
            page = self.current_page
            page_objects = self.last_page_length if page  == (self.pages_num - 1 )  else page_length_default

            self.__show_page(page, page_objects)

        return 'Wait'

    def show_prev_page(self):

        self.__make_object_index()

        if self.current_page <= 0 :     # before first page or first page

            self.current_page = 0 
            self.show_first_page()

        else:
            
            self.current_page -= 1

            page = self.current_page
            page_length_default = Constants.OBJECTS_PER_SCREEN
            page_objects = self.last_page_length if page == (self.pages_num - 1)  else page_length_default

            self.__show_page(page, page_objects)

        return 'Wait'



class Message:
    def __init__(self, msg='NoMessage'):
        self.msg = msg
        self.published = '000-00-00'

    def put_message(self):

        self.published = dt.datetime.utcnow()
       
        obj_str = self.make_obj_string()
        
        with open(Constants.FILE_PATH, 'a') as file:
            file.write(obj_str)

        return obj_str

    def show(self):
        print(self.make_obj_string())
       

class News_message(Message):
    def __init__(self, msg='NoMessage', city='NoCity'):
        super().__init__(msg)
        self.city = city
        
    def make(self):
        # input data check could be added
        self.msg = input('News message: ')
        self.city = input('City: ')

        obj_str = self.put_message()
        print(obj_str)
        
        return 'Wait'

    def make_obj_string(self):
        return (
        f"<----------\n"
        f"News, {self.published}\n"
        f"Text: {self.msg}\n"
        f"City: {self.city}\n"
        f"---------->")


class Private_ad_message(Message):

    def __init__(self, ad='NoAd', expiration_date='NoDate'):
        super().__init__(ad)
        self.expiration_date = expiration_date

    def __expire_days(self):

        now_date = dt.date.today()

        sy, sm, sd = self.expiration_date.split('-')
        y = int(sy)
        m = int(sm)
        d = int(sd)
        try:
            exp_date = dt.date(y, m, d)
        except:
            exp_date = now_date
        exp_days = exp_date - now_date

        return f'{exp_days}'

    def make(self):
        # input data check could be added
        self.msg = input('New Private Ad: ')
        self.expiration_date = input('Expiration_date: ')

        obj_str = self.put_message()
        print(obj_str)

        return 'Wait'

    def make_obj_string(self):
        return (
        f"<----------\n"
        f"Private Ad, {self.published}\n"
        f"Text: {self.msg}\n"
        f"City: {self.expiration_date}\n"
        f"Days Left: {self.__expire_days()}\n"
        f"---------->")


class Book_message(Message):

    def __init__(self, book_name='NoBookName', isbn='NoISBN', publish_year='NoYear'):
        super().__init__(book_name)
        self.isbn = isbn
        self.publish_year = publish_year

    def make(self):
        # input data check could be added
        self.msg = input('New Book title: ')
        self.isbn = input('ISBN: ')    
        self.publish_year = input('Publish_year: ')   

        obj_str = self.put_message()
        print(obj_str)

        return 'Wait'

    def make_obj_string(self):
        return (
        f"<----------\n"
        f"Book, {self.published}\n"
        f"Title: {self.msg}\n"
        f"ISBN: {self.isbn}\n"
        f"Publish_Year: {self.publish_year}\n"
        f"---------->")


message_types = ['News', 'Private Ad', 'Book']

news_prop = {'Message': 2,
             'City': 1}  # 'Property': 1 one line, 2 - multy line
ad_prop =   {'Message': 2, 
             'Expiration Date': 1}
book_prop = {'Title': 2, 
            'Isbn': 1, 
            'Publish Year': 1}

news_map = {'Message': 'msg', 
            'City': 'city'}  # Names to Parameters mapping
ad_map =   {'Message': 'ad', 
            'Expiration Date': 'expiration_date'}
book_map = {'Title': 'book_name', 
            'Isbn': 'isbn', 
            'Publish Year': 'publish_year'}

message_prop = {'News':       news_prop,
                 'Private Ad': ad_prop,
                 'Book':       book_prop}

messages_init = {'News':       News_message,
                 'Private Ad': Private_ad_message,
                 'Book':       Book_message}


class Ingest:
    def __init__(self, 
                 ingest_file_path, 
                 output_file_path, 
                 arch_path,
                 hist_fname,
                 err_fname):
        self.ing_file_path = ingest_file_path
        self.out_file_path = output_file_path
        self.arch_file_path = arch_path
        self.hist_file_name = hist_fname
        self.err_file_name = err_fname
    
    def change_source_file(self):
        curr_path = self.ing_file_path
        print(f'Current ingest file path: {curr_path}')
        while True:
            new_path = input("New ingest file path: ")
            if new_path == 'Exit': 
                self.ing_file_path = curr_path
                return curr_path
            if os.path.isfile(new_path):
                break
        self.ing_file_path = new_path
        return new_path

    def __objects_from_text(self):
        """
        Result:
         objects_lines_list : text to  lines, source linex except skipped lines
         obj_index_list     : list with indexes of the first row of the object in objects_lines_list
         skipped_lines_list : list of skipped lines in the source text  
        """
        return U.parse_objects_from_text(self.ing_file_path, message_types)

    def __make_object(self, obj_type, obj_lines, obj_prop):

        if obj_type not in message_types:
            return empty_object 
        
        skipped = ''
        
        if obj_type == 'News':

            prop = U.get_obj_prop(obj_type, news_prop, obj_lines, skipped)
            params = {news_map[k]: v for k, v in prop.items()}
            obj = News_message(**params)
            # obj.put_message()
            obj_str = obj.make_obj_string()
 
        elif obj_type == 'Private Ad':

            prop = U.get_obj_prop(obj_type, ad_prop, obj_lines, skipped)
            params = {ad_map[k]: v for k, v in prop.items()}
            obj = Private_ad_message(**params)
            # obj.put_message()
            obj_str = obj.make_obj_string()
            
        elif obj_type == 'Book':
                    
            prop = U.get_obj_prop(obj_type, book_prop, obj_lines, skipped)
            params = {book_map[k]: v for k, v in prop.items()}
            obj = Book_message(**params)
            # obj.put_message()
            obj_str = obj.make_obj_string()
            
        return obj

  

MENU_SHOW_ALL = {
    '__init__': ('init object', obj := Messages(Constants.FILE_PATH)),
    '1': ('show First page',    obj.show_first_page),
    '2': ('show Previous page', obj.show_prev_page),
    '3': ('show Next page',     obj.show_next_page),
    '4': ('show Last page',     obj.show_last_page),
    '0': ('Exit', lambda: 'Exit')
}


MENU_INGEST = {
    '__init__': ('init object',    
                 obj := Ingest(ingest_file_path='/'.join([Constants.INGEST_FILE_PATH_DEFAULT, Constants.INGEST_FILE_NAME_DEFAULT]), 
                                output_file_path=Constants.FILE_PATH, 
                                arch_path=Constants.ARCHIVE_FILE_PATH_DEFAULT,
                                hist_fname=Constants.ARCHIVE_SUCCFILE_DEFAULT,
                                err_fname=Constants.ARCHIVE_ERRFILE_DEFAULT)
                ),
    '1': ('Choose file to read',   obj.change_source_file),
    '2': ('Ingest from text file', obj.from_text),
    '3': ('Ingest from JSON',      lambda: 'Not developed yet'),
    '4': ('Ingest from XML',       lambda: 'Not developed yet'),
    '0': ('Exit', lambda: 'Exit')
}

MENU = {
    '__init__': ('init object', None),    
    '1': ('Make News message',        News_message().make),
    '2': ('Make Private Add message', Private_ad_message().make),
    '3': ('Make_Book_message',        Book_message().make),
    '4': ('Enter messages from file', U.Menu(MENU_INGEST, f'INGEST MENU --------------\nCurrent ingest file: {Constants.INGEST_FILE_PATH_DEFAULT}').run),
    '5': ('Show all the messages',    U.Menu(MENU_SHOW_ALL, 'SHOW FILE MENU --------------').run),
    '0': ('Exit programm', lambda: 'Exit')
}


if __name__ == '__main__':

    # create file if not exists
    try:
        with open(Constants.FILE_PATH, 'r') as file:
            pass
    except FileNotFoundError:
        with open(Constants.FILE_PATH, 'w') as file:
            pass
    
    # run app - main menu
    
    menu_res = U.Menu(MENU, 'Main menu').run()
    
    print(menu_res)
