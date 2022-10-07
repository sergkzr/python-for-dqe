# 1.News – text and city as input. Date is calculated during publishing.
#
# 2.Privat ad – text and expiration date as input. Day left is calculated during publishing.
#
# 3.Your unique one with unique publish rules: text and 


import datetime as dt

class Message:

    def __init__(self, msg):
        self.msg = msg


class News_message(Message):

    def __init__(self, msg, city):
        Message.__init__(self, msg)
        self.city = city

    def make_feed_string(self):
        return f"""
News --------------------
text: {self.msg}
city: {self.city}
------------------------- 
"""


class Private_ad__message(Message):

    def __init__(self, ad, expiration_date):
        Message.__init__(self, ad)
        self.expiration_date = expiration_date

    def __expire_days(self):
        return str(5)

    def make_feed_string(self):
        return f"""
Private Ad --------------------
text: {self.msg}
city: {self.expiration_date}
days left: {self.__expire_days()}
-------------------------------
"""


class Book__message(Message):

    def __init__(self, book_name, isbn, publish_year):
        Message.__init__(self, book_name)
        self.isbn = isbn
        self.publish_year = publish_year

    def make_feed_string(self):
        return f"""
Book_anounce --------------------
Title: {self.msg}
ISBN: {self.isbn}
publish_year: {self.publish_year}
------------------------- 
"""



if __name__ == '__main__':

    news0 = News_message('We are waiting for Pope', 'Napoly')
    print(news0.make_feed_string())

    ad0 = Private_ad__message('Be ready to see new slippers in owr stories!', '2022-12-25')
    print(ad0.make_feed_string())
    
    book0 = Book__message('PySpark and Big Data', 'ISBN: 23456123', '2010')
    print(book0.make_feed_string())
    
