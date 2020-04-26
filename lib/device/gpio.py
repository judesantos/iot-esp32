
import machine

def handleCommand(req):
    validCommand = True
    res = {
        "response": {}
    }

    pin = req['pin']
    io_type = machine.Pin.OUT if 'out' is req['type'] else machine.Pin.IN
    # get GPIO object
    led = machine.Pin(pin, io_type)
    command = req['data']['command']

    if 'enable' == command:
        # set its value
        value = 1 if req['data']['value'] is True else 0
        led.value(value)
    else:
        validCommand = False

    # check state
    if True is validCommand:
        gpio_state="OFF"
        if led.value() == 1:
            gpio_state="ON"
        ''' send response '''
        res['response'] = {
            'state': gpio_state
        }
    else:
        res['response'] = {
            'error': 'Command not recognized'
        }

    res['request'] = req
    return res

