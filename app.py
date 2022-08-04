import telebot
from extensions import APIException, Converter
from config import TOKEN, keys

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def helps(message):
    text = "Приветствую, я бот - конвертер валюты!!!\n" \
           "Чтобы начать работу, введите 3(три) параметра через пробел в следующем формате:\n" \
           "1 - <тип валюты>\n2 - <в какую валюту перевести>\n3 - <количество валюты цифрами>\n" \
           "Увидеть список всех доступных валют: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message):
    try:
        vals = message.text.lower().split(' ')
        text = Converter.get_price(vals)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду:\n{e}')
    else:
        bot.send_message(message.chat.id, text)


bot.polling()
