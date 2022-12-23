from Database import DBClient
from flask import Flask, render_template, request, abort, session, redirect
import routeros_api, json
from AccessModule import AccessModule

def getFunctionUsers(app, listNav):
    @app.route("/ajax/usersListUpdate", methods=["POST"])
    def ajaxUsersListUpdate():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "users" not in accessO.getPermission():
                abort(403)

        connector = DBClient()
        dataUser = connector.executeSelect('''SELECT `fullName`, `login`, `idUser`, `idUser` FROM `users`''')
        dataUser = list(dataUser)
        if(dataUser):
            for i in  range(0, len(dataUser)):
                dataUser[i] = list(dataUser[i])
                dataUser[i][2] = '''<button type="button" class="btn btn-outline-success" onclick="showEdit({0});">Редагувати</button>'''.format(dataUser[i][2]);
                dataUser[i][3] = '''<button type="button" class="btn btn-outline-danger" onclick="showRemove({0});">Видалити</button>'''.format(dataUser[i][3]);
                dataUser[i].insert(0, i+1)  
        connector.DBclose()
        del connector
        return(json.dumps({"data":dataUser}))
    @app.route("/ajax/getUserData", methods=["POST"])
    def ajaxGetUserData():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "users" not in accessO.getPermission():
                abort(403)
        if "idUser" in request.form:
            connector = DBClient()
            dataUser = connector.executeSelect('''SELECT `idUser`, `fullName`, `login`, `permission` FROM `users` WHERE `idUser` = "{0}"'''.format(request.form["idUser"]))
            connector.DBclose()
            del connector
            accessO.addLogUser("Перегляд даних користувача id".format(request.form["idUser"]))
            return(json.dumps({"data":dataUser}))
        else:
            abort(401)
    @app.route("/ajax/editUserData", methods=["POST"])
    def ajaxEditUserData():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "users" not in accessO.getPermission():
                abort(403)
        if "idUser" in request.form:
            connector = DBClient()
            sql = '''UPDATE `users` SET `fullName`='{0}',`login`='{1}',`permission`='{2}',`authObject`="" WHERE `idUser` = "{3}"'''.format(request.form["name"],request.form["login"],request.form["permission"],request.form["idUser"])
            if request.form["password"] != "":
                sql = ''' UPDATE `users` SET `fullName`='{0}',`login`='{1}',`permission`='{2}', `password`=SHA1("{3}"), `authObject`="" WHERE `idUser` = "{4}"'''.format(request.form["name"],request.form["login"],request.form["permission"], request.form["password"],request.form["idUser"])
            if(connector.execute(sql) != None):
                connector.DBclose()
                del connector
                accessO.addLogUser("Реедагування даних користувача id {0}".format(request.form["idUser"]))
                return("True")
            else:
                connector.DBclose()
                del connector
                return("False")
        else:
            abort(401)


    @app.route("/ajax/removeUserData", methods=["POST"])
    def ajaxRemoveUserData():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "users" not in accessO.getPermission():
                abort(403)
        if "idUser" in request.form:
            connector = DBClient()
            if(connector.execute('''DELETE FROM `users` WHERE `idUser`="{0}"'''.format(request.form["idUser"])) != None):
                connector.DBclose()
                del connector
                accessO.addLogUser("Видалення користувача id {0}".format(request.form["idUser"]))
                return("True")
            else:
                connector.DBclose()
                del connector
                return("False")
        else:
            abort(401)


    @app.route("/ajax/addUserData", methods=["POST"])
    def ajaxAddUserData():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "users" not in accessO.getPermission():
                abort(403)
            connector = DBClient()
            sql = '''INSERT INTO `users`(`fullName`, `login`, `password`, `permission`) VALUES ("{0}", "{1}", SHA1("{3}"), "{2}")'''.format(request.form["name"],request.form["login"],request.form["permission"], request.form["password"])
            executeAddUser = connector.execute(sql)
            if(executeAddUser != False):
                connector.DBclose()
                del connector
                accessO.addLogUser("В систему додано користувача {0}, присвоєно id {1}".format(request.form["login"], executeAddUser))
                return("True")
            else:
                connector.DBclose()
                del connector 
                return("False")



    @app.route('/users')
    def users():
        if "login" not in session:
            return(redirect("/login"))
        else:
            accessO = AccessModule()
            if not accessO.loadData(session["login"]):
                return(redirect("/exit"))
            elif "users" not in accessO.getPermission():
                abort(403)
        accessO.addLogUser("Перегляд сторінки Користувачі системи")
        return(render_template("base.html", module="users", head_name="Користувачі системи", listNav=listNav))


