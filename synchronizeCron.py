import sys, time
sys.path.append('modules')
from Database import DBClient
import routeros_api, json
#router
def getAccountConnectRouter(idRouter, allRouter=0):
    connector = DBClient()
    if(allRouter == 0):
        dataRouter = connector.executeSelect('''SELECT `ipAddress`, `loginAccess`, `passwordAccess` FROM `routers` WHERE `idRouter` = "{0}"'''.format(idRouter))
    else:
        dataRouter = connector.executeSelect('''SELECT `ipAddress`, `loginAccess`, `passwordAccess` FROM `routers` WHERE `idRouter` != "1"''')
    connector.DBclose()
    del connector
    if dataRouter == []:
        return(None)
    elif allRouter == 0:
        return({"ipAddress":dataRouter[0][0], "loginAccess": dataRouter[0][1], "passwordAccess":dataRouter[0][2]})
    else:
        listRouters = []
        for step in dataRouter:
            listRouters.append({"ipAddress":step[0], "loginAccess": step[1], "passwordAccess":step[2]})
        return(listRouters)
def changeIpAddressNetwatch(data):
    try:
        account = getAccountConnectRouter(1)
        connection = routeros_api.RouterOsApiPool(account["ipAddress"], username=account["loginAccess"], password=account["passwordAccess"], plaintext_login=True)
        api = connection.get_api()
        listNetwatch = api.get_resource('/tool/netwatch')
        if(listNetwatch.get(host=data["lastIpAddress"]) != []):
            idNetwath = listNetwatch.get(host=data["lastIpAddress"])[0]["id"]
            listNetwatch.set(id=idNetwath, host=data["newIpAddress"])
            if(listNetwatch.get(id=idNetwath)[0]["host"] == data["newIpAddress"]):
                connection.disconnect()
                return(True)
            else:
                connection.disconnect()
                return(False)
    except Exception as e:
        return(False)
   
def removeNetwatch(data):
    try:
        account = getAccountConnectRouter(1)
        connection = routeros_api.RouterOsApiPool(account["ipAddress"], username=account["loginAccess"], password=account["passwordAccess"], plaintext_login=True)
        api = connection.get_api()
        listNetwatch = api.get_resource('/tool/netwatch')
        if(listNetwatch.get(host=data["ipAddress"]) != []):
            listNetwatch.remove(id=listNetwatch.get(host=data["ipAddress"])[0]["id"])
            if(listNetwatch.get(host=data["ipAddress"]) == []):
                connection.disconnect()
                return(True)
            else:
                connection.disconnect()
                return(False)
    except Exception as e:
        return(False)
   
def addIpAddressNetwatch(data):
    try:
        account = getAccountConnectRouter(1)
        connection = routeros_api.RouterOsApiPool(account["ipAddress"], username=account["loginAccess"], password=account["passwordAccess"], plaintext_login=True)
        api = connection.get_api()
        listNetwatch = api.get_resource('/tool/netwatch')
        if(listNetwatch.get(host=data["ipAddress"]) == []):
            listNetwatch.add(host=data["ipAddress"], interval="30s", up_script=':global urlSend "setActiveRouter?ipAddress=$host"\r\n/system script run sendScript', down_script=':global urlSend "setNotactiveRouter?ipAddress=$host"\r\n/system script run sendScript')
            if(listNetwatch.get(host=data["ipAddress"]) != []):
                connection.disconnect()
                return(True)
            else:
                connection.disconnect()
                return(False)
        else:
            connection.disconnect()
            return(False)     
    except Exception as e:
        return(False)

def reloadNetwatch(data):
    try:
        account = getAccountConnectRouter(1)
        connection = routeros_api.RouterOsApiPool(account["ipAddress"], username=account["loginAccess"], password=account["passwordAccess"], plaintext_login=True)
        api = connection.get_api()
        listNetwatch = api.get_resource('/tool/netwatch')
        if(listNetwatch.get(host=data["ipAddress"]) != []):
            idNetwath = listNetwatch.get(host=data["ipAddress"])[0]["id"]
            listNetwatch.set(id=idNetwath)
            connection.disconnect()
            return(True)
        else:
            connection.disconnect()
            return(False)     
    except Exception as e:
        return(False)
#clients

