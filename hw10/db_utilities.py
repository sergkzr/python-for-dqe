# utilities for database
# pyodbc + sqlite3 according to hw specification

import pyodbc

FILE_DB = './data/feed_data.db'

qr_create_message_index = """
    CREATE TABLE IF NOT EXISTS msg_index (
      id integer PRIMARY KEY AUTOINCREMENT,
      timecreated datetime NOT NULL,
      msgtype varchar(30) NOT NULL,
      msgref integer NOT NULL
    );
"""
    
qr_create_news_table = """
    CREATE TABLE IF NOT EXISTS news (
      id integer PRIMARY KEY AUTOINCREMENT,
      message nvarchar(4098),
      city nvarchar(30)
    );
"""

qr_create_privateadd_table = """
    CREATE TABLE IF NOT EXISTS privatead (
      id integer PRIMARY KEY AUTOINCREMENT,
      message nvarchar(30),
      expiration_date nvarchar(10),
      expire_days nvarchar(30)
    );
"""

qr_create_book_table = """
    CREATE TABLE IF NOT EXISTS book (
      id integer PRIMARY KEY AUTOINCREMENT,
      title nvarchar(128),
      isbn nvarchar(14),
      publish_year nvarchar(4)
    );
"""


class DB:
    def __init__(self, db_file_path):

        print('Started working with DB.')
        print(f'DB file: {FILE_DB}')

        # set connection, create db file in case it is absent
        self.cnxn = pyodbc.connect(f'Driver=SQLite3 ODBC Driver;Database={FILE_DB};Trusted_connection=yes')

        # conditioanelly initialize DB: create tables needed if there are no tables in the DB
        self.__dbinitialize()
        
        # show the results of tables creation
        print(self.query_exec("SELECT * FROM PRAGMA_TABLE_INFO('msg_index')"))
        print(self.query_exec("SELECT * FROM PRAGMA_TABLE_INFO('news')"))
        print(self.query_exec("SELECT * FROM PRAGMA_TABLE_INFO('privatead')"))
        print(self.query_exec("SELECT * FROM PRAGMA_TABLE_INFO('book')"))
        
    def __dbinitialize(self):
        # if no tables in db - create them
        #     msg_news, msg_private_ad, msg_book - for message types
        #     msg_catalog - for index of messages

        self.query_exec(qr_create_message_index)
        self.query_exec(qr_create_news_table)
        self.query_exec(qr_create_privateadd_table)
        self.query_exec(qr_create_book_table)


    def query_exec(self, query, verbose=False, commit=True):
        """
        Returns:
           inserted rowid in one row list (local for corresponding table) in case INSERT statement was executed
           resultset (list of rows) in case SELECT statemnt was executed
           empty list in any other case
           AND
           rowcount: number of rows affected by the query
        """

        cur = self.cnxn.cursor()

        try:
            cur.execute(query)

        except Exception as e:
            print(f'Query was not executed due to errors in it:\n{query}')
            print(f'Error messages: \n{e}')
            cur.close() 
            return [], -1 
        
        rowcount = cur.rowcount
        messages = cur.messages

        # print(f'Successfuly, {rowcount} rows affected.\nMessages:\n{messages}')

        if (verb := query.split()[0].strip().lower()) == 'select':
            # only case where rowset is returned
            rows = cur.fetchall()
        elif verb == 'insert':
            # works as needed when one row inserted - we use it for this case only
            # in case multiple rows inserted - probably returns the row id for the last insrted row
            rows = cur.execute('select last_insert_rowid()').fetchone()
        else:
            rows = []
    
        if commit:
            self.cnxn.commit()

        cur.close() 

        if verbose:
            print(f'Query: {query}')
            print(f'Rows affected: {rowcount}')
            print(f'Result: {rows}')
            print(f'Messages from ODBC driver:\n{messages}')

        return rows, rowcount


    def dbclose(self):
        self.cnxn.close()
        print(f'Finished working with DB: {FILE_DB}')

    def dbcommit(self):
        self.cnxn.commit()

    def dbrollback(self):
        self.cnxn.rollback()


    def get_news(self, ind_id):
        
        get_news_sql = f"""
           SELECT i.id, i.timecreated, i.msgtype, i.msgref, n.message, n.city
           FROM msg_index i JOIN news n ON i.msgref = n.id
           WHERE i.id = {ind_id}
        """

        rows, rc = self.query_exec(get_news_sql, commit=False)
        if rc != 1:
            return '{}', None, -1  # empty json string, time, requested ind_id

        print(rc)
        print(rows)

        # un-pack object properties from object db row
        ind_id_, news_timecreated, msgtype, msgref, news_msg, news_city= rows[0]

        if msgtype != 'News':
            return f'Tried to get "News" object from DB, ind_id: {ind_id} but read object of {msgtype} type.', None, -1

        # make obj news dictionary
        # we loss creation date currently, in the news object dictionary

        return (
            {
            '__ObjectType': 'News',
            'Published': news_timecreated,
            'Message': news_msg,
            'City': news_city
            },
            news_timecreated,
            ind_id
        )


    def get_privatead(self, ind_id):

        return (
            {},
            None,
            -1     
        )
        

    
    def get_book(self, indid):
      
        return (
            {},
            None,
            -1     
        )

    
    def put_news(self, newsobj):

        objtype = 'News'
        
        news_insert_sql = f"""INSERT INTO news (message, city) VALUES("{newsobj.msg}", "{newsobj.city}")"""

        id = self.put_obj_message(news_insert_sql, verbose=False, commit=False)
        
        if id == -1:
            # previouse insert was not successfull
            self.dbrollback()
            return -1  
        
        # previouse insert was successfull
        # if new row / new message successfully inserted - add row to msg_index

        ind_id = self.put_obj_index(objtype, id, newsobj.published, commit=False)
        
        if ind_id == -1:
            # not able to write to index 
            self.dbrollback()
            return -1 
            
        self.dbcommit()

        return ind_id 


    def put_privatead(self, privateadobj):
        
        return -1

    
    def put_book(self, bookobj):
        
        return -1


    def put_obj_message(self, obj_insert_sql, verbose=False, commit=False):
      
        # insert statement - returns (last_row_inserted_id as list, returned_messages as list)
        # first returned result can be -1 for notsuccessfull insert

        last_row_inserted, rmess = self.query_exec(obj_insert_sql, verbose=verbose, commit=commit)
        id = last_row_inserted[0] if last_row_inserted else -1
        
        return id 


    def put_obj_index(self, objtype, objpk, published, verbose=False, commit=False):

        sql = f'INSERT INTO msg_index (timecreated, msgtype, msgref) VALUES("{published}", "{objtype}", "{objpk}")'
        lrow_inserted, _ = self.query_exec(sql, verbose=verbose, commit=commit)

        ind_id = lrow_inserted[0] if lrow_inserted else -1
        print(f'Index inserted: {ind_id}')

        return ind_id


    # def get_obj_byind(self, objtype, objind):
    #     """
    #     Returns: objref, errmessage: (obj, '') | (None, 'Error message')
    #     """
    #     rows, _ = self.query_exec(f'select * from msg_index where id={objind}')
    #     #          
    #     if len(rows) != 1:
    #         # error reading the index row
    #         return None, f'Error reading object through index {objtype=}, {objind=}'

    #     if (msgtype := rows[0].msgtype) != objtype:
    #         # error not the same object type
    #         return None, f'Mesage type read {msgtype} is not the message type requested: {objtype}'

    #     obj = None
    #     errmessage = 'err message'

    #     # . . .
    #     # id timecreated msgtype msgref       
    #     #  try to read object thr

    #     if objtype == 'News':
    #         tablename = ''
    #     elif objtype == 'Private Ad':
    #         tablename = ''
    #     elif objtype == 'Book':
    #         tablename = ''
    #     else:
    #         return None, f'Not existed objtype: {objtype}'

    #     rows, _ = self.query_exec(f'select * from {tablename} where id={rows[0].msgref}')

    #     # one row expected         
    #     if len(rows) != 1:
    #         return None, f'Error reading object from table{tablename}.'

    #     # exactly one row read, get object properties
    #     row = rows[0]
    #     id = row.id
    #     msg = row.msg
    #     city = row.city

    #     # make object to be returned
    #     # depends on object type ...
    #     # new control dictionary ??


    #     obj = News(msg, city)  ###  NOT POSSIBLE _ NAME NOT KNOWN !!!!!!!!!!!!!!!!!!!!!!!

    #     return obj, errmessage 


    def get_text_for_stats(self):

        # extract only fields for text statistics: message, City, Title, isbn?
        txt = 'text from db \nto make word and letter statistics'

        return txt


if __name__ == '__main__':

    db = DB(FILE_DB)

    print('Here is code to work with open db...')

    rows, rc = db.query_exec('insert into book (title, isbn, publish_year) values("Ititle of the first book published", "13579246801234", "2033")', verbose=True)
    
    rows, rc = db.query_exec('SELECT * FROM book', verbose=True)
    
    rows, rc = db.query_exec('delete from book', verbose=True)
    
    rows, rc = db.query_exec('SELECT * FROM book', verbose=True)
    
    res, rc = db.query_exec("SELECT name FROM sqlite_master", verbose=True)
    
    res, rc = db.query_exec("SELECT name FROM notable", verbose=True)

    db.dbclose()
    
