from Database import DBClient
from flask import Flask, render_template, request, abort, session, redirect
import json
from AccessModule import AccessModule


def getFunctionLogUsers(app, listNav):

    @app.route("/ajax/logUsersListUpdate", methods=["POST"])
    def ajaxlogUsersListUpdate():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "logUsers" not in accessO.getPermission():
                abort(403)

        connector = DBClient()
        if request.form["loadAllData"] != "0":
            sql = '''SELECT  IF(`users`.`fullName` IS NULL, CONCAT("Видалений користувач з id ", `logsuser`.`idUser`), `users`.`fullName`), `date`, `text` FROM `logsuser` LEFT JOIN `users` ON `users`.`idUser` = `logsuser`.`idUser` ORDER BY `logsuser`.`idLog` DESC'''
        else:
            sql = '''SELECT  IF(`users`.`fullName` IS NULL, CONCAT("Видалений користувач з id ", `logsuser`.`idUser`), `users`.`fullName`), `date`, `text` FROM `logsuser` LEFT JOIN `users` ON `users`.`idUser` = `logsuser`.`idUser` ORDER BY `logsuser`.`idLog` DESC LIMIT 30 '''
        dataUserLog = connector.executeSelect(sql)
        dataUserLog = list(dataUserLog)
        if(dataUserLog):
            for i in  range(0, len(dataUserLog)):
                dataUserLog[i] = list(dataUserLog[i])
                dataUserLog[i].insert(0, i+1)  
        connector.DBclose()
        del connector
        return(json.dumps({"data":dataUserLog},default=str))

   
    @app.route('/logUsers')
    def logUsers():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "logUsers" not in accessO.getPermission():
                abort(403)
        accessO.addLogUser("Перегляд сторінки Логи")
        return(render_template("base.html", module="logUsers", head_name="Логи"))