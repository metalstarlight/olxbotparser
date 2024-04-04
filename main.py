import logging
import asyncio
from config import URL, DRIVER_PATH
from db import checkUserSync, init_db, checkUser
from olxparser import get_parsed_elements
import bot

# Update olx every 30 seconds
UPDATE_EVERY = 30

isConnectionOkFlag = True
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
mainUser = None

async def botSchedule():
        global mainUser
        while True:
            bot.messageExt = await checkUser()
            mainUser = bot.messageExt
            if bot.messageExt is not None :
                await bot.send_expresses(bot.messageExt) #chatid
            await asyncio.sleep(3)


async def scheduled(wait_for, parser, checkConnection=None):
        global mainUser
        while(True):
            try:
                await parser(URL)
                await checkConnection(mainUser)
                await asyncio.sleep(wait_for)
            except Exception as e:
                print(f"Exception is: {e}")
                pass


async def checkConnection(userId):
    try:
        reader, writer = await asyncio.open_connection('google.com', 80)
        writer.close()
        await writer.wait_closed()
        logging.info('Connection is OK')
        # if mainUser is not None:
        #     await bot.checkConnection(userId) # Отключил чтоб не заёбывал
        return True
    except OSError as err:
        logging.warning(f'CONNECTION LOST! : {err}\n')
        return False

async def main():
    logging.info('Parser started')
    # loop = asyncio.get_event_loop()
    # loop.create_task(       
    #     scheduled(wait_for = 30, parser = await get_parsed_elements(URL), botSchedule=await botSchedule())
    # )
    # bot.executor.start_polling(dispatcher=bot.dp, on_startup=bot.on_startup, skip_updates=True)
    
            
    await asyncio.gather(bot.dp.start_polling(),
                        scheduled(wait_for = UPDATE_EVERY, parser = get_parsed_elements, 
                                  checkConnection = checkConnection), botSchedule())
    # try:
    #     await asyncio.wait_for(taskCreate, timeout=35)
    # except asyncio.CancelledError:
    #     print('EXCEPTION! CANCELLED: Request was cancelled')
    # except asyncio.TimeoutError:
    #     print('EXCEPTION! TIMED OUT: Request took too long')
    

if __name__ == "__main__":
    init_db()
    mainUser = checkUserSync()
    asyncio.get_event_loop().run_until_complete(main())