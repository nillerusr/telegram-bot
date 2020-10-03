#!/usr/bin/python3
from PIL import Image
import VKApi, telebot, os, re, google
from telebot import types
from utils import *
from urllib.parse import quote, unquote

match_wiki = re.compile('<.*?>')

info = load_json('data/info.json')

vkaudio = VKApi.VKApi( info.vk.token_audio )
vkgroup = VKApi.VKApi( info.vk.token_group, is_group = True)

bot = telebot.TeleBot(info.telegram.token)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
	bot.reply_to(message, 'Ну здравствуй\nПомощь:\n\n'
		'/audio - поиск аудио в вк\n'
		'/g - поиск изображений в гугле\n'
		'/wiki - поиск статьи на википедии\n'
		'/gif - поиск гифок в вк')

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

@bot.message_handler(commands=['wiki'])
def wikipedia(message):
	try:
		a=requests.post('https://ru.wikipedia.org/w/api.php?action=opensearch&format=json&search=%s'%quote(args(message))).json()[1]
		w=requests.get('https://ru.wikipedia.org/w/api.php?action=query&redirects&prop=extracts&format=json&exintro=&titles=%s'%quote(a[0])).json()['query']['pages']
		html=unquote(w[list(w.keys())[0]]['extract'])
		cleantext = 'Страница: https://ru.wikipedia.org/wiki/%s\n   '%a[0].replace(' ','_')
		cleantext += re.sub(match_wiki, '', html)
		if len(a) > 1:
			cleantext += '\n  Похожие запросы: '+'; '.join(a[1:])
		bot.reply_to(message, cleantext)
	except Exception as e:
		print(e)
		bot.reply_to(message, "Ничего не найдено!")

@bot.message_handler(commands=['gif'])
def search_gif(message):
	count = 0
	docs=vkgroup.docs.search(q=args(message), count=200).response.items
	for i in docs:
		if count >= 5: break
		if i.ext == 'gif':
			if (i.size/1024/1024) > 10:
				continue

			fname = get_random_string(8)+'.mp4'
			if download_file(i.url, fname):
				f=open(fname, 'rb')
				bot.send_animation(message.chat.id, f)
				count+=1
				os.remove(fname)
bot.infinity_polling()
