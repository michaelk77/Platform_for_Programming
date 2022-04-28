# -*- coding: utf-8 -*-


import datetime
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
import telebot
import autopep8
from subprocess import run, PIPE
import time
import os
import random
from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, select, update
import pymorphy2
import googletrans
import datetime as dt
import threading

from telebot import types

morph = pymorphy2.MorphAnalyzer()
metadata = MetaData()
engine = create_engine(os.environ['bd'])
Users = Table("Users", metadata,
              Column('id', Integer(), primary_key=True),
              Column('userid', String(100), unique=True, nullable=False),
              Column("balls", Integer()))

Superlist = Table("Superlist", metadata,
                  Column('id', Integer(), primary_key=True),
                  Column('userid', String(100), unique=True, nullable=False),
                  Column("premium", String(100)), Column("ban", String(100)))

metadata.create_all(engine)

keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Выполнение', 'Pep-8', "Упаковка в .py")
keyboard1.row("Код из файла", "Как пользоваться")
keyboard1.row("Стандартные конструкции Python")
keyboard1.row("Документация", "Premium")

standartcomads = ["Выполнение", "Pep-8", "Упаковка в .py", "Код из файла", "Как пользоваться",
                  "Стандартные конструкции Python", "Документация"]

keyboard2 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard2.row("Есть ввод", "Ввода нет", "Отмена→")
keyboard3 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard3.row('Ввод данных', 'Типы данных', "Назад→")
keyboard3.row('if/else', 'Циклы', "Операции")
keyboard3.row('Практика', "Поддержка бота")

teoriyamenu = ["Ввод данных", "Типы данных", "Назад→", "if/else", "Циклы", "Операции", "Практика",
               "Поддержка бота"]

keyboardpractice = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardpractice.row('Ввод данных.', 'Типы данных.', "Назад")
keyboardpractice.row('if/else.', 'Циклы.', "Операции.")
keyboardpractice.row("Баллы")

practicmenu = ['Ввод данных.', 'Типы данных.', "Назад", 'if/else.', 'Циклы.', "Операции.", "Баллы"]

keyboardadmin = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardadmin.row('Ban', 'Premium.')

bot = telebot.TeleBot(os.environ['testbot'])
logbot = telebot.TeleBot(os.environ['logid'])

admin = os.environ['id']
banlist = []

inline_btn_1 = types.InlineKeyboardButton('Что же это за бот?', callback_data='button1')
inline_kb1 = types.InlineKeyboardMarkup().add(inline_btn_1)
inline_btn_1 = types.InlineKeyboardButton('Что тут можно делать?', callback_data='button2')
inline_btn_2 = types.InlineKeyboardButton('Cразу приступим!', callback_data='button3')
inline_kb2 = types.InlineKeyboardMarkup().add(inline_btn_1, inline_btn_2)


@bot.message_handler(commands=['start'])
def process_command_1(message):
    w = str([message.text, message.from_user.id, message.from_user.first_name,
             message.from_user.last_name])
    logbot.send_message(admin, w)
    bot.send_message(message.from_user.id, "Привет👋", reply_markup=inline_kb1)


@bot.callback_query_handler(func=lambda call: True)
def bottonconfig(call):
    if call.data == "button1":
        process_callback_button1(call)
    elif call.data == "button2":
        process_callback_button2(call)
    elif call.data == "button3":
        process_callback_button3(call)


def process_callback_button1(callback_query):
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.from_user.id,
                     'Данный бот эта целая платформа для програмирования на python, '
                     'настолько большая что вам станет лень читать про все функции которые '
                     'тут есть',
                     reply_markup=inline_kb2)


def process_callback_button2(callback_query):
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.from_user.id,
                     "Инструкция по пользованию ботом:\n\nВыполнение - это команда после "
                     "которой "
                     "бот попросит вас отправить код своей программы и выполнит его(обратно "
                     "возможна лишь отправка тексового материала, в ином случае будет выведена "
                     "ошибка)\n\nPep-8 - "
                     "очень полезная функция которая после отправки боту кода программы "
                     "отформатирует код по этому стандарту, некоторые учебные площадки "
                     "обязывают учеников сдавать код в стандарте Pep-8\n\nУпаковка в .py - "
                     "функция по переводу вашего программного кода в файл .py(полезна когда "
                     "нет доступа к компьютеру)\n\nКод из файла - Получение python кода из "
                     "вашего файла\n\nСтандартные конструкции Python - Описание "
                     "присутствует после нажатия этой кнопки\n\nмаксимальное "
                     "время работы программы 3 секунды(этого вполне достаточно)(в случае "
                     "привышения будет выведено "
                     "сообщение об ошибке в "
                     "программе)\n\nПоддержка бота: https://t.me/mkpythonbk при обращении "
                     "укажите что вы из данного бота", reply_markup=keyboard1
                     )


