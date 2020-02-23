import telepot
import time
from pprint import pprint
from telepot.loop import MessageLoop
from tinydb import TinyDB, Query
from tinydb.middlewares import CachingMiddleware
from tinydb.storages import JSONStorage
import sys
import signal

class ChatHandler:
	def __init__(self, Chat_class, token, db_filename):
		self.bot = telepot.Bot(token)
		self.db = TinyDB(db_filename, storage=CachingMiddleware(JSONStorage))
		self.chat = Chat_class(self.bot, self.db, 0)
		self.Chat_class = Chat_class
	def start(self):
		signal.signal(signal.SIGINT, self.sigint_handler)
		MessageLoop(self.bot, {'chat': self.handle_message, 'callback_query': self.handle_callback}).run_as_thread()
		while 1:
			time.sleep(0.007)
	def handle_message(self, msg):
		chat_id = msg['chat']['id']
		doc_id = self.load(chat_id)
		if len(msg['text']) > 1 and msg['text'][0] == '/' and msg['text'][1] != ' ':
			self.chat.on_command_received(msg['text'])
		else:
			self.chat.on_message_received(msg)
		self.backup(doc_id, chat_id)
	def handle_callback(self, msg):
		chat_id = msg['message']['chat']['id']
		doc_id = self.load(chat_id)
		self.chat.on_callback_received(msg)
		self.backup(doc_id, chat_id)
	def load(self, chat_id):
		q = Query()
		db_table = self.db.table('chats')
		item = db_table.get(q.chat_id == chat_id)
		if item is None:
			self.chat = self.Chat_class(self.bot, self.db, chat_id)
			return None
		else:
			self.chat.__setstate__(dict(item))
			return item.doc_id
	def backup(self, doc_id, chat_id):
		d = self.chat.__getstate__()
		db_table = self.db.table('chats')
		if doc_id is None:
			db_table.insert(d)
		else:
			db_table.write_back(documents=[d], doc_ids=[doc_id])
	def sigint_handler(self, signum, frame):
		self.db.close()
		print('SIGINT caught, closing database...')
		sys.exit(0)

class ChatInstance:
	def __init__(self, bot, db, chat_id):
		self.db = db
		self.bot = bot
		self.chat_id = chat_id
	def on_message_received(self, msg):
		raise NotImplementedError
	def on_command_received(self, msg):
		raise NotImplementedError
	def on_callback_received(self, msg):
		raise NotImplementedError
	def __getstate__(self):
		return {k: v for k, v in self.__dict__.items() if k != 'bot' and k != 'db'}
	def __setstate__(self, state):
		self.__dict__.update(state)