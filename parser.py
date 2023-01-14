import telebot
import requests

bot = telebot.TeleBot('tg bot token')
token = 'vk api token'
version = 5.131
count = 25

def pars(message, idgroup):
    response = requests.get('https://api.vk.com/method/wall.get?',
                            params={
                                'access_token': token,
                                'v': version,
                                'domain': idgroup,
                                'count': count
                            }
                            )
    data = response.json()['response']['items']
    for i, post in reversed(list(enumerate(data))):
        huy = str(i) + \
              '\nавтор: ' + str(post['from_id']) + \
              '\nкомментарии: ' + str(post['comments']['count']) + \
              '\nтекст: ' + str(post['text']) + \
              '\nдата: ' + str(post['date']) + \
              '\nпросмотры: ' + str(post['views']['count'])

        try:
            if len(data[i]['attachments'][0]['photo']) != 0:
                huy += '\n' + str(
                    data[i]['attachments'][0]['photo']['sizes'][- 1]['url'])
        except:
            pass

        bot.send_message(message.chat.id, huy)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Приветствую, {message.from_user.first_name}')
    bot.send_message(message.chat.id, f'Введите id группы')

@bot.message_handler(content_types=['text'])
def main(message):
    pars(message, str(message.text))

bot.polling()