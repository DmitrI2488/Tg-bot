from telebot import types
import sqlite3
import telebot
import os
import settings
import random
import requests
import json
import datetime


class Catalog:
    def __init__(self, name):
        self.name = name


class Product:
    def __init__(self, user_id):
        self.user_id = user_id
        self.product = None
        self.section = None
        self.price = None
        self.amount = None
        self.code = None
        self.name = None


class AddProduct:
    def __init__(self, section):
        self.section = section
        self.product = None
        self.price = None
        self.info = None
        self.name = None


class DownloadProduct:
    def __init__(self, name_section):
        self.name_section = name_section
        self.name_product = None


class ok:
    def __init__(self, code, chat_id, username, sum, u_id):
        self.code = code
        self.chat_id = chat_id
        self.username = username
        self.sum = sum
        self.u_id = u_id


class GiveBalance:
    def __init__(self, login):
        self.login = login
        self.user_id = None
        self.balance = None
        self.code = None


class Admin_sending_messages:
    def __init__(self, user_id):
        self.user_id = user_id
        self.text = None


class replenishment:
    def __init__(self, valute, username, sums, crypt, ids):
        self.username = username
        self.sum = sums
        self.i_pay = 0
        self.valute = valute
        self.code = random.randint(111, 999)
        self.crypt = crypt
        self.id = ids


# Menu catalog
def menu_catalog():
    conn = sqlite3.connect("base_ts.sqlite")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM catalog')
    row = cursor.fetchall()

    menu = types.InlineKeyboardMarkup(row_width=1)

    for i in row:
        menu.add(types.InlineKeyboardButton(text=f'{i[0]}', callback_data=f'{i[1]}'))

    menu.add(types.InlineKeyboardButton(text='Назад', callback_data='exit_to_menu'))

    cursor.close()
    conn.close()

    return menu


# Menu section
def menu_section(name_section):
    conn = sqlite3.connect("base_ts.sqlite")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM '{name_section}' ")
    row = cursor.fetchall()

    menu = types.InlineKeyboardMarkup(row_width=1)

    for i in row:
        menu.add(types.InlineKeyboardButton(text=f'{i[0]}', callback_data=f'{i[2]}'))

    menu.add(types.InlineKeyboardButton(text='Назад', callback_data='exit_to_menu'))

    cursor.close()
    conn.close()

    return menu


# Menu product
def menu_product(product, dict):
    conn = sqlite3.connect("base_ts.sqlite")
    cursor = conn.cursor()
    row = cursor.execute(f'SELECT * FROM section WHERE code = "{product}"').fetchone()
    section = row[1]
    code = row[2]
    info = row[3]
    row = cursor.execute(f'SELECT * FROM "{section}" WHERE price = "{code}"').fetchone()
    dict.section = section
    dict.product = product
    dict.price = row[1]
    dict.name = row[0]

    text = settings.text_purchase.format(
        name=row[0],
        info=info,
        price=row[1],
    )

    return text, dict


#   Admin menu - add_to_section_to_catalog
def add_section_to_catalog(name_section):
    # Connection
    conn = sqlite3.connect("base_ts.sqlite")
    cursor = conn.cursor()
    code = random.randint(11111, 99999)
    # Add
    cursor.execute(f"INSERT INTO catalog VALUES ('{name_section}', '{code}')")
    conn.commit()

    # Create table section
    conn.execute(f"CREATE TABLE '{code}' (name text, list text, price text, code text)")

    # Close connection
    cursor.close()
    conn.close()


# Admin menu - del_section_to_catalog
def del_section_to_catalog(name_section):
    # Connection
    conn = sqlite3.connect("base_ts.sqlite")
    cursor = conn.cursor()

    # Del
    cursor.execute(f"DELETE FROM catalog WHERE code = '{name_section}'")
    conn.commit()

    cursor.execute(f"DROP TABLE '{name_section}'")

    row = cursor.execute(f'SELECT * FROM section WHERE section = "{name_section}"').fetchall()

    for i in range(len(row)):
        cursor.execute(f'DROP TABLE "{row[i][2]}"')

        cursor.execute(f'DELETE FROM section WHERE code = "{row[i][2]}"')
        conn.commit()

    # Close connection
    cursor.close()
    conn.close()


