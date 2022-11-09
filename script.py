import configparser # pip install configparse
from datetime import datetime
from telethon import TelegramClient
from pymongo import MongoClient
from bson.objectid import ObjectId


# INIT CONFIGURATIONS
print('Initializing configurations')
config = configparser.ConfigParser()
config.read('config.ini')

API_ID = config.get('default','api_id')
API_HASH = config.get('default','api_hash')
BOT_TOKEN = config.get('default','bot_token')
session_name = "session/Bot"

# READ VALUES FOR DB
USERNAME = config.get('default','username')
PASSWORD = config.get('default','password') 
DATABASE_NAME = config.get('default','db_name')
COLLECTION_NAME = config.get('default','collection_name')

client = TelegramClient(session_name, API_ID, API_HASH).start(bot_token = BOT_TOKEN)

url = "mongodb+srv://"+USERNAME+":"+PASSWORD+"@clusterbot.gxgqhc5.mongodb.net/?retryWrites=true&w=majority"
cluster = MongoClient(url)


#INSERT
@client.on(events.NewMessage(pattern="(?i)/insert"))
async def insert(event):
    sender = await.get_sender


#MAIN

if __name__ == '__main__':
    try:
        print('Init database')
        db = cluster[DATABASE_NAME]
        products = db[COLLECTION_NAME]

        print('bot started')
        client.run_until_disconnected()

    except Exception as error:
        print('Cause {}'.format(error))