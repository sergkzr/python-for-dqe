# HW6: files and modules

import datetime as dt
import os
# from time import sleep

import utilities as U
import ingest_from_text as IT

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

    def show(self, oneline=False):
        print(self.make_obj_string(oneline))
       

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

    def make_obj_string(self, oneline=False):
        if oneline:
            return f'<News: {self.published}, City: {self.city}, Msg: {self.msg[:20]}>'
        else:
            return (
            f"<----------\n"
            f"News: {self.published}\n"
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

    def make_obj_string(self, oneline=False):
        if oneline:
            return f'<Private AD: {self.published}, Expiration Date: {self.expiration_date}, Days Left: {self.__expire_days()}, Txt: {self.msg[:20]}>'
        else:
            return (
            f"<----------\n"
            f"Private Ad, {self.published}\n"
            f"Text: {self.msg}\n"
            f"Expiration Date: {self.expiration_date}\n"
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

    def make_obj_string(self, oneline=False):
        if oneline:
            return f'<Book: {self.published}, ISBN: {self.isbn}, Publish Year: {self.publish_year}, Title: {self.msg[:20]}>'
        else:
            return (
            f"<----------\n"
            f"Book, {self.published}\n"
            f"Title: {self.msg}\n"
            f"ISBN: {self.isbn}\n"
            f"Publish_Year: {self.publish_year}\n"
            f"---------->")


# ## MESSAGE OBJECTS METADATA ####################################

message_types = {
    'News': News_message, 
    'Private Ad': Private_ad_message, 
    'Book': Book_message
}

# Ingest 'Property': 1 one line, 2 - multy line

news_ingest_prop =  {
    'Message': 2, 
    'City': 1
} 
ad_ingest_prop =  {
    'Message': 2, 
    'Expiration Date': 1
}
book_ingest_prop = {
    'Title': 2, 
    'Isbn': 1, 
    'Publish Year': 1
}

message_ingest_prop = {
    'News':       news_ingest_prop,
    'Private Ad': ad_ingest_prop,
    'Book':       book_ingest_prop
}

# map ingest property name to object property name

news_ingest_to_objprop_map = {
    'Message': 'msg', 
    'City': 'city'
}  
ad_ingest_to_objprop_map = {
    'Message': 'ad', 
    'Expiration Date': 'expiration_date'
}
book_ingest_to_objprop_map = {
    'Title': 'book_name', 
    'Isbn': 'isbn', 
    'Publish Year': 'publish_year'
}

message_ingest_to_objprop_map = {
    'News':       news_ingest_to_objprop_map,
    'Private Ad': ad_ingest_to_objprop_map,
    'Book':       book_ingest_to_objprop_map
}

# messages_init = {'News':       News_message,
#                  'Private Ad': Private_ad_message,
#                  'Book':       Book_message}

## ######################################################

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
        self.hist_file_name = err_fname
    
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

    def from_text(self):

        objects_lines, obj_index, obj_type, skipped_lines = IT.parse_objects_from_text(self.ing_file_path)

        objects_dict_list, skipped_lines_2 = IT.parse_objects_from_obj_lines(objects_lines, obj_index, obj_type)

        allowed_dict_list, skipped_lines_3 = IT.allowed_obj_dicts_from_obj_dicts(objects_dict_list, message_types, message_ingest_prop)

        objects_list, skipped_lines_4 = IT.parse_objects_from_dict_list(allowed_dict_list, message_types, message_ingest_to_objprop_map)

        skipped = ''.join(skipped_lines + skipped_lines_2 + skipped_lines_3 + skipped_lines_4)

        print(f'There are skipped lines in input text file:\n{skipped}')
        print('Objects found:')
        for i, obj in enumerate(objects_list):
            print(f'{i:02}', sep='')
            obj.show(oneline=True)

        print('Ignore ingest or Save objects found?', sep='')
        while True:
            ans = input('I|S')
            if ans == 'I':
                return f'Ingest from file {self.ing_file_path} ignored'
            elif ans == 'S':
                break
            else:
                pass

        # save all the 'valid objects
        # copy ingest file to arch with processing date
        # delete ingest file
        # save skipped lines in err file with processing date
        # save valid objects to arch file with processing date



        print(f'Objects from file {self.ing_file_path} ingested')
        print(f'Source file moved to archive: {self.arch_file_path} {self.ing_file_path}')
        print(f'Skipped lines saved to: {self.arch_file_path} {self.hist_file_name}')
        print(f'Ingested objects logged to file: {self.arch_file_path} {self.hist_file_name}')
        

        return 'Wait'



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
