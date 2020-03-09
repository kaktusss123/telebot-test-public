from telebot.types import ReplyKeyboardMarkup, KeyboardButton

start_markup = ReplyKeyboardMarkup()
start_markup.add(KeyboardButton('Список производителей электроники'))

has_next_markup = ReplyKeyboardMarkup(row_width=1)
has_next_markup.add(KeyboardButton('>>'))
has_next_markup.add(KeyboardButton('Назад'))

no_next_markup = ReplyKeyboardMarkup()
no_next_markup.add(KeyboardButton('Назад'))