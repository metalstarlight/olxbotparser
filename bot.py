from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from config import TOKEN_API
from db import KawaExpress, addAndUpdateuser, checkUser, getIfBotIsActivated
import aioschedule
import db
from datetime import datetime

bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot=bot)
Bot.set_current(bot)
kb = ReplyKeyboardMarkup(resize_keyboard=True) #передать аргументы
isBotActivated: bool = False
#kb.add(KeyboardButton('/help'))
help_button = KeyboardButton('/start')
description_button = KeyboardButton('/description')
update_button = KeyboardButton('/update')

kb.add(help_button).insert(description_button).insert(update_button)
messageExt = None

HELP_COMMAND = """ 
/help - список команд 
/start - начать работу с ботом
/description - описание бота
/sticker - отправить стикер
/image - отправлю тебе картинку
/location - отправить локацию
"""
DESCRIPTION = """Бот для поиска на olx экспрессов KRUPS. \nВ разработке."""


async def on_startup(_):    # не запускается автоматом
    global isBotActivated, mainUser
    userList = await checkUser()
    mainUser = userList[0]
    print("""\n    ***********
    Bot has been started
    ***********""")


@dp.message_handler(commands=['start'])  # описываем команду для обработки
async def start_command(message: types.Message):  # type: ignore
    await message.answer('Активирована автоматическая отправка объявлений (/start - старт, /stop - остановить )')
    global isBotActivated
    global messageExt
    messageExt = message
    await addAndUpdateuser(userTypesMessage=message, isActivatedBot=True)
    isBotActivated = True
    await message.delete()


@dp.message_handler(commands=['help'])  # описываем команду для обработки
async def help_command(message: types.Message):
    await message.reply(HELP_COMMAND, reply_markup=kb)
    await message.delete()

@dp.message_handler(commands=['stop'])  # описываем команду для обработки
async def help_command(message: types.Message):
    global isBotActivated
    isBotActivated = False
    addAndUpdateuser(userTypesMessage=message, isActivatedBot=False)
    await message.reply('Отправка остановлена ( /start - возобновить)', reply_markup=ReplyKeyboardRemove())
    await message.delete()

# декоратор, включающий дополнительное поведение
@dp.message_handler(commands=['image'])
# types - обязательно передавать тип message
async def echo_rand(messaga: types.Message):
    # if messaga.text.count(' ') >= 1:
    #     pass                            # ответить при наличии не менее двух слов (проходим мимо)
    # #randChar = chr(random.randint(0, 1000))  # chr() - из числа в символ, ord() - символ в число
    # await messaga.answer(text=random.choice(string.ascii_letters)) # написать сообщение. не reply
    # await bot.send_message(chat_id=messaga.chat.id, text="Hey there!") # если юзаем message.chat.id то то же самое что message.answer
    # если message.from_user.id - то отвечает бот только в личку
    await bot.send_photo(chat_id=messaga.chat.id, photo='https://i.ytimg.com/vi/EXOhOzMZ8qI/hqdefault.jpg', reply_markup=kb)
    await messaga.delete()


@dp.message_handler(commands=['update'])
async def send_expresses(message: types.Message):
    # выберите все записи из базы данных, где isSentToTelegram равно False
    isBotActivated = await getIfBotIsActivated()
    if isBotActivated == True:
        expresses = KawaExpress.select().where(KawaExpress.isSentToTelegram == False)
        # отправить каждую запись пользователю и обновить поле isSentToTelegram
        # if expresses is None:
        #     text = f'Новых пока нет'
        #     await bot.send_message(message if type(message) is int else message.chat.id, text)
        for separateExpress in expresses:
            # создать сообщение с информацией о записи
            #await bot.send_photo(message.chat.id, photo=separateExpress.image)
            text = f'Название: {separateExpress.title}\nЦена: --------------  {separateExpress.price}  --------------\nГде: {separateExpress.whereAndDate}\n{separateExpress.url}'
            await bot.send_message(message if type(message) is int else message.chat.id, text)
            print(datetime.now().strftime("%d-%m-%Y %H:%M:%S"),"    New xpress has been sent for id: ", message if type(message) is int else message.chat.id)
            # обновите поле isSentToTelegram для этой записи
            separateExpress.isSentToTelegram = True
            separateExpress.save()
            
            
@dp.message_handler()
async def checkConnection(chatId):
    await bot.send_message(chatId, "Connection is OK")