def process_callback_button3(callback_query):
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.from_user.id,
                     'Ну поехали!', reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def start(message):
    global banlist
    for i in banlist:
        if str(message.from_user.id) in i:
            tim = dt.datetime.strptime(i[1], "%Y-%m-%d")
            if tim > datetime.datetime.now():
                print("чел ты в муте")
                w = str([message.text, message.from_user.id, message.from_user.first_name,
                         message.from_user.last_name, "кто то рвется из бана"])
                logbot.send_message(admin, w)
                bot.send_message(message.from_user.id, f"Вы не можете пользоваться ботом до {i[1]}")
                bot.register_next_step_handler(message, zab)
                return

    if message.text in practicmenu:
        practice3000(message)
        return
    if message.text in teoriyamenu:
        programingboster3000(message)
        return

    w = str([message.text, message.from_user.id, message.from_user.first_name,
             message.from_user.last_name])
    logbot.send_message(admin, w)

    if message.text == '/start':
        bot.send_message(message.from_user.id,
                         "Здравствуйте, данный бот предназначен для удобного выполнения python "
                         "программ и их редактирования",
                         reply_markup=keyboard1)
    elif message.text == "/help" or message.text == "Как пользоваться":
        bot.send_message(message.from_user.id,
                         "Инструкция по пользованию ботом:\n\nВыполнение - это команда после "
                         "которой "
                         "бот попросит вас отправить код своей программы и выполнит его(обратно "
                         "возможна лишь отправка тексового материала, в ином случае будет выведена "
                         "ошибка)\n\nPep-8 - "
                         "очень полезная функция которая после отправки боту кода программы "
                         "отформатирует код по этому стандарту, некоторые учебные площадки "
                         "обязывают учеников сдавать код в стандарте Pep-8\n\nУпаковка в .py - "
                         "функция по переводу вашего программного кода в файл .py(полезна когда "
                         "нет доступа к компьютеру)\n\nКод из файла - Получение python кода из "
                         "вашего файла\n\nСтандартные конструкции Python - Описание "
                         "присутствует после нажатия этой кнопки\n\nмаксимальное "
                         "время работы программы 3 секунды(этого вполне достаточно)(в случае "
                         "привышения будет выведено "
                         "сообщение об ошибке в "
                         "программе)\n\nПоддержка бота: https://t.me/mkpythonbk при обращении "
                         "укажите что вы из данного бота",
                         reply_markup=keyboard1)
    elif message.text == "Выполнение":
        bot.send_message(message.from_user.id,
                         "жду код вашей программы что запустить")
        bot.register_next_step_handler(message, runpyprogramm)
    elif message.text == "Pep-8":
        bot.send_message(message.from_user.id,
                         "Жду вашу программу чтобы сделать ее красивой")
        bot.register_next_step_handler(message, refpyprogramm)
    elif message.text == "Упаковка в .py":
        bot.send_message(message.from_user.id,
                         "Жду код вашей программу для упаковки")
        bot.register_next_step_handler(message, upocov)
    elif message.text == "Стандартные конструкции Python":
        bot.send_message(message.from_user.id,
                         "Тут вы найдете простые программы на python с примерами работы, "
                         "для улучшения ваших знаний програмирования\nВы можете сами запускать "
                         "наши примеры прямо в боте", reply_markup=keyboard3)
        bot.register_next_step_handler(message, programingboster3000)
    elif message.text == "Назад→" or message.text == "Назад":
        bot.send_message(message.from_user.id, "Возвращаемся в главное меню", reply_markup=keyboard1)
    elif message.text == "Код из файла":
        bot.send_message(message.from_user.id, "Отправьте ваш файл с программой на питоне")
        bot.register_next_step_handler(message, vipolnfromfile)
    elif message.text == "Документация":
        bot.send_message(message.from_user.id, "Отправьте  запрос для поиска в документации")
        bot.register_next_step_handler(message, poiskdocumentation)
    elif message.from_user.id == admin and str(message.text).lower() in ["admin", "adminka", "админ",
                                                                         "админка"]:
        bot.send_message(message.from_user.id, "Входим в админку", reply_markup=keyboardadmin)
        print("привет админ")
        bot.register_next_step_handler(message, adminka)
    elif message.text == "Premium":
        premiumfunc(message)
    elif message.text in standartcomads:
        start(message)
        return
    else:
        bot.send_message(message.from_user.id,
                         "Неизвестная команда\nПопробуйте /help если не знаете ка пользоваться",
                         reply_markup=keyboard1)
    print(message.from_user.id)


