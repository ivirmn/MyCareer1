# faq.py
import telebot
from telebot import types

# faq.py

QUESTIONS_AND_ANSWERS = {
    "faq1": "Что это за портал?",
    "faq2": "Как зарегистрироваться?",
    "faq3": "Как отправить заявку?",
    "faq4": "Как проверить статус заявки?",
    "faq5": "Куда обратиться за дополнительной помощью?",
    "faq6": "Чем хорош наш центр?",
    "back": "Назад"
}

ANSWERS = {
    "faq1": "Это портал, созданный для помощи в поиске работы и стажировок...",
    "faq2": "Чтобы зарегистрироваться, перейдите на наш сайт и следуйте инструкциям...",
    "faq3": "Чтобы отправить заявку, выберите подходящую вакансию и нажмите 'Отправить заявку'...",
    "faq4": "Чтобы проверить статус заявки, войдите в свой аккаунт на нашем сайте и перейдите в раздел 'Мои заявки'...",
    "faq5": "Если у вас возникли дополнительные вопросы, вы можете обратиться в наш центр поддержки...",
    "faq6": "Наш центр предоставляет широкий спектр услуг и возможностей для карьерного роста...",
}


def get_faq_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    for key, question in QUESTIONS_AND_ANSWERS.items():
        if key == "back":
            button = types.InlineKeyboardButton(question, callback_data=f"faq_back")
        else:
            button = types.InlineKeyboardButton(question, callback_data=f"faq_{key}")
        keyboard.add(button)
    return keyboard


def get_answer(question_key):
    return ANSWERS.get(question_key)
