from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InputMediaPhoto, ForceReply
import config
import time
import operator
import buttons
import keyboards
from custom_filters import button_filter, inline_button_filter, reply_text_filter
from weather import get_current_weather, get_forecast
from random_cat import get_random_cat
from database import Database



class Client(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.database = Database() # подключаем базу
    def stop(self, *args, **kwargs):
        self.database.close() # отключаем базу
        return super().stop(*args, **kwargs)


bot = Client(
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    name="my_cool_bot",
)


@bot.on_message(filters=filters.command("start") | button_filter(buttons.back_button))
async def start_command(client: Client, message: Message):
    user = client.database.get_user(message.from_user.id)
    if user is None:
        client.database.create_user(message.from_user.id)
    print(user.__dict__ if user else None)
    await message.reply(f"Hello: {message.from_user.first_name}",
                        reply_markup=keyboards.main_keyboard)


@bot.on_message(filters=filters.command("help") | button_filter(buttons.help_button))
async def help_command(client: Client, message: Message):
    commands = await client.get_bot_commands()
    text_commands = "Список доступных команд:\n\n"
    for command in commands:
        text_commands += f"/{command.command} - {command.description}\n"
    await message.reply(text_commands,
                        reply_markup=keyboards.main_keyboard)


@bot.on_message(filters=filters.command("calc"))
async def calc_command(client: Client, message: Message):
    ops = {
        "+": operator.add, "-": operator.sub,
        "*": operator.mul, "/": operator.truediv,
    }

    if len(message.command) != 4:
        return await message.reply(
            "Неверное количество аргументов\n"
            "Пример использования:\n"
            "/calc 1 + 2\n"
    )
    _, left, op, right = message.command
    op = ops.get(op)
    if op is None:
        return await message.reply("Неизвестный оператор")
    if not left.isdigit() or not right.isdigit():
        return await message.reply("Аргументы должны быть числами")
    left, right = int(left), int(right)
    await message.reply(f"Результат: {op(left, right)}")


@bot.on_message(filters=filters.command("time") | button_filter(buttons.time_button))
async def time_command(client: Client, message: Message):
    current_time = time.strftime("%H:%M:%S")
    await message.reply(f"Текущее время: {current_time}",
                        reply_markup=keyboards.main_keyboard
                        )


@bot.on_message(filters=filters.command("settings") | button_filter(buttons.settings_button))
async def settings_command(client: Client, message: Message):
    await message.reply(
        "Настройки",
        reply_markup=keyboards.settings_keyboard)



@bot.on_message(filters=filters.command('weather'))
async def weather_command(client: Client, message: Message):
    if message.command and len(message.command) > 1:
        city = ' '.join(message.command[1:])
    else:
        user = client.database.get_user(message.from_user.id)
        if user is not None and user.city is not None:
            city = user.city
        else:
            city = "Москва"
    weather = get_current_weather(city)
    await message.reply(weather, reply_markup=keyboards.weather_inline_keyboard)


@bot.on_callback_query(filters=inline_button_filter(buttons.weather_current_inline_button))
async def weather_current_inline_button_callback(client: Client, query: CallbackQuery):
    user = client.database.get_user(query.from_user.id)
    if user is not None and user.city is not None:
        city = user.city
    else:
        city = "Москва"
    weather = get_current_weather(city)
    if weather == query.message.text:
        return
    await query.message.edit_text(
        weather,
        reply_markup=keyboards.weather_inline_keyboard
    )

@bot.on_callback_query(filters=inline_button_filter(buttons.weather_forecast_inline_button))
async def weather_forecast_inline_button_callback(client: Client, query: CallbackQuery):
    city = "Москва"
    weather = get_forecast(city)
    if weather == query.message.text:
        return
    await query.message.edit_text(
        weather,
        reply_markup=keyboards.weather_inline_keyboard
    )

@bot.on_message(filters=filters.command("cats") | button_filter(buttons.cats_button))
async def cats_command(client: Client, message: Message):
    cat = get_random_cat()
    await client.send_photo(
        chat_id=message.chat.id,
       photo=cat,
        reply_markup=keyboards.cats_inline_keyboard,
    ) 

@bot.on_callback_query(filters=inline_button_filter(buttons.cats_inline_button))
async def cats_random_inline_button_callback(client: Client, query: CallbackQuery):
    cat = get_random_cat()
    await query.message.edit_media(
        media=InputMediaPhoto(cat),
        reply_markup=keyboards.cats_inline_keyboard,
    )


change_city_text = f"Меняем город!\n\nНапиши в ответ на это сообщение название своего города, а я его сразу запомню!"



@bot.on_message()
async def echo(client: Client, message: Message):
    await message.reply(message.text)


bot.run()
