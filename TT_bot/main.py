from telebot.apihelper import ApiException
import telebot
from telebot import types
import weath_pars
import adding_an_entry
import os.path
import data_transformation as d_t
import pathlib
import calc
import logger as lg

API_TOKEN = ''
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    names = f'Привет, {message.from_user.first_name}!'
    bot.send_message(message.chat.id, names)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    nb = types.KeyboardButton("Телефонный справочник")
    calc = types.KeyboardButton("Калькулятор")
    weath = types.KeyboardButton("Погода в Екатеринбурге")
    markup.add(nb, calc, weath)
    bot.send_message(message.chat.id, 'Нажмите кнопку', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_mes(msg):
    if msg.text == "Погода в Екатеринбурге":
        lg.actions(msg.text)
        weather = weath_pars.show_weather()
        bot.send_message(msg.chat.id, text=weather)
    elif msg.text == 'Калькулятор':
        lg.actions(msg.text)
        calculator(msg)
    elif msg.text == "Телефонный справочник":
        lg.actions(msg.text)
        menu = "1. Посмотреть записи \n 2. Добавить новую запись \n 3. Импорт данных\n 4. Экспорт данных"
        bot.send_message(msg.chat.id, menu)
    elif msg.text == "1":
        try:
            lg.actions('Посмотреть записи')
            txt = adding_an_entry.show_data()
            for i in txt:
                bot.send_message(msg.chat.id, i)
            bot.send_message(msg.chat.id, 'Для выхода в меню нажмите любую букву')
        except ApiException:
            pass
    elif msg.text == "2":
        lg.actions('Добавить новую запись')
        message = bot.send_message(msg.chat.id, 'Напишите фамилию, имя, телефон, почту и комментарий в одну строку')
        bot.register_next_step_handler(message, start_2)
        lg.actions(message.text)
    elif msg.text == "4":
        lg.actions('Экспорт данных')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        f1 = types.KeyboardButton(".txt")
        f2 = types.KeyboardButton(".scv")
        markup.add(f1, f2)
        mess = bot.send_message(msg.chat.id, 'Выберите формат для импорта', reply_markup=markup)
        bot.register_next_step_handler(mess, handl_button)
    elif msg.text == "3":
        lg.actions('Импорт данных')
        bot.send_message(msg.chat.id, 'Загрузите файл')
    else:
        start(msg)


@bot.message_handler(content_types=['document'])
def handle_doc(message):
    lg.actions('Пользователь отправил документ')
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    path = pathlib.Path.cwd()
    save_path = os.path.join(path, message.document.file_name)
    with open(save_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    sticker = "https://github.com/TelegramBots/book/raw/master/src/docs/sticker-fred.webp"
    bot.send_message(message.chat.id, "Пожалуй, сохраню \n Чтобы вернуться в меню нажмите любую букву")
    bot.send_sticker(message.chat.id, sticker)


def calculator(msg):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    f1 = types.KeyboardButton("Комплексные")
    f2 = types.KeyboardButton("Рациональные")
    markup.add(f1, f2)
    mess = bot.send_message(msg.chat.id, 'С какими числами будем работать?', reply_markup=markup)
    bot.register_next_step_handler(mess, handl_button)


def handl_button(msg):
    if msg.text == ".txt":
        lg.actions(msg.text)
        dir_path = pathlib.Path.cwd()
        save_path = os.path.join(str(dir_path) + '/data_file.txt')
        file = open(save_path, 'r', encoding='utf-8')
        bot.send_document(msg.chat.id, file)
        bot.send_message(msg.chat.id, 'Чтобы вернуться в меню нажмите любую букву')
    elif msg.text == ".scv":
        lg.actions(msg.text)
        d_t.converting_to_csv()
        dir_path = pathlib.Path.cwd()
        save_path = os.path.join(str(dir_path) + '/data_file.csv')
        file = open(save_path, 'r', encoding='utf-8')
        bot.send_document(msg.chat.id, file)
        bot.send_message(msg.chat.id, 'Чтобы вернуться в меню нажмите любую букву')
    elif msg.text == "Комплексные":
        lg.actions(msg.text)
        message = bot.send_message(msg.chat.id, 'Введите выражение в формате: 5+3j + 2-2j')
        res = bot.register_next_step_handler(message, add_num)
        bot.send_message(msg.chat.id, res)
        lg.actions(msg.text)
    elif msg.text == "Рациональные":
        lg.actions(msg.text)
        message = bot.send_message(msg.chat.id, 'Введите выражение в формате: 5/11 + 3/4')
        res = bot.register_next_step_handler(message, compl_nums)
        bot.send_message(msg.chat.id, res)
        lg.actions(msg.text)


def compl_nums(message):
    num1, num2, op = d_t.ratio_formatting(message.text)
    res = calc.Calc_block(num1, num2, op)
    bot.send_message(message.chat.id, f'Ответ: {res} \n Чтобы вернуться в меню нажмите любую букву')
    lg.actions(message.text)


def add_num(message):
    num1, num2, op = d_t.compl(message.text)
    res = calc.Calc_block(num1, num2, op)
    bot.send_message(message.chat.id, f'Ответ: {res} \n Чтобы вернуться в меню нажмите любую букву')
    lg.actions(message.text)


def start_2(message):
    adding_an_entry.new_entry(message.text)
    bot.send_message(message.chat.id, 'Готово! \n Чтобы вернуться в меню нажмите любую букву')
    lg.actions(message.text)


bot.polling(none_stop=True)