def changeDataClients(data):
    try:
        account = getAccountConnectRouter(data["idRouter"])
        connection = routeros_api.RouterOsApiPool(account["ipAddress"], username=account["loginAccess"], password=account["passwordAccess"], plaintext_login=True)
        api = connection.get_api()
        listClient = api.get_resource('/ppp/secret')
        if(listClient.get(name=data["numberContract"]) != []):
            idClient = listClient.get(name=data["numberContract"])[0]["id"]
            listClient.set(id=idClient, name=data["numberContract"], profile=data["idTariff"], password=data["ppoePassword"])
            if(listClient.get(id=idClient)[0]["name"] == data["numberContract"]):
                connection.disconnect()
                return(True)
            else:
                connection.disconnect()
                return(False)
    except Exception as e:
        return(False)
   
def removeDataClients(data):
    try:
        account = getAccountConnectRouter(data["idRouter"])
        connection = routeros_api.RouterOsApiPool(account["ipAddress"], username=account["loginAccess"], password=account["passwordAccess"], plaintext_login=True)
        api = connection.get_api()
        listClient = api.get_resource('/ppp/secret')
        if(listClient.get(name=data["numberContract"]) != []):
            listClient.remove(id=listClient.get(name=data["numberContract"])[0]["id"])
            if(listClient.get(name=data["numberContract"]) == []):
                connection.disconnect()
                return(True)
            else:
                connection.disconnect()
                return(False)
    except Exception as e:
        return(False)
   
def addDataClients(data):
    try:
        account = getAccountConnectRouter(data["idRouter"])
        connection = routeros_api.RouterOsApiPool(account["ipAddress"], username=account["loginAccess"], password=account["passwordAccess"], plaintext_login=True)
        api = connection.get_api()
        listClient = api.get_resource('/ppp/secret')
        if(listClient.get(name=data["numberContract"]) == []):
            listClient.add(name=data["numberContract"], service='pppoe', profile=data["idTariff"], password=data["ppoePassword"])
            if(listClient.get(name=data["numberContract"]) != []):
                connection.disconnect()
                return(True)
            else:
                connection.disconnect()
                return(False)
        else:
            connection.disconnect()
            return(False)     
    except Exception as e:
        return(False)




def provideService(data):
    try:
        account = getAccountConnectRouter(data["idRouter"])
        connection = routeros_api.RouterOsApiPool(account["ipAddress"], username=account["loginAccess"], password=account["passwordAccess"], plaintext_login=True)
        api = connection.get_api()
        listClient = api.get_resource('/ppp/secret')
        if(listClient.get(name=data["numberContract"]) != []):
            idClient = listClient.get(name=data["numberContract"])[0]["id"]
            listClient.set(id=idClient, profile=data["tariff"])
            if(listClient.get(name=data["numberContract"], profile=data["tariff"]) != []):
                connection.disconnect()
                return(True)
            else:
                connection.disconnect()
                return(False)
        else:
            connection.disconnect()
            return(False)     
    except Exception as e:
        return(False)

def prohibitServiceProvision(data):
    try:
        account = getAccountConnectRouter(data["idRouter"])
        connection = routeros_api.RouterOsApiPool(account["ipAddress"], username=account["loginAccess"], password=account["passwordAccess"], plaintext_login=True)
        api = connection.get_api()
        listClient = api.get_resource('/ppp/secret')
        if(listClient.get(name=data["numberContract"]) != []):
            idClient = listClient.get(name=data["numberContract"])[0]["id"]
            listClient.set(id=idClient, profile="profileDrop")
            if(listClient.get(name=data["numberContract"], profile="profileDrop") != []):
                connection.disconnect()
                return(True)
            else:
                connection.disconnect()
                return(False)
        else:
            connection.disconnect()
            return(False)     
    except Exception as e:
        return(False)


