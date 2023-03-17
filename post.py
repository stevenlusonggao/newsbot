import requests
import os

def post(article, time):
    bot_token = os.environ.get('TELEGRAM_API') # replace with your bot token
    chat_id = "-1001773030359" # replace with your channel id
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    message = article['title'] + " " + article['url'] + " " + "\n" + "[Published: " + time + "]"
    data = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        print("Message posted successfully!")
    else:
        print("Failed to post message. Error:", response.text)
    
    return 



 
    