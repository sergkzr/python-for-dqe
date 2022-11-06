
import string as st
import datetime as dt

# FILE = 'data/for_ingest/for_ingest.txt'

# class Constants:

#     FILE_PATH = './data/feed_data'   # like internal DB file path
#     OBJECTS_PER_SCREEN = 3

#     INGEST_FILE_PATH_DEFAULT = './data/for_ingest'
#     INGEST_FILE_NAME_DEFAULT = 'for_ingest_2.txt'

#     ARCHIVE_FILE_PATH_DEFAULT = './data/archive'
#     ARCHIVE_ERRFILE_DEFAULT = 'ingest_err'
#     ARCHIVE_SUCCFILE_DEFAULT = 'ingest_succ'


# class Empty_object:
#     def __init__(self):
#         self.message = 'Empty object'

#     def show(self):
#         print(self.message)

# empty_object = Empty_object()



# def check_date(date_str):

#     date_valid = True

#     # check date
#     try:
#         y, m, d = date_str.split('-')
#     except:
#         return False
    
#     y = int(y)
#     m = int(m)
#     d = int(d)

#     if not ((y >= 1945) and (y <= 2030)):
#         date_valid = False
#     elif not ((m >= 1) and (m <= 12)):
#         date_valid = False
#     elif not ( (d >= 1) and (d <= (31 if m in [1, 3, 5, 7, 8, 10, 12] else (30 if m in [4, 6, 9, 11] else 29))) ):
#         date_valid = False

#     return date_valid


# def check_year(year_str):
    
#     year_valid = True
    
#     # check year
#     try:
#         y = int(year_str)
#     except:
#         return False

#     if not ((y >= 1900) and (y <= 2030)):
#         year_valid = False

#     return year_valid

# def check_message(message_str_list):
#     message_valid = True
#     # check message
#     return message_valid

# def chek_ISBN(isbn, year=2008):

#     isbn_valid = True

#     # check isbn
#     if not isbn.isdigit():
#         return False

#     # 13 digits after 2007
#     # 10 digits before year 2008
#     if not ((year >= 2008) and (len(isbn) == 13)):
#         isbn_valid = False
#     elif not ((year < 2008) and (len(isbn) == 10)):
#         isbn_valid = False
    
#     return isbn_valid


# class Message:
#     def __init__(self, msg='NoMessage'):
#         self.msg = msg
#         self.published = '0000-00-00'

#     def put_message(self):

#         self.published = dt.datetime.utcnow()
       
#         obj_str = self.make_obj_string()
        
#         with open(Constants.FILE_PATH, 'a') as file:
#             file.write(obj_str)

#         return obj_str

#     def show(self):
#         print(self.make_obj_string())
       

# class News_message(Message):
#     def __init__(self, msg='NoMessage', city='NoCity'):
#         super().__init__(msg)
#         self.city = city
        
#     def make(self):
#         # input data check could be added
#         self.msg = input('News message: ')
#         self.city = input('City: ')

#         obj_str = self.put_message()
#         print(obj_str)
        
#         return 'Wait'

#     def make_obj_string(self):
#         return (
#         f"<----------\n"
#         f"News, {self.published}\n"
#         f"Text: {self.msg}\n"
#         f"City: {self.city}\n"
#         f"---------->")


# class Private_ad_message(Message):

#     def __init__(self, ad='NoAd', expiration_date='NoDate'):
#         super().__init__(ad)
#         self.expiration_date = expiration_date

#     def __expire_days(self):

#         now_date = dt.date.today()

#         sy, sm, sd = self.expiration_date.split('-')
#         y = int(sy)
#         m = int(sm)
#         d = int(sd)
#         try:
#             exp_date = dt.date(y, m, d)
#         except:
#             exp_date = now_date
#         exp_days = exp_date - now_date

#         return f'{exp_days}'

#     def make(self):
#         # input data check could be added
#         self.msg = input('New Private Ad: ')
#         self.expiration_date = input('Expiration_date: ')

