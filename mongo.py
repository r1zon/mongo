import csv
import re
from pymongo import MongoClient
import pymongo
from datetime import datetime

def read_data(artists_collection):
	with open('artists.csv', encoding='utf-8', newline='') as csvfile:
		tickets_csv = csv.DictReader(csvfile, delimiter=',')
		tickets_list = list(tickets_csv)
		for i in tickets_list:
			i['Цена'] = int(i['Цена'])
			i['Дата'] = '2020.'+i['Дата']
			i['Дата'] = datetime.strptime(i['Дата'], '%Y.%d.%m')
			print(i)
		header = tickets_list.pop(0)
		result = artists_collection.insert_many(tickets_list)

def show_tickets(artists_collection):
	for i in artists_collection.find():
		print(i['Дата'])
		print(i)

def find_cheapest(artists_collection):
	for i in artists_collection.find().sort('Цена', pymongo.ASCENDING):
		print(i)

def find_by_name(name, artists_collection):
	regex = re.compile(r"{}".format(name), re.IGNORECASE)
	for i in artists_collection.find({'Исполнитель': regex}).sort('Цена', pymongo.ASCENDING):
		print(i)

def add_new(artist, price, place, date, artists_collection):
	ticket = {'Исполнитель': artist,
			  'Цена': price,
			  'Место': place,
			  'Дата': date
	}
	ticket['Дата'] = '2020.' + ticket['Дата']
	ticket['Дата'] = datetime.strptime(ticket['Дата'], '%Y.%d.%m')
	result = artists_collection.insert_one(ticket)

def find_tickets_inrange(start_date, finish_date, artists_collection):
	for i in artists_collection.find({'Дата': {'$gte': start_date, '$lte': finish_date}}).sort('Дата', pymongo.ASCENDING):
		print(i)

def main():
	client = MongoClient()
	tickets_db = client['tickets']
	artists_collection = tickets_db['artists']
	while True:
		next = input('Выберите команду:\n'
					 'a - добавить файл в базу данных\n'
					 'an - добавить новые билеты в базу\n'
					 's - показать таблицу билетов\n'
					 'sp - отсортировать по возрастанию цены\n'
					 'f - найти билеты по исполнителю\n'
					 'ft - найти билеты по дате\n'
					 'd  - очистить базу\n'
					 'q - выйти из программы\n')
		if next == 'a':
			read_data(artists_collection)
		if next == 'an':
			artist = input('Введите исполнителя\n')
			price = int(input('Введите стоимость\n'))
			place = input('Введите место проведения\n')
			date = input('Введите дату\n')
			add_new(artist, price, place, date, artists_collection)
		if next == 's':
			show_tickets(artists_collection)
		if next == 'ft':
			start_date, finish_date = input('Введите через пробел границы диапазона дат для поиска\n').split()
			start_date = '2020.' + start_date
			finish_date = '2020.' + finish_date
			start_date = datetime.strptime(start_date, '%Y.%d.%m')
			finish_date = datetime.strptime(finish_date, '%Y.%d.%m')
			print(finish_date)
			print(start_date)
			find_tickets_inrange(start_date, finish_date, artists_collection)
		if next == 'sp':
			find_cheapest(artists_collection)
		if next == 'f':
			name = input('Начните вводить имя исполнителя:\n')
			find_by_name(name,artists_collection)
		if next == 'd':
			artists_collection.remove()
		if next == 'q':
			break

if __name__ == '__main__':
	main()