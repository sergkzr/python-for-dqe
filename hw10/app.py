# HW10: files and modules

import datetime as dt
import os
import csv
import json
# from time import sleep

import utilities as U
import ingest_utils as Ing
import statistics_csv as ST
import db_utilities as DB



class Constants:

    FILE_PATH = './data/feed_data'   # like internal DB file path
    DB_FILE_PATH = './data/feed_data.db'
    FILE_STATS_WORDCOUNT = './data/wordcount'
    FILE_STATS_SYMBCOUNT = './data/lettercount'

    OBJECTS_PER_SCREEN = 3

    INGEST_FILE_PATH_DEFAULT = './data/for_ingest'
    INGEST_FILE_NAME_DEFAULT = 'for_ingest'  ### plus extention: .txt|.json|.xml
    
    ARCHIVE_FILE_PATH_DEFAULT = './data/archive'



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

            with open(self.file_name, 'r', encoding='UTF-8') as file:
                
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
        self.published = '0000-00-00'


    def put_message_file(self):

        self.published = dt.datetime.utcnow()
        obj_str = self.make_obj_string()
        
        with open(Constants.FILE_PATH, 'a', encoding='UTF-8') as file:
            file.write(obj_str)

        return obj_str


    # def put_message_db(self):

    #     self.published = dt.datetime.utcnow()
    #     objtype, obj_insert_sql = self.make_obj_insert_sql()

    #     obj_ind, obj_pk = db.put_message(objtype, obj_insert_sql, self.published)

    #     obj = db.get_object_byind()

    #     return obj.make_obj_string(oneline=True)


    def put_message(self):

        obj_oneline_str = self.put_message_db()
        obj_str = self.put_message_file()

        # make_stats(mode='file')
        make_stats(mode='db')

        return obj_oneline_str, obj_str

    
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
            return f'<News: {self.published}, City: {self.city}, Msg: {self.msg[:20]}...>'
        else:
            return (
            f"<----------\n"
            f"News, {self.published}\n"
            f"Text: {self.msg}\n"
            f"City: {self.city}\n"
            f"---------->\n")


    def put_message_db(self):

        self.published = dt.datetime.utcnow()

        obj_ind_id = db.put_news(self)
        if obj_ind_id == -1:
            # cannot put news object to DB
            return 'Cannot put News to Db.'

        obj_dict, time_created, ind_id = db.get_news(obj_ind_id)
        if not obj_dict:
            # cannot get previously put object 
            return 'Cannot get News created from Db.'

        print(obj_dict)
        
        obj_json_str = json.dumps(obj_dict)

        return obj_json_str



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
            return f'<Private Ad: {self.published}, Expiration Date: {self.expiration_date}, Days Left: {self.__expire_days()}, Txt: {self.msg[:20]}...>'
        else:
            return (
            f"<----------\n"
            f"Private Ad, {self.published}\n"
            f"Text: {self.msg}\n"
            f"Expiration Date: {self.expiration_date}\n"
            f"Days Left: {self.__expire_days()}\n"
            f"---------->\n")


    def put_message_db(self):

        return '{"__ObjectType": "Dummy"}'


    # def make_obj_insert_sql(self):
    #     objtype = 'Private Ad'
    #     # TODO: expire_days - add to table definition and to query
    #     prad_insert_sql = f'insert into privatead (message, expiration_date, expire_days) values("{self.msg}", "{self.expiration_date}", "{self.__expire_days()}")'
    #     return objtype, prad_insert_sql
        


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
            return f'<Book: {self.published}, ISBN: {self.isbn}, Publish Year: {self.publish_year}, Title: {self.msg[:20]}...>'
        else:
            return (
            f"<----------\n"
            f"Book, {self.published}\n"
            f"Title: {self.msg}\n"
            f"ISBN: {self.isbn}\n"
            f"Publish Year: {self.publish_year}\n"
            f"---------->\n")


    # def make_obj_insert_sql(self):
    #     objtype = 'Book'
    #     # TODO: expire_days - add to table definition and to query
    #     book_insert_sql = f'insert into book (title, isbn, publish_year) values("{self.msg}", "{self.isbn}", "{self.publish_year}")'
    #     return objtype, book_insert_sql


    def put_message_db(self):

        return '{"__ObjectType": "Dummy"}'



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

    ing_txt = 'txt'
    ing_json = 'json'
    ing_xml = 'xml'

    def __init__(self, 
                 ingest_file_path,
                 ingest_file_name, 
                 output_file_path,
                 arch_path):

        self.ing_file_path = ingest_file_path
        self.ing_file_name = ingest_file_name
        self.out_file_path = output_file_path
        self.arch_file_path = arch_path

    
    def change_source_file(self):
        # change the NAME of ingest file in default ingest directory, 
        # EXTENTION/TYPE will be added automatically by correspondent ingest method
        curr_name = self.ing_file_name
        print(f'Current ingest path: {self.ing_file_path}')
        print(f'Current ingest file name: {self.ing_file_name}')
        print('Possible extentions: .txt|.json|.xml|.dbconn')

        while True:
            new_name = input("New ingest file name (without extention, Exit to cancel): ")
            if new_name == 'Exit': 
                self.ing_file_name = curr_name
                return f'File name was not changed: {curr_name}'
            # check if any file with the name mentioned exists
            file_list = os.listdir(self.ing_file_path)
            for filedir in file_list:
                print(f'filedir: {filedir} splitted:', sep='')
                fn, ft = filedir.split('.')
                if (fn == new_name) and ft in ('txt', 'json', 'xml', 'dbconn'):
                    break
            else:
                print(f'No any file with new name and allowed extention in the directory {self.ing_file_path}')
        self.ing_file_name = new_name
        return f'New ingest file name: {new_name}'

    
    def from_text(self):

        text_file_path = os.path.join(self.ing_file_path, Constants.INGEST_FILE_NAME_DEFAULT+'.txt')
        # check if file does exist
        try:
            with open(text_file_path, encoding='UTF-8') as file:
                pass
        except:
            return f'File {text_file_path} does not exist.'

        objects_lines, obj_index, obj_type, skipped_lines = Ing.parse_objects_from_text(text_file_path)

        objects_dict_list, skipped_lines_2 = Ing.parse_objects_from_obj_lines(objects_lines, obj_index, obj_type)

        allowed_dict_list, skipped_lines_3 = Ing.allowed_obj_dicts_from_obj_dicts(objects_dict_list, message_types, message_ingest_prop)

        objects_list, skipped_lines_4 = Ing.parse_objects_from_dict_list(allowed_dict_list, message_types, message_ingest_to_objprop_map)

        skipped = ''.join(skipped_lines + skipped_lines_2 + skipped_lines_3 + skipped_lines_4)

        Ing.manage_objects(objects_list, skipped, text_file_path, Constants.ARCHIVE_FILE_PATH_DEFAULT)
        
        return 'Wait'


    def from_json(self):

        json_file_path = os.path.join(self.ing_file_path, Constants.INGEST_FILE_NAME_DEFAULT+'.json')
        # check if file does exist
        try:
            with open(json_file_path, encoding='UTF-8') as file:
                pass
        except:
            return f'File {json_file_path} does not exist.'
       
        print(f'From file: {json_file_path}')

        obj_dict_list, skipped_list = Ing.parse_obj_from_json(json_file_path)

        allowed_dict_list, skipped_lines_3 = Ing.allowed_obj_dicts_from_obj_dicts(obj_dict_list, message_types, message_ingest_prop)

        objects_list, skipped_lines_4 = Ing.parse_objects_from_dict_list(allowed_dict_list, message_types, message_ingest_to_objprop_map)

        skipped = ''.join(skipped_list + skipped_lines_3 + skipped_lines_4)

        Ing.manage_objects(objects_list, skipped, json_file_path, Constants.ARCHIVE_FILE_PATH_DEFAULT)

        return 'Wait'


    def from_xml(self):

        xml_file_path = os.path.join(self.ing_file_path, Constants.INGEST_FILE_NAME_DEFAULT+'.xml')
        # check if file does exist
        try:
            with open(xml_file_path, encoding='UTF-8') as file:
                pass
        except:
            return f'File {xml_file_path} does not exist.'
       
        print(f'From file: {xml_file_path}')

        obj_dict_list, skipped_list = Ing.parse_obj_from_xml(xml_file_path)

        allowed_dict_list, skipped_lines_3 = Ing.allowed_obj_dicts_from_obj_dicts(obj_dict_list, message_types, message_ingest_prop)

        objects_list, skipped_lines_4 = Ing.parse_objects_from_dict_list(allowed_dict_list, message_types, message_ingest_to_objprop_map)

        skipped = ''.join(skipped_list + skipped_lines_3 + skipped_lines_4)

        Ing.manage_objects(objects_list, skipped, xml_file_path, Constants.ARCHIVE_FILE_PATH_DEFAULT)

        return 'Wait'



