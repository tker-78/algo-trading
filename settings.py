import configparser

conf = configparser.ConfigParser()
conf.read('settings.ini')

apiLabel= conf["gmo"]["api_label"]
apiKey = conf["gmo"]["api_key"]
secretKey = conf["gmo"]["secret_key"]

dbName = conf["db1"]["db_name"]