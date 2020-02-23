from chathandler import ChatInstance, ChatHandler
from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup
import sys
import json
import pprint

class Chat(ChatInstance):
	def __init__(self, bot, chat_id=0):
		super().__init__(bot, chat_id)
		self.n = 0
	def on_message_received(self, msg):
		self.n += 1
		self.bot.sendMessage(self.chat_id, 'n=%d'%self.n)
	def on_command_received(self, command):
		if command == '/start':
			s = '''🏻 Привет, я чат-бот курса «Сам себе SMM» от Айжан Мазалиевой!
⠀
💪🏻Я рад видеть людей, которые хотят развиваться, достигать целей и всегда открыты новому!
⠀
Это фундаментальные принципы,которых мы придерживаемся, и раз ты тут - мы единомышленники💫
⠀
Чтобы начать обучение, нажми кнопку « старт»👇🏻'''
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
	print('except')
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