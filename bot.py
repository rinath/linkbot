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
	def on_message_received(self, msg):
		text = msg['text']
		print('chat_id: ' + str(self.chat_id) + ', message: ' + text)
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
		print('chat_id: ' + str(self.chat_id) + ', command: ' + command)
		if command == '/start':
			table = self.db.table('promocodes')
			q = Query()
			codes = table.get(q.type == 'promocode')
			self.bot.sendMessage(self.chat_id, codes['codes']['/start'])
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