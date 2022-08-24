import time
import config
import random
import cryptocode
from db import engine, Users
from sqlalchemy.orm import Session
from filters import IsAdminFilter
from dispetcher import bot, dp
from aiogram.types.chat_permissions import ChatPermissions
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from aiogram.utils.exceptions import CantRestrictSelf, CantRestrictChatOwner


dp.filters_factory.bind(IsAdminFilter)
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
        session = Session(bind=engine)
        key = random.randint(0, 1000_000)
        tg_id = int(callback_query.message.from_user.id) ^ key
        tg_username = cryptocode.encrypt(str(callback_query.message.from_user.username), bin(key))
        session.add(Users(tg_id=tg_id, tg_username=tg_username, kay_id=key, kay_name=bin(key)))
        session.commit()
        await callback_query.message.reply("Тебе додано до бази 🍉")

    if callback_query.data == "button2" and callback_query.from_user.id == user_id:
        await bot.send_message(callback_query.message.chat.id, f'Русня detected')
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
        await bot.kick_chat_member(chat_id=callback_query.message.chat.id, user_id=callback_query.from_user.id)


@dp.message_handler(is_admin=True, commands=["ban"], commands_prefix="!/")
async def cmd_ban(msg: Message):
    try:
        if not msg.reply_to_message:
            await msg.reply("Команда має бути відповіддю на повідомлення")
            return
        await msg.bot.kick_chat_member(config.group_id, msg.reply_to_message.from_user.id)
        await msg.reply_to_message.reply("Нема тіла, нема діла, юсер блокнутий")
        await msg.bot.delete_message(config.group_id, msg.message_id)
    except CantRestrictSelf:
        await msg.reply("Я краще свого господаря і знаю, що не можу сам себе забанити")
    except CantRestrictChatOwner:
        await msg.reply("Стенд можна перемогти лише стендом, але навіть адміни безсилі проти творця цього чату")


@dp.message_handler(is_admin=True, commands=["mute"], commands_prefix="!/")
async def cmd_mute(msg: Message):
    try:
        if not msg.reply_to_message:
            await msg.reply("Команда має бути відповіддю на повідомлення")
            return
        mute_time = 1
        try:
            if msg["text"].split()[2] == "h":
                mute_time = float(msg["text"].split()[1]) * 3600
            elif msg["text"].split()[2] == "d":
                mute_time = float(msg["text"].split()[1]) * 3600 * 24
            elif msg["text"].split()[2] == "w":
                mute_time = float(msg["text"].split()[1]) * 3600 * 24 * 7
            elif msg["text"].split()[2] == "m":
                mute_time = float(msg["text"].split()[1]) * 3600 * 24 * 30
            elif msg["text"].split()[2] == "y":
                mute_time = float(msg["text"].split()[1]) * 3600 * 24 * 365
        except IndexError:
            mute_time = float(msg["text"].split()[1]) * 60
        await msg.bot.restrict_chat_member(config.group_id, msg.reply_to_message.from_user.id, until_date=time.time() + mute_time)
        await msg.reply_to_message.reply("Посиди і подумай над своєю поведінкою")
        await msg.bot.delete_message(config.group_id, msg.message_id)
    except CantRestrictSelf:
        await msg.reply("Я краще свого господаря і знаю, що не можу сам себе забанити")
    except CantRestrictChatOwner:
        await msg.reply("Стенд можна перемогти лише стендом, але навіть адміни безсилі проти творця цього чату")


@dp.message_handler(is_admin=True, commands=["unmute"], commands_prefix="!/")
async def cmd_unmute(msg: Message):
    if not msg.reply_to_message:
        await msg.reply("Команда має бути відповіддю на повідомлення")
        return
    await bot.restrict_chat_member(msg.chat.id, msg.from_user.id, ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_add_web_page_previews=True,
        can_send_other_messages=True
    ))


@dp.message_handler(commands=["help"], commands_prefix="!/")
async def cmd_help(msg: Message):
    file = open("/app/handlers/help.txt")
    await msg.reply(str(file.read()))
    file.close()


@dp.message_handler(commands=["meow"], commands_prefix="!/")
async def cmd_meow(msg: Message):
    if msg.from_user.id != config.bot_owner:
        await msg.reply("Ця команда лише для пана Діо (Крабіка)")
        return
    await msg.reply("Пане Крабік, я себе гарно вів, сподіваюсь ви задоволені )))")


@dp.message_handler(commands=["add"], commands_prefix="!/")
async def cmd_add(msg: Message):
    session = Session(bind=engine)
    if msg.reply_to_message:
        for i in range(len(session.query(Users).all())):
            if list(session.query(Users).all())[i].tg_id ^ list(session.query(Users).all())[i].kay_id == msg.reply_to_message.from_user.id:
                await msg.reply(f"Цей юзер вже є в базі 🍉")
                break
        else:
            key = random.randint(0, 1000_000)
            tg_id = int(msg.from_user.id) ^ key
            tg_username = cryptocode.encrypt(str(msg.from_user.username), bin(key))
            session.add(Users(tg_id=tg_id, tg_username=tg_username, kay_id=key, kay_name=bin(key)))
            session.commit()
            await msg.reply(f"Юзера @{msg.reply_to_message.from_user.username} додано до бази 🍉 даних")
            return
    for i in range(len(session.query(Users).all())):
        if list(session.query(Users).all())[i].tg_id ^ list(session.query(Users).all())[i].kay_id == msg.from_user.id:
            await msg.reply(f"Ти вже є в базі 🍉")
            break
    else:
        key = random.randint(0, 1000_000)
        tg_id = int(msg.from_user.id) ^ key
        tg_username = cryptocode.encrypt(str(msg.from_user.username), bin(key))
        session.add(Users(tg_id=tg_id, tg_username=tg_username, kay_id=key, kay_name=bin(key)))
        session.commit()
        await msg.reply("Тебе додано до бази 🍉")
        return
