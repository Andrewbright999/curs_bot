from typing import List
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_callback_buttons(btns: List[str]):
    keyboard = InlineKeyboardBuilder()
    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text,callback_data=data))
    return keyboard.adjust(1).as_markup()

def buttons_list(btn_list, prefix):
    btns = {}
    for btn in btn_list:
        btns[btn] = prefix+btn
    return btns