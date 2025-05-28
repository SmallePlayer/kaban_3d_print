from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, KeyboardButton
from aiogram import F
from aiogram.utils.formatting import (Bold, as_list, as_marked_section)
import time
import cv2
from config import BOT_TOKEN, admin_pes, admin_eg
from capture import Capture
from mqtt_publisher import pub
import sqlite3
import json


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

state_first = True
state_second = False

def get_id_cam():
    try:
        # Читаем JSON-файл
        with open("cam.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            
        # Выводим список камер
        print("📷 Список камер из JSON:")
        for camera in data["cameras"]:
            print(f"ID: {camera['id']}, Название: {camera['name']}")

    except FileNotFoundError:
        print("❌ Ошибка: Файл cameras.json не найден!")
    except json.JSONDecodeError:
        print("❌ Ошибка: Неправильный формат JSON!")
    except KeyError:
        print("❌ Ошибка: В файле нет ключа 'cameras'!")

def create_photo(photo, id):
    cam = Capture(id_camera=id)
    time.sleep(0.2)
    frame = cam.get_frame()
    if frame is None:
            return

    cv2.imwrite(photo, frame)

@dp.message(Command("start", "=", prefix="</"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()

    # Добавляем 5 кнопок "Принтер 1", "Принтер 2", ..., "Принтер 5" в одну строку
    # for i in range(0, 7):
    #     builder.add(KeyboardButton(text=f"Принтер {i}"))
    builder.add(KeyboardButton(text=f"Принтер {0}"))
    builder.add(KeyboardButton(text=f"Принтер {4}"))
    builder.add(KeyboardButton(text=f"Принтер {6}"))

    builder.adjust(3, 3, 3)
    # Переносим следующую кнопку на новую строку
    builder.row(KeyboardButton(text="Статус принтеров"))

    await message.answer(
        "Выберите действие:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )

@dp.message(F.text.startswith("Принтер"))
async def status_printr_1(message: types.Message):
    printer_number = message.text.split()[1]

    photo = "printer.jpg"
    create_photo(photo, int(printer_number))

    frame_send = FSInputFile(photo)

    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="<="),
        types.KeyboardButton(text=f"Вкл/Выкл {printer_number}")
    )
    builder.row(
        types.KeyboardButton(text=f"Принтер {printer_number}"))

    await message.answer_photo(frame_send)
    await message.answer(f"Включить/Выключить принтер {printer_number}", reply_markup=builder.as_markup(resize_keyboard=True))

@dp.message(F.text.startswith("Вкл/Выкл"))
async def status_printr_change_1(message: types.Message):
    printer_number = message.text.split()[1]
    global state_first
    state_first = not state_first
    pub(state_first)

    await bot.send_message(admin_eg, f"Статус принтера {printer_number}: {state_first}")
    await bot.send_message(admin_pes, f"Статус принтера {printer_number}: {state_first}")
    #await message.answer(f"Статус принтера {printer_number}: {state_first}")


@dp.message(F.text == "Статус принтеров")
async def status_printr_3(message: types.Message):
    content = as_list(
        as_marked_section(
            Bold("Статус принтеров:"),
            f"Принтер Ender 3: {state_first}",
            f"Принтер Neptune 4: {state_second}",
        )
    )
    await message.answer(**content.as_kwargs())

@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Доступные команды:\n/start - Начать работу\n/help - Справка")

@dp.message(Command("hello"))
async def cmd_hello(message: Message):
    chat_id = message.chat.id
    name = message.from_user.full_name
    print(f"{name} = {chat_id}")
    await message.answer(
        f"Привет, {name}"
    )


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
