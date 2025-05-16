import json

# Функция для поиска по номеру направления и городу (университеты)
def search_by_direction_and_city(direction_number, city):
    with open('universities_datav3.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    results = []
    for entry in data:
        if entry['Номер направления'] == direction_number and entry['Город'].lower() == city.lower():
            results.append({
                'Университет': entry['Университет'],
                'Тип специальности': entry['Тип специальности']
            })
    return results

# Функция для поиска по номеру направления и городу (колледжи)
def search_by_direction_and_city_college(direction_number, city):
    with open('collage_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    results = []
    for entry in data:
        if entry['Номер направления'] == direction_number and entry['Город'].lower() == city.lower():
            results.append({
                'Колледж': entry['Университет'],  # Используем ключ "Университет" из JSON
                'Тип специальности': entry['Тип специальности']
            })
    return results

# Функция для получения списка всех уникальных городов (университеты)
def get_unique_cities():
    with open('universities_datav3.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Используем словарь для хранения уникальных городов
    cities = {}

    for entry in data:
        city_name = entry.get('Город')  # Используем .get() для безопасного доступа
        if city_name:  # Проверяем, что город не пустой
            cities[city_name.lower()] = city_name  # Ключ — город в нижнем регистре, значение — оригинальное название

    # Возвращаем словарь уникальных городов
    return cities

# Функция для получения списка всех уникальных городов (колледжи)
def get_unique_cities_college():
    with open('collage_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Используем словарь для хранения уникальных городов
    cities = {}

    for entry in data:
        city_name = entry.get('Город')  # Используем .get() для безопасного доступа
        if city_name:  # Проверяем, что город не пустой
            cities[city_name.lower()] = city_name  # Ключ — город в нижнем регистре, значение — оригинальное название

    # Возвращаем словарь уникальных городов
    return cities

# Функция для поиска города в данных университетов
def find_city(city_input):
    cities = get_unique_cities()
    city_input_cleaned = city_input.strip().lower()
    # print(f"Ищем город: {city_input_cleaned}")  # Отладочный вывод
    # print(f"Доступные города: {cities}")  # Отладочный вывод
    if city_input_cleaned in cities:
        return cities[city_input_cleaned]
    else:
        return None

# Функция для поиска города в данных колледжей
def find_city_college(city_input):
    cities = get_unique_cities_college()
    city_input_cleaned = city_input.strip().lower()  # Удаляем пробелы и приводим к нижнему регистру
    if city_input_cleaned in cities:
        return cities[city_input_cleaned]  # Возвращаем оригинальное название города
    else:
        return None