import os
import time
from whatsapp_api_client_python import API

# --- ضع بياناتك السرية من موقع Green-API هنا ---
ID_INSTANCE = "7107647927"
API_TOKEN_INSTANCE = "29b152422c3c4a78939c00f2bd3c91aa6ddefe7c205e48158d"

greenAPI = API.GreenApi(ID_INSTANCE, API_TOKEN_INSTANCE)
print("البوت يعمل الآن في السحاب ومستعد لحفظ الروابط...")

def receive_messages():
    while True:
        try:
            receive_notification = greenAPI.receive.receiveNotification()
            if receive_notification.body:
                notification = receive_notification.body
                type_of_notif = notification.get("typeWebhook")
                
                if type_of_notif == "incomingMessageReceived":
                    message_data = notification.get("messageData", {})
                    text_message_data = message_data.get("textMessageData", {})
                    text_message = text_message_data.get("textMessage", "")
                    chat_id = notification.get("senderData", {}).get("chatId", "")
                    
                    # فحص روابط مجموعات وقنوات الواتساب وحفظها في ملف نصي
                    if "chat.whatsapp.com" in text_message or "whatsapp.com/channel" in text_message:
                        with open("links_saved.txt", "a") as file:
                            file.write(f"{text_message}\n")
                        # رد تلقائي يؤكد الحفظ للطرف الآخر
                        greenAPI.sending.sendMessage(chat_id, "تم استلام الرابط وحفظه بنجاح بالنيابة عن عمرو!")
                
                greenAPI.receive.deleteNotification(notification.get("receiptId"))
        except:
            pass
        time.sleep(2)

if __name__ == "__main__":
    receive_messages()

