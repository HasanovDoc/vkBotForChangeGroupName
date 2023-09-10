import vk_api
import datetime
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from config import *

vk_session = vk_api.VkApi(token = main_token)
longpoll = VkBotLongPoll(vk_session, groupId)

flag = True

WEEKDAYNUM = 1 #В какой день недели менять название беседы, (По умолчанию 0 - Понедельник)
weeNum = datetime.datetime.today().isocalendar().week #Текущий номер недели


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



sendMessage(2, "Бот запущен")

for event in longpoll.listen():
    weeNum = datetime.datetime.today().isocalendar().week
    id = event.chat_id
    titleChat = getTitleChatName(id)
    
    if datetime.datetime.today().weekday() == WEEKDAYNUM:
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
            















# class MyLongPoll(VkBotLongPoll):
#     def listen(self):
#         while True:
#             try:
#                 for event in self.check():
#                     yield event
#             except Exception as e:
#                 print(e)
            
# class VkBot:
#     def __init__(self):
#         self.vk_session = vk_api.VkApi(token = main_token)
#         self.longpoll = MyLongPoll(self.vk_session, 222452856)
#         # self.vk_id = self.vk_session.get_user_id()
#         # self.vk_name = self.vk_session.get_user_name()
#         # self.vk_photo = self.vk_session.get_user_photo(self.vk_id)
#         # self.vk_friends = self.vk_session.friends.get()
#         # self.vk_groups = self.vk_session.groups.get()
#         # self.vk_wall = self.vk_session.wall.get(owner_id=self.vk_id)
#         # self.vk_messages = self.vk_session.messages.get(owner_id=self.vk_id)
#     def run(self):
#         for event in self.longpoll.listen():
#             if event.type == VkEventType.MESSAGE_NEW:
#                 msg = event.object.message
        
# if __name__ == '__main__':
#     VkBot().run()
        

# vk_session = vk_api.VkApi(token=main_token)
# longpoll = VkLongPoll(vk_session)

