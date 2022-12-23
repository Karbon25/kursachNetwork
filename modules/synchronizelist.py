from Database import DBClient
from flask import Flask, render_template, request, abort, session, redirect
import json
from AccessModule import AccessModule


def getFunctionSynchronizeList(app, listNav):

    @app.route("/ajax/synchronizeListUpdate", methods=["POST"])
    def ajaxSynchronizeListUpdate():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "synchronizelist" not in accessO.getPermission():
                abort(403)

        connector = DBClient()
        if request.form["loadAllData"] == "0":
            sql = '''SELECT `routers`.`name`, `nameTask`, `synchronized`, `numberAttempts`, `idTask` FROM `synchronizelist` INNER JOIN `routers` ON `routers`.`idRouter` = `synchronizelist`.`idRouter` WHERE `synchronized` = 0 ORDER BY `idTask` DESC'''
        else:
            sql = '''SELECT `routers`.`name`, `nameTask`, `synchronized`, `numberAttempts`, `idTask` FROM `synchronizelist` INNER JOIN `routers` ON `routers`.`idRouter` = `synchronizelist`.`idRouter` ORDER BY `idTask` DESC'''
            
        dataSynchronize = connector.executeSelect(sql)
        dataSynchronize = list(dataSynchronize)
        if(dataSynchronize):
            for i in  range(0, len(dataSynchronize)):
                dataSynchronize[i] = list(dataSynchronize[i])
                if dataSynchronize[i][2] == 0:
                    dataSynchronize[i][4] = '''<button type="button" class="btn btn-outline-danger" onclick="showRemove({0});">Видалити</button>'''.format(dataSynchronize[i][4]);
                else:
                    dataSynchronize[i][4] = "Синхронізовані задачі не видаляються"
                

                if dataSynchronize[i][2] == 0:
                    dataSynchronize[i][2] = '''<p style="color:red">Не синхронізовано</p>'''
                else:
                    dataSynchronize[i][2] = '''<p style="color:green">Синхронізовано</p>'''
               
                dataSynchronize[i].insert(0, i+1)  
        connector.DBclose()
        del connector
        return(json.dumps({"data":dataSynchronize},default=str))

    @app.route("/ajax/removeSynchronizeList", methods=["POST"])
    def ajaxRemoveSynchronizeList():
        print("hello")
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "synchronizelist" not in accessO.getPermission():
                abort(403)
        
        if "idTask" in request.form:
            connector = DBClient()
            dataTask = connector.executeSelect('''SELECT `idTask`, `nameTask` FROM `synchronizelist` WHERE `synchronized` = 0 and `idTask`="{0}"'''.format(request.form["idTask"]))
            if(dataTask != []):
                if(connector.execute('''DELETE FROM `synchronizelist` WHERE `idTask` =  "{0}"'''.format(request.form["idTask"])) != None):
                    connector.DBclose()
                    del connector
                    accessO.addLogUser("Видалення задачі синхронізації {0}".format(dataTask[0][1]))
                    return("True")
                else:
                    connector.DBclose()
                    del connector
                    return("False")
            else:
                connector.DBclose()
                del connector
                return("False")
        else:
            print("hello0")
            abort(401)


    @app.route('/synchronizelist')
    def synchronizeList():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "synchronizelist" not in accessO.getPermission():
                abort(403)
        accessO.addLogUser("Перегляд стрінки Синхронізація")
        return(render_template("base.html", module="synchronizeList", head_name="Синхронізація"))