from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime, timedelta
from collections import defaultdict
import telebot

from constants import *
from keyboards import *

bot = telebot.TeleBot(TOKEN)

offset = defaultdict(lambda _: 1)  # Будем хранить смещение по списку в CHUNK_SIZE
msg_ids = {}  # id сообщения со старым списком, необходимо для удаления


@bot.message_handler(commands=['start', 'help'])
def start(msg: Message) -> None:
    """Обработчик для /start и /help
    Приветствует юзера и отправляет ему клавиатуру для показа списка
    
    :param msg: сообщение
    :type msg: Message
    """
    bot.send_message(msg.chat.id, TIMES[((
        datetime.now() + timedelta(hours=1)).hour) // 6], reply_markup=start_markup)


@bot.message_handler(func=lambda msg: msg.text == 'Список производителей электроники')
def show_list(msg: Message) -> None:
    """Показывает первую часть списка и отправляет клавиатуу для показа следующей части
    
    :param msg: сообщение
    :type msg: Message
    """
    offset[msg.chat.id] = 1
    new_msg = bot.send_message(msg.chat.id, '\n'.join(map(lambda t: f'{t[0]}){t[1]}', enumerate(ELECTRONICS_LIST[:CHUNK_SIZE], 1))), reply_markup=has_next_markup if len(
        ELECTRONICS_LIST) > offset[msg.chat.id] * CHUNK_SIZE else no_next_markup)
    msg_ids[msg.chat.id] = new_msg.message_id


@bot.message_handler(func=lambda msg: msg.text == '>>' and offset[msg.chat.id] * CHUNK_SIZE < len(ELECTRONICS_LIST))
def show_next(msg: Message) -> None:
    """Показывает следующую часть списка, удаляет предыдущее сообщение 
    и отправляет клавиатуру для показа следующей части
    
    :param msg: сообщение
    :type msg: Message
    """
    bot.delete_message(msg.chat.id, msg_ids[msg.chat.id])
    msg_ids[msg.chat.id] = bot.send_message(msg.chat.id, '\n'.join(map(lambda t: f'{t[0]}){t[1]}', enumerate(ELECTRONICS_LIST[offset[msg.chat.id] * CHUNK_SIZE: (offset[msg.chat.id]+1) * CHUNK_SIZE], offset[msg.chat.id] * CHUNK_SIZE + 1))), reply_markup=has_next_markup if len(
        ELECTRONICS_LIST) > (offset[msg.chat.id] + 1) * CHUNK_SIZE else no_next_markup).message_id
    offset[msg.chat.id] += 1


@bot.message_handler(func=lambda msg: msg.text == 'Назад')
def go_back(msg: Message) -> None:
    """Обработчик кнопки "Назад", Возвращает на приветствие
    
    :param msg: сообщение
    :type msg: Message
    """
    start(msg)


@bot.message_handler(func=lambda _: True)
def default(msg: Message) -> None:
    """Обработчик всех остальных сообщений, не подошедших под верхние функции
    Ничего не делает
    
    :param msg: сообщение
    :type msg: Message
    """
    bot.send_message(msg.chat.id, 'Команда не распознана')


bot.polling(none_stop=True)
