import sqlite3


def _db_conn():
    return sqlite3.connect('db/magicbookshelf.db')


def _execute(query, bindings=[], conn=None, rows=None):
    if not conn:
        conn = _db_conn()
    with conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        return (cursor.execute(query, bindings).fetchone(), cursor.rowcount)

def create_book(title, author, uid, conn=None):
    return {'title': title,
            'author': author,
            'uid': uid}

def store_book(book, conn=None):
    query = ("INSERT INTO Book (title, author, uid) "
             "values (:title, :author, :uid);")
    _execute(query, book, conn=conn)

def retrieve_book_by_uid(uid, conn=None):
    query = "SELECT * FROM Book WHERE uid=:uid"
    (book, _) = _execute(query, [uid], conn=conn)
    if book:
        return dict(book)
    else:
        return None

def checkin_book(book, conn=None):
    query = "UPDATE Book SET checkedin=1 WHERE uid=:uid"
    _execute(query, [book['uid']], conn=conn)

def checkout_book(book, conn=None):
    uid = book['uid']
    query = "UPDATE Book SET checkedin=0 WHERE uid=:uid"
    _execute(query, [uid], conn=conn)
