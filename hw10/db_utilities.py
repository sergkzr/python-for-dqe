# utilities for database
# pyodbc + sqlite3 according to hw specification

import pyodbc
import datetime as dt
from time import sleep

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
      text nvarchar(4096),
      city nvarchar(30)
    );
"""

qr_create_privateadd_table = """
    CREATE TABLE IF NOT EXISTS privatead (
      id integer PRIMARY KEY AUTOINCREMENT,
      text nvarchar(4096),
      expiration_date nvarchar(10)
    );
"""

qr_create_book_table = """
    CREATE TABLE IF NOT EXISTS book (
      id integer PRIMARY KEY AUTOINCREMENT,
      title nvarchar(256),
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
        # sqlite3 SPECIFIC
        print('SQLite version:', self.query_exec('SELECT sqlite_version()')[0][0][0])
        print('Through pyodbc version:', pyodbc.version)
        # print(self.query_exec("SELECT sql FROM sqlite_master WHERE name='msg_index'")[0][0][0])
        # print(self.query_exec("SELECT sql FROM sqlite_master WHERE name='news'")[0][0][0])
        # print(self.query_exec("SELECT sql FROM sqlite_master WHERE name='privatead'")[0][0][0])
        # print(self.query_exec("SELECT sql FROM sqlite_master WHERE name='book'")[0][0][0])
        print('Messages in DB:')
        print(self.query_exec("SELECT msgtype, COUNT(1) FROM msg_index GROUP BY msgtype")[0])
        _ = input('Press ENTER key to continue.')
        # sleep(4)
        
    def __dbinitialize(self):
        # if no tables in db - create them
        #     msg_news, msg_private_ad, msg_book - for message types
        #     msg_catalog - for index of messages

        self.query_exec(qr_create_message_index)
        self.query_exec(qr_create_news_table)
        self.query_exec(qr_create_privateadd_table)
        self.query_exec(qr_create_book_table)

 
    def dbcommit(self):
        self.cnxn.commit()

    def dbrollback(self):
        self.cnxn.rollback()

    def dbclose(self):
        self.cnxn.close()
        print(f'Finished working with DB: {FILE_DB}')


    def query_exec(self, query, verbose=False, commit=True):
        """
        Returns:
           inserted rowid in one row list (local for corresponding table) in case INSERT statement was executed
           resultset (list of rows) in case SELECT statement was executed
           empty list in any other case
           AND
           rowcount: number of rows affected by the query
        """

        verb = query.split()[0].strip().lower()
        
        cur = self.cnxn.cursor()

        try:
            cur.execute(query)
            rowcount = cur.rowcount
            messages = cur.messages

        except Exception as e:
            print(f'Query was not executed due to errors in it:\n{query}')
            print(f'Error messages: \n{e}')
            cur.close() 
            return [], -1 
        
        # print(f'Successfuly, {rowcount} rows affected.\nMessages:\n{messages}')

        if verb == 'select':

            # only case where rowset is returned
            # bad practice here in case of large dataset fetched, but ...
            rows = cur.fetchall()
            rowcount = len(rows)
        
        elif verb == 'insert':
        
            # works as needed when one row inserted - we use it for this case only
            # in case multiple rows inserted - probably returns the row id for the last inserted row
            # sqlite3 SPECIFIC
            rows = cur.execute('SELECT last_insert_rowid()').fetchone()
            # leave rowcount from the insert sql statement
            
        else:
            rows = []
            # leave rowcount from previously executed sql statement
    
        if commit:
            self.cnxn.commit()

        cur.close() 

        if verbose:
            print(f'Query: {query}')
            print(f'Rows affected: {rowcount}')
            print(f'Result: {rows}')
            print(f'Messages from ODBC driver:\n{messages}')

        return rows, rowcount


    def put_obj_message(self, obj_insert_sql, verbose=False, commit=False):
      
        # insert statement - returns last_row_inserted_id 
        # returned result can be -1 for notsuccessfull insert

        last_row_inserted, rmess = self.query_exec(obj_insert_sql, verbose=verbose, commit=commit)
        id = last_row_inserted[0] if last_row_inserted else -1
        
        return id 


    def put_obj_index(self, objtype, objpk, published, verbose=False, commit=False):

        sql = f'INSERT INTO msg_index (timecreated, msgtype, msgref) VALUES("{published}", "{objtype}", "{objpk}")'
        lrow_inserted, _ = self.query_exec(sql, verbose=verbose, commit=commit)

        ind_id = lrow_inserted[0] if lrow_inserted else -1
        # print(f'Index inserted: {ind_id}')

        return ind_id


    def get_news(self, ind_id):
        
        # exactly one row returned in case of successfull execution
        get_news_sql = f"""
           SELECT i.id, i.timecreated, i.msgtype, i.msgref, n.text, n.city
           FROM msg_index i JOIN news n ON i.msgref = n.id
           WHERE i.id = {ind_id}
        """

        rows, rc = self.query_exec(get_news_sql, commit=False, verbose=True)
        if rc != 1:
            return '{}', None, -1  # empty json string, time, requested ind_id

        # un-pack object properties from object db row
        ind_id_, news_timecreated, msgtype, msgref, news_text, news_city= rows[0]

        if msgtype != 'News':
            return f'Tried to get "News" object from DB, ind_id: {ind_id}/{ind_id_} but read object of {msgtype} type.', None, -1

        # make obj news dictionary
        # we loss creation date currently, in the news object dictionary

        return (
            {
            '__ObjectType': 'News',
            'Message': news_text,
            'City': news_city
            },
            news_timecreated,
            ind_id
        )


    def get_privatead(self, ind_id):

        # exactly one row returned in case of successfull execution
        get_news_sql = f"""
           SELECT i.id, i.timecreated, i.msgtype, i.msgref, a.text, a.expiration_date
           FROM msg_index i JOIN privatead a ON i.msgref = a.id
           WHERE i.id = {ind_id}
        """

        rows, rc = self.query_exec(get_news_sql, commit=False, verbose=True)
        if rc != 1:
            return '{}', None, -1  # empty json string, time, requested ind_id

        # un-pack object properties from object db row
        ind_id_, privad_timecreated, msgtype, msgref, ad_text, ad_expdate = rows[0]

        if msgtype != 'Private Ad':
            return f'Tried to get "Private Ad" object from DB, ind_id: {ind_id}/{ind_id_} but read object of {msgtype} type.', None, -1

        # make obj Private Ad dictionary
        # we loss creation date currently, in the news object dictionary

        return (
            {
            '__ObjectType': 'Private Ad',
            'Message': ad_text,
            'Expiration Date': ad_expdate
            },
            privad_timecreated,
            ind_id
        )

    
    def get_book(self, ind_id):

        # exactly one row returned in case of successfull execution
        get_news_sql = f"""
           SELECT i.id, i.timecreated, i.msgtype, i.msgref, b.title, b.isbn, b.publish_year
           FROM msg_index i JOIN book b ON i.msgref = b.id
           WHERE i.id = {ind_id}
        """

        rows, rc = self.query_exec(get_news_sql, commit=False, verbose=True)
        if rc != 1:
            return '{}', None, -1  # empty json string, time, requested ind_id

        # un-pack object properties from object db row
        ind_id_, book_timecreated, msgtype, msgref, book_title, book_isbn, book_publish_year = rows[0]

        if msgtype != 'Book':
            return f'Tried to get "Private Ad" object from DB, ind_id: {ind_id}/{ind_id_} but read object of {msgtype} type.', None, -1

        # make obj Book dictionary
        # we loss creation date currently, in the news object dictionary

        return (
            {
            '__ObjectType': 'Book',
            'Title': book_title,
            'ISBN': book_isbn,
            'Publish Year': book_publish_year
            },
            book_timecreated,
            ind_id
        )
      
    
    def put_news(self, newsobj):

        objtype = 'News'
        
        news_insert_sql = f"""INSERT INTO news (text, city) VALUES("{newsobj.msg}", "{newsobj.city}")"""

        id = self.put_obj_message(news_insert_sql, verbose=False, commit=False)
        
        if id == -1:
            # previouse insert was not successfull
            self.dbrollback()
            return -1  
        
        # previouse insert was successfull
        # add row to msg_index

        ind_id = self.put_obj_index(objtype, id, newsobj.published, commit=False)
        
        if ind_id == -1:
            # not able to write to index 
            self.dbrollback()
            return -1 
            
        self.dbcommit()
        return ind_id 


    def put_privatead(self, privateadobj):

        objtype = 'Private Ad'
                
        news_insert_sql = f"""INSERT INTO privatead (text, expiration_date) 
                              VALUES("{privateadobj.msg}", "{privateadobj.expiration_date}")"""

        id = self.put_obj_message(news_insert_sql, verbose=False, commit=False)
        
        if id == -1:
            # previouse insert was not successfull
            self.dbrollback()
            return -1  
        
        # previouse insert was successfull
        # add row to msg_index

        ind_id = self.put_obj_index(objtype, id, privateadobj.published, commit=False)
        
        if ind_id == -1:
            # not able to write to index 
            self.dbrollback()
            return -1 
            
        self.dbcommit()
        return ind_id 

    
    def put_book(self, bookobj):
    
        objtype = 'Book'
                
        book_insert_sql = f"""INSERT INTO book (title, isbn, publish_year) 
                              VALUES("{bookobj.msg}", "{bookobj.isbn}", "{bookobj.publish_year}")"""

        id = self.put_obj_message(book_insert_sql, verbose=False, commit=False)
        
        if id == -1:
            # previouse insert was not successfull
            self.dbrollback()
            return -1  
        
        # previouse insert was successfull
        # add row to msg_index

        ind_id = self.put_obj_index(objtype, id, bookobj.published, commit=False)
        
        if ind_id == -1:
            # not able to write to index 
            self.dbrollback()
            return -1 
            
        self.dbcommit()
        return ind_id 
        

    def get_text_for_stats(self):

        # extract only fields for text statistics: message, City, Title, isbn?
        # txt = 'text from db \nto make word and letter statistics'

        news_sql = 'SELECT text, city FROM news'
        privad_sql = 'SELECT text FROM privatead'
        book_sql = 'SELECT title FROM book'

        text = ''

        rows, rc = self.query_exec(news_sql, verbose=False, commit=False)
        for row in rows:
            text = '\n'.join([text, row.text, row.city])

        rows, rc = self.query_exec(privad_sql, verbose=False, commit=False)
        for row in rows:
            text = '\n'.join([text, row.text])

        rows, rc = self.query_exec(book_sql, verbose=False, commit=False)
        for row in rows:
            text = '\n'.join([text, row.title])

        return text[1:]


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
    