#         obj_str = self.put_message()
#         print(obj_str)

#         return 'Wait'

#     def make_obj_string(self):
#         return (
#         f"<----------\n"
#         f"Private Ad, {self.published}\n"
#         f"Text: {self.msg}\n"
#         f"Expiration Date: {self.expiration_date}\n"
#         f"Days Left: {self.__expire_days()}\n"
#         f"---------->")


# class Book_message(Message):

#     def __init__(self, book_name='NoBookName', isbn='NoISBN', publish_year='NoYear'):
#         super().__init__(book_name)
#         self.isbn = isbn
#         self.publish_year = publish_year

#     def make(self):
#         # input data check could be added
#         self.msg = input('New Book title: ')
#         self.isbn = input('ISBN: ')    
#         self.publish_year = input('Publish_year: ')   

#         obj_str = self.put_message()
#         print(obj_str)

#         return 'Wait'

#     def make_obj_string(self):
#         return (
#         f"<----------\n"
#         f"Book, {self.published}\n"
#         f"Title: {self.msg}\n"
#         f"ISBN: {self.isbn}\n"
#         f"Publish_Year: {self.publish_year}\n"
#         f"---------->")

# ## MESSAGE OBJECTS METADATA ####################################

# message_types = {
#     'News': News_message, 
#     'Private Ad': Private_ad_message, 
#     'Book': Book_message
# }

# # Ingest 'Property': 1 one line, 2 - multy line

# news_ingest_prop =  {
#     'Message': 2, 
#     'City': 1
# } 
# ad_ingest_prop =  {
#     'Message': 2, 
#     'Expiration Date': 1
# }
# book_ingest_prop = {
#     'Title': 2, 
#     'Isbn': 1, 
#     'Publish Year': 1
# }

# message_ingest_prop = {
#     'News':       news_ingest_prop,
#     'Private Ad': ad_ingest_prop,
#     'Book':       book_ingest_prop
# }

# # map ingest property name to object property name

# news_ingest_to_objprop_map = {
#     'Message': 'msg', 
#     'City': 'city'
# }  
# ad_ingest_to_objprop_map = {
#     'Message': 'ad', 
#     'Expiration Date': 'expiration_date'
# }
# book_ingest_to_objprop_map = {
#     'Title': 'book_name', 
#     'Isbn': 'isbn', 
#     'Publish Year': 'publish_year'
# }

# message_ingest_to_objprop_map = {
#     'News':       news_ingest_to_objprop_map,
#     'Private Ad': ad_ingest_to_objprop_map,
#     'Book':       book_ingest_to_objprop_map
# }

# # messages_init = {'News':       News_message,
# #                  'Private Ad': Private_ad_message,
# #                  'Book':       Book_message}

## ######################################################

def isobjtypename(s:str)->bool:
    # object type name can contain only alphabet symbols and digits and spaces
    for c in s:
        if c in st.punctuation:
            return False
    return True