def addNewTariff(data):
    try:
        flag = True
        accountAll = getAccountConnectRouter(0, 1)
        for account in accountAll:
            connection = routeros_api.RouterOsApiPool(account["ipAddress"], username=account["loginAccess"], password=account["passwordAccess"], plaintext_login=True)
            api = connection.get_api()
            listProfile = api.get_resource('/ppp/profile')
            if(listProfile.get(name=data["idTariff"]) == []):
                listProfile.add(name=data["idTariff"], local_address="192.168.10.1", remote_address="PPoE_Pool", rate_limit="{0}m/{1}m".format(data["rxLimit"], data["txLimit"]), use_mpls="no", use_compression="no", use_encryption="yes", only_one="yes", on_up=''':global urlSend "setActiveUser?userNumber"\r\n:global textSend $user\r\n/system script run sendScript''', on_down=''':global urlSend "setNotactiveUser?userNumber"\r\n:global textSend $user\r\n/system script run sendScript''')
                if(listProfile.get(name=data["idTariff"]) != []):
                    listPPPoEServer = api.get_resource('/interface/pppoe-server/server')
                    listPPPoEServer.add(service_name="serviceTariff_{0}".format(data["idTariff"]), default_profile=data["idTariff"], interface="bridgeNat", authentication="mschap1,mschap2", keepalive_timeout="10", one_session_per_host="yes", max_sessions="unlimited", disabled="no")
                    if(listPPPoEServer.get(service_name="serviceTariff_{0}".format(data["idTariff"])) == []):
                        flag = False
                else:
                    flag = False
            connection.disconnect()
        return(flag)
    except Exception as e:
        return(False)

def removeTariff(data):
    try:
        accountAll = getAccountConnectRouter(0, 1)
        for account in accountAll:
            connection = routeros_api.RouterOsApiPool(account["ipAddress"], username=account["loginAccess"], password=account["passwordAccess"], plaintext_login=True)
            api = connection.get_api()
            listProfile = api.get_resource('/ppp/profile')
            if(listProfile.get(name=data["idTariff"]) != []):
                listProfile.remove(id=listProfile.get(name=data["idTariff"])[0]["id"])
                if(listProfile.get(name=data["idTariff"]) == []):
                    listPPPoEServer = api.get_resource('/interface/pppoe-server/server')
                    if(listPPPoEServer.get(service_name="serviceTariff_{0}".format(data["idTariff"])) != []):
                        listPPPoEServer.remove(id=listPPPoEServer.get(service_name="serviceTariff_{0}".format(data["idTariff"]))[0]["id"])
                        if(listPPPoEServer.get(service_name="serviceTariff_{0}".format(data["idTariff"])) != []):
                            flag=False
                    else:
                        flag=False
                else:
                    flag=False
            else:
                flag=False

            connection.disconnect()
        return(flag)
    except Exception as e:
        return(False)
def changeTariff(data):
    try:
        flag=True
        accountAll = getAccountConnectRouter(0, 1)
        for account in accountAll:
            connection = routeros_api.RouterOsApiPool(account["ipAddress"], username=account["loginAccess"], password=account["passwordAccess"], plaintext_login=True)
            api = connection.get_api()
            listProfile = api.get_resource('/ppp/profile')
            if(listProfile.get(name=data["idTariff"]) != []):
                listProfile.set(id=listProfile.get(name=data["idTariff"])[0]["id"], rate_limit="{0}m/{1}m".format(data["rxLimit"], data["txLimit"]))
                if(listProfile.get(name=data["idTariff"], rate_limit="{0}m/{1}m".format(data["rxLimit"], data["txLimit"])) == []):
                   flag=False 
            else:
                flag=False
            connection.disconnect()
        return(flag)
    except Exception as e:
        return(False)

if __name__ == '__main__':
    connector = DBClient()
    dataSynchronize = connector.executeSelect('''SELECT `idTask`, `jsonData` FROM `synchronizelist` WHERE `synchronized` = 0 ORDER BY `synchronized` ASC''')
    for step in dataSynchronize:
        # try:
        print("Задача {0}".format(step[0]))
        stepJSON = json.loads(step[1])
        functionCall = globals()[stepJSON["loadModule"]]
        if(functionCall(stepJSON["paramModule"])):
            connector.execute('''UPDATE `synchronizelist` SET `synchronized`=1, `numberAttempts`=`numberAttempts`+1 WHERE `idTask`="{0}" '''.format(step[0]))
        else:
            connector.execute('''UPDATE `synchronizelist` SET `numberAttempts`= `numberAttempts`+1 WHERE `idTask`="{0}" '''.format(step[0]))
        # except Exception as e:
        #     print("Виникла помилка при обробці запиту {0}".format(step[0]))  

    connector.DBclose()
    del connector