def runpyprogramm(message):
    if message.text in standartcomads:
        start(message)
        return
    if message.text in teoriyamenu:
        programingboster3000(message)
        return
    if message.text in practicmenu:
        practice3000(message)
        return

    try:
        w = str([message.text, message.from_user.id, message.from_user.first_name,
                 message.from_user.last_name])
        logbot.send_message(admin, w)
        z = str(message.text)
        print(z)
        if "sqlalchemy" in z or "psycopg2" in z:
            bot.send_message(message.from_user.id,
                             "Нельзя использовать библиотеки sqlalchemy или psycopg2",
                             reply_markup=keyboard1)
        if "pip" in z:
            bot.send_message(message.from_user.id,
                             "Нельзя скачивать библиотеки",
                             reply_markup=keyboard1)
            return
        if "webbrowser" in z:
            bot.send_message(message.from_user.id,
                             "Нельзя использовать webbroser",
                             reply_markup=keyboard1)
            return
        if "antigravity" in z:
            bot.send_message(message.from_user.id,
                             "Antigravity заблокированна, но ссылку но комикс мы оставим "
                             "https://xkcd.com/353/",
                             reply_markup=keyboard1)
            return
        if " os" in z:
            bot.send_message(message.from_user.id,
                             "мы не можем выполнить код с библиотекой os из-за проблем с "
                             "безопасностью",
                             reply_markup=keyboard1)
            return
        if "subprocess" in z:
            bot.send_message(message.from_user.id,
                             "мы не можем выполнить код с библиотекой subprocess из-за проблем с "
                             "безопасностью",
                             reply_markup=keyboard1)
            return
        if "main.py" in z or "prog" in z:
            bot.send_message(message.from_user.id,
                             "Мы сами используем такие названия файлов(main или prog), пожалуйста "
                             "переменуйти "
                             "свои файлы или переменные",
                             reply_markup=keyboard1)
            return
        if "requests" in z or "socket" in z or "flask" in z:
            bot.send_message(message.from_user.id,
                             "К сожалению интернет функции откючены с целью безопасности от спама",
                             reply_markup=keyboard1)
            return
        r = open("prog" + str(message.from_user.id) + ".py", "w", encoding="UTF-8")
        print(z)
        print(z, file=r)
        r.close()

        if "input" in z or "stdin" in z:
            bot.send_message(message.from_user.id, "Введите полные данные ввода")
            th = threading.Thread(bot.register_next_step_handler(message, sovvodom))
            th.start()
            th.join()
            return
        else:
            try:
                unactutpremium = 0
                w = str([message.text, message.from_user.id, message.from_user.first_name,
                         message.from_user.last_name])
                logbot.send_message(admin, w)
                s = select([Superlist]).where(Superlist.c.userid == str(message.from_user.id))
                conn = engine.connect()
                r = conn.execute(s)
                j = r.fetchall()
                print(j)
                try:
                    if j:
                        tim = dt.datetime.strptime(j[0][2], "%Y-%m-%d")
                        if dt.datetime.now() < tim:
                            unactutpremium = 1
                except:
                    print("пофиг")
                if unactutpremium:
                    solution = run(["python3", "prog" + str(message.from_user.id) + ".py"],
                                   stdout=PIPE,
                                   encoding="UTF-8", stderr=PIPE,
                                   text=True, timeout=30)
                else:
                    solution = run(["python3", "prog" + str(message.from_user.id) + ".py"],
                                   stdout=PIPE,
                                   encoding="UTF-8", stderr=PIPE,
                                   text=True, timeout=3)
                er = solution.stderr.splitlines()
                print(solution.stdout)
                print("\n", er, "\n")
                if solution.stderr:
                    if 'Traceback (most recent call last):' == er[0]:
                        er = er[1:]
                    if "prog" in er[0]:
                        er = er[1:]
                    er = "\n".join(er)
                    print(er)
                    bot.send_message(message.from_user.id,
                                     "Во время выполнения программы произошла ошибка")
                    bot.send_message(message.from_user.id, er, reply_markup=keyboard1)
                    os.remove(os.getcwd() + "/prog" + str(message.from_user.id) + ".py")
                    return
                if solution.stdout:
                    if len(str(solution.stdout)) > 4096:
                        for x in range(0, len(str(solution.stdout)), 4096):
                            bot.send_message(message.chat.id, str(solution.stdout)[x:x + 4096])
                    else:
                        bot.send_message(message.chat.id, str(solution.stdout))
                    bot.send_message(message.from_user.id, "⬆готово⬆", reply_markup=keyboard1)
                else:
                    bot.send_message(message.from_user.id,
                                     "В программе нет вывода, или он не в текстовом формате(бот "
                                     "может вернуть только символы)")
                os.remove(os.getcwd() + "/prog" + str(message.from_user.id) + ".py")
            except Exception as e:
                bot.send_message(message.from_user.id, "У вас ошибка в коде", reply_markup=keyboard1)
                print(str(e))
                logbot.send_message(admin, str(e))
        # bot.send_message(message.from_user.id, "В программе есть ввод?", reply_markup=keyboard2)
        # bot.register_next_step_handler(message, vipoln)
    except Exception as e:
        bot.send_message(message.from_user.id,
                         "Что-то пошло не так")
        try:
            os.remove(os.getcwd() + "/prog" + str(message.from_user.id) + ".py")
        except:
            print("пофиг")
        print(str(e))
        logbot.send_message(admin, str(e))


def vipoln(message):
    try:
        if message.text == "Отмена→":
            bot.send_message(message.from_user.id, "Возвращаемся в главное меню",
                             reply_markup=keyboard1)
            return

        elif message.text == "Ввода нет":
            solution = run(["python3", "prog" + str(message.from_user.id) + ".py"], input="",
                           stdout=PIPE,
                           encoding="UTF-8",
                           text=True, timeout=15)
            print(solution.stdout)
            bot.send_message(message.from_user.id, str(solution.stdout))
            bot.send_message(message.from_user.id, "⬆готово⬆", reply_markup=keyboard1)
            os.remove(os.getcwd() + "/prog" + str(message.from_user.id) + ".py")
            return
        """elif message.text == "Есть ввод":
            bot.send_message(message.from_user.id, "Введите полные данные ввода")
            bot.register_next_step_handler(message, sovvodom)

        else:
            bot.send_message(message.from_user.id, "выберите из предложенных значений",
                             reply_markup=keyboard1)"""
    except Exception as e:
        bot.send_message(message.from_user.id, "У вас ошибка в коде", reply_markup=keyboard1)
        print(str(e))
        logbot.send_message(admin, str(e))


