from constants import *
from datetime import datetime
import os


class TraceManager():

    def checkTrace(self):

        if(os.path.exists(traceDirPath) == False):
            os.mkdir(traceDirPath)

        if(os.path.exists(traceFilePath) == False):
            file = open(traceFilePath, 'w')
            file.close()

        if(os.path.getsize(traceFilePath) >= 5000000):
            currDate = datetime.now()
            currDateStr = currDate.strftime("%Y%m%d")
            newTraceFilePath = traceDirPath + "\\" + currDateStr + "standard.txt" 
            os.rename(traceFilePath, newTraceFilePath)
            file = open(traceFilePath, 'w')
            file.close()
            
        return



    def addLine(self, text):

        self.checkTrace()

        traceFile = open(traceFilePath, 'a')

        currTime = datetime.now()
        currTimeStr = currTime.strftime("%Y-%m-%d %H-%M-%S")
        line = currTimeStr + "      " + text


        traceFile.write(line)
        
        traceFile.close()                      

        return  





