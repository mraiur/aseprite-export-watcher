import os
import json

configFilePath = "config.json"

if os.path.exists(configFilePath) == False:
    print('Configuration file not found ', configFilePath)
    exit()

fileHandler = open(configFilePath)
configJson = json.load(fileHandler)
fileHandler.close()

# Don't use directly the read data in case of a validation need
data = configJson