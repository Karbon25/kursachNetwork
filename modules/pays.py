from Database import DBClient
from flask import Flask, render_template, request, abort, session, redirect
import routeros_api, json
from AccessModule import AccessModule

def getFunctionPays(app, listNav):
    @app.route("/ajax/paysListUpdate", methods=["POST"])
    def ajaxPaysListUpdate():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "pays" not in accessO.getPermission():
                abort(403)

        connector = DBClient()
        dataPays = connector.executeSelect('''SELECT IF(`clients`.`fullName` IS NULL, CONCAT("Видалений клієнт з id ", `pays`.`idClient`), `clients`.`fullName`), SUM(`pays`.`price`), `pays`.`idClient`, `pays`.`idClient` FROM `pays` LEFT JOIN `clients` ON `clients`.`idClient` = `pays`.`idClient` GROUP BY `pays`.`idClient`''')
        dataPays = list(dataPays)
        dataClients = connector.executeSelect('''SELECT `fullName`, 0, `idClient`, `idClient` FROM `clients` WHERE `idClient` NOT IN(SELECT `clients`.`idClient` as `idClient` FROM `clients` INNER JOIN `pays` ON `clients`.`idClient` = `pays`.`idClient`)''')
        for step in dataClients:
            dataPays.append(step)
        if(dataPays):
            for i in  range(0, len(dataPays)):
                dataPays[i] = list(dataPays[i])
                dataPays[i][1] = round(float(dataPays[i][1]), 2)
                dataPays[i][2] = '''<button type="button" class="btn btn-outline-success" onclick="showPays({0});">Перегляд оплат</button>'''.format(dataPays[i][2]);
                dataPays[i][3] = '''<button type="button" class="btn btn-outline-success" onclick="addPays({0});">Внести оплату</button>'''.format(dataPays[i][3]);
                dataPays[i].insert(0, i+1) 
        connector.DBclose()
        del connector
        return(json.dumps({"data":dataPays},default=str))


    @app.route("/ajax/getPays", methods=["POST"])
    def ajaxGetPaysData():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "pays" not in accessO.getPermission():
                abort(403)
        if "idClient" in request.form:
            connector = DBClient()
            dataPays = connector.executeSelect('''SELECT `price`, `date` FROM `pays` WHERE `idClient` = "{0}" ORDER BY `idPays` DESC'''.format(request.form["idClient"]))
            dataPays = list(dataPays)
            if(dataPays):
                for i in  range(0, len(dataPays)):
                    dataPays[i] = list(dataPays[i])
                    dataPays[i].insert(0, i+1)  

            if(dataPays):
                dataClient = connector.executeSelect('''SELECT `numberContract` FROM `clients` WHERE `idClient` = "{0}"'''.format(request.form["idClient"]))
                if dataClient != []:
                    accessO.addLogUser("Отримання історії оплат клієнта {0}".format(dataClient[0][0]))
                else:
                    accessO.addLogUser("Отримання історії оплатнесення оплати клієнта id {0}".format(request.form["idClient"]))
                connector.DBclose()
                del connector
                return(json.dumps({"data":dataPays},default=str))
            else:
                connector.DBclose()
                del connector
                return("False")
        else:
            abort(401)


    @app.route("/ajax/addPays", methods=["POST"])
    def ajaxAddPaysData():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "pays" not in accessO.getPermission():
                abort(403)
            if "idClient" in request.form and "price" in request.form and "date" in request.form:
                connector = DBClient()
                if(connector.execute('''INSERT INTO `pays`(`idClient`, `price`, `date`) VALUES ("{0}","{1}","{2}")'''.format(request.form["idClient"],request.form["price"],request.form["date"]))!= False):
                    dataClient = connector.executeSelect('''SELECT `numberContract` FROM `clients` WHERE `idClient` = "{0}"'''.format(request.form["idClient"]))
                    if dataClient != []:
                        accessO.addLogUser("Внесення оплати клієнта {0} на сумму {1}".format(dataClient[0][0], request.form["price"]))
                    else:
                        accessO.addLogUser("Внесення оплати клієнта id {0} на сумму {1}".format(request.form["idClient"],request.form["price"]))
                    connector.DBclose()
                    del connector 
                    return("True")
                else:
                    connector.DBclose()
                    del connector 
                    return("False")
            else:
                return("False")

    @app.route('/pays')
    def pays():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "pays" not in accessO.getPermission():
                abort(403)
        accessO.addLogUser("Перегляд сторінки Баланс")
        return(render_template("base.html", module="pays", head_name="Баланс"))