# Admin menu - add_product_to_section
def add_product_to_section(name_product, price, name_section, info, name):
    # Connection
    conn = sqlite3.connect("base_ts.sqlite")
    cursor = conn.cursor()

    code = random.randint(11111, 99999)

    cursor.execute(f"INSERT INTO '{name_section}' VALUES ('{name_product}', '{price}', '{code}', '{name}')")
    conn.commit()

    cursor.execute(
        f"INSERT INTO 'section' VALUES ('{name_product}', '{name_section}', '{code}', '{info}', '{name}')")
    conn.commit()

    # Create table product
    cursor.execute(f"CREATE TABLE '{code}' (list text, code text)")

    # Close connection
    cursor.close()
    conn.close()


def create_pay(username, sum, valute, code, crypt, chat_id, user_id):
    conn = sqlite3.connect("base_ts.sqlite")
    cursor = conn.cursor()

    i_pays = 0
    status = 0
    username = f'@{username}'
    cursor.execute(
        f'INSERT INTO "replenishment" VALUES ("{username}", "{sum}", "{i_pays}", "{valute}", "{code}", "{crypt}", "{status}", "{chat_id}", "{user_id}")')
    conn.commit()

    cursor.close()
    conn.close()


def i_pay(code):
    conn = sqlite3.connect("base_ts.sqlite")
    cursor = conn.cursor()

    i_pays = 1

    cursor.execute(f'UPDATE replenishment SET i_pay = "{i_pays}" WHERE code = "{code}"')
    conn.commit()

    cursor.close()
    conn.close()


# Admin menu - del_product_to_section
def del_product_to_section(name_product, section):
    # Connection
    conn = sqlite3.connect("base_ts.sqlite")
    cursor = conn.cursor()

    # del
    product = cursor.execute(f'SELECT * FROM "{section}" WHERE list = "{name_product}"').fetchone()

    cursor.execute(f"DELETE FROM '{section}' WHERE name = '{name_product}'")
    conn.commit()

    # Close connection
    cursor.close()
    conn.close()


def download_product(name_file, product):
    conn = sqlite3.connect("base_ts.sqlite")
    cursor = conn.cursor()

    file = open(name_file, 'r')

    for i in file:
        cursor.execute(f"INSERT INTO '{product}' VALUES ('{i}', '{random.randint(111111, 999999)}')")

    conn.commit()

    file.close()
    os.remove(name_file)

    cursor.close()
    conn.close()


def basket(user_id):
    conn = sqlite3.connect('base_ts.sqlite')
    cursor = conn.cursor()
    row = cursor.execute(f'SELECT * FROM purchase_information WHERE user_id = "{user_id}"').fetchall()

    text = ''

    for i in row:
        text = text + '💠 ' + i[2][:10:] + ' | ' + i[3] + '\n\n'

    return text


def first_join(user_id, name, code):
    conn = sqlite3.connect('base_ts.sqlite')
    cursor = conn.cursor()
    row = cursor.execute(f'SELECT * FROM users WHERE user_id = "{user_id}"').fetchall()

    name = f'@{name}'

    ref_code = code
    if ref_code == '':
        ref_code = 0

    if len(row) == 0:
        cursor.execute(
            f'INSERT INTO users VALUES ("{user_id}", "{name}", "{datetime.datetime.now()}", "{user_id}", "{ref_code}", "0")')
        conn.commit()


def admin_info():
    conn = sqlite3.connect('base_ts.sqlite')
    cursor = conn.cursor()
    row = cursor.execute(f'SELECT * FROM users').fetchone()

    current_time = str(datetime.datetime.now())

    amount_user_all = 0
    amount_user_day = 0
    amount_user_hour = 0

    while row is not None:
        amount_user_all += 1
        if row[2][:-15:] == current_time[:-15:]:
            amount_user_day += 1
        if row[2][:-13:] == current_time[:-13:]:
            amount_user_hour += 1

        row = cursor.fetchone()

    msg = '❕ Информация:\n\n' \
          f'❕ За все время - {amount_user_all}\n' \
          f'❕ За день - {amount_user_day}\n' \
          f'❕ За час - {amount_user_hour}'

    return msg


