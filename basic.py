import sheet as sh
import line
from datetime import datetime,timezone,timedelta

def findUserPosition(sheet,userID):
    USheet = sheet
    a = -1
    for i in range(0,len(USheet)):
        if USheet[i][0] == userID:
            a = i
    return a

def getUser(userID):
    USheet = sh.getUserSheet()
    userposition = findUserPosition(USheet,userID)
    if userposition == -1:
        return "don't have this user"
    
    return USheet[userposition]

def findTransPosition(sheet,transID):
    TSheet = sheet
    print(TSheet)
    a = -10
    for i in range(0,len(TSheet)):
        print(TSheet[i][0])
        if TSheet[i][0] == transID:
            a = i

    return a

def getTransaction(transID):
    TSheet = sh.getTransactionSheet()
    userposition = findUserPosition(TSheet,transID)
    if userposition == -1:
        return "don't have this transaction"
    return TSheet[userposition]

def getTransactionByUID(userID):
    TSheet = sh.getTransactionSheet()
    a = []
    print(len(a))
    for i in range(0,range(0,len(TSheet))):
        if TSheet[i][1] == userID or TSheet[i][2]:
            a.append(TSheet[i])
    if len(a) == 0:
        return "don't have any transaction"
    return a

def updateUserMoney(userID,money):
    USheet = sh.getUserSheet()
    User = getUser(userID)
    i = findUserPosition(USheet,userID)
    originM = float(User[2])
    newMoney = originM + float(money)
    sh.updateSheetValue('User','C',i+2,newMoney)

def makeTransaction(inUserID,outUserID,money):
    inUser = getUser(inUserID)
    outUser = getUser(outUserID)
    #先確認inUser有沒有錢
    haveMoney = float(outUser[2]) >= float(money)
    #再確認inUser的Type
    whatType = float(outUser[3]) >= float(money)

    if haveMoney == False:
        return 1
    date = timeNow()
    transactionID = inUserID+outUserID+date
    if whatType == False:
        sh.addTransactionSheet(transactionID,inUserID,outUserID,False,False,money,date)
        return 2
    if outUser[0] == 'ATM':
        sh.addTransactionSheet(transactionID,inUserID,outUserID,True,True,money,date)
        LineCheck(transactionID)
        return 0
    else:
        sh.addTransactionSheet(transactionID,inUserID,outUserID,True,False,money,date)
        #LineCheck(transactionID)
        # cancelURL = "https://www.google.com.tw/webhp?ei=7qgQWI-DL4r68QW8o6fACg&ved=0EKkuCAYoAQ"
        # checkURL = "https://www.google.com.tw/webhp?ei=7qgQWI-DL4r68QW8o6fACg&ved=0EKkuCAYoAQ"
        cancelURL = "https://sadbank.df.r.appspot.com/linecancle?id="+transactionID
        checkURL = 'https://sadbank.df.r.appspot.com/linecheck?id='+transactionID
        print(line.postMessage(outUser[4],inUser[0],money,cancelURL,checkURL))
        return 0
    #updateUserMoney(inUserID,money)
    #updateUserMoney(outUserID,-1*money)

def LineCheck(transactionID):
    TSheet = sh.getTransactionSheet()
    i = findTransPosition(TSheet,transactionID)
    inUserID = TSheet[i][1]
    outUserID = TSheet[i][2]
    money = float(TSheet[i][5])
    if outUserID =="ATM":
        sh.updateSheetValue('Transaction','E',str(i+2),True)
        updateUserMoney(inUserID,money)
        updateUserMoney(outUserID,-1*money)
    if sh.getTransactionSheet()[i][3] == "TRUE" and sh.getTransactionSheet()[i][4]=='FALSE':
        sh.updateSheetValue('Transaction','E',str(i+2),True)
        updateUserMoney(inUserID,money)
        updateUserMoney(outUserID,-1*money)

def LineCancle(transactionID):
    TSheet = sh.getTransactionSheet
    i = findTransPosition(TSheet,transactionID)
    sh.updateSheetValue('Transaction','D',str(i+2),False)

def timeNow():
    dt = datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8)))
    return dt.strftime("%Y-%m-%d%H:%M:%S") # 將時間轉換為 string