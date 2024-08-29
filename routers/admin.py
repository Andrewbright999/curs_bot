import datetime
from typing import Union

from aiogram import  Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command, BaseFilter

from config import ADMIN_LIST
from users import user_list, pikle_path



router = Router()


class AdminIdFilter(BaseFilter):  # [1]
    def __init__(self, chat_id: Union[str , list , int]): # [2]
        self.chat_id = chat_id

    async def __call__(self, message: Message) -> bool:  # [3]
        if isinstance(self.chat_id, str):
            print(message.chat.id)
            return message.chat.id == self.chat_id
        else:
            return message.chat.id in self.chat_id
        
        

router.message.filter(
    AdminIdFilter(chat_id = ADMIN_LIST)
)


async def send_save(message: Message): 
    pikle = FSInputFile(path=pikle_path, filename=f"save {datetime.datetime.now()}.pickle")
    await message.bot.send_document(chat_id=ADMIN_LIST[0], document=pikle, caption=f"Сохренение от {datetime.datetime.now()}\nКол-во чел: {len(user_list)}")


@router.message(Command("save")) 
async def cmd_start(message: Message):
    await send_save(message)
    



@router.message()
async def message_with_text(message: Message):
    counter = 0
    for user in user_list:
        try:
            await message.copy_to(chat_id=user)
            counter += 1
        except: 
            pass
    await message.answer(text=f"Сообщение отправлено: {counter} пользователям \n\nВсего пользователей зарегистрировано: {len(user_list)} \n\n{len(user_list) - counter} Заблокировали бота")

        