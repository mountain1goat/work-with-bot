import telebot
from telebot import types
import config
import requests
import sqlite3

# business entertainment general health science sports technology

def createSubs (cursor,connect, id_user, id_cat) :
    sql = "INSERT INTO subscriptions (id_user, id_cat) VALUES (:id_user, :id_cat)";
    cursor.execute(sql, {
        'id_user': id_user,
        'id_cat': id_cat}
    )
    connect.commit()

def deleteSubs(cursor, connect, id_user, id_cat):
	sql = "DELETE FROM subscriptions WHERE id_user=:id_user AND id_cat=:id_cat"
	cursor.execute(sql, {
		'id_user': id_user,
		'id_cat': id_cat}
				   )
	connect.commit()

def foundSub (cursor,connect, id_user, id_cat) :
	sql = "SELECT subscriptions.* FROM subscriptions WHERE id_user = :id_user AND id_cat=:id_cat"
	result = cursor.execute(sql, {'id_user': id_user, 'id_cat': id_cat}).fetchone()
	connect.commit()
	return result

def showCats (cursor,connect) :
	result = cursor.execute("SELECT categories.* FROM categories").fetchall()
	connect.commit()
	return result

def showSubs (cursor, connect, id_user) :
	sql = "SELECT subscriptions.id_cat FROM subscriptions WHERE id_user=:id_user"
	result = cursor.execute(sql, {'id_user': id_user}).fetchall()
	connect.commit()
	return result

connect = sqlite3.connect('users.db', check_same_thread=False)
cursor = connect.cursor()

bot = telebot.TeleBot(config.bot_token)


def subs(id_us, id_cat):
	res = foundSub(cursor, connect, id_us, id_cat)
	if res == None:
		createSubs(cursor, connect, id_us, id_cat)
		bot.send_message(id_us, 'Вы подписаны!')
	else:
		bot.send_message(id_us, 'Вы уже подписаны на эту категорию!')

def outSubs(id_us, id_cat):
	res = foundSub(cursor, connect, id_us, id_cat)
	if res == None:
		bot.send_message(id_us, 'Вы не подписаны на эту категорию!')
	else:
		deleteSubs(cursor, connect, id_us, id_cat)
		bot.send_message(id_us, 'Вы отписаны!')


