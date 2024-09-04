# -1001820813942 channel id
from typing import Union

from aiogram import  Router
from aiogram.types import Message
from aiogram.filters import BaseFilter
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import CHANNEL_ID



router = Router()


class ChannelFilter(BaseFilter):  # [1]
    def __init__(self, chat_id: Union[str , list , int]): # [2]
        self.chat_id = chat_id

    async def __call__(self, message: Message) -> bool:  # [3]
        if isinstance(self.chat_id, str):
            print(message.chat.id)
            return message.chat.id == self.chat_id
        else:
            return message.chat.id in self.chat_id
        
        

router.message.filter(
    ChannelFilter(chat_id = CHANNEL_ID)
)


@router.channel_post()
async def message_with_text(message: Message):
    post_text = message.text
    start_line = post_text.find("(|")
    end_line = post_text.find("|)")
    print(end_line)
    if (start_line + end_line) > -2:
        line = post_text[start_line+2:end_line]
        post_text = post_text[:start_line]
        await message.edit_text(post_text)
        line = line.split("==")
        link = line[-1].removeprefix(" ")
        print(link)
        caption = line[0]
        inline_kb_list = [
        [InlineKeyboardButton(text=caption, url=link)],
        ]
        kb =  InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
        # urlkb.add(urlButton)
        await message.edit_reply_markup(reply_markup=kb)
        
    # print(post_text)
"(|Записаться == https://t.me/tolgonai_curs_bot|)"


"(|\w\w == \w |)"

"Напишите боту хочу на диагнос"