from Database import DBClient
from flask import Flask, render_template, request, abort, session, redirect
import routeros_api, json, addSynchronizeList
from AccessModule import AccessModule

def getFunctionClient(app, listNav):
    @app.route("/ajax/clientsListUpdate", methods=["POST"])
    def ajaxClientsListUpdate():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "clients" not in accessO.getPermission():
                abort(403)
        connector = DBClient()
        dataClient = connector.executeSelect('''SELECT `fullName`, `numberContract`, `tariff`.`name`, `routers`.`name`, `state`, `clients`.`active`, `idClient`, `idClient` FROM `clients` INNER JOIN `tariff` ON `clients`.`idTariff` = `tariff`.`idTariff` LEFT JOIN `routers` ON `routers`.`idRouter` = `clients`.`idRouter` ORDER BY `clients`.`idClient` ASC''')
        dataClient = list(dataClient)
        if(dataClient):
            for i in  range(0, len(dataClient)):
                dataClient[i] = list(dataClient[i])
                if(dataClient[i][3] == None):
                    dataClient[i][3] = '''<p style="color:red">Не під'єднано</p>'''
                if dataClient[i][4] == 0:
                    dataClient[i][4] = '''<p style="color:red">Послуга не надається</p>'''
                else:
                    dataClient[i][4] = '''<p style="color:green">Послуга надається</p>'''
                if dataClient[i][5] == 0:
                    dataClient[i][5] = '''Не активне'''
                else:
                    dataClient[i][5] = '''Активне'''
                dataClient[i][6] = '''<button type="button" class="btn btn-outline-success" onclick="showEdit({0});">Редагувати</button>'''.format(dataClient[i][6]);
                dataClient[i][7] = '''<button type="button" class="btn btn-outline-danger" onclick="showRemove({0});">Видалити</button>'''.format(dataClient[i][7]);
                dataClient[i].insert(0, i+1)  
        connector.DBclose()
        del connector
        return(json.dumps({"data":dataClient}))


    @app.route("/ajax/clientsGetTariffs", methods=["POST"])
    def ajaxcClientsGetTariffs():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "clients" not in accessO.getPermission():
                abort(403)

        connector = DBClient()
        if request.form["all"] == "True":
            result = connector.executeSelect('''SELECT `idTariff`, `name` FROM `tariff`''')
        else:
            result = connector.executeSelect('''SELECT `idTariff`, `name` FROM `tariff` WHERE `activeTariff` = 1''')
        connector.DBclose()
        del connector
        if(result):
            resultData = "<option value=""></option>"
            for step in result:
                resultData += '''<option value="{0}">{1}</option>'''.format(step[0], step[1])
            return(resultData)
        else:
            return("False")


    @app.route("/ajax/clientsGetRouters", methods=["POST"])
    def ajaxClientsGetRouters():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "clients" not in accessO.getPermission():
                abort(403)

        connector = DBClient()
        result = connector.executeSelect('''SELECT `idRouter`, `name` FROM `routers`''')
        connector.DBclose()
        del connector
        if(result):
            resultData = "<option value=""></option>"
            for step in result:
                if step[0] != 1:
                    resultData += '''<option value="{0}">{1}</option>'''.format(step[0], step[1])
            return(resultData)
        else:
            return("False")





    @app.route("/ajax/getClientData", methods=["POST"])
    def ajaxGetСlientData():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "clients" not in accessO.getPermission():
                abort(403)
        if "idClient" in request.form:
            connector = DBClient()
            dataClient = connector.executeSelect('''SELECT `idClient`, `fullName`, `address`, `idTariff`, `tel`, `numberContract`, `idRouter`, `ppoePassword`, `ConnectionDate`  FROM `clients` WHERE `idClient` = "{0}"'''.format(request.form["idClient"]))
            connector.DBclose()
            del connector
            if(dataClient):
                accessO.addLogUser("Користувач отримав дані клієнта {0}".format(dataClient[0][5]))
                return(json.dumps({"data":dataClient},default=str))
            else:
                return("False")
        else:
            abort(401)

    @app.route("/ajax/editClientData", methods=["POST"])
    def ajaxEditClientData():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "clients" not in accessO.getPermission():
                abort(403)
        if "idClient" in request.form:
            connector = DBClient()
            if(connector.execute('''UPDATE `clients` SET `fullName`="{0}",`address`="{1}",`idTariff`="{2}",`tel`="{3}",`idRouter`="{4}",`ppoePassword`="{5}" WHERE `idClient` = "{6}"'''.format(request.form["fullName"],request.form["address"],request.form["idTariff"],request.form["tel"],request.form["idRouter"],request.form["ppoePassword"],request.form["idClient"])) != None):
                connector.DBclose()
                del connector
                jsonData = {"loadModule":"changeDataClients", "paramModule":{"idRouter": request.form["idRouter"], "numberContract":request.form["numberContract"], "idTariff": request.form["idTariff"], "ppoePassword": request.form["ppoePassword"]}}
                addSynchronizeList.addSynchronizeList(request.form["idRouter"],"Зміна даних клієнта {0}".format(request.form["numberContract"]), json.dumps(jsonData))
                accessO.addLogUser("Користувач змінив дані клієнта {0}".format(request.form["numberContract"]))
                return("True")
            else:
                connector.DBclose()
                del connector
                return("False")

            
        else:
            abort(401)


    @app.route("/ajax/removeClientData", methods=["POST"])
    def ajaxRemoveClientData():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "clients" not in accessO.getPermission():
                abort(403)
        if "idClient" in request.form:
            connector = DBClient()
            dataClient = connector.executeSelect('''SELECT `numberContract`, `idRouter` FROM `clients` WHERE `idClient` = "{0}"'''.format(request.form["idClient"]))
            if(connector.execute('''DELETE FROM `clients` WHERE `idClient` =  "{0}"'''.format(request.form["idClient"])) != None):
                connector.DBclose()
                del connector
                jsonData = {"loadModule":"removeDataClients", "paramModule":{"idRouter": dataClient[0][1], "numberContract":dataClient[0][0]}}
                addSynchronizeList.addSynchronizeList(dataClient[0][1],"Видалення клієнта {0}".format(dataClient[0][0]), json.dumps(jsonData))
                accessO.addLogUser("Користувач видалив клієнта {0}".format(dataClient[0][0]))
                return("True")
            else:
                connector.DBclose()
                del connector
                return("False")
        else:
            abort(401)


    @app.route("/ajax/addClientData", methods=["POST"])
    def ajaxAddClientData():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "clients" not in accessO.getPermission():
                abort(403)
            connector = DBClient()
            stateExecuteAdd = connector.execute('''INSERT INTO `clients`(`fullName`, `address`, `idTariff`, `tel`, `numberContract`, `idRouter`, `ppoePassword`, `ConnectionDate`, `state`, `active`) VALUES ("{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}","0","0")'''.format(request.form["fullName"],request.form["address"],request.form["idTariff"],request.form["tel"],request.form["numberContract"],request.form["idRouter"],request.form["ppoePassword"],request.form["ConnectionDate"]))
            if(stateExecuteAdd != False):
                connector.DBclose()
                del connector 
                jsonData = {"loadModule":"addDataClients", "paramModule":{"idRouter": request.form["idRouter"], "numberContract":request.form["numberContract"], "idTariff": request.form["idTariff"], "ppoePassword": request.form["ppoePassword"]}}
                addSynchronizeList.addSynchronizeList(request.form["idRouter"],"Додання клієнта {0}".format(request.form["numberContract"]), json.dumps(jsonData))
                accessO.addLogUser("Користувач додав клієнта {0}. Присвоєне id {1}".format(request.form["numberContract"], stateExecuteAdd))  
                return("True")
            else:
                connector.DBclose()
                del connector 
                return("False")



    @app.route('/clients')
    def clients():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "clients" not in accessO.getPermission():
                abort(403)
        accessO.addLogUser("Перегляд сторінки Клієнти")
        return(render_template("base.html", module="clients", head_name="Клієнти"))


