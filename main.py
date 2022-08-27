from inspect import trace
from operator import truediv
import tracemalloc
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import *
from constants import *
from api_key import API_KEY  # this file is not committed because it contains the private token for the bot
from datetime import datetime
from csvManager import *
from traceManager import TraceManager




# CLASS THAT CONTAINS ALL THE INFO ABOUT THE TRANSACTION
class Transaction():

    time     = ""
    amount   = ""
    amountTemp = ""
    type     = 0
    method   = 0
    category = 0
    note     = ""

    category_ary = ['Rent','Groceries', 'Living', 'Transport', 'Sport', 'Living']
    methods_ary  = ['Cash', 'PayPal', 'PP card', 'CC card']
    digits_ary   = ['0','1','2','3','4','5','6','7','8','9','.']
    digit_end    = 'K'

    # FLAGS
    ENTRY_FLAG  = False
    EXPENSE_FLAG  = False
    TIME_FLAG     = False
    METHOD_FLAG   = False
    CATEGORY_FLAG = False
    NOTE_FLAG     = False
    AMOUNT_FLAG   = False


    def reset(self):
        time     = ""
        amount   = ""
        amountstr = ""
        type     = 0
        method   = 0
        category = 0
        note     = ""
        PAYMENT_FLAG  = False
        EXPENSE_FLAG  = False
        TIME_FLAG     = False
        METHOD_FLAG   = False
        CATEGORY_FLAG = False
        NOTE_FLAG     = False
        AMOUNT_FLAG   = False



buttonsMenu = [[KeyboardButton(txt_date)],
              [KeyboardButton(txt_amount)], 
              [KeyboardButton(txt_category)], 
              [KeyboardButton(txt_method)],
              [KeyboardButton(txt_note)],
              [KeyboardButton(txt_complete)]]



# Function is called when user writes /start in chat
def new_command(update, context):
    traceManager.addLine("New transaction have been initialized \n")
    button = [[KeyboardButton(txt_transaction)]]
    context.bot.send_message(chat_id=update.effective_chat.id, text= "Generate new transaction", 
                             reply_markup=ReplyKeyboardMarkup(button, resize_keyboard=True, one_time_keyboard=True))


# FUnction is called when user activates a new transaction with the button
def handle_message(update, context):

    # EXPENSE / ENTRY BUTTON
    if txt_transaction in update.message.text:
        buttons = [[KeyboardButton(txt_expense)], [KeyboardButton(txt_entry)]]
        context.bot.send_message(chat_id=update.effective_chat.id, text = "Which type of transaction is it?", reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True))


    # FIELDS TO FILL BUTTONS
    if txt_expense in update.message.text or txt_entry in update.message.text:



        if txt_expense in update.message.text:
            trans.type = 0
            trans.EXPENSE_FLAG = True
            traceManager.addLine("New type inserted: expense - " + str(trans.type) + '\n')
        if txt_entry in update.message.text:
            trans.type = 1
            trans.ENTRY_FLAG = True
            traceManager.addLine("New type inserted: entry - " + str(trans.type) + '\n')

        context.bot.send_message(chat_id=update.effective_chat.id, text = "Select the field to fill", reply_markup=ReplyKeyboardMarkup(buttonsMenu))


    ## INLINE BUTTONS

    #TIME
    if txt_date in update.message.text:
        trans.TIME_FLAG = True
        buttons = [[InlineKeyboardButton("Current time", callback_data="current_time")], [InlineKeyboardButton("Insert time", callback_data="insert_time")]]
        update.message.reply_text("Select type of time:", reply_markup=InlineKeyboardMarkup(buttons))


    # AMOUNT
    if txt_amount in update.message.text:
        trans.AMOUNT_FLAG = True
        buttons = [
                    [KeyboardButton("1",    callback_data = "1"),
                     KeyboardButton("2",    callback_data = "2"),
                     KeyboardButton("3",    callback_data = "3")],
                    [KeyboardButton("4",    callback_data = "4"),
                     KeyboardButton("5",    callback_data = "5"),
                     KeyboardButton("6",    callback_data = "6")],
                    [KeyboardButton("7",    callback_data = "7"),
                     KeyboardButton("8",    callback_data = "8"),
                     KeyboardButton("9",    callback_data = "9")],
                    [KeyboardButton(".",    callback_data = "."),
                     KeyboardButton("0",    callback_data = "0"),
                     KeyboardButton("K",  callback_data = "K")]]
        update.message.reply_text("Insert amount of money:", reply_markup=ReplyKeyboardMarkup(buttons))


    # CATEGORY
    if txt_category in update.message.text:
        trans.CATEGORY_FLAG = True
        buttons = [
                   [InlineKeyboardButton("🏠 Rent",    callback_data = trans.category_ary[0])], 
                   [InlineKeyboardButton("🍕 Groceries",    callback_data = trans.category_ary[1])], 
                   [InlineKeyboardButton("🧻 Living", callback_data = trans.category_ary[2])], 
                   [InlineKeyboardButton("✈️ Transport",  callback_data = trans.category_ary[3])], 
                   [InlineKeyboardButton("🧗 Sport", callback_data = trans.category_ary[4])],
                   [InlineKeyboardButton("🎁 Other",  callback_data = trans.category_ary[5])] ]
        update.message.reply_text("Define the category:", reply_markup=InlineKeyboardMarkup(buttons))


    # METHOD
    if txt_method in update.message.text:
        trans.METHOD_FLAG = True
        buttons = [[InlineKeyboardButton("💶 Cash", callback_data = trans.methods_ary[0])], 
                   [InlineKeyboardButton("🌐 PayPal", callback_data = trans.methods_ary[1])], 
                   [InlineKeyboardButton("💳 PP card", callback_data = trans.methods_ary[2])], 
                   [InlineKeyboardButton("🏦 CC card", callback_data = trans.methods_ary[3])]]
        update.message.reply_text("Define payment method:", reply_markup=InlineKeyboardMarkup(buttons))


    # NOTES
    if txt_note in update.message.text:
        trans.NOTE_FLAG = True
        buttons = [[InlineKeyboardButton(txt_date)], [InlineKeyboardButton(txt_amount)]]
        update.message.reply_text("Insert the note:")


    # TERMINATE
    if txt_complete in update.message.text:
        update.message.reply_text("Terminating transaction...")

        print_transInfo(update, context)

        csvManager.addLineCSV(update, traceManager, trans)

    return "Sorry I cannot understand your command"