#### statistics making - reading/showing

def show_stats():

    fwords = Constants.FILE_STATS_WORDCOUNT
    fletters = Constants.FILE_STATS_SYMBCOUNT

    print(f'words statistics is here:')
    try:
        with open(fwords, 'r', encoding='UTF-8') as wfile:
            wreader = csv.reader(wfile, delimiter='-')
            for line in wreader:
                print(line)
    except:
        print('No word stats file, sorry.')

    print(f'letters statistics is here:')
    try:
        with open(fletters, 'r', encoding='UTF-8') as lfile:
            lreader = csv.DictReader(lfile)
            for row in lreader:
                print(row)
    except:
        print('No letters stats file, sorry.')

    return 'Wait'


def make_stats(mode='file'):

    fwords = Constants.FILE_STATS_WORDCOUNT
    fletters = Constants.FILE_STATS_SYMBCOUNT

    if mode == 'file':

        fdata = Constants.FILE_PATH
        txt = ST.get_text_from_feed_data(fdata)

    elif mode == 'db':
        
        txt = db.get_text_for_stats()
    
    
    # make words statistics
    word_count = ST.word_count(txt.lower())
    # print(word_count)

    # make letters statistics
    d1, d2, d3 = ST.letters_count(txt)

    # make statistics csv files
    ST.write_stat_wordcount(word_count, fwords)   
    ST.write_stat_lettercount(d1, d2, fletters)


