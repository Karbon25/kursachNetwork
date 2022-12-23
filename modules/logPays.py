from Database import DBClient
from flask import Flask, render_template, request, abort, session, redirect
import json
from AccessModule import AccessModule


def getFunctionLogPays(app, listNav):

    @app.route("/ajax/logPaysListUpdate", methods=["POST"])
    def ajaxlogPaysListUpdate():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "logPays" not in accessO.getPermission():
                abort(403)

        connector = DBClient()
        if request.form["loadAllData"] != "0":
            sql = '''SELECT  IF(`clients`.`fullName` IS NULL, CONCAT("Видалений клієнт з id ", `logspay`.`idClient`), `clients`.`fullName`), `date`, `pay` FROM `logspay` LEFT JOIN `clients` ON `clients`.`idClient` = `logspay`.`idClient` ORDER BY `logspay`.`idPay` DESC'''
        else:
            sql = '''SELECT  IF(`clients`.`fullName` IS NULL, CONCAT("Видалений клієнт з id ", `logspay`.`idClient`), `clients`.`fullName`), `date`, `pay` FROM `logspay` LEFT JOIN `clients` ON `clients`.`idClient` = `logspay`.`idClient` ORDER BY `logspay`.`idPay` DESC LIMIT 100 '''
        dataPaysLog = connector.executeSelect(sql)
        dataPaysLog = list(dataPaysLog)
        if(dataPaysLog):
            for i in  range(0, len(dataPaysLog)):
                dataPaysLog[i] = list(dataPaysLog[i])
                dataPaysLog[i].insert(0, i+1)  
        connector.DBclose()
        del connector
        return(json.dumps({"data":dataPaysLog},default=str))

   
    @app.route('/logPays')
    def logPays():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "logPays" not in accessO.getPermission():
                abort(403)
        accessO.addLogUser("Перегляд сторінки Списання з рахунків клієнтів")   
        return(render_template("base.html", module="logPays", head_name="Списання з рахунків клієнтів"))