from chathandler import ChatInstance, ChatHandler
from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup

class Chat(ChatInstance):
	def __init__(self, bot, chat_id=0):
		super().__init__(bot, chat_id)
		self.n = 0
	def on_message_received(self, msg):
		self.n += 1
		self.bot.sendMessage(self.chat_id, f'n={self.n}')
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

mybot = ChatHandler(Chat, '1002235702:AAHNyEsp3KbkAvfXPygmNNmZ-4BVItaPtWs', 'db.json')
mybot.start()