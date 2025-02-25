import telebot
import datetime
from database_handler import DatabaseHandler
from translate import Translator

token = "7542245520:AAFPNt13ZYt8Kf4ZcOixjDTbd42B0ZczC0s"
bot = telebot.TeleBot(token=token)
db = DatabaseHandler()


def for_user_translate(name, mes):
    return Translator(to_lang=db.determine_lang(name)).translate(mes)


def show_menu(message):
    main_menu = telebot.types.ReplyKeyboardMarkup()
    emodjis = ["📒", "🔍", "️️⚙️"]
    buttons_text = ["Add a note", "Find a note", "Settings"]
    for i in range(len(buttons_text)):
        main_menu.add(telebot.types.KeyboardButton(
            text=str(for_user_translate(message.from_user.username, buttons_text[i]) + emodjis[i])))
    bot.send_message(message.from_user.id, text=for_user_translate(message.from_user.username, "Menu"),
                     reply_markup=main_menu)


@bot.message_handler(commands=['start'])
def start(message):
    lang_markup = telebot.types.InlineKeyboardMarkup()
    lang_english = telebot.types.InlineKeyboardButton("English", callback_data="lang_english")
    lang_russian = telebot.types.InlineKeyboardButton("Russian", callback_data="lang_russian")
    lang_spanish = telebot.types.InlineKeyboardButton("Spanish", callback_data="lang_spanish")
    lang_markup.add(lang_english, lang_russian, lang_spanish)
    bot.send_message(message.chat.id, text=f"Hello {message.from_user.first_name}, what language you prefer?",
                     reply_markup=lang_markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("lang_"))
def lang_set(call):
    name = str(call.from_user.username)
    if call.data == "lang_english":
        db.add_user(name, "en")
    elif call.data == "lang_russian":
        db.add_user(name, "ru")
    elif call.data == "lang_spanish":
        db.add_user(name, "es")

    bot.send_message(call.message.chat.id,
                     text=for_user_translate(call.message.from_user.username,
                                             "Hello again, I am a bot for advanced note adding. Something like a smart custom database for your needs"))
    bot.send_message(call.message.chat.id,
                     text=for_user_translate(call.message.from_user.username,
                                             "So, before we get started, add some traits for each of your notes. To do this, just write down the name of a trait"))
    bot.send_message(call.message.chat.id,
                     text=for_user_translate(call.message.from_user.username,
                                             "To stop the process, write the /stop command"))
    bot.register_next_step_handler(call.message, get_category_propose_hint)


temporal_category_storage = ""


def get_category_propose_hint(message):
    global temporal_category_storage

    if message.text != "/stop":
        temporal_category_storage = message.text
        propose_hint_markup = telebot.types.InlineKeyboardMarkup()
        yes_hint = telebot.types.InlineKeyboardButton(text=for_user_translate(message.from_user.username, "Yes"),
                                                      callback_data="hint_yes")
        no_hint = telebot.types.InlineKeyboardButton(text=for_user_translate(message.from_user.username, "No"),
                                                     callback_data="hint_no")
        propose_hint_markup.add(yes_hint, no_hint)
        bot.send_message(message.chat.id,
                         text=for_user_translate(message.from_user.username, "Do you want to add some hints to such category?"),
                         reply_markup=propose_hint_markup)
    else:
        bot.send_message(message.chat.id, text=for_user_translate(message.from_user.username,
                                                                  "Ok, when all those steps done, enjoy notes"))
        bot.send_message(message.chat.id,
                         text=for_user_translate(message.from_user.username,
                                                                  "Litle reminder: you can get a menu by a /menu command"))
        show_menu(message)


def hint_set(message):
    global temporal_category_storage
    db.add_hints_and_category(message.from_user.username, temporal_category_storage, message.text)
    temporal_category_storage = ""

    bot.send_message(message.chat.id,
                     text=for_user_translate(message.from_user.username,
                                             "Ok your hints were saved, go on writing categories..."))
    bot.register_next_step_handler(message, get_category_propose_hint)


@bot.callback_query_handler(func=lambda call: call.data.startswith("hint_"))
def hint_fork(call):
    global temporal_category_storage
    if call.data == "hint_yes":
        bot.send_message(call.message.chat.id,
                         text=for_user_translate(call.message.from_user.username,
                                                 "Write down hints, separated by commas (hint, hint ...)"))
        bot.register_next_step_handler(call.message, hint_set)
    elif call.data == "hint_no":
        db.add_category(call.message.from_user.username, temporal_category_storage)
        temporal_category_storage = ""
        bot.send_message(call.message.chat.id,
                         text=for_user_translate(call.message.from_user.username,
                                                 "Ok your hints were saved, go on writing categories..."))
        bot.register_next_step_handler(call.message, get_category_propose_hint)


bot.infinity_polling()