from typing import Union
from aiogram import  Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from users import user_list
from config import ADMIN_LIST
from buttons.inline_buttons import get_callback_buttons, buttons_list



router = Router()


def send_link(username, chat_id):
    if username:
        return "@"+username
    else:
        return f"https://t.me/{chat_id}"
    
    
async def admin_forward(msg: Union[Message, CallbackQuery], add_msg: str = None, forward: bool = True):
    for admin in ADMIN_LIST:
        try:
            if add_msg:
                await msg.bot.send_message(chat_id=admin, text=add_msg)
            if forward:
                await msg.forward(chat_id=admin)    
        except:
            pass
        
        
class ChickIn(StatesGroup):
    register_name = State()
    webinar_check_in = State()
    stream_pool = State()


@router.message(Command("start")) 
@router.message(F.text.lower() == "диагностика")
async def cmd_start(message: Message, state: FSMContext):
    state.clear()
    uid = message.from_user.id
    username = message.from_user.username
    user_list.check_user(uid)
    await admin_forward(message, add_msg=f"{send_link(username, uid)} Запустил бота", forward=False)
    sream_btn = buttons_list(["Записаться на диагностику✅"], "check_in_")
    markup = get_callback_buttons(sream_btn)
    await message.answer("""<b>Приветствую Вас!</b>
Чтобы записаться на бесплатную диагностику, нажмите кнопку👇""",reply_markup=markup)
    await state.set_state(ChickIn.register_name)
    
    
@router.callback_query(F.data == "check_in_Записаться на диагностику✅")
async def diagnostic_check_in(callback: CallbackQuery, state: FSMContext):
    uid = callback.from_user.id
    username = callback.from_user.username
    await admin_forward(callback.message, add_msg=f"{send_link(username, uid)} записался на диагностику", forward=False )
    await callback.message.edit_text("""Как Вас зовут?""")
    await state.set_state(ChickIn.register_name)


    
@router.message(ChickIn.register_name)
async def message_with_text(message: Message, state: FSMContext):
    await state.clear()
    uid = message.from_user.id
    username = message.from_user.username
    await admin_forward(message, add_msg=f"Имя {send_link(username, uid)}")
    user_list.check_user(uid)
    sream_btn = buttons_list(["Хочу участвовать✅","Пока думаю⏳"], "stream_poll_")
    markup = get_callback_buttons(sream_btn)
#     await message.answer(text="""<b>Приятно познакомиться!</b>

# Я свяжусь с Вами для подбора времени и дня для диагностики.

# Хочу сообщить, что скоро будет запуск терапевтической группы, хотите ли принять участие?""", reply_markup=markup)
    if username == None:
        await message.answer(text="""<b>Благодарю за доверие!</b>
<i>Для проведения согласования времени записи напишите мне</i>: @tolgonai_g

Хочу сообщить, что скоро будет запуск терапевтической группы, хотите ли принять участие?""", reply_markup=markup)
    else:
        await message.answer(text="""<b>Благодарю за доверие!</b>
Я свяжусь с Вами, чтобы предложить доступное время для записи.

Хочу сообщить, что скоро будет запуск терапевтической группы, хотите ли принять участие?""", reply_markup=markup)
    
    


@router.callback_query(F.data.contains("stream_poll_")) 
async def webinar_check_in(callback: CallbackQuery, state: FSMContext):
    username = callback.from_user.username
    chat_id = callback.from_user.id
    answer = callback.data.split("_")[-1]
    await state.clear()
    if answer == "Хочу участвовать✅":
        await admin_forward(callback.message, add_msg=f"{send_link(username, chat_id)} хочет✅ поучавствовать в потоке", forward=False)
        await callback.message.answer("""<b>Благодарю за доверие!<b>
Ожидайте, пожалуйста, Вашу запись""")
        await callback.message.delete_reply_markup()
        await state.clear()
    elif answer == "Пока думаю⏳":
        await admin_forward(callback.message, add_msg=f"{send_link(username, chat_id)} пока думает⏳", forward=False)
        await callback.message.delete_reply_markup()
        wait_btn = buttons_list(["Хочу записаться на поток🖐"], "wait_poll_")
        markup = get_callback_buttons(wait_btn)
        await callback.message.answer("""Обдумайте. Для Вас до 10 сентября будет доступна 15% скидка на участие в группе. Приходите!""",reply_markup=markup)
    if username == None:
        await callback.message.edit_text(text="""<b>Приятно познакомится!</b>
<i>Для проведения согласования времени записи напишите мне</i>: @tolgonai_g""" )
    else:
        await callback.message.edit_text(text="""<b>Приятно познакомится!</b>
Я свяжусь с Вами, чтобы предложить доступное время для записи.""")
        
        
@router.callback_query(F.data.contains("wait_poll_")) 
async def webinar_check_in(callback: CallbackQuery):
    username = callback.from_user.username
    chat_id = callback.from_user.id
    await admin_forward(callback.message, add_msg=f"{send_link(username, chat_id)} подумал и решил поучавствовать в потоке", forward=False)
    await callback.message.edit_text("""<b>Благодарю за доверие!<b>
Ожидайте, пожалуйста, Вашу запись""")
    if username == None:
        await callback.message.answer(text="<i>Для проведения диагностики напишите мне</i>: @tolgonai_g")
    await callback.message.delete_reply_markup()


@router.message(F.text)
async def message_with_text(message: Message):
    username = message.from_user.username
    chat_id = message.from_user.id
    print(message.from_user.id)
    user_list.check_user(message.from_user.id)
    await admin_forward(message, add_msg=f"{send_link(username, chat_id)} отправил сообщение")
        
        