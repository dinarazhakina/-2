import logging
import time
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Мок-база данных студентов
students_db = {
    "Сарызин Илья": {
        "Математика": {"посещаемость": 0, "баллы": 0, "последнее_обновление": time.time()},
        "Физика": {"посещаемость": 0, "баллы": 0, "последнее_обновление": time.time()},
    },
    "Жакина Динара": {
        "Математика": {"посещаемость": 100, "баллы": 100, "последнее_обновление": time.time()},
        "Физика": {"посещаемость": 100, "баллы": 100, "последнее_обновление": time.time()},
    },
    "Фельдт Андрей": {
        "Математика": {"посещаемость": 0, "баллы": 0, "последнее_обновление": time.time()},
        "Физика": {"посещаемость": 0, "баллы": 0, "последнее_обновление": time.time()},
    },
    "Наурзбаева Альбина": {
        "Математика": {"посещаемость": 100, "баллы": 100, "последнее_обновление": time.time()},
        "Физика": {"посещаемость": 100, "баллы": 100, "последнее_обновление": time.time()},
    },
    "Шабанов Руслан": {
        "Математика": {"посещаемость": 0, "баллы": 0, "последнее_обновление": time.time()},
        "Физика": {"посещаемость": 0, "баллы": 0, "последнее_обновление": time.time()},
    },
    "Гергерт Анна": {
        "Математика": {"посещаемость": 100, "баллы": 100, "последнее_обновление": time.time()},
        "Физика": {"посещаемость": 100, "баллы": 100, "последнее_обновление": time.time()},
    },
    "Москавчук Александр": {
        "Математика": {"посещаемость": 0, "баллы": 0, "последнее_обновление": time.time()},
        "Физика": {"посещаемость": 0, "баллы": 0, "последнее_обновление": time.time()},
    },
    "Назарова Анастасия": {
        "Математика": {"посещаемость": 100, "баллы": 100, "последнее_обновление": time.time()},
        "Физика": {"посещаемость": 100, "баллы": 100, "последнее_обновление": time.time()},
    },
    "Вольнов Кирилл": {
        "Математика": {"посещаемость": 0, "баллы": 0, "последнее_обновление": time.time()},
        "Физика": {"посещаемость": 0, "баллы": 0, "последнее_обновление": time.time()},
    },
    "Зданникова Алина": {
        "Математика": {"посещаемость": 100, "баллы": 100, "последнее_обновление": time.time()},
        "Физика": {"посещаемость": 100, "баллы": 100, "последнее_обновление": time.time()},
    }
}

# Инициализация бота
bot = Bot(token="7688345230:AAGUovjbhRHRBOy_1fpVltWymrJGcxH1Rp4")
dp = Dispatcher()


def get_student_info(student_name: str, subject: str = None) -> str:
    """Генерация информации о студенте"""
    if student_name not in students_db:
        return "Студент не найден"

    if subject:
        if subject not in students_db[student_name]:
            return "Дисциплина не найдена"

        data = students_db[student_name][subject]
        last_update = time.strftime("%d.%m.%Y %H:%M", time.localtime(data["последнее_обновление"]))
        return (
            f"📊 {student_name} | {subject}\n"
            f"✅ Посещаемость: {data['посещаемость']}%\n"
            f"🏆 Баллы: {data['баллы']}/100\n"
            f"🔄 Обновлено: {last_update}"
        )
    else:
        info = f"📚 Студент: {student_name}\n\n"
        for subj, data in students_db[student_name].items():
            info += f"📖 {subj}: {data['баллы']} баллов ({data['посещаемость']}% посещаемости)\n"
        return info


@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Обработка команды /start"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Моя успеваемость")],
            [KeyboardButton(text="Список студентов")]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "👋 Добро пожаловать в систему учета успеваемости!\n"
        "Выберите действие:",
        reply_markup=keyboard
    )


@dp.message(lambda message: message.text == "Список студентов")
async def list_students(message: Message):
    """Показать список студентов"""
    students = "\n".join(students_db.keys())
    await message.answer(f"🎓 Список студентов:\n{students}")


@dp.message(lambda message: message.text == "Моя успеваемость")
async def ask_student_name(message: Message):
    """Запрос ФИ студента"""
    await message.answer("Введите ФИ студента:")


@dp.message()
async def process_student_request(message: Message):
    """Обработка запросов об успеваемости"""
    text = message.text

    # Проверяем, является ли запрос именем студента
    if text in students_db:
        student_info = get_student_info(text)
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                         [KeyboardButton(text=f"{text}|{subject}")]
                         for subject in students_db[text].keys()
                     ] + [[KeyboardButton(text="Назад")]],
            resize_keyboard=True
        )

        await message.answer(student_info, reply_markup=keyboard)
    elif "|" in text:
        # Запрос по конкретному предмету
        student_name, subject = text.split("|", 1)
        if student_name in students_db and subject in students_db[student_name]:
            await message.answer(get_student_info(student_name, subject))
        else:
            await message.answer("Данные не найдены")
    elif text == "Назад":
        await cmd_start(message)
    else:
        await message.answer("Команда не распознана")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    logger.info("Бот запускается...")
    import asyncio

    asyncio.run(main())