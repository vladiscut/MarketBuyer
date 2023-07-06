import sqlite3

#ЗАКАЗЫ
def create_table_orders():
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS orders(order_id INTEGER PRIMARY KEY,user_name TEXT, user_id INTEGER, listids TEXT, date TEXT, adress TEXT, phone TEXT, shipment TEXT);""")
    cur.close()
    conn.commit()

def create_order(user_name, user_id, list_ids, order_date, adress, phone, shipment):
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    cur.execute("""INSERT into orders (user_name, user_id, listids, date, adress, phone, shipment) VALUES (?, ?, ?, ?, ?, ?, ?)""", [user_name, user_id, list_ids, order_date, adress, phone, shipment])
    cur.close()
    conn.commit()


def check_orders(user_id):
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    # print(user_id)
    orders = cur.execute("""select * from orders where user_id=?""", [user_id]).fetchall()
    cur.close()
    conn.commit()
    return orders
###########################################


#ИЗБРАННОЕ
def create_table_favorite():
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS favorite(user_id INTEGER, itemid INTEGER);""")
    cur.close()
    conn.commit()

def add_to_fav(user_id, itemid):
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    cur.execute("""INSERT into favorite (user_id, itemid) VALUES (?, ?)""", [user_id, itemid])
    cur.close()
    conn.commit()

def del_from_fav(user_id, itemid):
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    cur.execute("""delete from favorite where user_id=? and itemid=?""",  [user_id, itemid]).fetchall()
    cur.close()
    conn.commit()

def check_favTable(user_id):
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    # print(user_id)
    cart_data = cur.execute("""select * from favorite where user_id=?""", [user_id]).fetchall()
    cur.close()
    conn.commit()
    return cart_data
###########################################

#ПОЛЬЗОВАТЕЛИ
def create_table_user():
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(user_id INTEGER UNIQUE, name TEXT);""")
    cur.close()
    conn.commit()

def create_user(user_id,user_first_name):
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    cur.execute("""INSERT OR IGNORE into users (user_id, name) VALUES (?, ?)""", [user_id, user_first_name])
    cur.close()
    conn.commit()
######################################

#КОРЗИНА
def create_table_cart():
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS cart(user_id INTEGER, itemid INTEGER, weight REAL, sumprice REAL);""")
    cur.close()
    conn.commit()

def check_cartTable(user_id):
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    # print(user_id)
    cart_data = cur.execute("""select * from cart where user_id=?""", [user_id]).fetchall()
    cur.close()
    conn.commit()
    return cart_data


def add_to_cart(user_id, itemid, weight, sumprice):
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    cur.execute("""INSERT into cart (user_id, itemid, weight, sumprice) VALUES (?, ?, ?, ?)""", [user_id, itemid, weight, sumprice])
    cur.close()
    conn.commit()

def clean_cart_product(user_id, itemid):
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    cur.execute("""delete from cart where user_id=? and itemid=?""",  [user_id, itemid]).fetchall()
    cur.close()
    conn.commit()

def clean_cart_db(user_id):
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    cur.execute("""delete from cart where user_id=?""",  [user_id]).fetchall()
    cur.close()
    conn.commit()

##########################################################