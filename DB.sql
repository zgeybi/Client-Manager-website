-- Создание таблицы клиентов
CREATE TABLE clients (
    id INTEGER PRIMARY KEY,
    account_number TEXT,
    last_name TEXT,
    first_name TEXT,
    middle_name TEXT,
    birth_date DATE,
    inn TEXT,
    responsible_fio TEXT,
    status TEXT DEFAULT 'Не в работе'
);

-- Создание таблицы пользователей
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    fio TEXT,
    login TEXT,
    password TEXT
);
