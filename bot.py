from chathandler import ChatInstance, ChatHandler
from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup
import telepot
import sys
import json
import pprint
import urllib3
from tinydb import Query
from datetime import datetime

class Chat(ChatInstance):
	def __init__(self, bot, db, chat_id):
		super().__init__(bot, db, chat_id)
		self.access_granted = False
	def on_message_received(self, msg):
		text = msg['text']
		if not self.access_granted:
			self.bot.sendMessage(self.chat_id, 'У вас нет доступа к этому боту. Чтобы заполучить доступ, обратитесь к Айжан Мазалиевой')
			print('ACCESS DENIED, ' + str(datetime.now()) + ', chat_id: ' + str(self.chat_id) + ', message: ' + text)
			return
		print(str(datetime.now()) + ', chat_id: ' + str(self.chat_id) + ', message: ' + text)
		table = self.db.table('promocodes')
		q = Query()
		codes = table.get(q.type == 'promocode')
		if text not in codes['codes']:
			self.bot.sendMessage(self.chat_id, 'Я всего лишь бот, и не понимаю, что мне надо сделать! Помнишь, я говорил, подбирать кодовое слово бесполезно?)')
		else:
			self.bot.sendMessage(self.chat_id, codes['codes'][text])
#		self.n += 1
#		self.bot.sendMessage(self.chat_id, 'n=%d'%self.n)
	def on_command_received(self, command):
		if not self.access_granted:
			if command == '/start dQw4w9WgXcQ':
				self.access_granted = True
			else:
				return
		print(str(datetime.now()) + ', chat_id: ' + str(self.chat_id) + ', command: ' + command)
		if command.startswith('/start'):
			table = self.db.table('promocodes')
			q = Query()
			codes = table.get(q.type == 'promocode')
			self.bot.sendMessage(self.chat_id, codes['codes']['/start'])
		else:
			self.bot.sendMessage(self.chat_id, 'Неправильная команда. Напишите /start. Я всего лишь бот, и не понимаю, что мне надо сделать! Помнишь, я говорил, подбирать кодовое слово бесполезно?)')
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