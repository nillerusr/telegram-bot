#!/usr/bin/python3
import VKApi, telebot, string, random, os
from utils import *

info = load_json('data/info.json')

vkaudio = VKApi.VKApi( info.vk.token_audio )
bot = telebot.TeleBot(info.telegram.token)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
	bot.reply_to(message, "Ну здравствуй\nПомощь:\n")

def get_random_string(length):
	letters = string.ascii_lowercase
	result_str = ''.join(random.choice(letters) for i in range(length))
	return result_str

@bot.message_handler(commands=['audio'])
def send_audio(message):
	audios = vkaudio.audio.search(v=5.63,q=args(message),count=10,sort=2)
	for a in audios.response.items:
		d=vkaudio.audio.getById( audios=str(a.owner_id)+'_'+str(a.id) ).response[0]
		filename = get_random_string(8)+'.mp3'
		if download_file(d.url, filename):
			f=open(filename, 'rb')
			try:
				bot.send_audio(message.chat.id, f, 0, 'test', d.artist+' - '+d.title)
			except: None
			os.remove(filename)

bot.infinity_polling()