def sovvodom(message):
    w = str([message.text, message.from_user.id, message.from_user.first_name,
             message.from_user.last_name])
    logbot.send_message(admin, w)
    if message.text in standartcomads:
        start(message)
        return
    if message.text in teoriyamenu:
        programingboster3000(message)
        return
    if message.text in practicmenu:
        practice3000(message)
        return

    try:
        unactutpremium = 0
        w = str([message.text, message.from_user.id, message.from_user.first_name,
                 message.from_user.last_name])
        logbot.send_message(admin, w)
        s = select([Superlist]).where(Superlist.c.userid == str(message.from_user.id))
        conn = engine.connect()
        r = conn.execute(s)
        j = r.fetchall()
        print(j)
        try:
            if j:
                tim = dt.datetime.strptime(j[0][2], "%Y-%m-%d")
                if dt.datetime.now() < tim:
                    unactutpremium = 1
        except:
            print("net cviasy")
        if unactutpremium:
            print("prem")
            solution = run(["python3", "prog" + str(message.from_user.id) + ".py"],
                           input=message.text,
                           stdout=PIPE, encoding="UTF-8", stderr=PIPE,
                           text=True, timeout=30)
        else:
            solution = run(["python3", "prog" + str(message.from_user.id) + ".py"],
                           input=message.text,
                           stdout=PIPE, encoding="UTF-8", stderr=PIPE,
                           text=True, timeout=3)
        er = solution.stderr.splitlines()
        print(solution.stdout)
        print("\n", er, "\n")
        if solution.stderr:
            if 'Traceback (most recent call last):' == er[0]:
                er = er[1:]
            if "prog" in er[0]:
                er = er[1:]
            er = "\n".join(er)
            print(er)
            bot.send_message(message.from_user.id, "Во время выполнения программы произошла ошибка")
            bot.send_message(message.from_user.id, er, reply_markup=keyboard1)
            return
        if solution.stdout:
            if len(str(solution.stdout)) > 4096:
                for x in range(0, len(str(solution.stdout)), 4096):
                    bot.send_message(message.chat.id, str(solution.stdout)[x:x + 4096])
            else:
                bot.send_message(message.chat.id, str(solution.stdout))
            bot.send_message(message.from_user.id, "⬆готово⬆", reply_markup=keyboard1)
        else:
            bot.send_message(message.from_user.id,
                             "В программе нет вывода, или он не в текстовом формате(бот "
                             "может вернуть только символы)")
        os.remove(os.getcwd() + "/prog" + str(message.from_user.id) + ".py")
    except Exception as e:
        bot.send_message(message.from_user.id, "У вас ошибка в коде или во вводе",
                         reply_markup=keyboard1)
        print(str(e))
        logbot.send_message(admin, str(e))


def refpyprogramm(message):
    w = str([message.text, message.from_user.id, message.from_user.first_name,
             message.from_user.last_name])
    logbot.send_message(admin, w)
    if message.text in standartcomads:
        start(message)
        return
    if message.text in teoriyamenu:
        programingboster3000(message)
        return
    if message.text in practicmenu:
        practice3000(message)
        return

    w = str([message.text, message.from_user.id, message.from_user.first_name,
             message.from_user.last_name])
    logbot.send_message(admin, w)
    z = message.text
    print(z)
    bot.send_message(message.from_user.id, "Редактирую")
    y = z.splitlines()
    for i in range(len(y)):
        kol = 0
        kol1 = 0
        if "print" in y[i]:
            j = 0
            while j < len(y[i]):
                if "\"" == y[i][j]:
                    kol += 1
                if "\'" == y[i][j]:
                    kol1 += 1
                if kol % 2 == 0 and kol1 % 2 == 0 and y[i][j] in "+-**//":
                    if y[i][j + 1] == y[i][j]:
                        y[i] = y[i][:j] + f" {y[i][j] + y[i][j]} " + y[i][j + 2:]
                        j += 3
                    else:
                        y[i] = y[i][:j] + f" {y[i][j]} " + y[i][j + 1:]
                        j += 2
                j += 1
    z = "\n".join(y)
    z = autopep8.fix_code(z, options={'aggressive': 10000})
    print(z)
    bot.send_message(message.from_user.id, z)
    bot.send_message(message.from_user.id, "⬆Код переформатирован⬆")


def upocov(message):
    if message.text in standartcomads:
        start(message)
        return
    if message.text in teoriyamenu:
        programingboster3000(message)
        return
    if message.text in practicmenu:
        practice3000(message)
        return

    w = str([message.text, message.from_user.id, message.from_user.first_name,
             message.from_user.last_name])
    logbot.send_message(admin, w)
    z = message.text
    print(z)
    bot.send_message(message.from_user.id, "упаковываю")
    r = open("prog" + str(message.from_user.id) + ".py", "w", encoding="UTF-8")
    print(z, file=r)
    r.close()
    r = open("prog" + str(message.from_user.id) + ".py", "r", encoding="UTF-8")
    bot.send_document(message.chat.id, r, visible_file_name="program.py")
    r = open("prog" + str(message.from_user.id) + ".py", "w", encoding="UTF-8")
    r.close()
    os.remove(os.getcwd() + "/prog" + str(message.from_user.id) + ".py")


