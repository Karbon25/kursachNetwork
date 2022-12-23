from Database import DBClient
from flask import Flask, render_template, request, abort, session, redirect
import routeros_api, json, addSynchronizeList
from AccessModule import AccessModule


def getFunctionRouter(app, listNav):
    @app.route("/ajax/routersListUpdate", methods=["POST"])
    def ajaxRoutersListUpdate():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "routers" not in accessO.getPermission():
                abort(403)

        connector = DBClient()
        dataRouter = connector.executeSelect('''SELECT `name`, `address`, `active`, `ipAddress`, `idRouter`, `idRouter`, `idRouter` FROM `routers` ORDER BY `idRouter` ASC''')
        dataRouter = list(dataRouter)
        if(dataRouter):
            for i in  range(0, len(dataRouter)):
                dataRouter[i] = list(dataRouter[i])
                if(dataRouter[i][2] == 0):
                    dataRouter[i][2] = '''<p style="color:red">Не активний</p>'''
                else:
                    dataRouter[i][2] = "Активний"
                dataRouter[i][4] = '''<button type="button" class="btn btn-outline-success" onclick="checkRouter({0});">Оновити стан</button>'''.format(dataRouter[i][4]);
                dataRouter[i][5] = '''<button type="button" class="btn btn-outline-success" onclick="showEdit({0});">Редагувати</button>'''.format(dataRouter[i][5]);
                if dataRouter[i][6] != 1:
                    dataRouter[i][6] = '''<button type="button" class="btn btn-outline-danger" onclick="showRemove({0});">Видалити</button>'''.format(dataRouter[i][6]);
                else:
                    dataRouter[i][6] = '''Не видаляємий ''';
                dataRouter[i].insert(0, i+1)  
        connector.DBclose()
        del connector
        return(json.dumps({"data":dataRouter}))

    @app.route("/ajax/getRouterData", methods=["POST"])
    def ajaxGetRouterData():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "routers" not in accessO.getPermission():
                abort(403)
        if "idRouter" in request.form:
            connector = DBClient()
            dataRouter = connector.executeSelect('''SELECT `idRouter`, `name`, `address`, `token`, `ipAddress`, `loginAccess`, `passwordAccess` FROM `routers` WHERE `idRouter` = "{0}"'''.format(request.form["idRouter"]))
            accessO.addLogUser("Отримання даних обладнення id {0}".format(request.form["idRouter"]))
            connector.DBclose()
            del connector
            return(json.dumps({"data":dataRouter}))
        else:
            abort(401)
    @app.route("/ajax/checkRouterActive", methods=["POST"])
    def ajaxCheckRouterActive():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "routers" not in accessO.getPermission():
                abort(403)
        if "idRouter" in request.form:
            connector = DBClient()
            dataRouter = connector.executeSelect('''SELECT `ipAddress` FROM `routers` WHERE `idRouter` = "{0}"'''.format(request.form["idRouter"]))
            connector.DBclose()
            del connector
            if dataRouter != []:
                accessO.addLogUser("Відправка запиту перевірки доступності обладнення id {0}".format(request.form["idRouter"]))
                jsonData = {"loadModule":"reloadNetwatch", "paramModule":{"ipAddress":dataRouter[0][0]}}
                addSynchronizeList.addSynchronizeList(1,"Оновлення стану роутера {0}".format(dataRouter[0][0]), json.dumps(jsonData))
            return("True")
        else:
            abort(401)

    @app.route("/ajax/editRouterData", methods=["POST"])
    def ajaxEditRouterData():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "routers" not in accessO.getPermission():
                abort(403)
        if "idRouter" in request.form:
            connector = DBClient()
            dataRouter = connector.executeSelect('''SELECT `ipAddress` FROM `routers` WHERE `idRouter` = "{0}"'''.format(request.form["idRouter"]))
            if(connector.execute('''UPDATE `routers` SET `name`="{0}",`address`="{1}",`active`='0',`token`="{2}",`ipAddress`="{3}",`loginAccess`="{4}",`passwordAccess`="{5}" WHERE `idRouter` = "{6}"'''.format(request.form["name"],request.form["address"],request.form["token"],request.form["ip_address"],request.form["username"],request.form["password"],request.form["idRouter"])) != None):
                connector.DBclose()
                del connector
                if dataRouter != []:
                    accessO.addLogUser("Редагування даних обладнення id{0}".format(request.form["idRouter"]))
                    jsonData = {"loadModule":"changeIpAddressNetwatch", "paramModule":{"lastIpAddress":dataRouter[0][0], "newIpAddress":request.form["ip_address"]}}
                    addSynchronizeList.addSynchronizeList(1,"Зміна ip адреси роутера з {0} на {1}".format(dataRouter[0][0], request.form["ip_address"]), json.dumps(jsonData))
                return("True")
            else:
                connector.DBclose()
                del connector
                return("False")

            
        else:
            abort(401)


    @app.route("/ajax/removeRouterData", methods=["POST"])
    def ajaxRemoveRouterData():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "routers" not in accessO.getPermission():
                abort(403)
        if "idRouter" in request.form:
            if request.form["idRouter"] == "1":
                return("False")
            else:
                connector = DBClient()
                dataRouter = connector.executeSelect('''SELECT `ipAddress` FROM `routers` WHERE `idRouter` = "{0}"'''.format(request.form["idRouter"]))
                if(connector.execute('''DELETE FROM `routers` WHERE `idRouter` = "{0}"'''.format(request.form["idRouter"])) != None):
                    connector.DBclose()
                    del connector
                    if dataRouter != []:
                        accessO.addLogUser("Видалення обладнення id {0}".format(request.form["idRouter"]))
                        jsonData = {"loadModule":"removeNetwatch", "paramModule":{"ipAddress":dataRouter[0][0]}}
                        addSynchronizeList.addSynchronizeList(1,"Видалення роутера з ip адресою {0}".format(dataRouter[0][0]), json.dumps(jsonData))
                    return("True")

                else:
                    connector.DBclose()
                    del connector
                    return("False")

            
        else:
            abort(401)


    @app.route("/ajax/addRouterData", methods=["POST"])
    def ajaxAddRouterData():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "routers" not in accessO.getPermission():
                abort(403)
        if "ip_address" in request.form:
            connector = DBClient()
            dataRouter = connector.executeSelect('''SELECT `ipAddress` FROM `routers` WHERE `ipAddress` = "{0}"'''.format(request.form["ip_address"]))
            if(dataRouter != []):
                connector.DBclose()
                del connector
                return("Ір адреса використовується іншим обладненням")
            else:
                dataToken = ""
                while True:
                    dataToken = connector.executeSelect('''SELECT r.`randomToken`, `idRouter` FROM `routers` RIGHT JOIN (SELECT SHA1(rand()) as `randomToken` ) r ON `idRouter` = r.`randomToken`''')
                    if dataToken[0][1] == None:
                        break
                executeAddRouter = connector.execute(''' INSERT INTO `routers`(`name`, `address`, `active`, `token`, `ipAddress`, `loginAccess`, `passwordAccess`) VALUES ("{0}", "{1}", "0", "{2}", "{3}", "{4}", "{5}")'''.format(request.form["name"],request.form["address"],dataToken[0][0],request.form["ip_address"],request.form["username"],request.form["password"]))
                if(executeAddRouter != False):
                    connector.DBclose()
                    del connector 
                    accessO.addLogUser("Додання обладення IP адреса {0}, присвоєно id {1}".format(request.form["ip_address"], executeAddRouter))
                    jsonData = {"loadModule":"addIpAddressNetwatch", "paramModule":{"ipAddress":request.form["ip_address"]}}
                    addSynchronizeList.addSynchronizeList(1,"Додання роутера з ip адресою {0}".format(request.form["ip_address"]), json.dumps(jsonData))
                    return("True")
                else:
                    connector.DBclose()
                    del connector 
                    return("Помилка підключення")
        else:
            abort(401)

    @app.route('/routers')
    def routers():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "routers" not in accessO.getPermission():
                abort(403)
            accessO.addLogUser("Перегляд стрінки Обладнення")
        return(render_template("base.html", module="routers", head_name="Обладнення"))