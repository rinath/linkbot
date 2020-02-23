from chathandler import ChatInstance, ChatHandler
from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup
import telepot
import sys
import json
import pprint
import urllib3
from tinydb import Query

class Chat(ChatInstance):
	def __init__(self, bot, db, chat_id):
		super().__init__(bot, db, chat_id)
		self.n = 0
	def on_message_received(self, msg):
		text = msg['text']
		table = self.db.table('promocodes')
		q = Query()
		codes = table.get(q.type == 'promocode')
		if text not in codes['codes']:
			self.bot.sendMessage(self.chat_id, 'Я всего лишь бот, и не понимаю, что мне надо сделать! Помнишь, я говорил, подбирать кодовое слово бесполезно?)')
		else:
			self.bot.sendMessage(self.chat_id, 'Новый урок: ' + codes['codes'][text])
#		self.n += 1
#		self.bot.sendMessage(self.chat_id, 'n=%d'%self.n)
	def on_command_received(self, command):
		if command == '/start':
			s = '''Я вижу, ты настроен серьезно! Меня это очень радует)

Но для начала, давай пройдемся по правилам прохождения курса:

1. В этом сообщение тебе пришла ссылка на 1 урок.
2. Как только ты выполнишь первое домашнее задание, и оно будет принято куратором, ты получишь кодовое слово, которое надо ввести сюда ( строка внизу)
3. Если слово введено правильно, ты получишь ссылку на следующий урок и сможешь проходишь обучение дальше.
4. Если слово введено неправильно, я не смогу отправить тебе урок. Подбирать слова бесполезно ( это сделано для того, чтобы ты получил максимальную пользу и обратную связь по урокам)

Лови ссылку на 1 урок и начинай обучение прямо сейчас:

https://youtu.be/UQxbZLkm7uU

Ах да, совсем забыл тебя предупредить - видео-уроки идут в записи, поэтому некоторые временные обозначения могут отличаться.

Удачи!'''
			self.bot.sendMessage(self.chat_id, s)
	def on_callback_received(self, msg):
		print('callback:' + msg['data'])

settings = {}
settings_file = 'settings.json'
def exit():
	print('Put telegram bot\'s token in file %s' % settings_file)
	sys.exit(0)

try:
	with open(settings_file, 'r') as f:
		s = f.read()
		settings = json.loads(s)
		if settings['token'] is None:
			exit()
except FileNotFoundError:
	with open(settings_file, 'w') as f:
		settings = {'token': None, 'use_proxy': False}
		json.dump(settings, f, indent=4)
		exit()

if settings['use_proxy']:
	proxy_url = "http://proxy.server:3128"
	telepot.api._pools = {
	    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
	}
	telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

mybot = ChatHandler(Chat, settings['token'], 'db.json')
mybot.start()