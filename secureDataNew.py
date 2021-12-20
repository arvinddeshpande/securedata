import os
import json
from datetime import datetime
import pathlib

def main():
    global securePath
    global settings
    global data
    global logPath

    thisDirectory = pathlib.Path(__file__).parent.resolve()
    os.chdir(thisDirectory)
    
    # initialize settings file if it doesn't exist
    _settingsFile = open('settings.json', 'r+')
    if(len(_settingsFile.read()) == 0):
        _settingsFile.write('{}')
    _settingsFile.close()

    # initialize data file if it doesn't exist
    _dataFile = open('data.json', 'r+')
    if(len(_dataFile.read()) == 0):
        _dataFile.write('{}')
    _dataFile.close()

    settings = json.load(open('settings.json'))
    data = json.load(open('data.json'))

    # Determines where data is stored, like `securePath = "/home/raspberry/data"`
    securePath = getItem('path_secureData') or setItem(
        'path_secureData', str(thisDirectory), fileName='settings.json')

    logPath = getItem('path_log') or setItem(
        'path_log', securePath + '/log', fileName='settings.json')
    if not os.path.exists(logPath):
        os.makedirs(logPath)
 
def getItem(*attribute):
    """
    Returns a property in settings.json.
    Usage: get('person', 'name')
    """

    global settings
    _settings = settings

    for index, item in enumerate(attribute):
        if item in _settings:
            _settings = _settings[item]
        else:
            print(f"Warning: {item} not found in {_settings if index > 0 else 'settings.json'}")
            return None

    return _settings

def setItem(*attribute, value=None, fileName='data.json'):
    """
    Sets a property in data.json (or some other `fileName`).
    Usage: set('person', 'name', 'Tyler')
    The last argument is the value to set, unless value is specified.
    Returns the value set.
    """

    global data

    if(not value):
        value = attribute[-1]

    _data = data if fileName == 'data.json' else json.load(open(fileName))

    # iterate through entire JSON object and replace 2nd to last attribute with value

    partition = _data
    for index, item in enumerate(attribute[:-1]):
        if item not in partition:
            partition[item] = value if index == len(attribute) - 2 else {}
            partition = partition[item]
            print(f"Warning: {item} not found in {partition if index > 0 else fileName}")
        else:
            if(index == len(attribute) -2):
                partition[item] = value
            else:
                partition = partition[item]

    with open(fileName, 'w+') as file:
        json.dump(_data, file, indent=4)

    return value

def readFile(file):
    """
    Reads a file (creating it if it doesn't exist) and returns its contents
    """
    with open(file, 'r+') as file:
        return file.read()

def writeFile(fileName, filePath="", content=""):
    """
    Writes a file to the specified path and creates subfolders if necessary
    """

    global logPath
    if(filePath == ""):
        filePath = logPath

    if not os.path.exists(filePath):
        os.makedirs(filePath)

    with open(filePath + "/" + fileName, 'w+') as file:
        file.write(content)

def log(content="", logName="LOG_DAILY", clear=False, filePath=""):
    """
    Appends to a log file, or deletes it if clear is True.
    """

    global logPath
    if(filePath == ""):
        filePath = logPath

    if(clear):
        print(f"Clearing {logName}")
        try:
            os.remove(logName)
        except:
            print(f"Error: {logName} not found")
        return

    content = f"{datetime.now().strftime('%H:%M:%S')}: {content}"

    print(content)

    writeFile(fileName=logName, filePath=filePath, content=content)

# Initialize
main()