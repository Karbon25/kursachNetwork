from flask import session
import pickle, os
import codecs
from Database import DBClient
class AccessModule():
	def setData(self, login, idUser, permission, username):
		self.__login = login
		self.__idUser = idUser
		session["login"] = self.__login
		self.__permission = permission.split(" ")
		self.__username = username
		self.__token = os.urandom(24)
		session["token"] = self.__token
		self.__saveData()
	def getName(self):
		return(self.__username)
	def getLogin(self):
		return(self.__login)
	def getPermission(self):
		return(self.__permission)
	def loadData(self, login):
		try:
			result = False
			connector = DBClient()
			dataLogin = connector.executeSelect('''SELECT `authObject` FROM `users` WHERE `login` = "{0}"'''.format(login))
			if(dataLogin):
				dataLoad = pickle.loads(codecs.decode(dataLogin[0][0].encode(), "base64"))
				if(dataLoad[4] == session["token"]):
					self.__idUser = dataLoad[0]
					self.__username = dataLoad[1]
					self.__login = dataLoad[2]
					self.__permission = dataLoad[3]
					self.__token = dataLoad[4]
					result = True
			connector.DBclose()
			del connector
			return(result)
		except Exception as e:
			return(False)
		
	def addLogUser(self, message):
		connector = DBClient()
		connector.execute('''INSERT INTO `logsuser`(`idUser`, `text`, `date`) VALUES ("{0}", "{1}", NOW())'''.format(self.__idUser, message))
		connector.DBclose()
		del connector
	def __saveData(self):
		if(self.__login != None):
			connector = DBClient()
			connector.execute('''UPDATE `users` SET `authObject`="{0}" WHERE `login` = "{1}"'''.format(codecs.encode(pickle.dumps([self.__idUser, self.__username, self.__login, self.__permission, self.__token]), "base64").decode(), self.__login))
			connector.DBclose()
			del connector
		