def check_payment(user_id):
    conn = sqlite3.connect('base_ts.sqlite')
    cursor = conn.cursor()
    try:
        session = requests.Session()
        session.headers['authorization'] = 'Bearer ' + settings.QIWI_TOKEN
        parameters = {'rows': '5'}
        h = session.get(
            'https://edge.qiwi.com/payment-history/v1/persons/{}/payments'.format(settings.QIWI_NUMBER),
            params=parameters)
        req = json.loads(h.text)
        result = cursor.execute(f'SELECT * FROM check_payment WHERE user_id = {user_id}').fetchone()
        comment = result[1]

        for i in range(len(req['data'])):
            if comment in str(req['data'][i]['comment']):
                balance = cursor.execute(f'SELECT * FROM users WHERE user_id = "{user_id}"').fetchone()

                balance = float(balance[5]) + float(req["data"][i]["sum"]["amount"])

                cursor.execute(f'UPDATE users SET balance = {balance} WHERE user_id = "{user_id}"')
                conn.commit()

                cursor.execute(f'DELETE FROM check_payment WHERE user_id = "{user_id}"')
                conn.commit()

                referral_web(user_id, float(req["data"][i]["sum"]["amount"]))

                return 1, req["data"][i]["sum"]["amount"]
    except Exception as e:
        print(e)

    return 0, 0


def replenish_balance(user_id):
    conn = sqlite3.connect('base_ts.sqlite')
    cursor = conn.cursor()

    code = random.randint(1111111111, 9999999999)

    cursor.execute(f'SELECT * FROM check_payment WHERE user_id = "{user_id}"')
    row = cursor.fetchall()

    if len(row) > 0:
        cursor.execute(f'DELETE FROM check_payment WHERE user_id = "{user_id}"')
        conn.commit()

    cursor.execute(f'INSERT INTO check_payment VALUES ("{user_id}", "{code}", "0")')
    conn.commit()

    msg = settings.replenish_balance.format(
        number=settings.QIWI_NUMBER,
        code=code,
    )

    return msg


def cancel_payment(user_id):
    conn = sqlite3.connect('base_ts.sqlite')
    cursor = conn.cursor()

    cursor.execute(f'DELETE FROM check_payment WHERE user_id = "{user_id}"')
    conn.commit()


def profile(user_id):
    conn = sqlite3.connect('base_ts.sqlite')
    cursor = conn.cursor()

    row = cursor.execute(f'SELECT * FROM users WHERE user_id = "{user_id}"').fetchone()

    return row


def buy(dict):
    conn = sqlite3.connect('base_ts.sqlite')
    cursor = conn.cursor()

    data = str(datetime.datetime.now())
    lists = ''
    cursor.execute(f'SELECT * FROM "{dict.product}"')
    lists = lists + f'💠 {data[:19]} | {dict.name}\n'
    cursor.execute(
        f'INSERT INTO purchase_information VALUES ("{dict.user_id}", "{dict.code}", "{data}", "{dict.name}")')
    conn.commit()

    # cursor.execute(f'UPDATE {dict.code} SET amount_MAX = amount_MAX-{"amount"} WHERE code = "{dict.code}"')
    conn.commit()
    balance = cursor.execute(f'SELECT * FROM users WHERE user_id = "{dict.user_id}"').fetchone()
    balance = float(balance[5]) - (float(dict.price))
    cursor.execute(f'UPDATE users SET balance = "{balance}" WHERE user_id = "{dict.user_id}"')
    conn.commit()

    return lists


def give_balance(dict):
    conn = sqlite3.connect('base_ts.sqlite')
    cursor = conn.cursor()

    cursor.execute(f'UPDATE users SET balance = "{dict.balance}" WHERE name = "{dict.login}"')
    conn.commit()


def check_balance(user_id, price):
    conn = sqlite3.connect('base_ts.sqlite')
    cursor = conn.cursor()

    cursor.execute(f'SELECT * FROM users WHERE user_id = "{user_id}"')
    row = cursor.fetchone()

    if float(row[5]) >= float(price):
        return 1
    else:
        return 0


def list_sections():
    conn = sqlite3.connect("base_ts.sqlite")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM catalog')
    row = cursor.fetchall()

    sections = []

    for i in row:
        sections.append(i[1])

    return sections


def list_product():
    conn = sqlite3.connect("base_ts.sqlite")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM section')
    row = cursor.fetchall()

    list_product = []

    for i in row:
        list_product.append(i[2])

    return list_product