def programingboster3000(message):
    if message.text in standartcomads:
        start(message)
        return
    if message.text in practicmenu:
        practice3000(message)
        return

    if message.text == "Назад→":
        bot.send_message(message.from_user.id, "Возвращаемся в главное меню", reply_markup=keyboard1)
        bot.register_next_step_handler(message, start)
        return
    elif message.text == "Ввод данных":
        bot.send_message(message.from_user.id,
                         "Программа:\na = input()\nprint(a)\n\n\nРезультатом программы станет ровно "
                         "то что вы ввели после ее старта", reply_markup=keyboard1)
    elif message.text == "Типы данных":
        bot.send_message(message.from_user.id,
                         "Программа:\na = input()\nb = int(input())\nс = float(input())\n\n\nВы "
                         "вводите "
                         "3 значения но первое это строчка, второе число, третье это нецелое "
                         "число(например 12.45)", reply_markup=keyboard1)
    elif message.text == "if/else":
        bot.send_message(message.from_user.id,
                         "Программа:\na = int(input())\nb = int(input())\nif a == b:\n   print("
                         "\"одинаковое\")\nelse:\n   print(\"разное\")\n\n\nПрограмма получает на "
                         "ввод 2 числа от пользователя и пишет равны ли они или нет",
                         reply_markup=keyboard1)
    elif message.text == "Циклы":
        bot.send_message(message.from_user.id,
                         "Программа:\na = int(input())\nb = int(input())\nfor i in range(a):\n   "
                         "print(b)\n\n\nПрограмма получает на ввод 2 числа от пользователя и "
                         "выводит 2 число ровно столько раз сколько написанно в первом числе",
                         reply_markup=keyboard1)
    elif message.text == "Операции":
        bot.send_message(message.from_user.id,
                         "Программа:\na = int(input())\nb = int(input())\nz = a + b\nprint("
                         "z*2)\n\n\nПрограмма получает на ввод 2 числа от пользователя и "
                         "складывает эти числа и кладет в новую переменную, а потом выводит эту "
                         "новую переменную умножив на 2\nтакже есть:   +(сложение) /(деление) //("
                         "деление нацело) **( "
                         "возведение в степень) %(остаток от деления)", reply_markup=keyboard1)
    elif message.text == "Практика":
        bot.send_message(message.from_user.id, "Выберите тип задач",
                         reply_markup=keyboardpractice)
        bot.register_next_step_handler(message, practice3000)
    elif message.text == "Поддержка бота":
        bot.send_message(message.from_user.id,
                         "Поддержка бота: https://t.me/mkpythonbk при обращении укажите что вы из "
                         "данного бота",
                         reply_markup=keyboard1)
    elif message.text in teoriyamenu:
        programingboster3000(message)
        return


