import time
import cofig
from dispetcher import bot, dp
from aiogram.types.chat_permissions import ChatPermissions
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message


inline_btn_1 = InlineKeyboardButton('Звичайно Український', callback_data='button1')
inline_btn_2 = InlineKeyboardButton('російський', callback_data='button2')
inline_kb = InlineKeyboardMarkup(row_width=2).add(inline_btn_1, inline_btn_2)
user_id: int = 0


@dp.message_handler(content_types=["new_chat_members"])
async def on_user_joined(message: Message):
    global user_id
    user_id = message.new_chat_members[-1].id
    await bot.restrict_chat_member(message.chat.id, message.new_chat_members[-1].id, until_date=time.time() + 32000000)
    await message.delete()
    await message.answer("Для того, що б писати у чат треба відповісти на питання")
    await message.answer(f"Чий Крим, @{message.new_chat_members[0].username} ?", reply_markup=inline_kb)


@dp.callback_query_handler()
async def process_callback_button(callback_query: CallbackQuery):
    global user_id
    await bot.answer_callback_query(callback_query.id)
    if callback_query.data == "button1" and callback_query.from_user.id == user_id:
        await bot.send_message(callback_query.message.chat.id, f'Українця знайдено, думку схвалено')
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
        await bot.restrict_chat_member(callback_query.message.chat.id, callback_query.from_user.id, ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_add_web_page_previews=True,
            can_send_other_messages=True
        ))

    if callback_query.data == "button2" and callback_query.from_user.id == user_id:
        await bot.send_message(callback_query.message.chat.id, f'Русня detected')
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
        await bot.kick_chat_member(chat_id=callback_query.message.chat.id, user_id=callback_query.from_user.id)


@dp.message_handler(is_admin=True, commands=["ban"], commands_prefix="!/")
async def cmd_ban(msg: Message):
    if not msg.reply_to_message:
        await msg.reply("Команда має бути відповіддю на повідомлення")
        return
    await msg.bot.delete_message(cofig.group_id, msg.message_id)
    await msg.bot.kick_chat_member(cofig.group_id, msg.reply_to_message.from_user.id)
    await msg.reply_to_message.reply("Нема тіла, нема діла, юсер блокнутий")


@dp.message_handler(is_admin=True, commands=["mute"], commands_prefix="!/")
async def cmd_mute(msg: Message):
    if not msg.reply_to_message:
        await msg.reply("Команда має бути відповіддю на повідомлення")
        return
    mute_time = float(msg.split()[1]) * 60
    await msg.bot.delete_message(cofig.group_id, msg.message_id)
    await msg.bot.restrict_chat_member(cofig.group_id, msg.reply_to_message.from_user.id, until_date=time.time() + mute_time)
    await msg.reply_to_message.reply("Посиди і подумай над своєю поведінкою")
