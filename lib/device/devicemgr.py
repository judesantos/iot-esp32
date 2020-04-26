
from lib.device import gpio

def processRequest(req):
    prop = req['property']
    if 'gpio' == prop:
        return gpio.handleCommand(req)
    return None
