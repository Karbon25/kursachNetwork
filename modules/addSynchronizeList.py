from Database import DBClient
def addSynchronizeList(router, name, json):
	connector = DBClient()
	connector.execute('''INSERT INTO `synchronizelist`(`idRouter`, `nameTask`, `jsonData`, `synchronized`, `numberAttempts`) VALUES ("{0}", "{1}", '{2}', 0, 0)'''.format(router, name, json.replace('"', '\\"')))
	connector.DBclose()
	del connector