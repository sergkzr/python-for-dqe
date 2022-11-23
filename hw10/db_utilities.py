# utilities for database
# pyodbc + sqlite3 according to hw specification

import pyodbc

FILE_DB = './data/feed_data.db'

qr_create_message_index = """
    CREATE TABLE IF NOT EXISTS msg_index (
      id integer PRIMARY KEY AUTOINCREMENT,
      timecreated datetime,
      msgtype varchar(30),
      msgref integer
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
      expiration_date nvarchar(10)
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
        self.cnxn = pyodbc.connect(f'Driver=SQLite3 ODBC Driver;Database={FILE_DB};Trusted_connection=yes')

        self.__dbinitialize()
        
        print(self.query_exec("SELECT * FROM PRAGMA_TABLE_INFO('msg_index')"))
        print(self.query_exec("SELECT * FROM PRAGMA_TABLE_INFO('news')"))
        print(self.query_exec("SELECT * FROM PRAGMA_TABLE_INFO('privatead')"))
        print(self.query_exec("SELECT * FROM PRAGMA_TABLE_INFO('book')"))
        
    def __dbinitialize(self):
        # if no tables in db - create them
        #     msg_news, msg_private_ad, msg_book
        #     msg_catalog

        self.query_exec(qr_create_message_index)
        self.query_exec(qr_create_news_table)
        self.query_exec(qr_create_privateadd_table)
        self.query_exec(qr_create_book_table)


    def query_exec(self, query, verbose=False, commit=True):

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

        if query.split()[0].strip().lower() == 'select':
            # only case where rowset is returned
            rows = cur.fetchall()
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


    def put_news(self, newsobj):
        pass

    def put_privatead(self, padobj):
        pass
    
    def put_book(self, bookobj):
        pass


    def put_objindex(self, o):
        pass

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
    
