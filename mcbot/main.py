import json

import requests
import telebot
from requests.auth import HTTPBasicAuth
from telebot import types
from telebot.async_telebot import AsyncTeleBot
from log import setup_logger, delete_old_logs
from faq import QUESTIONS_AND_ANSWERS, get_faq_keyboard, get_answer
import config
from config import *
bot = AsyncTeleBot(config.token)
#bot = telebot.TeleBot(config.token)
logger = setup_logger(__name__)



@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    site_url_button = types.InlineKeyboardButton("Наш сайт", url='https://vsucareer.ru')
    tg_url_button = types.InlineKeyboardButton("Наша группа в Telegram", url='https://t.me/vsucareer')
    start_help_button = types.InlineKeyboardButton("Помощь", callback_data='help')  # Кнопка "Помощь" с callback_data
    markup.add(site_url_button, tg_url_button, start_help_button)
    bot.send_message(message.chat.id, "Здравствуйте, {0.first_name}! "
                                      "Выберите подходящий пункт)".format(message.from_user), reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'help':  # Если нажата кнопка "Помощь"
        bot.answer_callback_query(callback_query_id=call.id, text="")
        markup = get_faq_keyboard()
        bot.send_message(call.message.chat.id, "Часто задаваемые вопросы:", reply_markup=markup)
    elif call.data.startswith('faq_'):
        question_key = call.data.split('_')[1]
        answer = get_answer(question_key)
        bot.answer_callback_query(callback_query_id=call.id, text="")
        bot.send_message(call.message.chat.id, f"{QUESTIONS_AND_ANSWERS[question_key]}:\n{answer}")

@bot.callback_query_handler(func=lambda call: True)
def callback_query_faq(call):
    if call.data == 'faq':  # Если нажата кнопка "Помощь"
        bot.answer_callback_query(callback_query_id=call.id, text="")
        markup = get_faq_keyboard()
        bot.send_message(call.message.chat.id, "Часто задаваемые вопросы:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('faq_'))
def callback_query_answer(call):
    question_key = call.data.split('_')[1]
    answer = get_answer(question_key)
    bot.answer_callback_query(callback_query_id=call.id, text="")
    bot.send_message(call.message.chat.id, f"{QUESTIONS_AND_ANSWERS[question_key]}:\n{answer}")


@bot.message_handler(commands=['faq'])
def faq_command(message):
    bot.send_message(message.chat.id, "Часто задаваемые вопросы:")


@bot.message_handler(commands=['button'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Кнопка")
    markup.add(item1)
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)

@bot.message_handler(commands=['create_demand'])
def create_demand(message):
    telegram_id = message.from_user.id
    bot.send_message(message.chat.id, 'Пожалуйста, укажите цель заявки.')
    bot.register_next_step_handler(message, process_target, telegram_id)

def process_target(message, telegram_id):
    target = message.text

    data = {
        'telegram_id': telegram_id,
        'target': target
    }
    url = f'{DJANGO_API_URL}/api/api/create_demand/'
    response = requests.post(url, auth=HTTPBasicAuth(drf_login, drf_password), data=json.dumps(data), headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            bot.send_message(message.chat.id, f'Заявка с целью {result["demand"]["target"]} создана успешно.'
                                              f'\n Номер заявки: {result["demand"]["id"]}')
        else:
            bot.send_message(message.chat.id, f'Ошибка: {result.get("error")}')
    else:
        bot.send_message(message.chat.id, 'Ошибка сервера. Попробуйте немного позже.'
                                          '\n Если ошибка не исчезает, свяжитесь с Центром карьеры')


@bot.message_handler(commands=['active_demands'])
def send_active_demands(message):
    telegram_id = message.from_user.id
    url = f'{DJANGO_API_URL}/api/user/{telegram_id}/demands/'

    response = requests.get(url, auth=HTTPBasicAuth(drf_login, drf_password))

    if response.status_code == 200:
        demands = response.json()
        if demands:
            for demand in demands:
                text = (f"Заявка: {demand['target']}\n"
                        f"Дата создания: {demand['date_created']}\n"
                        f"Стадия: {demand['stage']}\n"
                        f"Результат: {demand['result']}\n")
                bot.send_message(telegram_id, text)
        else:
            bot.send_message(telegram_id, "У вас нет активных заявок.")
    else:
        bot.send_message(telegram_id, "Произошла ошибка при получении данных. Пожалуйста, попробуйте позже.")


@bot.message_handler(commands=['active_demands'])
def send_active_demands(message):
    telegram_id = message.from_user.id
    url = f'{DJANGO_API_URL}/api/user/{telegram_id}/demands/'

    response = requests.get(url, auth=HTTPBasicAuth(drf_login, drf_password))

    if response.status_code == 200:
        demands = response.json()
        if demands:
            for i, demand in enumerate(demands, start=1):
                text = (f"Заявка {i}:\n"
                        f"Заявка: {demand['target']}\n"
                        f"Дата создания: {demand['date_created']}\n"
                        f"Стадия: {demand['stage']}\n"
                        f"Результат: {demand['result']}\n\n")

                markup = types.InlineKeyboardMarkup()
                button = types.InlineKeyboardButton(text="Удалить",
                                                    callback_data=f"delete_{demand['id']}_{demand['target']}")
                markup.add(button)

                bot.send_message(telegram_id, text, reply_markup=markup)
        else:
            bot.send_message(telegram_id, "У вас нет активных заявок.")
    else:
        bot.send_message(telegram_id, "Произошла ошибка при получении данных. Пожалуйста, попробуйте позже.")


@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_'))
def confirm_delete(call):
    _, demand_id, demand_target = call.data.split('_')
    demand_id = int(demand_id)

    markup = types.InlineKeyboardMarkup(row_width=2)
    button_yes = types.InlineKeyboardButton(text="Да", callback_data=f"confirm_delete_yes_{demand_id}")
    button_no = types.InlineKeyboardButton(text="Нет", callback_data="confirm_delete_no")
    markup.add(button_yes, button_no)

    bot.send_message(call.message.chat.id,
                     f"Вы действительно хотите удалить заявку #{demand_id} с целью {demand_target}?",
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('confirm_delete_yes_'))
def delete_demand(call):
    demand_id = int(call.data.split('_')[-1])
    url = f'{DJANGO_API_URL}/api/demand/{demand_id}/'

    response = requests.delete(url, auth=HTTPBasicAuth(drf_login, drf_password))

    if response.status_code == 204:
        bot.send_message(call.message.chat.id, "Заявка успешно удалена.")
    else:
        bot.send_message(call.message.chat.id, "Произошла ошибка при удалении заявки. Пожалуйста, попробуйте позже.")


@bot.callback_query_handler(func=lambda call: call.data == 'confirm_delete_no')
def cancel_delete(call):
    bot.send_message(call.message.chat.id, "Удаление отменено.")

if __name__ == '__main__':
    bot.polling(none_stop=True)

bot.infinity_polling()

if __name__ == '__main__':
    delete_old_logs()

    # @bot.callback_query_handler(func=lambda call: True)
    # def callback_query(call):
    #     if call.data == 'help':  # Если нажата кнопка "Помощь"
    #         bot.answer_callback_query(callback_query_id=call.id, text="")
    #         markup = types.InlineKeyboardMarkup(row_width=1)
    #         faq_button = types.InlineKeyboardButton("Часто задаваемые вопросы", callback_data='faq')
    #         markup.add(faq_button)
    #         bot.send_message(call.message.chat.id, "Список доступных команд:\n/help - Помощь")
    #
    #
    # @bot.message_handler(commands=['help'])
    # def help_command(message):
    #     markup = types.InlineKeyboardMarkup(row_width=1)
    #     faq_button = types.InlineKeyboardButton("Часто задаваемые вопросы", callback_data='faq')
    #     markup.add(faq_button)
    #     bot.send_message(message.chat.id, "Список доступных команд:\n/help - Помощь")
