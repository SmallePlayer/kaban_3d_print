from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram import F
from aiogram.utils.formatting import (Bold, as_list, as_marked_section)

import time
import cv2
import os

from config import BOT_TOKEN, admin_pes, admin_eg


cap_ender = cv2.VideoCapture(0)
if not cap_ender.isOpened():
    print("Не удалось открыть камеру для Ender 3")
    exit()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

state_first = True
state_second = False

@dp.message(Command("start", "=", prefix="</"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="Первый принтер"),
        types.KeyboardButton(text="Второй принтер")
    )
    builder.row(
        types.KeyboardButton(text="Вкл/Выкл 1"),
        types.KeyboardButton(text="Вкл/Выкл 2")
    )
    builder.row(
        types.KeyboardButton(text="Статус принтеров")
    )
    await message.answer(
        "Выберите действие:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )

@dp.message(F.text == "Первый принтер")
async def status_printr_1(message: types.Message):
    photo = 'neptune.jpg'
    ret, frame = cap_ender.read()
    time.sleep(1)
    if ret:
        cv2.imwrite(photo, frame)
    else:
        print("No ret")
    frame_send = FSInputFile(photo)

    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="<="),
        types.KeyboardButton(text="Вкл/Выкл 1")
    )
    await message.answer_photo(frame_send)
    await message.answer("Включить/Выключить принтер", reply_markup=builder.as_markup(resize_keyboard=True))

@dp.message(F.text == "Вкл/Выкл 1")
async def status_printr_change_1(message: types.Message):
    global state_first
    state_first = not state_first
    await bot.send_message(admin_eg, f"Статус Neptune 4: {state_first}")
    await bot.send_message(admin_pes, f"Статус Neptune 4 : {state_first}")
    #await message.answer(f"Статус Neptune 4: {state_first}")

@dp.message(F.text == "Вкл/Выкл 2")
async def status_printr_change_1(message: types.Message):
    global state_second
    state_second = not state_second
    await bot.send_message(admin_eg, f"Статус Neptune 4: {state_first}")
    await bot.send_message(admin_pes, f"Статус Neptune 4 : {state_first}")
    #await message.answer(f"Статус Ender 3: {state_second}")

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
    #await bot.send_message(admin_eg, **content.as_kwargs())
    #await bot.send_message(admin_pes, **content.as_kwargs())

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
