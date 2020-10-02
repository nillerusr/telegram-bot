#!/usr/bin/python3
from PIL import Image
import VKApi, telebot, os, google
from telebot import types
from utils import *

info = load_json('data/info.json')

vkaudio = VKApi.VKApi( info.vk.token_audio )
bot = telebot.TeleBot(info.telegram.token)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
	bot.reply_to(message, 'Ну здравствуй\nПомощь:\n\n'
		'/audio - поиск аудио в вк\n'
		'/g - поиск изображений в гугле')

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
	if not audios.response.items:
		bot.reply_to(message, "Ничего не найдено!")

@bot.message_handler(commands=['google', 'g'])
def send_images(message):
	imgs=google.search_images(args(message))
	count=0
	m=[]
	files=[]
	for i in imgs:
		if count >= 10: break
		count+=1
		filename = get_random_string(8)
		fname=download_file(i, filename, ['jpeg', 'jpg', 'png', 'jpeg'])
		if fname:
			f=open(fname, 'rb')
			m.append(types.InputMediaPhoto(f))
			files.append(fname)
	if m:
		try:
			bot.send_media_group(message.chat.id, m)
		except Exception as e: print(e)
		for i in files: os.remove(i)


bot.infinity_polling()
