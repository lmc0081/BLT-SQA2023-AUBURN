import logging

def createLoggerObj(): 
    fileName  = 'Forensics-Logger-KubeSec.log' 
    formatStr = '%(asctime)s %(message)s'
    logging.basicConfig(format=formatStr, filename=fileName, level=logging.INFO)
    myLogObj = logging.getLogger('sqa2023project-logger') 
    return myLogObj