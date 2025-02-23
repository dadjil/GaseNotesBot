import telebot
import datetime
from database_handler import DatabaseHandler
import translate

token = "7542245520:AAFPNt13ZYt8Kf4ZcOixjDTbd42B0ZczC0s"
bot = telebot.TeleBot(token=token)
db = DatabaseHandler()
categories_hints = {}
categories = []


def show_menu(message):
    trans = translate.Translator(db.determine_lang(message.from_user.username), "english")
    main_menu = telebot.types.ReplyKeyboardMarkup()
    emodjis = ["📒","🔍","️️⚙️"]
    buttons_text = ["Add a note", "Find a note", "Settings"]
    for i in range(len(buttons_text)):
        main_menu.add(telebot.types.KeyboardButton(trans.translate(buttons_text[i])+emodjis[i]))
    bot.send_message(message.from_user.id, text=trans.translate("Menu"), reply_markup=main_menu)


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
    if call.data == "lang_english":
        db.insert([call.from_user.username, "english"], ["username", "language"], "Users")
    elif call.data == "lang_russian":
        db.insert("russian", "language", "Users")
    elif call.data == "lang_spanish":
        db.insert("spanish", "language", "Users")
    trans = translate.Translator(db.determine_lang(call.from_user.username), "english")
    bot.send_message(call.message.chat.id,
                     text=trans.translate("Hello again, i am a bot of advanced note adding. Something kind of smart custom database for your needs"))
    bot.send_message(call.message.chat.id,
                     text=trans.translate("So, before we get started, add some traits of each your note. To do this, just write down the name of a trait"))
    bot.send_message(call.message.chat.id,
                     text=trans.translate("To stop the process write a /stop command"))
    bot.register_next_step_handler(call.message, get_category_propose_hint)


def get_category_propose_hint(message):
    global categories_hints, categories
    txt=message.text
    trans = translate.Translator(db.determine_lang(message.from_user.username), "english")
    if message.text !="/stop":
        bot.send_message(message.chat.id,
                         text=f"{message.text} - "+trans.translate("Category was created!"))
        hint_markup = telebot.types.InlineKeyboardMarkup()
        hint_yes = telebot.types.InlineKeyboardButton(text=trans.translate("Yes"), callback_data="hint_yes")
        hint_no = telebot.types.InlineKeyboardButton(text=trans.translate("No"), callback_data="hint_no")
        hint_markup.add(hint_yes, hint_no)
        categories.append(message.text)
        bot.send_message(message.chat.id, text=trans.translate("Do you want to add some hints to such category?"),
                         reply_markup=hint_markup)
    else:
        bot.send_message(message.chat.id,
                         text=trans.translate("Now, when all the required data saved, menu can be showed. If something go wrong just type /menu to see the menu"))
        show_menu(message)

def get_hint(message):
    global categories_hints, categories
    trans = translate.Translator(db.determine_lang(message.from_user.username), "english")
    categories_hints[categories[-1]] = message.text
    bot.send_message(message.chat.id, text=trans.translate("Your hints were added! Go on writing categories"))
    bot.register_next_step_handler(message, get_category_propose_hint)
@bot.callback_query_handler(func=lambda call: call.data == "hint_")
def set_hint(call):
    global categories_hints, categories
    trans = translate.Translator(db.determine_lang(call.from_user.username), "english")
    if call.data == "hint_yes":
        bot.send_message(call.message.chat.id,
                         text=trans.translate("Write comma separated hints (looks like that: hint1, hint2...)"))
        bot.register_next_step_handler(call.message, get_hint)

    elif call.data == "hint_no":
        bot.send_message(call.message.chat.id, text=trans.translate("Ok, go on writing categories"))
        categories_hints[categories[-1]] = []
        bot.register_next_step_handler(call.message, get_category_propose_hint)



bot.infinity_polling()
