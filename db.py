from peewee import *
import json

db = SqliteDatabase('olx.db')

class BaseModel(Model):
    class Meta:
        database = db
        
        
class KawaExpress(BaseModel):
    title = CharField()
    price = CharField(null=True)
    whereAndDate = CharField(null=True)
    url = CharField()
    isSentToTelegram = BooleanField()
    image = BlobField(null=True)
    
    class Meta:
        table_name = 'kawa_express'

class TgUserId(BaseModel):
    userId = CharField()
    isActivatedBot = BooleanField()
    class Meta:
        table_name = 'tg_user_id'
    
    
    
db.connect()
db.create_tables([KawaExpress, TgUserId])

class SearchModel(BaseModel): # Пока не нужно, это для поиска по запросу из телеги
    title = CharField()
    chatid = CharField()
    
    
def find_all_expresses():
    return KawaExpress.select()

def find_id_search(chat_id):
    return SearchModel.select().where(SearchModel.chatid == chat_id) #чтобы отвечать конкретному юзеру, выбирает ключевые слова конкретного пользователя по чат_ид

def find_all_searches():
    return SearchModel.select()

#--------------------ДОБАВЛЕНИЕ ДАННЫХ и ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ--------------------
async def process_search_model(message):
    pass
    

def init_db():
    db.create_tables([KawaExpress, TgUserId])     #передаём модели в базу данных под которые будем создавать
    
async def process_add_express(title, price, whereAndDate, url, image:bytes=None, chat_id=None):
    imgBinary = image
    card_exist = True
    try:
        card = KawaExpress.select().where(KawaExpress.url == url).get()
    except DoesNotExist:
        card_exist = False

    if not card_exist:
        rec = KawaExpress(title=title, 
                          price = price, 
                          whereAndDate = whereAndDate, 
                          url=url, 
                          image=image,
                          isSentToTelegram=False)
        rec.save()
async def addAndUpdateuser(userTypesMessage, isActivatedBot, updateInfo:bool = False):
    try:
        if not updateInfo:
            tgUserId = TgUserId(userId=userTypesMessage, isActivatedBot=isActivatedBot)
            tgUserId.save()
        else:
            user = TgUserId.get(userId=userTypesMessage)
            user.isActivatedBot = isActivatedBot
            user.save()
    except Exception as e:
        print('Error when adding a user to the database or updating: ', e)

async def checkUser():
    try:
        mainUser = TgUserId.select().where(TgUserId.isActivatedBot == True).get()
        pyMainUser = json.loads(mainUser.userId)
        return int(pyMainUser['from']['id'])
    except Exception as e:
        print('It seems there is no users exists: ', e)
        return
    
async def getIfBotIsActivated() -> bool:
    user = TgUserId.select().where(TgUserId.isActivatedBot == True).get()
    return user.isActivatedBot
    
    
    
       # message.text = 
    # express = KawaExpress.create(title=title, 
    #                             price=price, 
    #                             whereAndDate = whereAndDate, 
    #                             url=url, 
    #                             image=image,
    #                             isSentToTelegram=False,
    #                             chatid=chat_id)
    # express.save()
    
async def add_search(title, chat_id):
    search = SearchModel.create(title=title, chatid=chat_id)
    
def checkUserSync():
    try:
        mainUser = TgUserId.select().where(TgUserId.isActivatedBot == True).get()
        pyMainUser = json.loads(mainUser.userId)
        return int(pyMainUser['from']['id'])
    except Exception as e:
        print('It seems there is no users exists: ', e)
        return