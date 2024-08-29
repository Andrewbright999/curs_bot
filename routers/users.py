from aiogram import  Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from users import user_list
from config import ADMIN_LIST
from buttons.inline_buttons import get_callback_buttons, buttons_list



router = Router()


class ChickIn(StatesGroup):
    name_get = State()
    webinar_check_in = State()
    stream_pool = State()

@router.message(Command("start")) 
async def cmd_start(message: Message, state: FSMContext):
    user_list.check_user(message.from_user.id)
    await message.answer("""<b>Приветствую Вас в группе!</b>
                         
Этот чат создан для оповещения всех ее участников о наших встречах, новостях, для получения ссылок и рекомендованного материала.

Благодарю за доверие!

<i>Представьтесь, пожалуйста.</i>
<b>Как Вас зовут?</b>""")
    for admin in ADMIN_LIST:
        await message.forward(chat_id=admin)   
    await state.set_state(ChickIn.name_get)


    
@router.message(ChickIn.name_get)
async def message_with_text(message: Message, state: FSMContext):
    user_list.check_user(message.from_user.id)
    check_in_btn = buttons_list(["Записаться на вебинар✅"], "webinar_check_in_")
    markup = get_callback_buttons(check_in_btn)
    await message.answer(text="""<b>Приятно познакомится!</b>
Нажмите кнопку для записи на вебинар""",reply_markup=markup)
    await state.set_state(ChickIn.webinar_check_in)
    for admin in ADMIN_LIST:
        await message.bot.send_message(chat_id=admin, text=f"ФИО @{message.from_user.username}:")
        await message.forward(chat_id=admin)    
    
@router.callback_query(ChickIn.webinar_check_in) 
async def webinar_check_in(callback: CallbackQuery, state: FSMContext):
    print(callback.data)
    for admin in ADMIN_LIST:
        await callback.bot.send_message(chat_id=admin, text=f"@{callback.from_user.username} записался на вебинар")
    sream_btn = buttons_list(["Хочу участвовать✅","Пока думаю⏳"], "stream_poll_")
    markup = get_callback_buttons(sream_btn)
    await state.set_state(ChickIn.stream_pool)
    await callback.message.edit_text("""<b>Вы записались, на вебинар✅</b>
                                     
Хотим сообщить, что у нас скоро запуск терапевтической группы, хотите ли вы поучавствовать?""")
    await callback.message.edit_reply_markup(reply_markup=markup)

@router.callback_query(ChickIn.stream_pool) 
async def webinar_check_in(callback: CallbackQuery, state: FSMContext):
    answer = callback.data.split("_")[-1]
    await state.clear()
    if answer == "Хочу участвовать✅":
        for admin in ADMIN_LIST:
            await callback.bot.send_message(chat_id=admin, text=f"@{callback.from_user.username} хочет✅ поучавствовать в потоке")
        await callback.message.edit_text("""Отлично, для вас будет 15%, за участие в вебинаре""")
        await callback.message.delete_reply_markup()
        await state.clear()
    elif answer == "Пока думаю⏳":
        for admin in ADMIN_LIST:
            await callback.bot.send_message(chat_id=admin, text=f"@{callback.from_user.username} пока думает⏳")
        wait_btn = buttons_list(["Хочу записаться на поток🖐"], "stream_poll_")
        markup = get_callback_buttons(wait_btn)
        await callback.message.edit_text("""Хорошо, для вас будет действовать <b>15%</b>, до 5 сентября""")
        await callback.message.edit_reply_markup(reply_markup=markup)
        
        
@router.callback_query() 
async def webinar_check_in(callback: CallbackQuery):
    answer = callback.data.split("_")[-1]
    if answer == "Хочу записаться на поток🖐":
        for admin in ADMIN_LIST:
            await callback.bot.send_message(chat_id=admin, text=f"@{callback.from_user.username} подумал и решил поучавствовать в потоке")
        await callback.message.edit_text("""Отлично, вы записались на поток со скидкой 15%""")
        await callback.message.delete_reply_markup()


@router.message(F.text)
async def message_with_text(message: Message):
    print(message.from_user.id)
    user_list.check_user(message.from_user.id)
    for admin in ADMIN_LIST:
        await message.bot.send_message(chat_id=admin, text=f"Сообщение от @{message.from_user.username}:")
        await message.forward(chat_id=admin)
        