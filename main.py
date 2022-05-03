from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import *
from constants import *
from api_key import API_KEY  # this file is not committed because it contains the private token for the bot
from datetime import datetime




# CLASS THAT CONTAINS ALL THE INFO ABOUT THE TRANSACTION
class transaction_info():

    time = ""
    amount = 0
    method = 0
    category = 0
    note = ""

    category_ary = ['food', 'travel', 'sport', 'living']
    methods_ary  = ['cash', 'pp_card', 'cc_card', 'paypal']

    # FLAGS
    PAYMENT_FLAG = False
    EXPENSE_FLAG = False
    TIME_FLAG = False
    METHOD_FLAG = False
    CATEGORY_FLAG = False
    NOTE_FLAG = False
    AMOUNT_FLAG = False


    def reset(self):
        time = ""
        amount = 0
        method = 0
        category = 0
        note = ""
        PAYMENT_FLAG = False
        EXPENSE_FLAG = False
        TIME_FLAG = False
        METHOD_FLAG = False
        CATEGORY_FLAG = False
        NOTE_FLAG = False
        AMOUNT_FLAG = False







def new_command(update, context):
    button = [[KeyboardButton(txt_transaction)]]
    context.bot.send_message(chat_id=update.effective_chat.id, text= "Generate new transaction", 
                             reply_markup=ReplyKeyboardMarkup(button, resize_keyboard=True, one_time_keyboard=True))







def handle_message(update, context):

    # EXPENSE / PAYMENT BUTTON
    if txt_transaction in update.message.text:
        buttons = [[KeyboardButton(txt_expense)], [KeyboardButton(txt_payment)]]
        context.bot.send_message(chat_id=update.effective_chat.id, text = "Which type of transaction is it?", reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True))


    # FIELDS TO FILL BUTTONS
    if txt_expense in update.message.text or txt_payment in update.message.text:

        buttons = [[KeyboardButton(txt_date)],
                [KeyboardButton(txt_amount)], 
                [KeyboardButton(txt_category)], 
                [KeyboardButton(txt_method)],
                [KeyboardButton(txt_note)],
                [KeyboardButton(txt_complete)]]

        if txt_expense in update.message.text:
            trans.EXPENSE_FLAG = True
        if txt_payment in update.message.text:
            trans.PAYMENT_FLAG = True

        context.bot.send_message(chat_id=update.effective_chat.id, text = "Select the field to fill", reply_markup=ReplyKeyboardMarkup(buttons))


    # INLINE BUTTONS

    #TIME
    if txt_date in update.message.text:
        trans.TIME_FLAG = True
        buttons = [[InlineKeyboardButton("Current time", callback_data="current_time")], [InlineKeyboardButton("Insert time", callback_data="insert_time")]]
        update.message.reply_text("Select type of time:", reply_markup=InlineKeyboardMarkup(buttons))


    # AMOUNT
    if txt_amount in update.message.text:
        trans.AMOUNT_FLAG = True
        update.message.reply_text("Insert amount of money:")


    # CATEGORY
    if txt_category in update.message.text:
        trans.CATEGORY_FLAG = True
        buttons = [[InlineKeyboardButton("🍕 Food",    callback_data = trans.category_ary[0])], 
                   [InlineKeyboardButton("✈️ Travel", callback_data = trans.category_ary[1])], 
                   [InlineKeyboardButton("🧗 Sport",  callback_data = trans.category_ary[2])], 
                   [InlineKeyboardButton("🏠 Living", callback_data = trans.category_ary[3])]]
        update.message.reply_text("Define the category:", reply_markup=InlineKeyboardMarkup(buttons))


    # METHOD
    if txt_method in update.message.text:
        trans.METHOD_FLAG = True
        buttons = [[InlineKeyboardButton("💶 Cash",    callback_data = trans.methods_ary[0])], 
                   [InlineKeyboardButton("💳 PP card", callback_data = trans.methods_ary[1])], 
                   [InlineKeyboardButton("🏦 CC card", callback_data = trans.methods_ary[2])], 
                   [InlineKeyboardButton("🌐 PayPal",  callback_data = trans.methods_ary[3])]]
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

    return "Sorry I cannot understand your command"



def print_transInfo(update, context):
    update.message.reply_text("The transaction collected data is:\n  Date:"+ trans.time +"\n  Amount: "+str(trans.amount)+"\n  Category: "+str(trans.category)+"\n  Method: "+str(trans.method)+"\n  Notes: "+str(trans.note))
    print("print info msg")



def queryHandler(update, context):
    query = update.callback_query.data
    update.callback_query.answer()

    if trans.CATEGORY_FLAG:
        # check for category
        for i in len(trans.category_ary):
            if trans.category_ary[i] in query:
                trans.category = i
                trans.CATEGORY_FLAG = False
                return

    if trans.METHOD_FLAG:
        # check for methodology
        for i in len(trans.methods_ary):
            if trans.methods_ary[i] in query:
                trans.method = i
                trans.METHOD_FLAG = False
                return

    if trans.TIME_FLAG:
        # check for time
        if 'current_time' in query:
            now = datetime.now()
            trans.time = now.strftime("%y/%m/%d")
            trans.TIME_FLAG = False
            print(trans.time)
            return
        
        if 'insert_time' in query:
            update.message.reply_text("Insert the date")
            trans.time = now.strftime("%y/%m/%d")
            trans.TIME_FLAG = False
            return

    return "No callbacks found"

    
def digits_keyboard(flag, context, update):

    if flag == 0:
        buttons = [[KeyboardButton("1")],[KeyboardButton("1")],[KeyboardButton("1")],]


    elif flag == 1:
        dummy = 0


    context.bot.send_message(chat_id=update.effective_chat.id, text = "Select the field to fill", reply_markup=ReplyKeyboardMarkup(buttons))







def error(update, context):
    print(f"Update: {update} caused error {context.error}")




def main():


    updater = Updater(API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", new_command))

    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_handler(CallbackQueryHandler(queryHandler))

    dp.add_error_handler(error)

    updater.start_polling(2)
    updater.idle()





print('**Bot started')
trans = transaction_info()
main()