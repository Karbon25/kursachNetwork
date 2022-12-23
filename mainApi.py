from flask import Flask, render_template, request
import sys
sys.path.append('modules')
from Database import DBClient
app = Flask(__name__)

        
def addLog(message, idRouter):
    print("hello")
    connector = DBClient()
    connector.execute(''' INSERT INTO `logsrouter`(`idRouter`, `text`, `date`) VALUES ("{0}", "{1}", NOW())'''.format(idRouter, message))      
    connector.DBclose()
    del connector


@app.route('/setActiveUser')
def setActiveUser():
    if(request.method == "GET"):
        if(request.args.get("token") and request.args.get("userNumber")):
            connector = DBClient()
            dataRouter = connector.executeSelect('''SELECT `idRouter`, `name` FROM `routers` WHERE `token` = "{0}"'''.format(request.args.get("token")))
            if(dataRouter):
                if(connector.execute('''UPDATE `clients` SET `active`="{0}" WHERE `numberContract` = "{1}"'''.format("1", request.args.get("userNumber"))) != None):
                    connector.DBclose()
                    del connector
                    addLog('''Клієнт {0} - приєднався. '''.format(request.args.get("userNumber")), dataRouter[0][0])
                    return("ok")
                else:
                    connector.DBclose()
                    del connector
                    return("error")
            else:
                connector.DBclose()
                del connector
                return("error")
        else:
            return("error")
    else:
        return("error")
@app.route('/setNotactiveUser')
def setNotactiveUser():
    if(request.method == "GET"):
        if(request.args.get("token") and request.args.get("userNumber")):
            connector = DBClient()
            dataRouter = connector.executeSelect('''SELECT `idRouter`, `name` FROM `routers` WHERE `token` = "{0}"'''.format(request.args.get("token")))
            if(dataRouter):
                if(connector.execute('''UPDATE `clients` SET `active`="{0}" WHERE `numberContract` = "{1}"'''.format("0", request.args.get("userNumber"))) != None):
                    connector.DBclose()
                    del connector
                    addLog('''Клієнт {0} - від'єднався. '''.format(request.args.get("userNumber")), dataRouter[0][0])
                    return("ok")
                else:
                    connector.DBclose()
                    del connector
                    return("error")
            else:
                connector.DBclose()
                del connector
                return("error")
        else:
            return("error")
    else:
        return("error")

@app.route('/setActiveRouter')
def setActiveRouter():
    if(request.method == "GET"):
        if(request.args.get("token") and request.args.get("ipAddress")):
            connector = DBClient()
            dataRouter = connector.executeSelect('''SELECT `idRouter`, `name` FROM `routers` WHERE `token` = "{0}"'''.format(request.args.get("token")))
            if(dataRouter):
                if(connector.execute('''UPDATE `routers` SET `active`="{0}" WHERE `ipAddress`="{1}"'''.format("1", request.args.get("ipAddress"))) != None):
                    connector.DBclose()
                    del connector
                    addLog('''Роутер з ip адресою {0} під'єднався. '''.format(request.args.get("ipAddress")), dataRouter[0][0])
                    return("ok")
                else:
                    connector.DBclose()
                    del connector
                    return("error")
            else:
                connector.DBclose()
                del connector
                return("error")
        else:
            return("error")
    else:
        return("error")

@app.route('/setNotactiveRouter')
def setNotactiveRouter():
    if(request.method == "GET"):
        if(request.args.get("token") and request.args.get("ipAddress")):
            connector = DBClient()
            dataRouter = connector.executeSelect('''SELECT `idRouter`, `name` FROM `routers` WHERE `token` = "{0}"'''.format(request.args.get("token")))
            if(dataRouter):
                if(connector.execute('''UPDATE `routers` SET `active`="{0}" WHERE `ipAddress`="{1}"'''.format("0", request.args.get("ipAddress"))) != None):
                    connector.execute('''UPDATE `clients` SET `active`="{0}" WHERE `idRouter` IN (SELECT `idRouter` FROM `routers` WHERE `ipAddress` = "{1}")'''.format("0", request.args.get("ipAddress")))
                    connector.DBclose()
                    del connector
                    addLog('''Роутер з ip адресою {0} від'єднався. '''.format(request.args.get("ipAddress")), dataRouter[0][0])
                    return("ok")
                else:
                    connector.DBclose()
                    del connector
                    return("error")
            else:
                connector.DBclose()
                del connector
                return("error")
        else:
            return("error")
    else:
        return("error")
@app.route('/appendLogRouter')
def appendLogRouter():
    if(request.method == "GET"):
        if(request.args.get("token") and request.args.get("message")):
            connector = DBClient()
            dataRouter = connector.executeSelect('''SELECT `idRouter`, `name` FROM `routers` WHERE `token` = "{0}"'''.format(request.args.get("token")))
            if(dataRouter):
                addLog(request.args.get("message"), dataRouter[0][0])
                connector.DBclose()
                del connector
                return("ok")
            else:
                connector.DBclose()
                del connector
                return("error")
        else:
            return("error")
    else:
        return("error")
if __name__ == '__main__':
    app.run('10.0.0.3', 5001, debug=True)