@bot.message_handler(commands=['start'])
def start(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	btn1 = types.KeyboardButton("👋 Поздороваться")
	btn2 = types.KeyboardButton("📰 Узнать новости")
	btn3 = types.KeyboardButton("⚙ Функции")
	btn4 = types.KeyboardButton("❓ Что я могу?")
	markup.add(btn1, btn2, btn3, btn4)
	bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я бот для просмотра новостей".format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def func(message):
	if (message.text == "👋 Поздороваться"):
		bot.send_message(message.chat.id, text="Привеет.. Спасибо что читаешь наши новости!)")
	elif (message.text == "⚙ Функции"):
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		btn1 = types.KeyboardButton("Мои подписки")
		btn2 = types.KeyboardButton("Подписаться")
		btn3 = types.KeyboardButton("Отписаться")
		back = types.KeyboardButton("Назад")
		markup.add(btn1, btn2, btn3, back)
		bot.send_message(message.chat.id, text="Выбери функцию ↓", reply_markup=markup)

	elif (message.text == "Мои подписки"):
		bot.send_message(message.from_user.id, 'Ваши подписки ↓')
		news = showCats(cursor, connect)
		text = ''
		for i in news:
			if foundSub(cursor, connect, message.from_user.id, i[0]) != None :
				cat = 'нет'
				if i[1] == 'business':
					cat = 'Бизнес'
				elif i[1] == 'entertainment':
					cat = 'Досуг'
				elif i[1] == 'general':
					cat = 'Общие'
				elif i[1] == 'health':
					cat = 'Здоровье'
				elif i[1] == 'science':
					cat = 'Наука'
				elif i[1] == 'sports':
					cat = 'Спорт'
				elif i[1] == 'technology':
					cat = 'Техналогии'

				text += cat + "\n"
				bot.send_message(message.from_user.id, text)
				text = ''

	elif (message.text == "Подписаться"):
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		btn1 = types.KeyboardButton("На Бизнес")
		btn2 = types.KeyboardButton("На Досуг")
		btn3 = types.KeyboardButton("На Общие")
		btn4 = types.KeyboardButton("На Здоровье")
		btn5 = types.KeyboardButton("На Наука")
		btn6 = types.KeyboardButton("На Спорт")
		btn7 = types.KeyboardButton("На Технологии")
		back = types.KeyboardButton("Назад")
		markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, back)
		bot.send_message(message.chat.id, text="Категории ↓", reply_markup=markup)

	elif (message.text == "Отписаться"):
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		btn1 = types.KeyboardButton("От Бизнес")
		btn2 = types.KeyboardButton("От Досуг")
		btn3 = types.KeyboardButton("От Общие")
		btn4 = types.KeyboardButton("От Здоровье")
		btn5 = types.KeyboardButton("От Наука")
		btn6 = types.KeyboardButton("От Спорт")
		btn7 = types.KeyboardButton("От Технологии")
		back = types.KeyboardButton("Назад")
		markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, back)
		bot.send_message(message.chat.id, text="Категории ↓", reply_markup=markup)

	# подписаться на категорию
	elif (message.text == "На Бизнес"):
		id_us = message.from_user.id
		id_cat = 3
		subs(id_us, id_cat)
	elif (message.text == "На Досуг"):
		id_us = message.from_user.id
		id_cat = 1
		subs(id_us, id_cat)
	elif (message.text == "На Общие"):
		id_us = message.from_user.id
		id_cat = 2
		subs(id_us, id_cat)
	elif (message.text == "На Здоровье"):
		id_us = message.from_user.id
		id_cat = 4
		subs(id_us, id_cat)
	elif (message.text == "На Наука"):
		id_us = message.from_user.id
		id_cat = 5
		subs(id_us, id_cat)
	elif (message.text == "На Спорт"):
		id_us = message.from_user.id
		id_cat = 6
		subs(id_us, id_cat)
	elif (message.text == "На Технологии"):
		id_us = message.from_user.id
		id_cat = 7
		subs(id_us, id_cat)
	# отписаться от категории
	elif (message.text == "От Бизнес"):
		id_us = message.from_user.id
		id_cat = 3
		outSubs(id_us, id_cat)
	elif (message.text == "От Досуг"):
		id_us = message.from_user.id
		id_cat = 1
		outSubs(id_us, id_cat)
	elif (message.text == "От Общие"):
		id_us = message.from_user.id
		id_cat = 2
		outSubs(id_us, id_cat)
	elif (message.text == "От Здоровье"):
		id_us = message.from_user.id
		id_cat = 4
		outSubs(id_us, id_cat)
	elif (message.text == "От Наука"):
		id_us = message.from_user.id
		id_cat = 5
		outSubs(id_us, id_cat)
	elif (message.text == "От Спорт"):
		id_us = message.from_user.id
		id_cat = 6
		outSubs(id_us, id_cat)
	elif (message.text == "От Технологии"):
		id_us = message.from_user.id
		id_cat = 7
		outSubs(id_us, id_cat)

	elif (message.text == "📰 Узнать новости"):
		bot.send_message(message.from_user.id, 'Новости ↓')

		cats = showCats(cursor, connect)
		for k in cats:
			if foundSub(cursor, connect, message.from_user.id, k[0]) != None:
				a = requests.get(f'https://newsapi.org/v2/top-headlines?apiKey={config.ap_key}&country=ru&category={k[1]}&pageSize=1')
				news = []
				for i in a.json()['articles']:
					news.append([i['title'], i['publishedAt'], i['url']])
				text = ''
				for i in news:
					text += i[0] + "\n" + i[1] + "\n" + i[2]
					bot.send_message(message.from_user.id, text)
					text = ''

		bot.send_message(message.from_user.id, 'вот и все все новости на сегодня')

	elif message.text == "❓ Что я могу?":
		bot.send_message(message.chat.id, text="👋 Поздароваться")
		bot.send_message(message.chat.id, text="📰 Узнать новости")
		bot.send_message(message.chat.id, text="Подписаться на конкретные категории новостей (⚙ Функции)")
		bot.send_message(message.chat.id, text="Отписаться от категории новостей (⚙ Функции)")
		bot.send_message(message.chat.id, text="Просмотреть свои подписки (⚙ Функции)")
		bot.send_message(message.chat.id, text="А что еще нужно?😏")

	elif (message.text == "Назад"):
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		button1 = types.KeyboardButton("👋 Поздороваться")
		button2 = types.KeyboardButton("📰 Узнать новости")
		button3 = types.KeyboardButton("⚙ Функции")
		button4 = types.KeyboardButton("❓ Что я могу?")
		markup.add(button1, button2, button3, button4)
		bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
	else:
		bot.send_message(message.chat.id, text="На такую комманду я не запрограммирован..")


bot.polling()
cursor.close()