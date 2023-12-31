import vk_api
import datetime
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from config import *

vk_session = vk_api.VkApi(token = main_token)
longpoll = VkBotLongPoll(vk_session, groupId)

WEEKDAYNUM = 0 #В какой день недели менять название беседы, (По умолчанию 0 - Понедельник)
weeNum = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=+4))).isocalendar().week #Текущий номер недели


def changeTitleName(id, text):
    vk_session.method('messages.editChat', {'chat_id': id, 'title': text})


def sendMessage(id, text):
    vk_session.method('messages.send', {'chat_id': id, 'random_id': 0, 'message': text})

def getTitleChatName(id):
    req = vk_session.method('messages.getConversationsById', {"peer_ids": 2000000000 + id})#["title"]
    for response in req['items']:
        chat_settings = response['chat_settings']
        title = chat_settings['title']
    return title

def changeTitle(id):
    titleChat = getTitleChatName(id)

    if datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=+4))).weekday() == WEEKDAYNUM:
        if weeNum % 2 == 0:
            if titleChat.count('ЗНАМЕНАТЕЛЬ') == 1:
                changeTitleName(id, titleChat.replace('ЗНАМЕНАТЕЛЬ', 'ЧИСЛИТЕЛЬ'))
        if weeNum % 2 == 1:
            if titleChat.count('ЧИСЛИТЕЛЬ') == 1:
                changeTitleName(id, titleChat.replace('ЧИСЛИТЕЛЬ', 'ЗНАМЕНАТЕЛЬ'))


sendMessage(2, "Бот запущен")

changeTitle(5)


for event in longpoll.listen():
    weeNum = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=+4))).isocalendar().week
    id = event.chat_id
    titleChat = getTitleChatName(id)

    if datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=+4))).weekday() == WEEKDAYNUM:
        if weeNum % 2 == 0:
            if titleChat.count('ЗНАМЕНАТЕЛЬ') == 1:
                changeTitleName(id, titleChat.replace('ЗНАМЕНАТЕЛЬ', 'ЧИСЛИТЕЛЬ'))
        if weeNum % 2 == 1:
            if titleChat.count('ЧИСЛИТЕЛЬ') == 1:
                changeTitleName(id, titleChat.replace('ЧИСЛИТЕЛЬ', 'ЗНАМЕНАТЕЛЬ'))


    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.from_chat:
            msg = event.object.message['text'].lower()

            if msg == '/bothello':
                sendMessage(id, "Привет! Я бот, который меняет название беседы.")
            if msg == '/getid':
                print(f"id бесседы - {id}")