from flask import Flask, render_template, request, redirect, session, abort
import routeros_api, json
import sys
sys.path.append('modules')
from Database import DBClient
from AccessModule import AccessModule
import routers, clients, users, tariffs,logRouter,logUsers,logPays,pays,synchronizelist

app = Flask(__name__)
listNav = [["users",["Користувачі системи", "/users"]], ["clients", ["Клієнти", "/clients"]], ["routers", ["Обладнення", "/routers"]], ["pays", ["Баланс", "/pays"]], ["logRouter", ["Логи обладнення", "/logRouter"]], ["logUsers", ["Логи користувачів", "/logUsers"]], ["tariffs", ["Тарифи", "/tariff"]], ["synchronizelist", ["Задачі синхронізації", "/synchronizelist"]], ["logPays", ["Списання з рахунків клієнтів", "/logPays"]]]

routers.getFunctionRouter(app, listNav)
clients.getFunctionClient(app, listNav)
users.getFunctionUsers(app, listNav)
tariffs.getFunctionTariffs(app, listNav)
logRouter.getFunctionLogRouter(app, listNav)
logUsers.getFunctionLogUsers(app, listNav)
logPays.getFunctionLogPays(app, listNav)
pays.getFunctionPays(app, listNav)
synchronizelist.getFunctionSynchronizeList(app, listNav)

@app.route('/')
def index():
    if "login" not in session:
        return(redirect("/login"))
    else:
        accessO = AccessModule()
        if not accessO.loadData(session["login"]):
            return(redirect("/exit"))
    connector = DBClient()
    countClient = connector.executeSelect('''SELECT COUNT(`idClient`) FROM `clients`''')[0][0]
    countActiveClient = connector.executeSelect('''SELECT COUNT(`idClient`) FROM `clients` WHERE `active` = 1''')[0][0]
    countStateActiveClient = connector.executeSelect('''SELECT COUNT(`idClient`) FROM `clients` WHERE `state` = 1''')[0][0]
    countRouters = connector.executeSelect('''SELECT COUNT(`idRouter`) FROM `routers`''')[0][0]
    countActiveRouter = connector.executeSelect('''SELECT COUNT(`idRouter`) FROM `routers` WHERE `active` = 1''')[0][0]
    connector.DBclose()
    del connector
    return(render_template("base.html", module="index", head_name="Головна", countClient=countClient, countActiveClient=countActiveClient, countStateActiveClient=countStateActiveClient, countRouters=countRouters, countActiveRouter=countActiveRouter))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        error = None
        if request.args.get("error"):
            error = request.args.get("error")
        return(render_template("login.html", error=error))
    else:
        if("login" in request.form and "password" in request.form):
            connector = DBClient()
            dataLogin = connector.executeSelect('''SELECT `idUser`, `fullName`, `login`, `permission` FROM `users` WHERE `login` = "{0}" and `password` = SHA1("{1}")'''.format(request.form["login"], request.form["password"]))
            if(dataLogin):
                dataLogin = dataLogin[0]
                accessO = AccessModule()
                accessO.setData(dataLogin[2], dataLogin[0], dataLogin[3], dataLogin[1])
                permission = accessO.getPermission()
                listNavUser = list()
                for key, value in listNav:
                    if key in permission:
                        listNavUser.append(value)
                session["nav"] = listNavUser
                session["username"] = dataLogin[1]
                accessO.addLogUser("Вхід в систему")
                connector.DBclose()
                del connector
                return(redirect("/"))
            else:
                connector.DBclose()
                del connector
                return(redirect("/login?error={0}".format("Не вірний логин чи пароль")))
        else:
            return(redirect("/login?error={0}".format("Введіть логин та пароль")))
@app.route("/exit")
def exit():
    if "login" in session:
        session.pop("login")
    if "username" in session:
        session.pop("username")
    if "token" in session:
        session.pop("token")
    if "nav" in session:
        session.pop("nav")
    return(redirect("/login"))
# @app.errorhandler(404)
# def error_404(error):
#     return("404")
# @app.errorhandler(403)
# def error_403(error):
#     return(render_template('error/403.html'))
# @app.errorhandler(401)
# def error_401(error):
#     return("401")
# @app.errorhandler(500)
# def error_500(error):
#     return(render_template('error/500.html'))
if __name__ == '__main__':
    app.secret_key = "12345652523343421235123512512"
    app.run('localhost', 81, debug=True)