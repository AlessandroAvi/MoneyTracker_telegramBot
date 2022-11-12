from inspect import trace
from operator import truediv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import *
from constants import *
from datetime import datetime
from traceManager import TraceManager
import csv

import configparser # pip install configparse
from pymongo import MongoClient


# CLASS THAT CONTAINS ALL THE INFO ABOUT THE TRANSACTION
class Transaction():

    time       = ""
    amount     = ""
    amountTemp = ""
    type       = 0
    method     = 0
    category   = 0
    note       = ""

    category_ary = ['Rent','Groceries', 'Living', 'Transport', 'Sport', 'Living']
    type_ary     = ['Expense','Entry']
    methods_ary  = ['Cash', 'PayPal', 'PP card', 'CC card']
    digits_ary   = ['0','1','2','3','4','5','6','7','8','9','.']
    digit_end    = 'K'

    # FLAGS
    ENTRY_FLAG     = False
    EXPENSE_FLAG   = False
    TIME_FLAG      = False
    TIME_FLAG2     = False
    METHOD_FLAG    = False
    CATEGORY_FLAG  = False
    NOTE_FLAG      = False
    AMOUNT_FLAG    = False
    TERMINATE_FLAG = False


    def reset(self):
        time       = ""
        amount     = ""
        amountTemp = ""
        type       = 0
        method     = 0
        category   = 0
        note       = ""
        PAYMENT_FLAG   = False
        EXPENSE_FLAG   = False
        TIME_FLAG      = False
        TIME_FLAG2     = False
        METHOD_FLAG    = False
        CATEGORY_FLAG  = False
        NOTE_FLAG      = False
        AMOUNT_FLAG    = False
        TERMINATE_FLAG = False



# Function is called when user writes /start in chat
def new_command(update, context):
    #traceManager.addLine("New transaction have been initialized \n")
    trans.reset()
    button = [[KeyboardButton(txt_transaction)]]
    context.bot.send_message(chat_id=update.effective_chat.id, text= "Generate new transaction", reply_markup=ReplyKeyboardMarkup(button, resize_keyboard=True, one_time_keyboard=True))

    addItemToDB()


def print_transInfo(update, context):
    update.message.reply_text("The transaction collected data is:\n  Date:     "+ trans.time +
                                                                "\n  Amount:   "+ trans.amount +
                                                                "\n  Type:     "+ trans.type_ary[trans.type] +
                                                                "\n  Category: "+str(trans.category_ary[trans.category])+
                                                                "\n  Method:   "+str(trans.methods_ary[trans.method])+
                                                                "\n  Notes:    "+str(trans.note))
    print("print info msg")


def addItemToDB():
    item = {"date": trans.time, "amount": float(trans.amount),  
            "type":trans.type, "method":trans.method, 
            "cat":trans.category, "note":trans.note}

    products.insert_one(item)
    return



##################################################
#       __  __    _    ___ _   _ 
#      |  \/  |  / \  |_ _| \ | |
#      | |\/| | / _ \  | ||  \| |
#      | |  | |/ ___ \ | || |\  |
#      |_|  |_/_/   \_\___|_| \_|
                           

# MONGO DATABASE
print('Initializing configurations')
config = configparser.ConfigParser()
config.read('config.ini')

BOT_TOKEN = config.get('default','bot_token')

# READ VALUES FOR DB
USERNAME = config.get('default','username')
PASSWORD = config.get('default','password') 
DATABASE_NAME = config.get('default','db_name')
COLLECTION_NAME = config.get('default','collection_name')

url = "mongodb+srv://"+USERNAME+":"+PASSWORD+"@clusterbot.gxgqhc5.mongodb.net/?retryWrites=true&w=majority"
cluster = MongoClient(url)

print('Init database')
db = cluster[DATABASE_NAME]
products = db[COLLECTION_NAME]


trans = Transaction()
trans.reset()

with open(r'''money_database.txt''', encoding='utf-8-sig') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    for row in csv_reader:
        trans.time     = row[0]
        trans.amount   = row[1]
        trans.amount   = trans.amount.replace(',', '.')
        trans.type     = row[2]
        trans.method   = row[3]
        trans.category = row[4]
        trans.note     = row[5]
        line_count += 1
        
        addItemToDB()
        trans.reset()

        print("Transaction number: " + str(line_count))
        print(row)
        print()