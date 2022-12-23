import sys
sys.path.append('modules')
from Database import DBClient
import addSynchronizeList, json
def pays():
	connector = DBClient()
	dataClient = connector.executeSelect('''SELECT `clients`.`idClient`, `tariff`.`price`, `clients`.`idTariff`, `clients`.`numberContract`, `clients`.`idRouter`, `clients`.`state` FROM `clients` INNER JOIN `tariff` ON `tariff`.`idTariff` = `clients`.`idTariff` WHERE `clients`.`idClient` NOT IN (SELECT `idClient` FROM `logspay` WHERE `date` = DATE(NOW()))''')
	for step in dataClient:
		dataPayClient = connector.executeSelect('''SELECT SUM(`price`) FROM `pays` WHERE `idClient` = "{0}" GROUP BY `idClient`'''.format(step[0]))
		if dataPayClient != []:
			if(float(dataPayClient[0][0]) >= round(float(float(step[1])*12/365), 2)):
				connector.execute('''INSERT INTO `pays`(`idClient`, `price`, `date`) VALUES ("{0}", "-{1}", NOW())'''.format(step[0], round(float(float(step[1])*12/365), 2)))
				connector.execute('''INSERT INTO `logspay`(`idClient`, `pay`, `date`) VALUES ("{0}", "{1}", NOW())'''.format(step[0], round(float(float(step[1])*12/365), 2)))
				if step[5] == 0:
					connector.execute('''UPDATE `clients` SET `state`= 1 WHERE `idClient` = "{0}"'''.format(step[0]))
					jsonData = {"loadModule":"provideService", "paramModule":{"idRouter":step[4], "numberContract":step[3], "tariff":str(step[2])}}
					addSynchronizeList.addSynchronizeList(step[4],"Надати послугу клієнту {0}".format(step[3]), json.dumps(jsonData))
			elif step[5] == 1:
				connector.execute('''UPDATE `clients` SET `state`= 0 WHERE `idClient` = "{0}"'''.format(step[0]))
				jsonData = {"loadModule":"prohibitServiceProvision", "paramModule":{"idRouter":step[4], "numberContract":step[3]}}
				addSynchronizeList.addSynchronizeList(step[4],"Заборонити надання послуги клієнту {0}".format(step[3]), json.dumps(jsonData))
		elif step[5] == 1:
			connector.execute('''UPDATE `clients` SET `state`= 0 WHERE `idClient` = "{0}"'''.format(step[0]))
			jsonData = {"loadModule":"prohibitServiceProvision", "paramModule":{"idRouter":step[4], "numberContract":step[3]}}
			addSynchronizeList.addSynchronizeList(step[4],"Заборонити надання послуги клієнту {0}".format(step[3]), json.dumps(jsonData))


if __name__ == '__main__':
	pays()
	