def check_ref_code(user_id):
    conn = sqlite3.connect("base_ts.sqlite")
    cursor = conn.cursor()

    cursor.execute(f'SELECT * FROM users WHERE user_id = "{user_id}"')
    user = cursor.fetchone()

    if int(user[3]) == 0:
        cursor.execute(f'UPDATE users SET ref_code = {user_id} WHERE user_id = "{user_id}"')
        conn.commit()

    return user_id


def referral_web(user_id, deposit_sum):
    conn = sqlite3.connect("base_ts.sqlite")
    cursor = conn.cursor()

    cursor.execute(f'SELECT * FROM users WHERE user_id = "{user_id}"')
    user = cursor.fetchone()

    if user[4] == '0':
        return
    else:
        user2 = cursor.execute(f'SELECT * FROM users WHERE user_id = "{user[4]}"').fetchone()

        profit = (deposit_sum / 100) * float(settings.ref_percent)

        balance = float(user[5]) + profit

        cursor.execute(f'UPDATE users SET balance = {balance} WHERE user_id = "{user[4]}"')
        conn.commit()

        ref_log(user2[0], profit, user2[1])


def ref_log(user_id, profit, name):
    conn = sqlite3.connect("base_ts.sqlite")
    cursor = conn.cursor()

    cursor.execute(f'SELECT * FROM ref_log WHERE user_id = "{user_id}"')
    user = cursor.fetchall()

    if len(user) == 0:
        cursor.execute(f'INSERT INTO ref_log VALUES ("{user_id}", "{profit}", "{name}")')
        conn.commit()
    else:
        all_profit = user[0][1]

        all_profit = float(all_profit) + float(profit)

        cursor.execute(f'UPDATE ref_log SET all_profit = {all_profit} WHERE user_id = "{user_id}"')
        conn.commit()


def check_all_profit_user(user_id):
    conn = sqlite3.connect("base_ts.sqlite")
    cursor = conn.cursor()

    cursor.execute(f'SELECT * FROM ref_log WHERE user_id = "{user_id}"')
    user = cursor.fetchall()

    if len(user) == 0:
        return 0
    else:
        return user[0][1]


def admin_top_ref():
    conn = sqlite3.connect("base_ts.sqlite")
    cursor = conn.cursor()

    cursor.execute(f'SELECT * FROM ref_log')
    users = cursor.fetchall()

    msg = '<b>Это топ рефералов за все время:</b>\n'
    for i in users:
        msg = msg + f'{i[0]}/{i[2]} - {i[1]} ₽\n'

    return msg


def get_id(username):
    conn = sqlite3.connect("base_ts.sqlite")
    cursor = conn.cursor()
    cursor.execute(f'SELECT user_id FROM users WHERE name = "{username}"')
    user = cursor.fetchone()
    return user[0]


def ok_pays(username):
    conn = sqlite3.connect("base_ts.sqlite")
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM replenishment WHERE username = "{username}" AND status = 0')
    row = cursor.fetchall()
    return row


def ok_pays2(username):
    conn = sqlite3.connect("base_ts.sqlite")
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM replenishment WHERE user_id = "{username}" AND status = 0')
    row = cursor.fetchall()
    return row


def agree(username, sum, code):
    conn = sqlite3.connect("base_ts.sqlite")
    cursor = conn.cursor()
    cursor.execute(f'UPDATE users SET balance = balance + {sum} WHERE user_id = "{username}"')
    conn.commit()
    cursor.execute(f'UPDATE replenishment SET status = "1" WHERE user_id = "{username}" AND code = "{code}"')
    conn.commit()


def disagree(username, code):
    conn = sqlite3.connect('base_ts.sqlite')
    cursor = conn.cursor()

    cursor.execute(f'DELETE FROM replenishment WHERE user_id = "{username}" AND code = "{code}"')
    conn.commit()


def check_id(username):
    conn = sqlite3.connect("base_ts.sqlite")
    cursor = conn.cursor()
    cursor.execute(f'SELECT code FROM replenishment WHERE username = "{username}"')
    user = cursor.fetchmany()

    return user


def auto_repl(user_id, sum):
    conn = sqlite3.connect('base_ts.sqlite')
    cursor = conn.cursor()
    try:
        balance = cursor.execute(f'SELECT balance FROM users WHERE user_id = "{user_id}"').fetchone()
        balance = float(balance[0]) + float(sum)
        cursor.execute(f'UPDATE users SET balance = {balance} WHERE user_id = "{user_id}"')
        conn.commit()
    except:
        pass