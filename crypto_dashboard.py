import json
from flask import Flask, render_template, abort
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

from distutils.util import strtobool

app = Flask(__name__)



def getCmcData(apiKey, url, endpoint, tickers):
	# prepare the request
	requestUrl = url + endpoint
	parameters = {
		'symbol' : tickers,
		'convert' : 'EUR',
		'aux' : 'cmc_rank'
	}
	headers = {
		'Accepts': 'application/json',
		'X-CMC_PRO_API_KEY': apiKey
	}
	
	#send the request
	session = Session()
	session.headers.update(headers)
	response = session.get(requestUrl, params=parameters).json()
	
	return response


def prepCmcData(rawData, tickers):
	data = rawData
	for coin in tickers.split(","):
		#on the sandbox version, CMC sometimes replaces the value for price change with "None", which throw an error when converting to float -> we juste replace it by 0
		if data["data"][coin]["quote"]["EUR"]["percent_change_24h"] == None:
			data["data"][coin]["quote"]["EUR"]["percent_change_24h"] = 0
		
		data["data"][coin]["quote"]["EUR"]["price"] = round(float(data["data"][coin]["quote"]["EUR"]["price"]), 4)
		data["data"][coin]["quote"]["EUR"]["percent_change_24h"] = round(float(data["data"][coin]["quote"]["EUR"]["percent_change_24h"]), 2)
	
	return data



def getCroData(url, endpoint, wallet):
	#prepare the request
	requestUrl = url + endpoint + "/" + wallet
	
	#send the request
	session = Session()
	response = session.get(requestUrl).json()
	
	return response

def prepCroData(rawData, croPrice):
	data = rawData
	for i in ["balance", "bondedBalance", "totalRewards", "totalBalance"]:
		data["result"][i][0]["amount"] = round(float(data["result"][i][0]["amount"]) / 100000000, 6)
		data["result"][i][0]["eurValue"] = round(float(data["result"][i][0]["amount"]) * float(croPrice), 3)
	
	return data




@app.route('/')
@app.route('/dashboard/')
def display_dashboard():
	with open("config.json", "r") as configFile :
		conf = json.loads(configFile.read())
		if strtobool(conf["testMode"]):
			conf.update(conf["test"])
		else:
			conf.update(conf["run"])
		conf.pop("test")
		conf.pop("run")
		print(json.dumps(conf, indent = 3))
	
	
	try :
		cmcData = getCmcData(url = conf["coinMarketCap"]["apiUrl"], endpoint = conf["coinMarketCap"]["endpoint"], tickers = conf["coinMarketCap"]["tickers"], apiKey = conf["coinMarketCap"]["apiKey"])
		print(cmcData)
	except(ConnectionError, Timeout, TooManyRedirects) as e:
		print(e)
		
	cmcData = prepCmcData(cmcData, conf["coinMarketCap"]["tickers"])
	
	
	try:
		croData = getCroData(url = conf["cryptoOrgChain"]["apiUrl"], endpoint = conf["cryptoOrgChain"]["endpoint"], wallet = conf["cryptoOrgChain"]["accountAddress"])
	except(ConnectionError, Timeout, TooManyRedirects) as e:
		print(e)
		
	croData = prepCroData(croData, cmcData["data"]["CRO"]["quote"]["EUR"]["price"])
	
	
	darkmode = bool(strtobool(conf["darkMode"]))
	
	return render_template('dashboard.html', cmc = cmcData, cro = croData, darkmode = darkmode, test = bool(strtobool(conf["testMode"])))







if __name__ == '__main__':
	app.run(debug = True)