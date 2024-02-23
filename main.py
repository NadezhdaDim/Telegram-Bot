import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите комманду боту в следующем формате:\n<имя валюты цену которой он хочет узнать> \
\n<имя валюты в которой надо узнать цену первой валюты> \
\n<количество первой валюты> \nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().split()

        if len(values) != 3:
            raise APIException('Введено неверное количество параметров')


        quote, base, amount = values
        total_base_sum = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
         bot.reply_to(message, f'Ошибка пользователя\n {e}')
    except Exception as e:
         bot.reply_to(message, f'Не удалось обработать команду\n {e}')
    else:
         text = f'Цена {amount} {quote} в {base} - {total_base_sum}'
         bot.send_message(message.chat.id, text)

bot.polling()