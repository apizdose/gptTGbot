import telebot
from openai import OpenAI
import json


client=OpenAI(api_key='YourApiKey')
bot = telebot.TeleBot('YourTGBotToken')
chatID='TgChatID'

model="Ты саркастичный помощник." #Модель поведения


@bot.message_handler(commands=["drop"])
def drop(message):
    if str(message.chat.id) == chatID:
        with open("history.json", "w", encoding='utf-8') as file:
            data=[{"role": "system", "content": model}]
            json.dump(data, file)
            
@bot.message_handler(func=lambda message: True)
def handle_message(message):

    with open("history.json", "r", encoding='utf-8') as file:
        text=file.read()
        history=json.loads(text)
        data=[{"role": "user", "content": str(message.text).replace("/","")}]
        dt=history+data

    with open("history.json", "w", encoding='utf-8') as file:
        json.dump(dt, file)

    if str(message.chat.id) == chatID:
                         
        try:
            completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=dt,
            max_tokens=999,
            temperature=0.8
            )
        
            bot.reply_to(message, completion.choices[0].message.content)
            
            with open("history.json", "r", encoding='utf-8') as file:
                text=file.read()
                history=json.loads(text)
                data=[{"role": "assistant", "content": str(completion.choices[0].message.content)}]
                dt=history+data

            with open("history.json", "w", encoding='utf-8') as file:
                json.dump(dt, file)
           

        except Exception as e:                
            bot.reply_to(message, f"Ничего не я ясно, я короче сломался, идите нафиг!")
            

bot.polling()
            
