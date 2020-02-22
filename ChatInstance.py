import telepot
from telepot.loop import MessageLoop

class ChatInstance:
	def initialize(self, token):
		self.bot = telepot.Bot(token)
	def __set_state__(self, state):
		pass

class Chat(ChatInstance):
	def start(self):
		MessageLoop()