def practice3000(message):
    if message.text in standartcomads:
        start(message)
        return
    if message.text in teoriyamenu:
        programingboster3000(message)
        return

    try:
        conn = engine.connect()
        z = select([Users]).where(
            Users.c.userid == str(message.from_user.id))
        r = conn.execute(z)
        i = list(r.first())
        if i:
            print("uze tut")
        else:
            ins = Users.insert().values(userid=str(message.from_user.id), balls=0)
            print(789)
            print(ins.compile().params)
            r = conn.execute(ins)
            s = select([Users])
            r = conn.execute(s)
            print(r.fetchall())
    except:
        try:
            ins = Users.insert().values(userid=str(message.from_user.id), balls=0)
            print(789)
            print(ins.compile().params)
            r = conn.execute(ins)
            s = select([Users])
            r = conn.execute(s)
            print(r.fetchall())
        except:
            print("Нет связи с модулем баллов")
            bot.send_message(message.from_user.id, "В данный момент нет связи с модулем баллов")
    if message.text == "Назад":
        bot.send_message(message.from_user.id, "Возвращаемся в главное меню", reply_markup=keyboard1)
        bot.register_next_step_handler(message, start)
        return
    elif message.text == "Ввод данных.":
        r = str(random.randint(1, 100))
        bot.send_message(message.from_user.id,
                         f"Программа:\na = input()\nprint(a)\n\n\nВвод:\n{r}\n\n\n Что выведет "
                         f"программа?")
        print(r)
        bot.register_next_step_handler(message, proverkapracticy, r)
    elif message.text == "Типы данных.":
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        c = round(random.uniform(1, 100), 2)
        r = random.randint(0, 2)
        t = ["a", "b", "c"]
        t2 = [a, b, c]
        bot.send_message(message.from_user.id,
                         "Программа:\na = input()\nb = int(input())\nс = float(input())\n\n\n"
                         f"Ввод:\n{a}\n{b}\n{c}\n\n\nВ качестве ответа укажите переменную {t[r]}")
        print(a, b, c, r)
        bot.register_next_step_handler(message, proverkapracticy, t2[r])
    elif message.text == "if/else.":
        a = random.randint(2, 5)
        b = random.randint(2, 5)
        bot.send_message(message.from_user.id,
                         "Программа:\na = int(input())\nb = int(input())\nif a == b:\n   print("
                         f"\"да\")\nelse:\n   print(\"нет\")\n\n\nВвод:\n{a}\n{b}\n\n\nЧто выведет "
                         f"программа?")
        print(a, b)
        if a == b:
            z = "да"
        else:
            z = "нет"
        bot.register_next_step_handler(message, proverkapracticy, z)
    elif message.text == "Циклы.":
        a = random.randint(1, 3)
        b = random.randint(1, 9)
        bot.send_message(message.from_user.id,
                         "Программа:\na = int(input())\nb = int(input())\nfor i in range(a):\n   "
                         f"print(b)\n\n\nВвод:\n{a}\n{b}\n\n\nСколько раз программа выведет число {b}")
        bot.register_next_step_handler(message, proverkapracticy, a)
    elif message.text == "Операции.":
        a = random.randint(1, 8)
        b = random.randint(1, 6)
        bot.send_message(message.from_user.id,
                         "Программа:\na = int(input())\nb = int(input())\nz = a + b\nprint("
                         f"z*2)\n\n\nВвод:\n{a}\n{b}\n\n\nЧто выведет программа?")
        bot.register_next_step_handler(message, proverkapracticy, (a + b) * 2)
    elif message.text == "Баллы":
        try:
            conn = engine.connect()
            r = conn.execute(select([Users]).where(Users.c.userid == str(message.from_user.id)))
            bal = r.first()[-1]
            print(bal)
            balov = morph.parse('баллы')[0]
            if 0 <= bal < 5:
                bot.send_message(message.from_user.id,
                                 f"у вас {bal} {balov.make_agree_with_number(bal).word}, что-то "
                                 f"маловато",
                                 reply_markup=keyboardpractice)
            elif 5 <= bal < 10:
                bot.send_message(message.from_user.id,
                                 f"у вас {bal} {balov.make_agree_with_number(bal).word}, неплохо",
                                 reply_markup=keyboardpractice)

            elif 10 <= bal < 50:
                bot.send_message(message.from_user.id,
                                 f"у вас {bal} {balov.make_agree_with_number(bal).word}, класс",
                                 reply_markup=keyboardpractice)
            elif bal >= 50:
                bot.send_message(message.from_user.id,
                                 f"у вас {bal} {balov.make_agree_with_number(bal).word}, НЕВЕРОЯТНО",
                                 reply_markup=keyboardpractice)
            bot.register_next_step_handler(message, practice3000)
            print(2)
            return
        except:
            print("Нет связи с модулем баллов")
            bot.send_message(message.from_user.id, "В данный момент нет связи с модулем баллов")
    elif message.text in practicmenu:
        practice3000(message)
        return


def proverkapracticy(message, trueansver):
    if message.text in standartcomads:
        start(message)
        return
    if message.text in teoriyamenu:
        programingboster3000(message)
        return
    if message.text in practicmenu:
        practice3000(message)
        return

    if message.text == "Назад→" or message.text == "Назад":
        bot.send_message(message.from_user.id, "Возвращаемся в главное меню",
                         reply_markup=keyboard1)
        return
    if message.text == trueansver or message.text == str(trueansver):
        print("pravilno")
        bot.send_message(message.from_user.id, "Все правильно", reply_markup=keyboardpractice)
        conn = engine.connect()
        r = conn.execute(select([Users]).where(Users.c.userid == str(message.from_user.id)))
        bal = r.first()[-1]
        print(bal)
        conn.execute(update(Users).where(Users.c.userid == str(message.from_user.id)).values(
            balls=bal + 1))
        if bal == 0:
            bot.send_message(message.from_user.id,
                             "Вы получили свой первый бал, продолжайте в том-же духе",
                             reply_markup=keyboardpractice)
        elif bal <= 5:
            bot.send_message(message.from_user.id,
                             f"Вы получили свой {bal + 1} бал, неплохо",
                             reply_markup=keyboardpractice)
        elif bal > 5:
            a = ["очередной", "новый", "следующий"]
            bot.send_message(message.from_user.id,
                             f"Вы получили свой {random.choice(a)} бал, вы молодец",
                             reply_markup=keyboardpractice)


    else:
        bot.send_message(message.from_user.id,
                         f"Вы ошиблись но не отчаивайтесь\nПравильный ответ {trueansver}",
                         reply_markup=keyboardpractice)
    bot.register_next_step_handler(message, practice3000)
    print(3)
    return


@bot.message_handler(content_types=['document'])
def vipolnfromfile(message):
    if message.text == None:
        try:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            downloaded_file = downloaded_file.decode("UTF-8")
            downloaded_file = str(downloaded_file)
            print(downloaded_file)
            bot.send_message(message.from_user.id, downloaded_file)
            bot.send_message(message.from_user.id,
                             "⬆Вот⬆ ваш код, если хотите вы можете выполнить его в этом боте, "
                             "выбрав соответствующую функцую",
                             reply_markup=keyboard1)
        except:
            print("что-то не то")
            bot.send_message(message.from_user.id,
                             "Что-то пошло не так", reply_markup=keyboard1)
    else:
        if message.text in standartcomads:
            start(message)
            return
        if message.text in teoriyamenu:
            programingboster3000(message)
            return
        if message.text in practicmenu:
            practice3000(message)
            return
        bot.send_message(message.from_user.id,
                         "Вы явно отправили что-то не то", reply_markup=keyboard1)


