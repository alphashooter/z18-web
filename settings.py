from sqlite3 import connect, Row


secret = '7zS6PLhQdr'
db = connect('db.sqlite3', check_same_thread=False)
db.row_factory = Row