###  Menu definitions

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
                 obj := Ingest(ingest_file_path=Constants.INGEST_FILE_PATH_DEFAULT,
                                ingest_file_name=Constants.INGEST_FILE_NAME_DEFAULT, 
                                output_file_path=Constants.FILE_PATH, 
                                arch_path=Constants.ARCHIVE_FILE_PATH_DEFAULT)
                ),
    '1': ('Choose file to read',   obj.change_source_file),
    '2': ('Ingest from text file', obj.from_text),
    '3': ('Ingest from JSON',      obj.from_json),
    '4': ('Ingest from XML',       obj.from_xml),
    '0': ('Exit', lambda: 'Exit')
}

MENU = {
    '__init__': ('init object', None),    
    '1': ('Make News message',        News_message().make),
    '2': ('Make Private Add message', Private_ad_message().make),
    '3': ('Make_Book_message',        Book_message().make),
    '4': ('Enter messages from file', U.Menu(MENU_INGEST, f'INGEST MENU --------------\nCurrent ingest file: {Constants.INGEST_FILE_PATH_DEFAULT}').run),
    '5': ('Show all the messages',    U.Menu(MENU_SHOW_ALL, 'SHOW FILE MENU --------------').run),
    '6': ('Show stats', show_stats),
    '0': ('Exit programm', lambda: 'Exit')
}


if __name__ == '__main__':

    # create file if not exists
    try:
        with open(Constants.FILE_PATH, 'r', encoding='UTF-8') as file:
            pass
    except FileNotFoundError:
        with open(Constants.FILE_PATH, 'w', encoding='UTF-8') as file:
            pass

    db = DB.DB(Constants.DB_FILE_PATH)
    
    # run app - main menu
    
    menu_res = U.Menu(MENU, 'Main menu').run()
    
    print(menu_res)

    db.dbclose()
