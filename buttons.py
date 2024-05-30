from pyrogram.types import KeyboardButton
from pyrogram import emoji
from pyrogram.types import KeyboardButton, InlineKeyboardButton

weather_button = KeyboardButton("Погода")
back_button = KeyboardButton(f"{emoji.BACK_ARROW} Назад")
time_button = KeyboardButton(f"{emoji.ALARM_CLOCK} Время")
help_button = KeyboardButton(f"{emoji.WHITE_QUESTION_MARK} Помощь")
settings_button = KeyboardButton(f"{emoji.GEAR} Настройки")
cats_button = KeyboardButton(f"{emoji.CAT} Котики")
change_city_button = KeyboardButton(f"{emoji.CITYSCAPE} Сменить город")
weather_current_inline_button = InlineKeyboardButton(f"{emoji.FIVE_O_CLOCK} Погода сейчас", "weather_current")
weather_forecast_inline_button = InlineKeyboardButton(f"{emoji.CALENDAR} Прогноз погоды", "weather_forecast")
cats_inline_button = InlineKeyboardButton(f"{emoji.CAT} Котики", "cats")