def poiskdocumentation(message):
    w = str([message.text, message.from_user.id, message.from_user.first_name,
             message.from_user.last_name])
    logbot.send_message(admin, w)
    if message.text in teoriyamenu:
        programingboster3000(message)
        return
    if message.text in practicmenu:
        practice3000(message)
        return
    if message.text in standartcomads:
        start(message)
        return

    translator = googletrans.Translator()
    result = translator.translate(message.text)
    result = result.text
    result = "+".join(result.split())
    g = None
    try:
        url = f"https://yandex.ru/search/?text={result}+python+org"
        ua = UserAgent()
        response = requests.post(url, headers={"User-Agent": ua.random})
        # quote_list = soup.findAll("div", id="lenta-card__text-quote-escaped")
        soup_ing = str(BeautifulSoup(response.content, 'lxml'))
        soup_ing = str(soup_ing).split(";")
        for i in soup_ing:
            if "python.org" in i and "href" in i or "pypi.org" in i and "href" in i:
                a = i[i.index("href") + 6:i.index("tabindex") - 2]
                result = "%20".join(result.split("+"))
                print(a + "#:~:text=" + result)
                g = a + "#:~:text=" + result
                break
        if g:
            bot.send_message(message.from_user.id, g, reply_markup=keyboard1)
            return
        else:
            bot.send_message(message.from_user.id,
                             f"Извените нас забанили в поисковике из за слишком большого "
                             f"количества запросов в день, но вы можете поискать тут: {url}",
                             reply_markup=keyboard1)
    except Exception as e:
        bot.send_message(message.from_user.id,
                         "У нас какие то проблеммы",
                         reply_markup=keyboard1)
        print(str(e))
        logbot.send_message(admin, str(e))


def adminka(message):
    bot.send_message(message.from_user.id, "Введи id и количество дней через пробел")
    if message.text == "Ban":
        bot.register_next_step_handler(message, banim)
    elif message.text == "Premium.":
        bot.register_next_step_handler(message, prem)


def banim(message):
    global banlist
    try:
        id, days = str(message.text).split()
        conn = engine.connect()
        z = select([Superlist]).where(
            Superlist.c.userid == id)
        r = conn.execute(z)
        i = list(r.fetchall())
        print(i)
        if i[0][0]:
            print("uze tut")
            s = select([Superlist]).where(Superlist.c.userid == str(id))
            r = conn.execute(s)
            j = r.fetchall()
            print(j)
            if j[0][3]:
                tim = dt.datetime.strptime(j[0][3], "%Y-%m-%d")
            else:
                tim = dt.datetime.now()
            kon = str(max(dt.datetime.now(), tim).date() + dt.timedelta(int(days)))
            conn.execute(
                update(Superlist).where(Superlist.c.userid == str(id)).values(
                    ban=str(kon)))
            s = select([Superlist]).where(Superlist.c.userid == str(id))
            r = conn.execute(s)
            j = r.fetchall()
            print(j)
            bot.send_message(admin, f"ban был продлен до {j[0][3]}")
            try:
                bot.send_message(int(id), f"Вы забанены до {j[0][3]}")
            except:
                bot.send_message(admin, "Аккаунта с таким id не существует")
            podgruskaban()

        else:
            print("новенький")
            kon = str(dt.datetime.now().date() + dt.timedelta(int(days)))
            ins = Superlist.insert().values(userid=str(id), premium="", ban=kon)
            r = conn.execute(ins)
            print(789)
            print(ins.compile().params)
            s = select([Superlist]).where(Superlist.c.userid == str(id))
            r = conn.execute(s)
            j = r.fetchall()
            print(j)
            bot.send_message(admin, f"ban был продлен до {j[0][3]}")
            try:
                bot.send_message(int(id), f"Вы забанены до {j[0][3]}")
            except:
                bot.send_message(admin, "Аккаунта с таким id не существует")
            podgruskaban()
    except Exception as e:
        print(e)
        logbot.send_message(admin, str(e))
        try:
            id, days = str(message.text).split()
            kon = str(dt.datetime.now().date() + dt.timedelta(int(days)))
            ins = Superlist.insert().values(userid=id, ban=kon, premium="")
            print(ins.compile().params)
            r = conn.execute(ins)
            s = select([Superlist]).where(Superlist.c.userid == str(id))
            conn = engine.connect()
            r = conn.execute(s)
            j = r.fetchall()
            print(j)
            bot.send_message(admin, f"ban был продлен до {j[0][3]}")
            try:
                bot.send_message(int(id), f"Вы забанены до {j[0][3]}")
            except:
                bot.send_message(admin, "Аккаунта с таким id не существует")
            podgruskaban()
        except Exception as e:
            print(e)
            print("Нет связи с модулем ban")
            bot.send_message(message.from_user.id, "В данный момент нет связи с модулем ban")