# FUnction is called whenever user writes womething in the chat
def queryReceivedHandler(update, context):
    query = update.callback_query.data
    update.callback_query.answer()

    if trans.TIME_FLAG:
        if 'current_time' in query:
            now = datetime.now()
            trans.time = now.strftime("%Y-%m-%d")
            trans.TIME_FLAG = False
            print(trans.time)
            traceManager.addLine("New date inserted: " + trans.time + '\n')
            return
        
        if 'insert_time' in query:
            update.message.reply_text("Insert the date")
            trans.time = now.strftime("%Y-%m-%d")
            trans.TIME_FLAG = False
            print(trans.time)
            traceManager.addLine("New date inserted manually: " + trans.time + '\n')
            return

    if trans.AMOUNT_FLAG:  
        if 'K' in query:
            trans.AMOUNT_FLAG = False  
            trans.amount = trans.amountTemp
            trans.amountTemp = ""
            print(trans.amountTemp)
            traceManager.addLine("New amount inserted manually: " + trans.amountTemp + '\n')  
            context.bot.send_message(reply_markup=ReplyKeyboardRemove(remove_keyboard=True))

            return
        for digit in trans.digits_ary:
            if digit in query:
                trans.amountTemp = trans.amountTemp + digit
                return

    if trans.CATEGORY_FLAG:
        cnt = 0
        for cat in trans.category_ary:
            if trans.category_ary[cnt] in query:
                trans.category = cnt
                trans.CATEGORY_FLAG = False
                debug = trans.category_ary[trans.category] + " - " +  str(trans.category)
                print(debug)
                traceManager.addLine("New category inserted: " + debug + '\n')
                return
            cnt = cnt+1

    if trans.METHOD_FLAG:
        cnt = 0
        for meth in trans.methods_ary:
            if trans.methods_ary[cnt] in query:
                trans.method = cnt
                trans.METHOD_FLAG = False
                debug = trans.methods_ary[trans.method] + " - " + str(trans.method)
                print(debug)
                traceManager.addLine("New method inserted: " + debug + '\n')
                return
            cnt = cnt+1

    if trans.NOTE_FLAG:      
        trans.note = query
        trans.NOTE_FLAG = False
        print(trans.note)
        traceManager.addLine("New note inserted: " + trans.note + '\n')
        return

    return "No callbacks found"




    
def digits_keyboard(flag, context, update):

    if flag == 0:
        buttons = [[KeyboardButton("1")],[KeyboardButton("1")],[KeyboardButton("1")],]


    elif flag == 1:
        dummy = 0


    context.bot.send_message(chat_id=update.effective_chat.id, text = "Select the field to fill", reply_markup=ReplyKeyboardMarkup(buttons))


def print_transInfo(update, context):
    update.message.reply_text("The transaction collected data is:\n  Date:"+ trans.time +"\n  Amount: "+ trans.amountTemp +"\n  Category: "+str(trans.category_ary[trans.category])+"\n  Method: "+str(trans.methods_ary[trans.method])+"\n  Notes: "+str(trans.note))
    print("print info msg")






def error(update, context):
    print(f"Update: {update} caused error {context.error}")








##################################################
#       __  __    _    ___ _   _ 
#      |  \/  |  / \  |_ _| \ | |
#      | |\/| | / _ \  | ||  \| |
#      | |  | |/ ___ \ | || |\  |
#      |_|  |_/_/   \_\___|_| \_|
                           


def main():

    pollingWaitTime = 0.5

    traceManager.addLine("** Bot started ** \n")
    traceManager.addLine("Polling wait time is: " + str(pollingWaitTime) + '\n')


    updater = Updater(API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", new_command))

    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_handler(CallbackQueryHandler(queryReceivedHandler))

    dp.add_error_handler(error)

    updater.start_polling(pollingWaitTime)
    updater.idle()




print('**Bot started')
trans        = Transaction()
traceManager = TraceManager()
csvManager   = CSVManager()
main()