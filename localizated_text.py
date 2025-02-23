from translate import Translator
class Localization:
    def __init__(self, language="english"):
        self.__language = language
        self.__translator = Translator(from_lang="english", to_lang=language)
        self.__menu_buttons = ["Add a note", "Settings", "Find for a category", "Get an CSV"]
        self.__inline_buttons = ["No", "Yes"]

        self.__inline_menus = {"date": "Do you want to add a default date function?",
                             "num": "Do you want to add numeration to CSV file output?",
                             "hint": "Do you want to add hints for a category?",
                             "user_submit": "All is right?"
                              }

        self.__replies = {"guid_over": "Ok, when preparations over, you can see a menu (/menu)",
                          "before_start": "Before we get start, answer some questions",
                          "error_user": "Please, repeat the user creation process"
                          }

    def get_list_of_translated_menu(self):
        return [self.__translator.translate(el) for el in self.__menu_buttons]

    def get_list_of_inline_buttons(self):
        return [self.__translator.translate(el) for el in self.__inline_buttons]

    def get_inline_menu_text(self, option):
        if option in self.__inline_buttons:
            return self.__translator.translate(self.__inline_buttons[option])
        else:
            print(f"{option} is not in inline menu list")

    def get_reply_text(self, option):
        if option in self.__replies:
            return self.__translator.translate(self.__replies[option])
        else:
            print(f"{option} is not in inline menu list")


