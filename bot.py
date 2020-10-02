#!/usr/bin/python3
import VKApi
import telebot

info = load_json('data/info.json')

vkaudio = VKApi.VKApi( info.vk.token_audio )
bot = telebot.TeleBot(info.telegram.token)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
	bot.reply_to(message, "Ну здравствуй")

bot.infinity_polling()