def prem(message):
    try:
        id, days = str(message.text).split()
        conn = engine.connect()
        z = select([Superlist]).where(
            Superlist.c.userid == id)
        r = conn.execute(z)
        i = list(r.fetchall())
        print(i)
        if i[0][0]:
            print("uze tut")
            s = select([Superlist]).where(Superlist.c.userid == str(id))
            r = conn.execute(s)
            j = r.fetchall()
            print(j)
            if j[0][2]:
                tim = dt.datetime.strptime(j[0][2], "%Y-%m-%d")
            else:
                tim = dt.datetime.now()
            kon = str(max(dt.datetime.now(), tim).date() + dt.timedelta(int(days)))
            conn.execute(
                update(Superlist).where(Superlist.c.userid == str(id)).values(
                    premium=str(kon)))
            s = select([Superlist]).where(Superlist.c.userid == str(id))
            r = conn.execute(s)
            j = r.fetchall()
            print(j)
            bot.send_message(admin, f"premium был продлен до {j[0][2]}")
            try:
                bot.send_message(int(id), f"premium был продлен до {j[0][2]}")
            except:
                bot.send_message(admin, "Аккаунта с таким id не существует")

        else:
            print("новенький")
            kon = str(dt.datetime.now().date() + dt.timedelta(int(days)))
            ins = Superlist.insert().values(userid=str(id), ban="", premium=kon)
            r = conn.execute(ins)
            print(789)
            print(ins.compile().params)
            s = select([Superlist]).where(Superlist.c.userid == str(id))
            r = conn.execute(s)
            j = r.fetchall()
            print(j)
            bot.send_message(admin, f"premium был продлен до {j[0][2]}")
            try:
                bot.send_message(int(id), f"premium был продлен до {j[0][2]}")
            except:
                bot.send_message(admin, "Аккаунта с таким id не существует")
    except Exception as e:
        print(e)
        logbot.send_message(admin, str(e))
        try:
            id, days = str(message.text).split()
            kon = str(dt.datetime.now().date() + dt.timedelta(int(days)))
            ins = Superlist.insert().values(userid=id, ban="", premium=kon)
            print(ins.compile().params)
            r = conn.execute(ins)

            s = select([Superlist]).where(Superlist.c.userid == str(id))
            conn = engine.connect()
            r = conn.execute(s)
            j = r.fetchall()
            print(j)
            bot.send_message(admin, f"premium был продлен до {j[0][2]}")
            try:
                bot.send_message(int(id), f"premium был продлен до {j[0][2]}")
            except:
                bot.send_message(admin, "Аккаунта с таким id не существует")
        except Exception as e:
            print(e)
            print("Нет связи с модулем premium")
            bot.send_message(message.from_user.id, "В данный момент нет связи с модулем premium")


def premiumfunc(message):
    s = select([Superlist]).where(Superlist.c.userid == str(message.from_user.id))
    conn = engine.connect()
    r = conn.execute(s)
    j = r.fetchall()
    print(j)
    if j:
        tim = dt.datetime.strptime(j[0][2], "%Y-%m-%d")
        if dt.datetime.now() < tim:
            bot.send_message(message.from_user.id, f"У вас есть премиум до {j[0][2]}")
        else:
            bot.send_message(message.from_user.id, f"Ваш премиум закончился {j[0][2]}")
            bot.send_message(message.from_user.id,
                             f"Если вы хотите продолжить премиум на месяц то отправьте 50 рублей на "
                             f"тинькофф по номеру 89680972248 с коментарием "
                             f"{message.from_user.id}\nПроверка осуществляеться вручную так что "
                             f"займет некоторое время")
    else:
        bot.send_message(message.from_user.id,
                         "Premium - дает доступ к увеличенному времени выполнения программ до 30 секунд, пока только это")
        bot.send_message(message.from_user.id,
                         f"Если вы хотите получить премиум на месяц то отправьте 50 рублей на "
                         f"тинькофф по номеру 89680972248 с коментарием "
                         f"{message.from_user.id}\nПроверка осуществляеться вручную так что "
                         f"займет некоторое время")


def podgruskaban():
    global banlist
    banlist = []

    try:
        conn = engine.connect()
        z = select([Superlist])
        r = conn.execute(z)
        i = list(r.fetchall())
        print(i)
        for j in i:
            if j[3]:
                banlist.append((j[1], j[3]))
        print(banlist)
    except Exception as e:
        print("pomogite", e)


def zab(message):
    podgruskaban()
    global banlist

    for i in banlist:
        if str(message.from_user.id) in i:
            tim = dt.datetime.strptime(i[1], "%Y-%m-%d")
            if tim > datetime.datetime.now():
                print("чел ты в муте")

                w = str([message.text, message.from_user.id, message.from_user.first_name,
                         message.from_user.last_name, "кто то рвется из бана"])
                logbot.send_message(admin, w)

                bot.send_message(message.from_user.id, f"Вы не можете пользоваться ботом до {i[1]}")
                bot.register_next_step_handler(message, zab)
                return
    bot.register_next_step_handler(message, start)


podgruskaban()

while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        time.sleep(1)
        print(str(e))
        logbot.send_message(admin, str(e))
