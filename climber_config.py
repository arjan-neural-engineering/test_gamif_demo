
# functions to append to bottom of climber_config.py (alternatively this
# module can be loaded directly)
import os.path
import json
def getClimberPath():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def loadLocalSysConfig():
    climberPath = getClimberPath()
    jsonFilename = climberPath + "/config_local/SystemConfig.json"
    if os.path.exists(jsonFilename):
        with open(jsonFilename, 'r') as f:
            sysConfig = json.load(f)
            f.close()
    else:
        sysConfig = False
        print("Warning: SystemConfig.json not found")
    return sysConfig

def loadLocalComPortConfig():
    climberPath = getClimberPath()
    jsonFilename = climberPath + "/config_local/ComPortConfig.json"
    if os.path.exists(jsonFilename):
        with open(jsonFilename, 'r') as f:
            comPortConfig = json.load(f)
            f.close()
    else:
        comPortConfig = False
        print("Warning: ComPortConfig.json not found")
    return comPortConfig
# functions to append to bottom of climber_config.py (alternatively this
# module can be loaded directly)
import os.path
import json
def getClimberPath():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def loadLocalSysConfig():
    climberPath = getClimberPath()
    jsonFilename = climberPath + "/config_local/SystemConfig.json"
    if os.path.exists(jsonFilename):
        with open(jsonFilename, 'r') as f:
            sysConfig = json.load(f)
            f.close()
    else:
        sysConfig = False
        print("Warning: SystemConfig.json not found")
    return sysConfig

def loadLocalComPortConfig():
    climberPath = getClimberPath()
    jsonFilename = climberPath + "/config_local/ComPortConfig.json"
    if os.path.exists(jsonFilename):
        with open(jsonFilename, 'r') as f:
            comPortConfig = json.load(f)
            f.close()
    else:
        comPortConfig = False
        print("Warning: ComPortConfig.json not found")
    return comPortConfig