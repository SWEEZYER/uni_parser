import asyncio
import re
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart
from aiogram.types import Message
from university_parser import search_by_direction_and_city, get_unique_cities, find_city, \
    search_by_direction_and_city_college, get_unique_cities_college, find_city_college

router = Router()


# Определяем состояния
class SearchStates(StatesGroup):
    WAITING_FOR_ACTION = State()  # Ожидание действия (поиск или список городов)
    WAITING_FOR_TYPE = State()  # Ожидание выбора типа учебного заведения (университет или колледж)
    WAITING_FOR_DIRECTION = State()  # Ожидание номера направления
    WAITING_FOR_CITY = State()  # Ожидание города


# Регулярное выражение для проверки формата направления (например, 09.03.04)
direction_pattern = re.compile(r"^\d{2}\.\d{2}\.\d{2}$")


# Обработчик старта
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(
        "Приветствую! Выберите, что хотите сделать:\n"
        "1️⃣ Найти учебные заведения по направлению и городу\n"
        "2️⃣ Получить список доступных городов\n\n"
        "Напишите 1 для поиска учебных заведений или 2 для списка городов."
    )
    await state.set_state(SearchStates.WAITING_FOR_ACTION)


# Обработчик выбора действия (поиск или список городов)
@router.message(SearchStates.WAITING_FOR_ACTION)
async def handle_action_choice(message: Message, state: FSMContext):
    choice = message.text.strip()
    await state.update_data(action_choice=choice)  # Сохраняем выбор действия

    if choice == '1':
        await message.answer("Выберите тип учебного заведения:\n1️⃣ Университет\n2️⃣ Колледж")
        await state.set_state(SearchStates.WAITING_FOR_TYPE)
    elif choice == '2':
        await message.answer("Выберите тип учебного заведения для списка городов:\n1️⃣ Университет\n2️⃣ Колледж")
        await state.set_state(SearchStates.WAITING_FOR_TYPE)
    else:
        await message.answer("Пожалуйста, выберите действие: напишите 1 для поиска или 2 для списка городов.")


@router.message(SearchStates.WAITING_FOR_TYPE)
async def handle_type_choice(message: Message, state: FSMContext):
    choice = message.text.strip()
    await state.update_data(type_choice=choice)  # Сохраняем выбор типа учебного заведения

    user_data = await state.get_data()
    action_choice = user_data.get('action_choice')  # Получаем сохраненный выбор действия

    if action_choice == '1':  # Если пользователь выбрал поиск
        if choice == '1' or choice == '2':
            await message.answer("Отлично! Введите номер направления (например, 37.03.01):")
            await state.set_state(SearchStates.WAITING_FOR_DIRECTION)
        else:
            await message.answer(
                "Пожалуйста, выберите тип учебного заведения: напишите 1 для университета или 2 для колледжа.")
    elif action_choice == '2':  # Если пользователь выбрал список городов
        if choice == '1':
            cities = get_unique_cities()
            city_list = list(cities.values())  # Преобразуем значения словаря в список
        elif choice == '2':
            cities = get_unique_cities_college()
            city_list = list(cities.values())  # Преобразуем значения словаря в список
        else:
            await message.answer(
                "Пожалуйста, выберите тип учебного заведения: напишите 1 для университета или 2 для колледжа.")
            return

        # Разбиваем список городов на части, если он слишком длинный
        chunk_size = 400  # Количество городов в одном сообщении
        city_chunks = [city_list[i:i + chunk_size] for i in range(0, len(city_list), chunk_size)]

        for i, chunk in enumerate(city_chunks, start=1):
            city_list_str = ', '.join(chunk)
            await message.answer(f"Часть {i} из {len(city_chunks)}:\n\n{city_list_str}")
            await asyncio.sleep(1)  # Пауза в 1 секунду между сообщениями

        # После вывода списка городов сбрасываем состояние
        await state.set_state(SearchStates.WAITING_FOR_ACTION)
        await message.answer(
            "Теперь выберите, что хотите сделать:\n"
            "1️⃣ Найти учебные заведения\n"
            "2️⃣ Список городов"
        )


# Обработчик ввода направления
@router.message(SearchStates.WAITING_FOR_DIRECTION)
async def handle_direction(message: Message, state: FSMContext):
    direction_number = message.text.strip()

    if not direction_pattern.match(direction_number):
        await message.answer("Пожалуйста, введите номер направления в правильном формате (например, 09.03.04).")
        return

    await state.update_data(direction_number=direction_number)
    await message.answer("Теперь введите город, в котором хотите найти учебные заведения.")
    await state.set_state(SearchStates.WAITING_FOR_CITY)


# Обработчик ввода города
@router.message(SearchStates.WAITING_FOR_CITY)
async def handle_city(message: Message, state: FSMContext):
    city_input = message.text.strip()

    if not city_input:
        await message.answer("Пожалуйста, введите название города.")
        return

    user_data = await state.get_data()
    type_choice = user_data.get('type_choice')

    if type_choice == '1':
        city = find_city(city_input)
    else:
        city = find_city_college(city_input)

    if not city:
        await message.answer(f"Такого города ({city_input}) нет в нашей базе данных.\n\n"
                             "Выберите, что хотите сделать:\n"
                             "1️⃣ Найти учебные заведения\n"
                             "2️⃣ Список городов")
        await state.set_state(SearchStates.WAITING_FOR_ACTION)
        return

    direction_number = user_data.get('direction_number')

    if type_choice == '1':
        results = search_by_direction_and_city(direction_number, city)
    else:
        results = search_by_direction_and_city_college(direction_number, city)

    if results:
        response = f"Найдено {len(results)} учебных заведений по направлению {direction_number} в городе {city}:\n\n"
        messages = []
        for result in results:
            entry = f"🎓 <b>{result['Университет'] if type_choice == '1' else result['Колледж']}</b>\n📚 Тип подготовки: {result['Тип специальности']}\n\n"

            if len(response) + len(entry) > 4000:
                messages.append(response)
                response = ""

            response += entry

        messages.append(response)

        for msg in messages:
            await message.answer(msg, parse_mode="HTML")
    else:
        await message.answer(
            f"По направлению {direction_number} в городе {city} учебных заведений не найдено.\n\n"
        )

    await state.set_state(SearchStates.WAITING_FOR_ACTION)
    await message.answer(
        "Теперь выберите, что хотите сделать:\n"
        "1️⃣ Найти учебные заведения\n"
        "2️⃣ Список городов"
    )


# Обработка неожиданных сообщений
@router.message()
async def handle_unexpected_message(message: types.Message):
    await message.answer(
        "Пожалуйста, выберите действие из меню. Напишите 1 для поиска учебных заведений или 2 для списка городов."
    )
