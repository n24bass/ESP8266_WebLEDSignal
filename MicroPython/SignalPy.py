#  SignalPy.py
#  usage: http://hostname:8080/ctrl/?red=50&green=255&blue=255&period=500&repeat=300

import utime as time
import usocket as socket
from machine import Timer, Pin, PWM

ESSID = 'your ESSID'
PASS = 'your password'
PORT = 8080

# LED parameters
param = {
    'red': 0,
    'green': 0,
    'blue': 0,
    'period': 0,
    'repeat': 0,
    }
tim = Timer(-1)
power = False

led_r = PWM(Pin(5, Pin.OUT, value = 0), freq = 512, duty = 0)
led_g = PWM(Pin(4, Pin.OUT, value = 0), freq = 512, duty = 0)
led_b = PWM(Pin(0, Pin.OUT, value = 0), freq = 512, duty = 0)

def tmfunc(*args):
    global param, power
    npower = power
    if param['repeat'] > 0:
        npower = not power
    if not npower:
            param['repeat'] = param['repeat'] - 1
    else:
        npower = False

    if power != npower:
        power = npower
        led(power)

def do_connect():
    import network
    # -- ESP8266 as station mode
    # sta_if = network.WLAN(network.STA_IF)
    # if not sta_if.isconnected():
    #     print('connecting to network...')
    #     sta_if.active(True)
    #     sta_if.connect(ESSID, PASS)
    #     while not sta_if.isconnected():
    #         pass
    # cf = sta_if.ifconfig()
    # -- ESP8266 as access point mode
    ap_if = network.WLAN(network.AP_IF)
    cf = ap_if.ifconfig()
    # --
    print('network config:', cf)
    return cf[0]

def parser(s):
    try:
        r = s.split('/')
        if r[1] != 'ctrl' or len(r) < 3 or r[2][0] != '?' : return
        p = dict([i.split('=') for i in [i for i in r[2][1:].split('&')]])
        print("params:",p)
        global param        # print("\nperser({0})".format(s), r)
        for i in ['red', 'green', 'blue', 'period', 'repeat']:
            max_value = 1023 if i in ['red', 'green', 'blue'] else 60000
            try:
                param[i] = min(int(p.get(i)), max_value)
            except:
                param[i] = 0
        tim.deinit()
        led(False)
        if param['period'] > 0:
            tim.init(period = param['period'], mode = Timer.PERIODIC, callback = tmfunc)
    except:
        pass

def led(sw):
    if sw:
        print("o\010", end="")
        led_b.duty(param['blue'])
        led_r.duty(param['red'])
        led_g.duty(param['green'])
    else:
        print("-\010", end="")
        led_b.duty(0)
        led_r.duty(0)
        led_g.duty(0)

# ------------

CONTENT = """\
HTTP/1.0 200 OK

Hello #{} from MicroPython!
"""

ip = do_connect()
ai = socket.getaddrinfo(ip, PORT)
addr = ai[0][4]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(addr)
s.listen(5)
counter=0

while True:
    res = s.accept()
    print("accept")
    client_s = res[0]
    client_addr = res[1]
    print("Client address:", client_addr)
    print("Client socket:", client_s)
    req = client_s.recv(1024)
    print("Request=", req)
    client_s.send(bytes(CONTENT.format(counter), "ascii"))
    parts = req.decode('ascii').split(' ')
    if len(parts) > 0:
        if parts[1] == '/exit':
            client_s.close()
            break
        parser(parts[1])
        client_s.send(bytes("valid param: {0}\n\n".format(param), "ascii"))
    else:
        client_s.send("invalid param {0}".format(req), "ascii")
    client_s.close()
    counter += 1

# ------------
