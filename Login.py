import sheet as sh

def login(Uid,Upassword):

    values = sh.getUserSheet()

    if not values:
        print('No data found.')
    else:
        loginSta = 0
        #print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            if row[0] == Uid:
                loginSta = 1
                if row[1] == Upassword:
                    loginSta = 2
                    
            #print(row[0])
        #print(loginSta)
        return loginSta

def register(Uid,Upassword,type,lineID):
    status = login(Uid,Upassword)

    if status == 0:
        if Uid == "":
            return 0
        #沒有這個帳號，辦一個
        sh.addUserSheet(Uid,Upassword,0,type,lineID)
        return 1
    else:
        #帳號存在
        return '帳號已經存在'

# Uid = input("請輸入帳號：")
# Upassword = input("請輸入密碼：")
# print(login(Uid,Upassword))