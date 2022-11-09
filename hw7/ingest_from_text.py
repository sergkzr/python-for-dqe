
import string as st
import datetime as dt
import os



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


def manage_files(source_file_path, arch_path, obj_list, skipped):

    dirname = os.path.dirname(source_file_path)
    basename = os.path.basename(source_file_path)
    name, ext = os.path.splitext(basename)
    
    dtnowstr = dt.datetime.now().strftime("%Y%m%d-%H-%M-%S")
    
    new_file_name = ''.join([name, '_arc', dtnowstr, ext])
    new_file_path = os.path.join(arch_path, new_file_name)
    
    # copy source file to archive
    
    with open(source_file_path) as rfile:
        text = rfile.read()

    with open(new_file_path, 'w') as wfile:
        wfile.write(text)

    # save skipped lines to archive file

    arch_err_file_name = ''.join([name, '_err', dtnowstr, ext])
    arch_err_file_path = os.path.join(arch_path, arch_err_file_name)
    
    with open(arch_err_file_path, 'w') as skipped_file:
        skipped_file.write(skipped)

    # save objects to db

    for ob in obj_list:
        obj_str = ob.put_message()
    
    # save ingested objects to archive

    arch_obj_file_name = ''.join([name, '_obj', dtnowstr, ext])
    arch_obj_file_path = os.path.join(arch_path, arch_obj_file_name)
    
    with open(arch_obj_file_path, 'w') as obj_file:
        for ob in obj_list:
            obj_str = ob.make_obj_string() 
            obj_file.write(obj_str)          

    # delete source ingest file

    os.remove(source_file_path)


    return source_file_path, new_file_path, arch_err_file_path, arch_obj_file_path




