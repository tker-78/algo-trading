import configparser

conf = configparser.ConfigParser()
conf.read('settings.ini')

apiLabel= conf["gmo"]["api_label"]
apiKey = conf["gmo"]["api_key"]
secretKey = conf["gmo"]["secret_key"]
tradeDuration = conf["gmo"]["duration"]
tradeCurrency = conf["gmo"]["currency"]

dbName = conf["db1"]["db_name"]


logFileName = conf["log"]["log_file"]
logFileNameStream = conf["log"]["log_file_stream"]