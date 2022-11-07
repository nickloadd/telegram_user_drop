import configparser
import json
import csv
# import asyncio

# from pyrogram import Client

from telethon.sync import TelegramClient
from telethon import connection

# для корректного переноса времени сообщений в json
from datetime import date, datetime

# классы для работы с каналами
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest

# Считываем учетные данные
config = configparser.ConfigParser()
config.read("PATH_TO_YOUR_CONFIG.INI")

# Получение списка легитиминых юзеров
legit_users = [] # список легитимных юзеров

with open("PATH_TO_YOUR_CSV_LIST_OF_USERS", 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        for y in row:
          legit_users.append(y)

to_delete = [] # список нелигитимных юзеров

chat_id = 'CHAT_NAME' # идентификатор чата

# Присваиваем значения внутренним переменным
api_id   = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']
#bot_token = config['Telegram']['bot_token']

client = TelegramClient(username, api_id, api_hash)

client.start()

list_usernames = []   # список юзеров в чате

async def dump_all_participants(channel):
	"""Записывает json-файл с информацией о всех участниках канала/чата"""
	offset_user = 0    # номер участника, с которого начинается считывание
	limit_user = 100   # максимальное число записей, передаваемых за один раз

	all_participants = []   # список всех участников канала
	filter_user = ChannelParticipantsSearch('')

	while True:
		participants = await client(GetParticipantsRequest(channel,
			filter_user, offset_user, limit_user, hash=0))
		if not participants.users:
			break
		all_participants.extend(participants.users)
		offset_user += len(participants.users)

	for participant in all_participants:
		list_usernames.append(participant.username)
		
async def main():
	url = input("Введите ссылку на канал или чат: ")
	channel = await client.get_entity(url)
	await dump_all_participants(channel)
	for j in list_usernames:
		if j not in legit_users:
			print("To delete:", j)
			to_delete.append(j)
			#await client.kick_participant(chat_id, j)

with client:
	client.loop.run_until_complete(main())

print(list_usernames)
