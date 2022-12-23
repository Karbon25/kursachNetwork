from Database import DBClient
from flask import Flask, render_template, request, abort, session, redirect
import routeros_api, json, addSynchronizeList
from AccessModule import AccessModule

def getFunctionTariffs(app, listNav):
    @app.route("/ajax/tariffsListUpdate", methods=["POST"])
    def ajaxTariffsListUpdate():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "tariffs" not in accessO.getPermission():
                abort(403)

        connector = DBClient()
        dataTariff = connector.executeSelect('''SELECT `name`, `price`, `activeTariff`, `idTariff`,`idTariff` FROM `tariff` ORDER BY `idTariff` DESC''')
        dataTariff = list(dataTariff)
        if(dataTariff):
            for i in  range(0, len(dataTariff)):
                dataTariff[i] = list(dataTariff[i])
                if dataTariff[i][2] == 1:
                    dataTariff[i][2] = '''<p>Тариф активний</p>'''
                else:
                    dataTariff[i][2] = '''<p style="color:red">Тариф не активний</p>'''
                dataTariff[i][3] = '''<button type="button" class="btn btn-outline-success" onclick="showEdit({0});">Редагувати</button>'''.format(dataTariff[i][3]);
                dataTariff[i][4] = '''<button type="button" class="btn btn-outline-danger" onclick="showRemove({0});">Видалити</button>'''.format(dataTariff[i][4]);
                dataTariff[i].insert(0, i+1)  
        connector.DBclose()
        del connector
        return(json.dumps({"data":dataTariff}))
    @app.route("/ajax/getTariffData", methods=["POST"])
    def ajaxGetTariffData():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "tariffs" not in accessO.getPermission():
                abort(403)
        if "idTariff" in request.form:
            connector = DBClient()
            dataTariff = connector.executeSelect('''SELECT `idTariff`, `name`, `price`, `rxLimit`, `txLimit`, `activeTariff` FROM `tariff` WHERE `idTariff` = "{0}"'''.format(request.form["idTariff"]))
            connector.DBclose()
            del connector
            if(dataTariff != []):
                accessO.addLogUser("Перегляд даних тарифу {0}".format(dataTariff[0][1]))
            return(json.dumps({"data":dataTariff}))
        else:
            abort(401)
    @app.route("/ajax/editTariffData", methods=["POST"])
    def ajaxEditTariffData():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "tariffs" not in accessO.getPermission():
                abort(403)
        if "idTariff" in request.form:
            connector = DBClient()
            if(connector.execute(''' UPDATE `tariff` SET `name`="{0}",`price`="{1}",`rxLimit`="{2}",`txLimit`="{3}",`activeTariff`="{4}" WHERE `idTariff` = "{5}"'''.format(request.form["name"], request.form["price"], request.form["rxLimit"], request.form["txLimit"], request.form["active"], request.form["idTariff"])) != None):
                jsonData = {"loadModule":"changeTariff", "paramModule":{"idTariff":str(request.form["idTariff"]), "rxLimit":str(request.form["rxLimit"]), "txLimit": str(request.form["txLimit"])}}
                addSynchronizeList.addSynchronizeList(1,"Зміни в тарифі {0}".format(request.form["idTariff"]), json.dumps(jsonData))
                connector.DBclose()
                del connector
                accessO.addLogUser("Зміна даних тарифу id {0}".format(request.form["idTariff"]))
                return("True")
            else:
                connector.DBclose()
                del connector
                return("False")
        else:
            abort(401)


    @app.route("/ajax/removeTariffData", methods=["POST"])
    def ajaxRemoveTariffData():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "tariffs" not in accessO.getPermission():
                abort(403)
        if "idTariff" in request.form:
            connector = DBClient()
            dataClient = connector.executeSelect('''SELECT `idClient` FROM `clients` WHERE `idTariff` = "{0}"'''.format(request.form["idTariff"]))
            if dataClient == []:
                if(connector.execute('''DELETE FROM `tariff` WHERE `idTariff`="{0}"'''.format(request.form["idTariff"])) != None):
                    accessO.addLogUser("Видалення тарифу id {0}".format(request.form["idTariff"]))
                    jsonData = {"loadModule":"removeTariff", "paramModule":{"idTariff":str(request.form["idTariff"])}}
                    addSynchronizeList.addSynchronizeList(1,"Видалення тарифу {0}".format(request.form["idTariff"]), json.dumps(jsonData))
                    connector.DBclose()
                    del connector
                    return("True")
                else:
                    connector.DBclose()
                    del connector
                    return("Виникла помилка. Тариф не видалено")
            else:
                return("В системі зареєстровані клієнти з даним тарифом. Змініть тариф на інший перед видаленням")
        else:
            abort(401)


    @app.route("/ajax/addTariffData", methods=["POST"])
    def ajaxAddTariffData():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "tariffs" not in accessO.getPermission():
                abort(403)
            connector = DBClient()
            executeReturn = connector.execute('''INSERT INTO `tariff`(`name`, `price`, `rxLimit`, `txLimit`, `activeTariff`) VALUES ("{0}","{1}","{2}","{3}","{4}")'''.format(request.form["name"], request.form["price"], request.form["rxLimit"], request.form["txLimit"], request.form["active"]))
            if(executeReturn != False):
                accessO.addLogUser("Додання тарифу {0} присвоєне id {1}".format(request.form["name"], executeReturn))
                jsonData = {"loadModule":"addNewTariff", "paramModule":{"idTariff":str(executeReturn), "rxLimit":str(request.form["rxLimit"]), "txLimit": str(request.form["txLimit"])}}
                addSynchronizeList.addSynchronizeList(1,"Завантаження нового тарифу {0}".format(executeReturn), json.dumps(jsonData))
                connector.DBclose()
                del connector
                return("True")
            else:
                connector.DBclose()
                del connector 
                return("False")



    @app.route('/tariff')
    def tariff():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "tariffs" not in accessO.getPermission():
                abort(403)
        accessO.addLogUser("Перегляд сторінки Тарифи")
        return(render_template("base.html", module="tariffs", head_name="Тарифи"))