def parse_objects_from_text(ing_file):
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
       obj_type_list      : list of object types as extracted from xtype line/ object header
       skipped_lines_list : list of skipped lines in the source text
    """

    error_result = ([], [], [], [])

    try:

        with open(ing_file, 'r') as file:
            lines = file.readlines()
        
        if not lines:
            # empty source file
            print(f'Empty file: {ing_file}')
            return error_result 

    except:

        # No file or invalid path
        print(f'Cannot-parse_objects_from_text: {ing_file}')
        return error_result

    objects_lines = []
    obj_index = []
    obj_type = [] 
    skipped_lines = []

    skip = True
    index = 0

    for i, line in enumerate(lines):
        # print(i, line, end='')
           
        if line.startswith('***') and len(line) > 3 and isobjtypename(line[3:]):

            obj_type_curr =  line[3:].strip().lower().title()

            objects_lines.append(line)
            obj_index.append(index)
            obj_type.append(obj_type_curr)

            index += 1 
            skip = False
                                
        elif skip:
            skipped_lines.append(line)

        else:  
            objects_lines.append(line)
            index += 1 
       
    return objects_lines, obj_index, obj_type, skipped_lines


def obj_lines_to_dict(object_lines, obj_type_val):

    # first row is object type name row
    # it should be followed by 0 or more object properties rows
    
    prop_dict = {'__ObjectType': obj_type_val}
    # res_error = {}
    
    # stop if object has no property lines
    if len(object_lines) == 1:
        # empty object 
        return prop_dict

    # parse object lines
    # expected format:
    # <prop_name> : <one or more lines of property value>
    
    skipped_list = []
    
    prop_name_list = []
    prop_value_list = []

    prop_name = '__Skipped'
    prop_value = []

    # iterate through object (property) lines, ignore first line
    
    for line in object_lines[1:]:

        if line.find(':') > 0:

            # save previouse property
            
            prop_name_list.append(prop_name)
            prop_value_list.append(prop_value)

            # start processing new property
            
            lp, lv = line.split(':', 1)
            prop_name = lp.strip().lower().title()
            prop_value = [lv]
            
        else :   # lines of object

            prop_value.append(line)


    # save last property
    prop_name_list.append(prop_name)
    prop_value_list.append(prop_value)

    #  make ingested object dictionary: {<prop>:<value, ...>}

    for key, value in zip(prop_name_list, prop_value_list):
        prop_dict |= {key: value}

    return prop_dict


def parse_objects_from_obj_lines(objects_lines, object_index_list, object_type_list):
    """
    -->> objects_dict_list, skipped_lines
    """
    
    objects_dict_list = []
    skipped_lines = []

    n_objects = len(object_index_list)
    
    for i, (obj_line_start, obj_type_val) in enumerate(zip(object_index_list, object_type_list)):
   
        if i == (n_objects - 1):       
            obj_line_end = len(objects_lines)     # last object
        else:
            obj_line_end = object_index_list[i+1]
            
        prop_dict = obj_lines_to_dict(objects_lines[obj_line_start:obj_line_end], obj_type_val)
     
        objects_dict_list.append(prop_dict)

        skipped_list = prop_dict.get('__Skipped', [])
        skipped_lines.extend(skipped_list)

    return  objects_dict_list, skipped_lines


def skip_object(obj_type_val: str, obj_dict: dict) -> list:
    """
    make list of lines from obj_dict
    obj_type_val: object type (value)
    obj_dict:     input object dictionary
    -->> list of object lines
    """
    skipped_lines = []
    
    obj_type_line = ''.join(['***', obj_type_val, '\n']) 
    skipped_lines.append(obj_type_line)

    # iterate through object dictionary

    for prop, value in obj_dict.items():

        if prop != '__ObjectType':
            
            skipped_lines.append(prop + ":" ) 
            skipped_lines.extend(value)

    return skipped_lines


def allowed_obj_dicts_from_obj_dicts(objects_dict_list, message_types, message_ingest_prop):
    """
      object dictionaries -> allowed object dictionaries, skipped lines for not allowed objects
      check object type value
      check if input object dict contains all the requested parameters for the given object type value
    """

    allowed_dict_list = []
    skipped_lines = []

    for obj_dict in objects_dict_list:

        obj_type_val = obj_dict.get('__ObjectType', '__NoObjectType')

        if obj_type_val not in message_types:
            
            # not allowed object to skipped lines
            skipped_lines.extend(skip_object(obj_type_val, obj_dict))
            continue

        # allowed obj type
        # check obj allowed object properties, according to object type

        skipped =  obj_dict.get('__Skipped', [])
        if skipped:
            #  skip all the object
            skipped_lines.extend(skip_object(obj_type_val, obj_dict))
            continue
        
        object_dict = { k:v for k, v in obj_dict.items() if k not in ['__Skipped', '__ObjectType'] }
            
        prop_in, prop_out = {}, {}
        
        for prop, v in object_dict.items():

            if prop in message_ingest_prop[obj_type_val]:
                prop_in |= {prop: v}
            else:
                # no such property in object metadata
                prop_out |= {prop: v}

        if len(prop_in) != len(message_ingest_prop[obj_type_val]):
            # number of properties is not equal to number of properties in metadata, skip entire object
            skipped_lines.extend(skip_object(obj_type_val, obj_dict))
            continue

        if prop_out:
            # there are properties not from allowed list, skip entire object
            skipped_lines.extend(skip_object(obj_type_val, obj_dict))
            continue

        # there are all the needed properties, process them

        for prop, val in prop_in.items():

            multyline_flag = message_ingest_prop[obj_type_val][prop]   # 1 OR 2

            if (len(val) > 1) and multyline_flag == 1:
                prop_in[prop] = val[0] 
                skipped_lines.extend(val[1:])
        
        allowed_dict_list.append(obj_dict)     

    return allowed_dict_list, skipped_lines


def parse_objects_from_dict_list(objects_dict_list, message_types, message_ingest_to_objprop_map):
    """
    Assumption: all the objects on input are of appropriate (allowed) type and have all the needed properties
    -->> allowed objects_list = [<obj> | None, ...], skipped_lines
    """
    
    objects_list = []
    skipped_lines = []

    for object_dict in objects_dict_list:

        # process allowed objects                   
        # for each object process object properties one by one
        # in case property checks are not successfull (if any) - skip entier object

        obj_type_val = object_dict.get('__ObjectType', 'NoObjectType')
        skipped = object_dict.get('__Skipped', [])

        obj_dict = { message_ingest_to_objprop_map[obj_type_val][k]: ''.join(v)[:-1] for k, v in object_dict.items() if k not in ['__ObjectType', '__Skipped'] }
        
        res_obj = message_types[obj_type_val](**obj_dict)
        
        if res_obj:
            objects_list.append(res_obj)
        else:
            objects_list.append(None)
            skip_object(obj_type_val, object_dict) 
            skipped_lines.extend(skip_object(obj_type_val, object_dict)) 

    return objects_list, skipped_lines



# if __name__ == '__main__':


#     objects_lines, obj_index, obj_type, skipped_lines = parse_objects_from_text(FILE)

#     print(f'File {FILE} parsed:')
#     print(f'******Objectslines:\n{objects_lines}')
#     print(f'******Objects index:\n{obj_index}') 
#     print(f'******Objects type:\n{obj_type}')   
#     print(f'******Skipped lines:\n{skipped_lines}')


#     objects_dict_list, skipped_lines_2 = parse_objects_from_obj_lines(objects_lines, obj_index, obj_type)

#     print(f'Objects dict list:')
#     print(f'******Objects dicts:\n{objects_dict_list}')
#     print(f'******Skipped lines:\n{skipped_lines_2}')


#     allowed_dict_list, skipped_lines_3 = allowed_obj_dicts_from_obj_dicts(objects_dict_list, message_types, message_ingest_prop)

#     print(f'Allowed objects dict list:')
#     print(f'******Objects dicts:\n{allowed_dict_list}')
#     print(f'******Skipped lines:\n{skipped_lines_3}')

    
#     objects_list, skipped_lines_4 = parse_objects_from_dict_list(allowed_dict_list, message_types, message_ingest_to_objprop_map)

#     print(f'Objects list:')
#     for i, obj in enumerate(objects_list):
#         print(f'{i:02}', sep='')
#         if obj is None:
#             print('No object')
#         else:
#             obj.show()
#     print(f'******Skipped lines:\n{skipped_lines_4}')

#     skipped = ''.join(skipped_lines + skipped_lines_2 + skipped_lines_3 + skipped_lines_4)
#     print()
#     print(f"All the skipped lines:\n{skipped}")
