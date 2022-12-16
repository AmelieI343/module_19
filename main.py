import telebot
from config import keys, TOKEN
from extensions import CurrencyConverter, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands = ['start','help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, f"You can convert the required amount of currency.\n"
                                      f"Available currencies: /values\n"
                                      f"Please enter the command in the format: \n<Base currency>"
                                      f" <Quote currency> <Amount of base currency>")

@bot.message_handler(commands = ['values'])
def handle_values(message):
    text = "Доступные валюты"
    for key in keys.keys():
        text = '\n'.join((text,key, ))
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Number of parameters should be 3')
        base, quote, amount = values
        total = CurrencyConverter().get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'User\'s error.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Command is unknown.\n{e}')
    else:
        text = f'Price {amount} {base} in {quote} = {total}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)

