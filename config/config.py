from os.path import dirname,abspath ,isfile,join
import json

def db_config():
    with open(dirname(abspath(__file__))+r'/config.json','r') as json_file:
        data=json.load(json_file)
    return data['db_config']['URI'], data['db_config']['collection_name']