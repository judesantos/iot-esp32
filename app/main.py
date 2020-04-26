
from lib.oled import OLED 
from lib import wifimgr
from lib.device import devicemgr
import ujson

try:
  import usocket as socket
except:
  import socket

oled = OLED.instance()

'''    
========================================================================

    Configure network - setup device as AP to configure local wifi access

========================================================================
'''

try:
    oled.text("Init AP server...")
    wlan = wifimgr.get_connection()
    if wlan is None:
        oled.text("  Connect failed")
        oled.text("  EXIT!")
        while True:
            pass
except OSError as e:
    print('wifi manager error:\n')
    print(e)
    oled.text("   Exception!")
    while True:
        pass

# access to local wifi now complete
# shutdown AP server
wifimgr.stop()


'''    
========================================================================

    Device is now connected to local LAN
    Initialize web services...

========================================================================
'''

oled.reset()
oled.text("   ESP32 App")
oled.text("ip:" + wifimgr.device_server_ip)
oled.text("")
oled.text(" listening...")

WS_log = True
WS_threaded = True

#
#    configure routes
#


''' 
    Main HTML page  
'''

from MicroWebSrv2 import *
from time import sleep

content = ''

@WebRoute(GET, '/')
def _rootAction(microWebSrv2, req):
    global content
    oled.textPosV("Request:", y=4)
    oled.textPosV(" %s" % req.UserAddress[0], y=5)
    # cached - load the first time
    if 0 == len(content):
        from app import html_tpl as tpl
        content = tpl.getMainPage()
    return req.Response.ReturnOk(content)

@WebRoute(GET, '/css/styles.css')
def _cssAction(microWebSrv2, req):
    #print('Got a css request')
    #print('dir: ' + str(os.listdir()))
    #print('cwd: ' + str(os.getcwd()))
    return req.Response.ReturnFile('/app/css/styles.css')


@WebRoute(GET, '/js/main.js')
def _jsAction(microWebSrv2, req):
    #print('Got a js request')
    #print('dir: ' + str(os.listdir()))
    #print('cwd: ' + str(os.getcwd()))
    return req.Response.ReturnFile('/app/js/main.js')


#   configure socket server
#

def _parseJson(s):
    try:
        json_o = ujson.loads(s)
    except:
        return None
    return json_o

def _jsonSuccessResponse(ws, resp, status=0, msg=''):
    print('_jsonSuccessResponse - send response')
    ws.SendTextMessage(ujson.dumps({
        "status": status,
        "message": msg,
        "data": resp
     }))

def _jsonErrorResponse(ws, req, status=-1, error='request failed'):
    return ws.SendTextMessage(ujson.dumps({
        "status": status,
        "message": error,
        "request": req
     }))

'''
    GPIO request
    {
        property: 'gpio',
        pin: 1,
        data: {
            command: 'enable',
            type: 'in/out',
            value: True/False
        }
    }
'''
def _processJsonRequest(ws, req):
    res = None
    #print('_processJsonRequest: ' + str(req))
    if 'property' in req:
        res = devicemgr.processRequest(req)
    if None == res:
        return _jsonErrorResponse(ws, req, error="invalid request")
    return _jsonSuccessResponse(ws, res)

def _onSocketAccept(microWebSrv2, ws):
    print('WebSocket accept!:')
    print(' - User: %s:%s' % ws.Request.UserAddress)
    print(' - Route: %s' % ws.Request.Path)
    print(' - Origin: %s' % ws.Request.Origin)
    # register event handlers
    ws.OnTextMessage = _onWsTextMsg
    ws.OnBinaryMessage = _onWsBinaryMsg
    ws.OnClosed = _onWsClosed

def _onWsTextMsg(ws, msg):
    print('webSocket rcvd: %s' % msg)
    try:
        req = _parseJson(msg)
        if not None is req:
            print('_onWsTextMsg - process request...')
            _processJsonRequest(ws, req)
        else:
            print('_onWsTextMsg - _isJson(msg) failed')
            _jsonErrorResponse(ws, msg, error="Not a valid json object")
    except Exception as err:
        print('_onWsTextMsg - exception: %s' % err)
  
def _onWsBinaryMsg(ws, msg):
    print('webSocket rcvd (binary): %s' % msg)

def _onWsClosed(ws):
    print('webSocket %s:%s closed' % ws.Request.UserAddress)


wsMod = MicroWebSrv2.LoadModule('WebSockets')
wsMod.OnWebSocketAccepted = _onSocketAccept

#
#   Init web server
#

srv = MicroWebSrv2()

srv.RootPath = '/'
srv.NotFoundURL = '/'
srv.SetEmbeddedConfig()

srv.BindAddress = (wifimgr.device_server_ip, 80)

srv.StartManaged()

try:
    while srv.IsRunning:
        sleep(1)
except KeyboardInterrupt:
    print('Stopping server...')
finally:
    oled.reset()
    srv.Stop()

print('Bye!')


