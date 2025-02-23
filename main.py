import telebot
import datetime
from database_handler import DatabaseHandler
from localizated_text import Localization

token = "7542245520:AAFPNt13ZYt8Kf4ZcOixjDTbd42B0ZczC0s"
bot = telebot.TeleBot(token=token)
db = DatabaseHandler()
temporal_user_form = {}


@bot.message_handler(commands=['start'])
def start(message):
    temporal_user_form["username"] = message.from_user.username
    lang_markup = telebot.types.InlineKeyboardMarkup()
    en = telebot.types.InlineKeyboardButton('English', callback_data='lang_en')
    rus = telebot.types.InlineKeyboardButton('Russian', callback_data='lang_ru')
    lang_markup.add(en, rus)
    bot.send_message(message.chat.id, text="What's language you prefer?", reply_markup=lang_markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def localization_set(call):
    if call.data == 'lang_en':
        temporal_user_form["language"] = "english"
    elif call.data == 'lang_ru':
        temporal_user_form["language"] = "russian"
    bot.register_next_step_handler(call.message, hello_and_ask_for_num)


def hello_and_ask_for_num(message):
    temporal_local = Localization(temporal_user_form["language"])

    bot.send_message(message.chat.id,
                     text=temporal_local.get_reply_text("before_start"))

    auto_numeration_markup = telebot.types.InlineKeyboardMarkup()

    yes = telebot.types.InlineKeyboardButton(text=temporal_local.get_list_of_inline_buttons()[1],
                                             callback_data='num_yes')
    no = telebot.types.InlineKeyboardButton(text=temporal_local.get_list_of_inline_buttons()[2],
                                            callback_data='num_no')
    auto_numeration_markup.add(yes, no)
    bot.send_message(message.chat.id, text=temporal_local.get_inline_menu_text("num"),
                     reply_markup=auto_numeration_markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('num_'))
def numeration_set(call):
    if call.data == 'num_yes':
        temporal_user_form["num_on"] = 1
    elif call.data == 'num_no':
        temporal_user_form["num_on"] = 0
    bot.register_next_step_handler(call.message, ask_for_date)


def ask_for_date(message):
    temporal_local = Localization(temporal_user_form["language"])
    date_func_markup = telebot.types.InlineKeyboardMarkup()

    yes = telebot.types.InlineKeyboardButton(text=temporal_local.get_list_of_inline_buttons()[1],
                                             callback_data='date_yes')
    no = telebot.types.InlineKeyboardButton(text=temporal_local.get_list_of_inline_buttons()[2],
                                            callback_data='date_no')
    date_func_markup.add(yes, no)
    bot.send_message(message.chat.id, text=temporal_local.get_inline_menu_text("date"),
                     reply_markup=date_func_markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('date_'))
def date_set(call):
    temporal_local = Localization(temporal_user_form["language"])
    if call.data == 'date_yes':
        temporal_user_form["date_on"] = 1
    elif call.data == 'date_no':
        temporal_user_form["date_on"] = 0
    try:
        for k, v in temporal_user_form.items():
            db.insert(val=v, col=k, table="Users")
    except Exception as e:
        bot.send_message(call.chat.id, text=str(e)+"\n"+temporal_local.get_reply_text("error_user"))
        return
    





