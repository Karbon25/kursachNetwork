from Database import DBClient
from flask import Flask, render_template, request, abort, session, redirect
import json
from AccessModule import AccessModule


def getFunctionLogRouter(app, listNav):

    @app.route("/ajax/logRouterListUpdate", methods=["POST"])
    def ajaxlogRouterListUpdate():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "logRouter" not in accessO.getPermission():
                abort(403)

        connector = DBClient()
        if request.form["loadAllData"] != "0":
            sql = '''SELECT IF(`routers`.`name` IS NULL, CONCAT("Видалений роутер з id ", `logsrouter`.`idRouter`), `routers`.`name`), `date`, `text` FROM `logsrouter` LEFT JOIN `routers` ON `routers`.`idRouter` = `logsrouter`.`idRouter` ORDER BY `idLog` DESC '''
        else:
            sql = '''SELECT IF(`routers`.`name` IS NULL, CONCAT("Видалений роутер з id ", `logsrouter`.`idRouter`), `routers`.`name`), `date`, `text` FROM `logsrouter` LEFT JOIN `routers` ON `routers`.`idRouter` = `logsrouter`.`idRouter` ORDER BY `idLog` DESC LIMIT 30 '''
            
        dataRouter = connector.executeSelect(sql)
        dataRouter = list(dataRouter)
        if(dataRouter):
            for i in  range(0, len(dataRouter)):
                dataRouter[i] = list(dataRouter[i])
                dataRouter[i].insert(0, i+1)  
        connector.DBclose()
        del connector
        return(json.dumps({"data":dataRouter},default=str))

   
    @app.route('/logRouter')
    def logRouter():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "logRouter" not in accessO.getPermission():
                abort(403)
        accessO.addLogUser("Перегляд сторінки Логи обладнення")
        return(render_template("base.html", module="logRouter", head_name="Логи обладнення"))