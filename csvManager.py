from constants import *
from traceManager import *


class CSVManager():

    def checkCSV(self):

        if(os.path.exists(csvDirPath) == False):
            os.mkdir(csvDirPath)

        if(os.path.exists(csvFilePath) == False):
            file = open(csvFilePath, 'w')
            file.close()           
        return


    def addLineCSV(self, update, trace, trans):

        csvFile = open(csvFilePath, 'a')

        line = trans.time + ";" + trans.amount + ";" + str(trans.category) + ";" + str(trans.method) + ";" + trans.note + '\n'

        csvFile.write(line)
        
        csvFile.close()                      

        print("Line added")
        update.message.reply_text("Transaction succesfully added to csv")
        trace.addLine("New data added to CSV: " + line)

