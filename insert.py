from faker import Faker
import psycopg2
import pandas as pd

fake = Faker('ru_RU')

conn = psycopg2.connect(
    dbname='mydatabase',
    user='postgres',
    password='',
    host='localhost',
    port='5432'
)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS clients (
    id SERIAL PRIMARY KEY,
    account_number TEXT,
    last_name TEXT,
    first_name TEXT,
    middle_name TEXT,
    birth_date DATE,
    inn TEXT,
    responsible_fio TEXT,
    status TEXT DEFAULT 'Не в работе'
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    fio TEXT,
    login TEXT,
    password TEXT
)
''')

users = []
for _ in range(10):
    fio = fake.name()
    login = fake.user_name()
    password = fake.password()
    users.append((fio, login, password))
    cursor.execute('INSERT INTO users (fio, login, password) VALUES (%s, %s, %s)', (fio, login, password))

for _ in range(50):
    account_number = fake.bban()
    last_name = fake.last_name()
    first_name = fake.first_name()
    middle_name = fake.middle_name()
    birth_date = fake.date_of_birth(minimum_age=18, maximum_age=90).isoformat()
    inn = 1
    responsible_fio = fake.random_element(users)[0]
    cursor.execute('INSERT INTO clients (account_number, last_name, first_name, middle_name, birth_date, inn, responsible_fio) VALUES (%s, %s, %s, %s, %s, %s, %s)', (account_number, last_name, first_name, middle_name, birth_date, inn, responsible_fio))

print(pd.read_sql('SELECT * FROM users', conn))
print(pd.read_sql('SELECT * FROM clients', conn))
conn.commit()
conn.close()
