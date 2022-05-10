import opc, time, random, numpy
from timeit import default_timer as timer
client = opc.Client('127.0.0.1:7890')
from threading import Thread
import traceback

mode = "campfire"
campfireMode = "hot"
override = "none"
sensitivity = 100
brightness  = 3
setting_decay = 4
setting_soundmode = "colorpulse"
setting_color = (255, 255, 255, 255)
setting_stepdirection = 1
setting_chasedelay = 0
setting_crowdblinder = 0
setting_crowdblinderactive = False
setting_blackoutactive = False
strobe_duration = 0.01
strobe_active = False
holdPutPixels = False
testingChain = 0

PORT_NUMBER = 8080

channels     = [0] * 512

# import serial
# display = serial.Serial("/dev/ttyACM0", 115200, timeout=1)


def crowdblinder(_original, _add):
    a = _original + _add
    # if a < 0:
    #     a = 0
    if a > 255:
        a = 255
    return a

def convertPixels(_pixels):
    global brightness, setting_crowdblinder, strobe_hot, setting_blackoutactive
    # brightness_normal = brightness / 255.0
    invbrightness = 3 - brightness
    pixelsConverted = []
    for pixelQuad in range(0, int(len(_pixels) / 3)):
        

        if setting_blackoutactive:
            for i in range(0, 4):
                pixelsConverted.append((0, 0, 0))
        else:
            if setting_crowdblinder > 0:
                pixelsConverted.append((
                       crowdblinder(_pixels[(pixelQuad * 3) + 0][0], -setting_crowdblinder) >> invbrightness,  # red 0
                        crowdblinder(_pixels[(pixelQuad * 3) + 0][1], -setting_crowdblinder) >> invbrightness, # green 0
                        crowdblinder(_pixels[(pixelQuad * 3) + 0][2], setting_crowdblinder) >> (invbrightness + 1),  # blue 0
                    ))
                    # (red 0, green 0, blue 0)
                    # (green 1, white 0, red 1)
                    # (white 1, blue 1, green 2)
                    # (blue 2, red 2, white 2)
                # pixelsConverted.append((0, 0, 0))
                # pixelsConverted.append((0, 0, 0))
                # pixelsConverted.append((0, 0, 0))
                # pixelsConverted.append((0, 0, 255))

                pixelsConverted.append((
                        crowdblinder(_pixels[(pixelQuad * 3) + 1][1], -setting_crowdblinder) >> invbrightness,  # green 1
                        crowdblinder(_pixels[(pixelQuad * 3) + 0][3], setting_crowdblinder) >> invbrightness,   # white 0
                        crowdblinder(_pixels[(pixelQuad * 3) + 1][0], -setting_crowdblinder) >> invbrightness,  # red 1
                    ))
                pixelsConverted.append((
                        crowdblinder(_pixels[(pixelQuad * 3) + 1][3], setting_crowdblinder) >> invbrightness,   # white 1
                        crowdblinder(_pixels[(pixelQuad * 3) + 1][2], setting_crowdblinder) >> (invbrightness + 1),   # blue 1
                        crowdblinder(_pixels[(pixelQuad * 3) + 2][1], -setting_crowdblinder) >> invbrightness,  # green 2
                ))
                pixelsConverted.append((
                        crowdblinder(_pixels[(pixelQuad * 3) + 2][2], setting_crowdblinder) >> (invbrightness + 1),   # blue 2
                        crowdblinder(_pixels[(pixelQuad * 3) + 2][0], -setting_crowdblinder) >> invbrightness,  # red 2
                        crowdblinder(_pixels[(pixelQuad * 3) + 2][3], setting_crowdblinder) >> invbrightness,   # white 2
                    ))
            else:
                pixelsConverted.append((
                        _pixels[(pixelQuad * 3) + 0][0] >> invbrightness,
                        _pixels[(pixelQuad * 3) + 0][1] >> invbrightness,
                        _pixels[(pixelQuad * 3) + 0][2] >> invbrightness,
                    ))
                pixelsConverted.append((
                        _pixels[(pixelQuad * 3) + 1][1] >> invbrightness,
                        _pixels[(pixelQuad * 3) + 0][3] >> invbrightness,
                        _pixels[(pixelQuad * 3) + 1][0] >> invbrightness,
                    ))
                pixelsConverted.append((
                        _pixels[(pixelQuad * 3) + 1][3] >> invbrightness,
                        _pixels[(pixelQuad * 3) + 1][2] >> invbrightness,
                        _pixels[(pixelQuad * 3) + 2][1] >> invbrightness,
                ))
                pixelsConverted.append((
                        _pixels[(pixelQuad * 3) + 2][2] >> invbrightness,
                        _pixels[(pixelQuad * 3) + 2][0] >> invbrightness,
                        _pixels[(pixelQuad * 3) + 2][3] >> invbrightness,
                    ))

        


    # print "\n\n\n\n\n" + str(pixelsConverted) + "\n\n\n\n\n"
    return pixelsConverted




def putPixels(_pixels):
    global strobe_active, holdPutPixels, client
    if not strobe_active:
        if not holdPutPixels:
            client.put_pixels(_pixels)



def putConvertedPixels(_pixels):
    global channels
    putPixels(convertPixels(_pixels))

    # channels = []
    pixelNumber = 0
    # print _pixels
    for pixel in _pixels:
        if pixelNumber < 48:
            # print pixel
            # print pixel[0]
            # print pixel[1]
            # print pixel[2]
            # print pixel[3]
            # print "pixelNumber: " + str(pixelNumber)
            # print "pixelNumber * 4: " + str(pixelNumber * 4)
            # print len(channels)
            # print "channels[" + str(pixelNumber * 4) + "]: " + str(channels[pixelNumber * 4])
            
            channels[(pixelNumber * 4)] = pixel[0]
            channels[(pixelNumber * 4) + 1] = pixel[1]
            channels[(pixelNumber * 4) + 2] = pixel[2]
            channels[(pixelNumber * 4) + 3] = pixel[3]
        pixelNumber += 1
    # print channels

    # sendChannels(channels, "10.0.0.245", 6454, 0, 0)



def step(_sequence, _delay):
    pixels = _sequence * 96
    putConvertedPixels(pixels)
    time.sleep(_delay)


def cycle(_color, _delay):
    step((_color, black, black, black), _delay)
    step((black, _color, black, black), _delay)
    step((black, black, _color, black), _delay)
    step((black, black, black, _color), _delay)

# sudo /usr/local/bin/fcserver /usr/local/bin/fcserver.json

# red = (255, 0, 0, 0)
# green = (0, 255, 0, 0)
# white = (0, 0, 0, 255)
# black = (0, 0, 0, 0)
# def christmasChase(_delay):
#     christmasSequence = (red, black, black, green, black, black, white, black, black)
#     for i in range(0, 9):
#         step(christmasSequence, 0.1)
#         christmasSequence = christmasSequence[8:] + christmasSequence[0:8]
#         print christmasSequence


# pixels = []
# while True:
#   # for i in range(0, 8):
#   #   christmasChase(0.1)

#   # color = (0, 0, 0, 255)
#   # for i in range(0, 5):
#   #   cycle(color, 0.1)

#   # color = (255, 0, 0, 0)
#   # for i in range(0, 5):
#   #   cycle(color, 0.1)

#   # color = (0, 255, 0, 0)
#   # for i in range(0, 5):
#   #   cycle(color, 0.1)

#   color = (0, 128, 255, 0)
#   for i in range(0, 5):
#       cycle(color, 0.1)

    
# pixels = []
# for i in range(0, 48):
#   pixels.append((255, 0, 0, 0))

# for i in range(0, 48):
#   pixels.append((0, 255, 0, 0))

# for i in range(0, 48):
#   pixels.append((0, 0, 255, 0))

# for i in range(0, 48):
#   pixels.append((0, 0, 0, 255))

# while True:
#   putConvertedPixels(pixels)
#   time.sleep(0.25)



def sweep(_color, _delay):
    putConvertedPixels([ (0, 0, 0, 0) ] * 384)

    for i in range(0, 186):
        pixels = []
        str = ""
        # print i
        for j in range(0, i):
            str += " "
            pixels.append((0, 0, 0, 0))
        for k in range(0, 12):
            str += "x"
            pixels.append(_color)
        for j in range(i + 12, 192):
            pixels.append((0, 0, 0, 0))
            str += " "
        # print str
        putConvertedPixels(pixels)
        time.sleep(_delay)

    for i in reversed(range(0, 186)):
        pixels = []
        str = ""
        # print i
        for j in range(0, i):
            str += " "
            pixels.append((0, 0, 0, 0))
        for k in range(0, 12):
            str += "x"
            pixels.append(_color)
        for j in range(i + 12, 192):
            pixels.append((0, 0, 0, 0))
            str += " "
        # print str
        putConvertedPixels(pixels)
        time.sleep(_delay)


def fullPulse(_color, _range):
    for i in range(0, _range):
        multiplier = float(i) / float(_range)
        # print int(float(_color[0]) * float(multiplier))
        pixels = [ (int(float(_color[0]) * float(multiplier)), int(float(_color[1]) * float(multiplier)), int(float(_color[2]) * float(multiplier)), int(float(_color[3]) * float(multiplier))) ] * 384
        putConvertedPixels(pixels)
    for i in reversed(range(0, _range)):
        multiplier = float(i) / float(_range)
        # print int(float(_color[0]) * float(multiplier))
        pixels = [ (int(float(_color[0]) * float(multiplier)), int(float(_color[1]) * float(multiplier)), int(float(_color[2]) * float(multiplier)), int(float(_color[3]) * float(multiplier))) ] * 384
        putConvertedPixels(pixels)






import socket, time, datetime
from threading import Thread

UDP_IP = "10.255.0.12"
UDP_PORT = 6454
UNIVERSE = 8
PHYSICAL = 0
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

channels     = [0] * 512

# universes = {0: {"channels": [0] * 512, "ipaddress": "10.0.0.20", "universe": 0, "physical": 0},
#              1: {"channels": [0] * 512, "ipaddress": "10.0.0.20", "universe": 1, "physical": 0},
#              2: {"channels": [0] * 512, "ipaddress": "10.0.0.20", "universe": 2, "physical": 0},
#              3: {"channels": [0] * 512, "ipaddress": "10.0.0.20", "universe": 3, "physical": 0}}

def changeChannel(_channels, _channel, _value):
    """Change a channel on _channels, accounting for the fact that DMX channels conventionally (and per spec) start at 1, not 0."""
    _channels[_channel - 1] = _value

def artnetPacketFromChannels(_channels, _universe, _physical):
    """Converts a 512-long byte array to a valid ArtNet packet that can be sent straight to a device."""
    channelString = ''
    for channel in _channels:
        try:
            if channel > 255:
                channelString += str(chr(255))
            else:
                channelString += str(chr(channel))
        except ValueError:
            channelString += str(chr(255))
    header = "Art-NetP" + (chr(0) * 5) + chr(_physical) + chr(_universe) + (chr(0) * 3)  # so simple amirite
    return header + channelString

def sendChannels(_channels, _ipaddress, _port, _universe, _physical):
    """Sends an ArtNet packet to the device of your choice.  Set the IP address to x.x.x.255 to broadcast to all devices.  Unicasting can help
    cut back on network traffic and is recommended."""
    sock.sendto(artnetPacketFromChannels(_channels, _universe, _physical), (_ipaddress, _port))


def fadeChannels(_channels, _newChannels, _duration_seconds):
    """Linear crossfade between two sets of channels.  Will change the variable assigned to _channels.  This function is blocking."""
    channels = [0] * 512
    oldChannels = _channels
    for i in range(0, int(_duration_seconds * 30 + 1)):
        progress = i / 30.0 / _duration_seconds
        
        for channel in range(0, 512):
            channels[channel] = int((oldChannels[channel] * (1.0 - progress)) + (_newChannels[channel] * progress))

        # sendChannels(channels)
        _channels = channels
        time.sleep(1.0 / 30.0)



def changeRGB(_channels, _startChannel, _rgb):
    """Allows you to set channels with an RGB tuple instead of individually."""
    rgb_tuple = maxBrightness(rgbtohex(_rgb))

    changeChannel(_channels, _startChannel, gammaCorrection(rgb_tuple[0], 0.6))
    changeChannel(_channels, _startChannel + 1, gammaCorrection(rgb_tuple[1], 0.6))
    changeChannel(_channels, _startChannel + 2, gammaCorrection(rgb_tuple[2], 0.6))
    #print str(_startChannel) + ": " + str(_channels[_startChannel - 1]), str(_channels[_startChannel]), str(_channels[_startChannel + 1])




packetsSent = 0
previousChannels = [0] * 512
forceNewPacketSend = False
def masterChannelSend(_ipaddress):
    print _ipaddress
    """Asynchronously sends channels out over ArtNet as often as needed (so whenever 'channels' changes, or if forceNewPacketSend is set)."""
    global channels, packetsSent, previousChannels, forceNewPacketSend, UNIVERSE, PHYSICAL, UDP_IP, UDP_PORT, mode
    while mode != "artnet":
        if True: #previousChannels != channels or forceNewPacketSend: # only send if something has updated or a second has passed
        # def sendChannels(_channels, _ipaddress, _port, _universe, _physical):
            sendChannels(channels, _ipaddress, 6454, 0, 0)
            # sendChannels(channels, "10.0.0.82", 6454, 0, 0)
            # sendChannels(channels, "10.0.0.83", 6454, 0, 0)
            # sendChannels(channels, "10.0.0.84", 6454, 0, 0)
            # sendChannels(channels, "10.0.0.85", 6454, 0, 0)
            previousChannels = channels
            packetsSent += 1
            forceNewPacketSend = False
        time.sleep(0.033)


masterChannelSendThread1 = Thread(target=masterChannelSend, kwargs={"_ipaddress": "10.0.0.255"})
masterChannelSendThread1.daemon = True
masterChannelSendThread1.start()

# masterChannelSendThread2 = Thread(target=masterChannelSend, kwargs={"_ipaddress": "10.0.0.82"})
# masterChannelSendThread2.daemon = True
# masterChannelSendThread2.start()

# masterChannelSendThread3 = Thread(target=masterChannelSend, kwargs={"_ipaddress": "10.0.0.83"})
# masterChannelSendThread3.daemon = True
# masterChannelSendThread3.start()

# masterChannelSendThread4 = Thread(target=masterChannelSend, kwargs={"_ipaddress": "10.0.0.84"})
# masterChannelSendThread4.daemon = True
# masterChannelSendThread4.start()

# masterChannelSendThread5 = Thread(target=masterChannelSend, kwargs={"_ipaddress": "10.0.0.85"})
# masterChannelSendThread5.daemon = True
# masterChannelSendThread5.start()



def packetCounter():
    """Counts the number of packets sent every second.  Sets forceNewPacketSend to True so that masterChannelSend() will send a packet
    once a second, even if nothing has changed (to keep devices up to date)."""
    global packetsSent, forceNewPacketSend
    while True:
        print "packets sent: " + str(packetsSent)
        packetsSent = 0
        forceNewPacketSend = True # send a new ArtNet packet after a second has passed to keep devices up to date
        time.sleep(1)


packetCounterThread = Thread(target=packetCounter)
packetCounterThread.daemon = True
packetCounterThread.start()





from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
PORT_NUMBER = 8080


def requestHandler_index(_request):
    return "text/html", """"""

def requestHandler_chase(_request):
    global mode
    mode = "chase"
    print "chase!"
    return "text/plain", "chase"

def requestHandler_soundactivated(_request):
    global mode, setting_soundmode, setting_color
    mode = "soundactivated"
    setting_soundmode = _request[2]
    if setting_color == (255, 255, 255, 255):
        setting_color = (0, 0, 0, 255)
    print "sound activated!"
    return "text/plain", "soundactivated"

def requestHandler_solid(_request):
    global mode, setting_color
    if setting_color == (255, 255, 255, 255):
        setting_color = (0, 0, 0, 255) # kill superwhite because otherwise it'll trip the overload protection on the battery
    mode = "solid"
    print "solid color!"
    return "text/plain", "solid"

def requestHandler_supachase(_request):
    global mode
    mode = "supachase"
    print "supachase!"
    return "text/plain", "supachase"

def requestHandler_christmaschase(_request):
    global mode
    mode = "christmaschase"
    print "christmaschase!"
    return "text/plain", "christmaschase"

def requestHandler_megapulse(_request):
    global mode
    mode = "megapulse"
    print "megapulse!"
    return "text/plain", "megapulse"

def requestHandler_colorscroll(_request):
    global mode
    mode = "colorscroll"
    print "colorscroll!"
    return "text/plain", "colorscroll"

def requestHandler_megarainbow(_request):
    global mode
    mode = "megarainbow"
    print "megarainbow!"
    return "text/plain", "megarainbow"

def requestHandler_campfire(_request):
    global mode, campfireMode
    mode = "campfire"
    campfireMode = "hot"
    print "campfire!"
    return "text/plain", "campfire"


def requestHandler_campfirecold(_request):
    global mode, campfireMode
    mode = "campfire"
    campfireMode = "cold"
    print "campfire cold"
    return "text/plain", "campfire cold"

def requestHandler_campfiregreen(_request):
    global mode, campfireMode
    mode = "campfire"
    campfireMode = "green"
    print "campfire green"
    return "text/plain", "campfire green"

def requestHandler_reversedirection(_request):
    global setting_stepdirection
    if setting_stepdirection == 1:
        setting_stepdirection = -1
    else:
        setting_stepdirection = 1
    print "reverse direction!"
    return "text/plain", "reverse direction"

def requestHandler_reverseandpop(_request):
    global holdPutPixels
    global setting_stepdirection
    if setting_stepdirection == 1:
        setting_stepdirection = -1
    else:
        setting_stepdirection = 1

    holdPutPixels = True
    client.put_pixels(convertPixels([ (0, 0, 255, 255) ] * 384))
    time.sleep(0.07)
    holdPutPixels = False

    print "reverse and pop!"
    return "text/plain", "reverse and pop"

def requestHandler_crowdblinderon(_request):
    global setting_crowdblinderactive
    setting_crowdblinderactive = True
    print "crowdblinderon"
    return "text/plain", "crowdblinderon"

def requestHandler_crowdblinderoff(_request):
    global setting_crowdblinderactive
    setting_crowdblinderactive = False
    print "crowdblinderoff"
    return "text/plain", "crowdblinderoff"

def requestHandler_blackouton(_request):
    global setting_blackoutactive
    setting_blackoutactive = True
    print "blackouton"
    return "text/plain", "blackouton"

def requestHandler_blackoutoff(_request):
    global setting_blackoutactive
    setting_blackoutactive = False
    print "blackoutoff"
    return "text/plain", "blackoutoff"

def requestHandler_strobeon(_request):
    global strobe_active, strobe_duration
    strobe_active = True
    strobe_duration = float(_request[2])
    print "strobe duration: " + str(strobe_duration)
    print "strobeon"
    return "text/plain", "strobeon"

def requestHandler_strobeoff(_request):
    global strobe_active
    strobe_active = False
    print "strobeoff"
    return "text/plain", "strobeoff"

def requestHandler_sensitivity(_request):
    global sensitivity
    print _request[2]
    sensitivity = int(_request[2])
    print "sensitivity: " + str(sensitivity)
    return "text/plain", "sensitivity"

def requestHandler_brightness(_request):
    global brightness
    print _request[2]
    brightness = int(_request[2])
    print "brightness: " + str(brightness)
    return "text/plain", "brightness"

def requestHandler_decay(_request):
    global setting_decay
    print _request[2]
    setting_decay = int(_request[2])
    print "decay: " + str(setting_decay)
    return "text/plain", "decay"

def requestHandler_chasedelay(_request):
    global setting_chasedelay
    print _request[2]
    setting_chasedelay = float(_request[2]) / 100.0
    print "chasedelay: " + str(setting_chasedelay)
    return "text/plain", "chasedelay"

setting_colorName = ""
def requestHandler_color(_request):
    global setting_color, mode, setting_colorName
    # mode = "color"
    print _request[2]
    color = _request[2]
    setting_colorName = color
    if color == "red":
        setting_color = (255, 0, 0, 0)
    elif color == "orange":
        setting_color = (255, 128, 0, 0)
    elif color == "yellow":
        setting_color = (255, 255, 0, 0)
    elif color == "green":
        setting_color = (0, 255, 0, 0)
    elif color == "blue":
        setting_color = (0, 0, 255, 0)
    elif color == "purple":
        setting_color = (255, 0, 255, 0)
    elif color == "white":
        setting_color = (0, 0, 0, 255)
    elif color == "superwhite":
        if mode == "supachase":
            setting_color = (255, 255, 255, 255)
    elif color == "rgbwhite":
        setting_color = (255, 255, 255, 0)
    elif color == "black":
        setting_color = (0, 0, 0, 0)
    print "color: " + str(setting_color)
    return "text/plain", "color"

def requestHandler_testChain(_request):
    global mode, testingChain
    print _request[2]
    testingChain = _request[2]
    mode = "testChain"
    print "testing chain: " + str(testingChain)
    return "text/plain", "testChain"


def requestHandler_totd(_request):
    global mode
    print "totd!"
    mode = "totd"
    return "text/plain", "totd"

def requestHandler_artnet(_request):
    global mode
    print "artnet!"
    mode = "artnet"
    return "text/plain", "artnet"



httpRequests = {''      : requestHandler_index,
                'chase' : requestHandler_chase,
                'soundactivated' : requestHandler_soundactivated,
                'solid' : requestHandler_solid,
                'supachase' : requestHandler_supachase,
                'christmaschase' : requestHandler_christmaschase,
                'megapulse' : requestHandler_megapulse,
                'colorscroll' : requestHandler_colorscroll,
                'megarainbow' : requestHandler_megarainbow,
                'campfire' : requestHandler_campfire,
                'campfirecold' : requestHandler_campfirecold,
                'campfiregreen' : requestHandler_campfiregreen,
                'reversedirection' : requestHandler_reversedirection,
                'reverseandpop' : requestHandler_reverseandpop,
                'crowdblinderon' : requestHandler_crowdblinderon,
                'crowdblinderoff' : requestHandler_crowdblinderoff,
                'blackouton' : requestHandler_blackouton,
                'blackoutoff' : requestHandler_blackoutoff,
                'strobeon' : requestHandler_strobeon,
                'strobeoff' : requestHandler_strobeoff,
                'sensitivity' : requestHandler_sensitivity,
                'brightness' : requestHandler_brightness,
                'decay' : requestHandler_decay,
                'chasedelay' : requestHandler_chasedelay,
                'color' : requestHandler_color,
                'test': requestHandler_testChain,
                'totd': requestHandler_totd,
                'artnet': requestHandler_artnet,
                }

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
    
    #Handler for the GET requests
    def do_GET(self):
        elements = self.path.split('/')

        responseFound = False
        for httpRequest, httpHandler in httpRequests.iteritems():
            # print elements[1] + " == " + httpRequest
            if elements[1] == httpRequest: # in other words, if the first part matches
                contentType, response = httpHandler(elements)
                responseFound = True

                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header('Content-type', contentType)
                self.end_headers()

                self.wfile.write(response)
        if not responseFound:
            contentType, response = requestHandler_index('/')

            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header('Content-type', contentType)
            self.end_headers()

            self.wfile.write(response)
            
        return


def http():
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ' , PORT_NUMBER

    server.serve_forever()

httpThread = Thread(target=http)
httpThread.daemon = True
httpThread.start()


import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket


class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print 'new connection'
        # self.write_message("omfg it werkz")
        # time.sleep(2)
        # self.write_message("totd")
        # time.sleep(2)
        # self.write_message("status")
        # time.sleep(2)
        # self.write_message("totd")
        # time.sleep(2)
        # self.write_message("status")
      
    def on_message(self, message):
        print 'message received:  %s' % message
        elements = ("/" + message).split('/') # to maintain ajax compatibility

        for httpRequest, httpHandler in httpRequests.iteritems():
            # print elements[1] + " == " + httpRequest
            if elements[1] == httpRequest:
                contentType, response = httpHandler(elements)
                print response
                # responseFound = True

                # self.send_response(200)
                # self.send_header("Access-Control-Allow-Origin", "*")
                # self.send_header('Content-type', contentType)
                # self.end_headers()

                # self.wfile.write(response)

        # # Reverse Message and send it back
        # print 'sending back message: %s' % message[::-1]
        # self.write_message(message[::-1])
 
    def on_close(self):
        print 'connection closed'
 
    def check_origin(self, origin):
        return True
 
application = tornado.web.Application([
    (r'/ws', WSHandler),
])
 
 
def socket():
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(9876)
    # myIP = socket.gethostbyname(socket.gethostname())
    # print '*** Websocket Server Started at %s***' % myIP
    tornado.ioloop.IOLoop.instance().start()

socketThread = Thread(target=socket)
socketThread.daemon = True
socketThread.start()


import scipy.interpolate as interp
import numpy as np

x = np.arange(-5.01, 5.01, 0.25)
y = np.arange(-5.01, 5.01, 0.25)
xx, yy = np.meshgrid(x, y)
z = np.sin(xx**2+yy**2)
f = interp.interp2d(x, y, z, kind='cubic')

def drawFromTopToBottom(_array):
    # start = timer()
    # pixels = [ [0, 0, 0, 0] ] * 384
    pixels = [[0 for i in range(4)] for j in range(384)]
    for color in range(0, 4):
        thisColor = []
        for x in range(0, len(_array)):
            thisColor.append(_array[x][color])
        # print thisColor
        array = np.asarray(thisColor)
        arraySize = array.size - 1
        array_interp = interp.interp1d(np.arange(array.size), array)
        array_resized_63 = array_interp(np.linspace(0, arraySize, 63))
        array_resized_35 = array_interp(np.linspace(0, arraySize, 35))

        for i in range(0, 62):
            pixels[i][color] = int(array_resized_63[i]) # buttonholes
        for i in range(0, 63):
            pixels[123 - i][color] = int(array_resized_63[i]) # buttons
        for i in range(0, 35):
            pixels[123 + i][color] = int(array_resized_35[i]) # back 1
        for i in range(0, 34):
            pixels[191 - i][color] = int(array_resized_35[i]) # back 2
        for i in range(0, 36):
            pixels[192 + i][color] = int(array_resized_63[i])
        for i in range(0, 12):
            pixels[240 - i][color] = int(array_resized_63[28 + i])
        for i in range(0, 34):
            pixels[240 + i][color] = int(array_resized_63[54 - i])
            pixels[288 + i][color] = int(array_resized_63[54 - i])
            pixels[336 + i][color] = int(array_resized_63[9 + i])
        for i in range(0, 10):
            pixels[278 + i][color] = int(array_resized_63[32 + i])
            pixels[326 + i][color] = int(array_resized_63[10 + i])
            pixels[374 + i][color] = int(array_resized_63[53 - i])



    pixels_tupled = []
    for pixel in pixels:
        pixels_tupled.append( (pixel[0], pixel[1], pixel[2], pixel[3] ))

    # print pixels_tupled

    # print timer() - start

    return pixels_tupled

# while True:
#     for i in range(0, 12):
#         array = []
#         for j in range(0, i):
#             array.append( (255, 0, 0, 0) )
#         for j in range(i, 12):
#             array.append( (0, 0, 255, 0) )
#         # print array
#         putConvertedPixels(drawFromTopToBottom(array))
#         time.sleep(0.1)


# pixels = []
# for i in range(0, 192):
#     pixels.append( (0, 0, 0, 0) )
# for i in range(0, 48):
#     pixels.append( (255, 0, 0, 0) )
# for i in range(0, 48):
#     pixels.append( (0, 255, 0, 0) )
# for i in range(0, 48):
#     pixels.append( (0, 0, 255, 0) )
# for i in range(0, 48):
#     pixels.append( (0, 0, 0, 255) )

# print pixels

# putConvertedPixels(pixels)
# putConvertedPixels(pixels)
# time.sleep(9999)


def twentyCharString(_string):
    lol = _string
    for i in range(len(lol), 20):
        lol += " "
    #print lol
    return lol

def displayWriteMonitor(_string):
    display.write(_string)
    print _string

line1Cleared = False
def displayManager():
    global line1Cleared, display, mode, sensitivity, brightness, setting_crowdblinderactive, setting_stepdirection, strobe_active, setting_chasedelay, setting_colorName, setting_decay, setting_blackoutactive
    displayLastMode = ""
    lastSensitivity = -1
    lastBrightness = -1
    lastSettingCrowdBlinderActive = -1
    lastSettingStepDirection = -2
    lastSettingStrobeActive = False
    lastSettingChaseDelay = -1
    lastSettingColorName = ""
    lastSettingDecay = -1
    lastSettingBlackoutActive = -3
    # display.write("0 fuck.")
    while True:
        if mode != displayLastMode:
            omg = mode
            for i in range(len(mode), 20):
                omg += " "
            displayWriteMonitor("0 " + omg + ".")

        if lastSensitivity != sensitivity or lastBrightness != brightness or lastSettingStepDirection != setting_stepdirection or lastSettingChaseDelay != setting_chasedelay or lastSettingDecay != setting_decay:
            wtf = "\6" + str(sensitivity) + " \1" + str(brightness) + " \3" + str(int(setting_chasedelay * 100.0)) + " \4" + str(setting_decay)
            for i in range(len(wtf), 20):
                wtf += " "
            displayWriteMonitor("3 " + wtf + ".")
            
        
        if lastSettingColorName != setting_colorName:
            lol = "\5" + str(setting_colorName)
            for i in range(len(lol), 20):
                lol += " "
            displayWriteMonitor("2 " + lol + ".")


        if lastSettingCrowdBlinderActive != setting_crowdblinderactive:
            if setting_crowdblinderactive:
                line1Cleared = False
                displayWriteMonitor("1 " + twentyCharString("CROWD BLINDER") + ".")


        elif lastSettingStrobeActive != strobe_active:
            if strobe_active:
                line1Cleared = False
                displayWriteMonitor("1 " + twentyCharString("STROBE") + ".")


        elif lastSettingBlackoutActive != setting_blackoutactive:
            if setting_blackoutactive:
                line1Cleared = False
                displayWriteMonitor("1 " + twentyCharString("BLACKOUT") + ".")


        if not line1Cleared and not strobe_active and not setting_crowdblinderactive and not setting_blackoutactive:
            displayWriteMonitor("1 " + twentyCharString("") + ".")
            line1Cleared = True


        displayLastMode = mode
        lastSensitivity = sensitivity
        lastBrightness = brightness
        lastSettingCrowdBlinderActive = setting_crowdblinderactive
        lastSettingStepDirection = setting_stepdirection
        lastSettingStrobeActive = strobe_active
        lastSettingChaseDelay = setting_chasedelay
        lastSettingColorName = setting_colorName
        lastSettingDecay = setting_decay

        # display.write("0 fuck.\n")

        time.sleep(0.1)


# displayManagerThread = Thread(target=displayManager)
# displayManagerThread.daemon = True
# displayManagerThread.start()



import alsaaudio, audioop, math


soundenabled = True
try:
    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK, cardindex=1)

    inp.setchannels(2)
    inp.setrate(11025)
    inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

    inp.setperiodsize(1024)
except Exception:
    traceback.print_exc()
    soundenabled = False
    print "Sound activation disabled!"



setting_decay = 4
numberOfPixels = 384
pixels = [(0, 0, 0, 0)] * numberOfPixels
colorIndex = 0
color = (255, 0, 0, 255)
timeSinceLastColorChange = time.time()
timeSinceLastFrame = time.time()
colorpulseValue = 0.0
def soundActivated():
    global pixels, setting_decay, colorIndex, color, timeSinceLastColorChange, timeSinceLastFrame, mode, sensitivity, setting_soundmode, colorpulseValue, setting_color, soundenabled

    # errorcount = 0
    while mode == "soundactivated" and soundenabled == True:
        start = timer()
        # noisycount = 0
        # try:                                                    
        #     block = stream.read(chunk)         
        # except IOError, e:                                      
        #     errorcount += 1                                     
        #     # print( "(%d) Error recording: %s"%(errorcount,e) )  
        #     noisycount = 1  

        # # startlfilter = timer()
        # samples = normalize(block)
        # bandpass_samples,zi = signal.lfilter(b2, a2, samples, zi=zi2*samples[0])
        # # amplitude = get_rms(samples)
        # bandpass_ampl = get_rms(bandpass_samples)
        # print "lfilter: " + str(timer() - startlfilter)
        # print amplitude
        # print bandpass_ampl

        # for i in range(0, 192):
        #     pixels[i] = (pixels[i][0] >> 1, pixels[i][1] >> 1, pixels[i][2] >> 1, pixels[i][3] >> 1)

        l,data = inp.read()

        # omgdata = numpy.fromstring(data,dtype=numpy.int16)
        # fft = abs(numpy.fft.fft(omgdata).real)
        # print fft
        # print len(data)
        # if l:
        # if not noisycount:
        try:
            leftonly = audioop.tomono(data, 2, 1, 0)

            amp = audioop.rms(leftonly, 2)

            # min_, max_ = audioop.minmax(leftonly, 2)
            # amp = max_ - min_

            

            # if time.time() - timeSinceLastFrame > 0.005:
            #     timeSinceLastFrame = time.time()
            if True:

                # value_normal = bandpass_ampl * 2000
                # if value_normal > 1.0:
                #     value_normal = 1.0

                # print value_normal

                
                amp = amp - 15
                if amp < 0:
                    amp = 0

                value = amp / float(sensitivity)

                if value > 63:
                    value = 63

                value_normal = float(value) / 63

                # value_normal = (1 / (value_normal * value_normal)) / 3000
                # print value_normal

                # if value > 32:
                if setting_soundmode == "vu-colorswitch":
                    white = 0
                else:
                    white = 255
                if value_normal > 0.5:
                    omg = time.time() - timeSinceLastColorChange
                    if omg > 0.2:
                        # print omg
                        timeSinceLastColorChange = time.time()
                        colorIndex = random.randrange(0, 6)
                        if colorIndex == 0:
                            color = (255, 0, 0, white)
                        elif colorIndex == 1:
                            color = (0, 255, 0, white)
                        elif colorIndex == 2:
                            color = (0, 0, 255, white)
                        elif colorIndex == 3:
                            color = (64, 0, 192, white)
                        elif colorIndex == 4:
                            color = (192, 64, 0, white)
                        elif colorIndex == 5:
                            color = (0, 128, 128, white)

               
                if setting_soundmode == "vu-hot" or setting_soundmode == "vu-color" or setting_soundmode == "vu-colorswitch":
                    if setting_soundmode == "vu-hot" or setting_soundmode == "vu-colorswitch":
                        for i in range(0, numberOfPixels):
                            # pixels[i] = (0, 0, pixels[i][3], 0)
                            pixels[i] = (pixels[i][0] - setting_decay if pixels[i][0] > 0 else 0, pixels[i][1] - setting_decay if pixels[i][1] > 0 else 0, pixels[i][2] - setting_decay if pixels[i][2] > 0 else 0, pixels[i][3] - (setting_decay * 4) if pixels[i][3] > 0 else 0)
                    elif setting_soundmode == "vu-color":
                        color = setting_color
                        for i in range(0, numberOfPixels):
                            pixels[i] = (pixels[i][0] - setting_decay if pixels[i][0] > 0 else 0, pixels[i][1] - (setting_decay * 2) if pixels[i][1] > 0 else 0, pixels[i][2] - (setting_decay * 3) if pixels[i][2] > 0 else 0, pixels[i][3] - setting_decay if pixels[i][3] > 0 else 0)
                    for i in range(0, int(value_normal * 62)):
                        pixels[i] = color
                    for i in range(0, int(value_normal * 63)):
                        pixels[123 - i] = color
                    for i in range(0, int(value_normal * 35)):
                        pixels[123 + i] = color
                    for i in range(0, int(value_normal * 34)):
                        pixels[191 - i] = color
                    for i in range(0, int(value_normal * 36)):
                        pixels[192 + i] = color
                    for i in range(0, int(value_normal * 12)):
                        pixels[240 - i] = color
                    for i in range(0, int(value_normal * 34)):
                        # pixels[240 + i] = color
                        pixels[273 - i] = color
                        # pixels[288 + i] = color
                        pixels[321 - i] = color
                        pixels[336 + i] = color
                    for i in range(0, int(value_normal * 10)):
                        pixels[278 + i] = color
                        pixels[326 + i] = color
                        # pixels[374 + i] = color
                        pixels[383 - i] = color
                elif setting_soundmode == "colorswitch":
                    # print color
                    pixels = [ (color[0], color[1], color[2], 0) ] * 384
                elif setting_soundmode == "colorpulse":
                    # print color
                    pixels = [ (int(float(setting_color[0]) * value_normal), int(float(setting_color[1]) * value_normal), int(float(setting_color[2]) * value_normal), int(float(setting_color[3]) * value_normal)) ] * 384

                
                putConvertedPixels(pixels)
        except Exception as e:
            print e

        # print timer() - start

    time.sleep(0.1) # prevent the cpu from going to 100% when soundactivated is on and soundenabled is false
                



def chase():
    global mode

    # if mode == "chase":
    #     sweep((255, 0, 0, 0), 0)
    #     sweep((0, 255, 0, 0), 0)

    # if mode == "chase":
    #     sweep((0, 0, 255, 0), 0)
    #     sweep((0, 0, 0, 255), 0)

    if mode == "chase":
        fullPulse((255, 0, 0, 0), 32)
        fullPulse((255, 128, 0, 0), 32)
        fullPulse((255, 255, 0, 0), 32)
        fullPulse((128, 255, 0, 0), 32)

    if mode == "chase":
        fullPulse((0, 255, 0, 0), 32)
        fullPulse((0, 255, 128, 0), 32)
        fullPulse((0, 255, 255, 0), 32)
        fullPulse((0, 128, 255, 0), 32)

    if mode == "chase":
        fullPulse((0, 0, 255, 0), 32)
        fullPulse((128, 0, 255, 0), 32)
        fullPulse((255, 0, 255, 0), 32)
        fullPulse((255, 0, 128, 0), 32)

    if mode == "chase":
        color = (0, 0, 0, 255)
        for i in range(0, 5):
            cycle(color, 0.1)

    if mode == "chase":
        color = (255, 0, 0, 0)
        for i in range(0, 5):
            cycle(color, 0.1)

    if mode == "chase":
        color = (0, 255, 0, 0)
        for i in range(0, 5):
            cycle(color, 0.1)

    if mode == "chase":
        color = (0, 128, 255, 0)
        for i in range(0, 5):
            cycle(color, 0.1)


def solid():
    # print mode
    global mode, setting_color
    while mode == "solid":
        # print "solid color"
        putConvertedPixels([ setting_color ] * 384)
        time.sleep(.1)


red = (255, 0, 0, 0)
green = (0, 255, 0, 0)
white = (0, 0, 0, 255)
black = (0, 0, 0, 0)
step = 0
def supachase():
    global mode, setting_color, setting_stepdirection, step, setting_chasedelay
    while mode == "supachase":
            # christmasSequence = (red, red, red, red, red, red, red, red, red, red, green, green, green, green, green, green, green, green, green, green, white, white, white, white, white, white, white, white, white, white)
            # length = len(christmasSequence)
            # for i in range(0, length):
            #     step(christmasSequence, 0.0)
            #     christmasSequence = christmasSequence[length - 4:] + christmasSequence[0:length - 4]
            #     print christmasSequence
        color = setting_color

        step += setting_stepdirection
        if setting_stepdirection == 1 and step >= 40:
            step = 1
        elif setting_stepdirection == -1 and step <= 0:
            step = 38

        if step == 1:
            putConvertedPixels([ black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black,  ] * 11)
        elif step == 2:
            putConvertedPixels([ black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black,  ] * 11)
        elif step == 3:
            putConvertedPixels([ black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black,  ] * 11)
        elif step == 4:
            putConvertedPixels([ black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black,  ] * 11)
        elif step == 5:
            putConvertedPixels([ black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black,  ] * 11)
        elif step == 6:
            putConvertedPixels([ black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black,  ] * 11)
        elif step == 7:
            putConvertedPixels([ black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black,  ] * 11)
        elif step == 8:
            putConvertedPixels([ black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black,  ] * 11)
        elif step == 9:
            putConvertedPixels([ black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black,  ] * 11)
        elif step == 10:
            putConvertedPixels([ black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black,  ] * 11)
        elif step == 11:
            putConvertedPixels([ black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black,  ] * 11)
        elif step == 12:
            putConvertedPixels([ black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black,  ] * 11)
        elif step == 13:
            putConvertedPixels([ black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black,  ] * 11)
        elif step == 14:
            putConvertedPixels([ black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black,  ] * 11)
        elif step == 15:
            putConvertedPixels([ black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black,  ] * 11)
        elif step == 16:
            putConvertedPixels([ black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black,  ] * 11)
        elif step == 17:
            putConvertedPixels([ black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black,  ] * 11)
        elif step == 18:
            putConvertedPixels([ black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color,  ] * 11)
        elif step == 19:
            putConvertedPixels([ color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color,  ] * 11)
        elif step == 20:
            putConvertedPixels([ color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color,  ] * 11)
        elif step == 21:
            putConvertedPixels([ color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color,  ] * 11)
        elif step == 22:
            putConvertedPixels([ color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color,  ] * 11)
        elif step == 23:
            putConvertedPixels([ color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color,  ] * 11)
        elif step == 24:
            putConvertedPixels([ color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color,  ] * 11)
        elif step == 25:
            putConvertedPixels([ color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color,  ] * 11)
        elif step == 26:
            putConvertedPixels([ color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color,  ] * 11)
        elif step == 27:
            putConvertedPixels([ color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color,  ] * 11)
        elif step == 28:
            putConvertedPixels([ color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color,  ] * 11)
        elif step == 29:
            putConvertedPixels([ color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color,  ] * 11)
        elif step == 30:
            putConvertedPixels([ color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color,  ] * 11)
        elif step == 31:
            putConvertedPixels([ color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color,  ] * 11)
        elif step == 32:
            putConvertedPixels([ color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color,  ] * 11)
        elif step == 33:
            putConvertedPixels([ color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color,  ] * 11)
        elif step == 34:
            putConvertedPixels([ color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color,  ] * 11)
        elif step == 35:
            putConvertedPixels([ color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color,  ] * 11)
        elif step == 36:
            putConvertedPixels([ color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color,  ] * 11)
        elif step == 37:
            putConvertedPixels([ color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color,  ] * 11)
        elif step == 38:
            putConvertedPixels([ color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black,  ] * 11)
        elif step == 39:
            putConvertedPixels([ black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black,  ] * 11)

        time.sleep(setting_chasedelay)


christmasStep = 0
def christmaschase():
    global mode, red, green, blue, setting_stepdirection, christmasStep, setting_chasedelay

    while mode == "christmaschase":

        christmasStep += setting_stepdirection
        if setting_stepdirection == 1 and christmasStep >= 12:
            christmasStep = 0
        elif setting_stepdirection == -1 and christmasStep <= 0:
            christmasStep = 11

        if christmasStep == 0:
            putConvertedPixels([ red, red, red, red, green, green, green, green, white, white, white, white ] * 32)
        elif christmasStep == 1:
            putConvertedPixels([ red, red, red, green, green, green, green, white, white, white, white, red ] * 32)
        elif christmasStep == 2:
            putConvertedPixels([ red, red, green, green, green, green, white, white, white, white, red, red ] * 32)
        elif christmasStep == 3:
            putConvertedPixels([ red, green, green, green, green, white, white, white, white, red, red, red ] * 32)
        elif christmasStep == 4:
            putConvertedPixels([ green, green, green, green, white, white, white, white, red, red, red, red ] * 32)
        elif christmasStep == 5:
            putConvertedPixels([ green, green, green, white, white, white, white, red, red, red, red, green ] * 32)
        elif christmasStep == 6:
            putConvertedPixels([ green, green, white, white, white, white, red, red, red, red, green, green ] * 32)
        elif christmasStep == 7:
            putConvertedPixels([ green, white, white, white, white, red, red, red, red, green, green, green ] * 32)
        elif christmasStep == 8:
            putConvertedPixels([ white, white, white, white, red, red, red, red, green, green, green, green ] * 32)
        elif christmasStep == 9:
            putConvertedPixels([ white, white, white, red, red, red, red, green, green, green, green, white ] * 32)
        elif christmasStep == 10:
            putConvertedPixels([ white, white, red, red, red, red, green, green, green, green, white, white ] * 32)
        elif christmasStep == 11:
            putConvertedPixels([ white, red, red, red, red, green, green, green, green, white, white, white ] * 32)

        time.sleep(setting_chasedelay)
        



def megarainbow():
    global mode
    while mode == "megarainbow":
        global setting_chasedelay
        delay = setting_chasedelay

        putConvertedPixels([ (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0),  ] * 17)
        time.sleep(delay)
        putConvertedPixels([ (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0),  ] * 17)
        time.sleep(delay)
        putConvertedPixels([ (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0),  ] * 17)
        time.sleep(delay)
        putConvertedPixels([ (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0),  ] * 17)
        time.sleep(delay)
        putConvertedPixels([ (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0),  ] * 17)
        time.sleep(delay)
        putConvertedPixels([ (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0),  ] * 17)
        time.sleep(delay)
        putConvertedPixels([ (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0),  ] * 17)
        time.sleep(delay)
        putConvertedPixels([ (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0),  ] * 17)
        time.sleep(delay)
        putConvertedPixels([ (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0),  ] * 17)
        time.sleep(delay)
        putConvertedPixels([ (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0),  ] * 17)
        time.sleep(delay)
        putConvertedPixels([ (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0),  ] * 17)
        time.sleep(delay)
        putConvertedPixels([ (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0),  ] * 17)
        time.sleep(delay)
        putConvertedPixels([ (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0),  ] * 17)
        time.sleep(delay)
        putConvertedPixels([ (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0),  ] * 17)
        time.sleep(delay)
        putConvertedPixels([ (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0),  ] * 17)
        time.sleep(delay)
        putConvertedPixels([ (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0),  ] * 17)
        time.sleep(delay)
        putConvertedPixels([ (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0),  ] * 17)
        time.sleep(delay)
        putConvertedPixels([ (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0),  ] * 17)
        time.sleep(delay)
        putConvertedPixels([ (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0),  ] * 17)
        time.sleep(delay)
        putConvertedPixels([ (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0),  ] * 17)
        time.sleep(delay)
        putConvertedPixels([ (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0),  ] * 17)
        time.sleep(delay)
        putConvertedPixels([ (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0),  ] * 17)
        time.sleep(delay)
        putConvertedPixels([ (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0),  ] * 17)
        time.sleep(delay)
        putConvertedPixels([ (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0),  ] * 17)
        time.sleep(delay)
        putConvertedPixels([ (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0),  ] * 17)
        time.sleep(delay)

def megapulse():
    global mode
    speed = 8
    if mode == "megapulse":
        fullPulse((255, 0, 0, 0), speed)
        fullPulse((255, 128, 0, 0), speed)
        fullPulse((255, 255, 0, 0), speed)
        fullPulse((128, 255, 0, 0), speed)

    if mode == "megapulse":
        fullPulse((0, 255, 0, 0), speed)
        fullPulse((0, 255, 128, 0), speed)
        fullPulse((0, 255, 255, 0), speed)
        fullPulse((0, 128, 255, 0), speed)

    if mode == "megapulse":
        fullPulse((0, 0, 255, 0), speed)
        fullPulse((128, 0, 255, 0), speed)
        fullPulse((255, 0, 255, 0), speed)
        fullPulse((255, 0, 128, 0), speed)


def colorscroll():
    global mode
    if mode == "colorscroll":
        putConvertedPixels([ (255, 0, 0, 0) ] * 384)
        time.sleep(.5)
        putConvertedPixels([ (255, 255, 0, 0) ] * 384)
        time.sleep(.5)
        putConvertedPixels([ (0, 255, 0, 0) ] * 384)
        time.sleep(.5)
        putConvertedPixels([ (0, 255, 255, 0) ] * 384)
        time.sleep(.5)
        putConvertedPixels([ (0, 0, 255, 0) ] * 384)
        time.sleep(.5)
        putConvertedPixels([ (255, 0, 255, 0) ] * 384)
        time.sleep(.5)
        putConvertedPixels([ (0, 0, 0, 255) ] * 384)
        time.sleep(.5)


lastMode = mode
def flash():
    global mode, lastMode
    if mode == "flash":
        putConvertedPixels([ (64, 64, 64, 255) ] * 384)
        putConvertedPixels([ (64, 64, 64, 255) ] * 384)
        time.sleep(0.3)
        putConvertedPixels([ (0, 0, 0, 20) ] * 384)
        mode = lastMode


# noiseConstant = [154,136,124,101,99,98,99,101,108,119,134,139,131,114,99,108,105,96,103,114,109,98,129,149,167,173,165,149,133,124,125,131,138,148,157,151,141,135,127,117,112,106,101,99,110,110,100,103,114,114,112,117,120,114,110,114,120,122,117,110,110,109,109,107,101,122,143,166,185,192,180,157,128,111,102,99,115,126,140,152,151,141,126,114,112,112,114,106,97,98,100,99,96,104,115,132,154,165,176,176,162,143,132,134,138,137,122,97,108,116,129,128,124,121,123,130,139,143,144,136,132,129,126,115,107,100,97,102,97,102,106,115,114,110,101,97,97,100,108,120,131,138,129,105,103,118,130,130,123,110,111,125,128,127,129,134,137,129,116,107,104,103,96,106,108,114,111,105,107,114,115,109,106,99,99,103,106,104,97,98,105,103,103,104,99,103,108,107,96,114,123,141,163,175,179,165,142,120,101,101,109,124,135,142,142,139,127,118,119,120,115,107,96,103,107,115,117,119,113,101,104,112,111,104,98,102,109,115,113,111,106,97,103,105,106,112,122,122,113,101,97,97,96,97,100,99,101,96,103,114,122,122,115,102,106,123,131,129,115,103,99,103,98,108,121,140,156,161,160,151,133,102,114,125,127,121,111,98,109,112,109,107,101,99,103,105,105,108,112,117,119,112,100,99,99,100,100,119,132,134,]
noiseConstant = [12,11,10,8,6,4,2,1,0,0,0,2,3,4,5,5,6,6,6,6,7,6,6,6,5,5,4,3,2,2,1,0,0,1,1,0,0,0,1,2,2,3,4,4,5,4,4,2,1,0,2,4,6,7,8,8,8,9,10,11,11,12,12,12,12,11,11,11,11,9,7,5,3,1,0,1,2,3,3,4,3,2,1,1,1,2,2,2,2,2,2,1,0,1,2,2,2,2,2,0,0,1,2,3,4,5,5,5,5,4,2,1,0,0,1,1,1,1,0,0,3,5,8,9,11,11,11,11,9,8,6,4,1,0,2,4,5,6,6,6,4,3,1,0,2,3,4,5,7,8,7,7,6,4,3,2,0,0,0,0,0,0,1,2,3,4,5,5,5,4,4,4,4,4,4,3,2,1,0,0,1,1,2,2,1,1,0,0,1,1,0,0,1,1,2,3,4,5,6,7,8,9,9,9,8,8,8,8,9,10,11,12,13,13,13,11,9,6,3,0,1,3,4,4,4,4,3,3,1,0,3,6,8,9,11,11,10,9,9,7,6,5,3,2,1,0,0,0,1,1,1,1,1,0,0,1,1,1,1,1,1,2,4,6,8,10,10,10,10,8,6,4,3,2,1,0,0,0,0,1,3,5,7,9,11,12,12,12,10,9,6,4,2,0,1,2,2,2,2,3,]
noiseFrame = 0
def campfire():
    global mode, noiseFrame, campfireMode
    while mode == "campfire":
        if campfireMode == "hot":
            pixelPreScale = [ (255, 255, 0, 64), (255, 200, 0, 32), (255, 192, 0, 0), (255, 128, 0, 0), (255, 96, 0, 0), (200, 60, 0, 0), (192, 48, 0, 0), (128, 32, 0, 0), (64, 16, 0, 0), (32, 8, 0, 0), (0, 0, 0, 0) ]
        elif campfireMode == "cold":
            pixelPreScale = [ (0, 255, 255, 64), (0, 200, 255, 32), (0, 192, 255, 0), (0, 128, 255, 0), (0, 96, 255, 0), (0, 60, 200, 0), (0, 48, 192, 0), (0, 32, 128, 0), (0, 16, 64, 0), (0, 8, 32, 0), (0, 0, 0, 0) ]
        elif campfireMode == "green":
            pixelPreScale = [ (64, 255, 64, 64), (32, 255, 32, 32), (0, 255, 0, 0), (0, 240, 0, 0), (0, 210, 0, 0), (0, 150, 0, 0), (0, 90, 0, 0), (0, 70, 0, 0), (0, 45, 0, 0), (0, 24, 0, 0), (0, 0, 0, 0) ]

        for i in range(0, noiseConstant[noiseFrame]):
            pixelPreScale.append((0, 0, 0, 0))

        # print pixelPreScale
        putConvertedPixels(drawFromTopToBottom(pixelPreScale))



        # thisNoise = noiseConstant[noiseFrame]
        # putConvertedPixels([(noiseConstant[noiseFrame], 0, 0, 0)] * 384)

        noiseFrame += 1
        if noiseFrame >= 300:
            noiseFrame = 0


testFrame = 0
testColor = 0
def testChain():
    global mode, testFrame, testColor, testingChain
    while mode == "testChain":
        if testColor == 0:
            testRGBA = (255, 0, 0, 0)
        elif testColor == 1:
            testRGBA = (0, 255, 0, 0)
        elif testColor == 2:
            testRGBA = (0, 0, 255, 0)
        elif testColor == 3:
            testRGBA = (0, 0, 0, 255)

        jam = []
        addedStart = 0
        for gap in range(0, int(testingChain) - 1):
            for i in range(0, 48):
                jam.append((0, 0, 0, 0))
                addedStart += 1
            # print jam

        

        # print jam
        activePixels = 0
        for length in range(0, testFrame):
            jam.append(testRGBA)
            activePixels += 1
            # print jam

        # print jam
        inactivePixels = 0
        for length in range(testFrame, 48):
            inactivePixels += 1
            jam.append((0, 0, 0, 0))
            # print jam

        # print jam
        addedEnd = 0
        for gap in range(int(testingChain) - 1, 8):
            for i in range(0, 48):
                jam.append((0, 0, 0, 0))
                addedEnd += 1
            #print jam

        # print jam

        print "jam length: " + str(len(jam))
        print "testFrame: " + str(testFrame)
        print "testColor: " + str(testColor)
        print "addedStart: " + str(addedStart)
        print "activePixels: " + str(activePixels)
        print "inactivePixels: " + str(inactivePixels)
        print "addedEnd: " + str(addedEnd)
        print ""

        putConvertedPixels(jam)
        time.sleep(0.01)

        testFrame += 1
        if testFrame == 48:
            testFrame = 0
            testColor += 1
            if testColor == 4:
                testColor = 0



def totd():
    global mode
    while mode == "totd":
        for i in range(0, 3):
            client.put_pixels(convertPixels([ (255, 0, 0, 0) ] * 384))
            client.put_pixels(convertPixels([ (255, 0, 0, 0) ] * 384))
            time.sleep(0.07)
            client.put_pixels(convertPixels([ (0, 0, 0, 0) ] * 384))
            client.put_pixels(convertPixels([ (0, 0, 0, 0) ] * 384))
            time.sleep(0.07)
        client.put_pixels(convertPixels([ (0, 0, 255, 0) ] * 384))
        client.put_pixels(convertPixels([ (0, 0, 255, 0) ] * 384))
        time.sleep(0.25)
        for i in range(0, 3):
            client.put_pixels(convertPixels([ (0, 0, 0, 192) ] * 384))
            client.put_pixels(convertPixels([ (0, 0, 0, 192) ] * 384))
            time.sleep(0.07)
            client.put_pixels(convertPixels([ (0, 0, 0, 0) ] * 384))
            client.put_pixels(convertPixels([ (0, 0, 0, 0) ] * 384))
            time.sleep(0.07)
        client.put_pixels(convertPixels([ (0, 0, 255, 0) ] * 384))
        client.put_pixels(convertPixels([ (0, 0, 255, 0) ] * 384))
        time.sleep(0.25)


import socket
import select
UDP_IP_ADDRESS = "10.0.0.89"
UDP_PORT_NO = 6454

serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))
serverSock.settimeout(1.0)

def artnet():
    print "omfg artnet"
    global mode
    print mode
    while mode == "artnet":
        # print "mode is artnet"
        try:
            # print "a"
            holdPutPixels = True
            data, addr = serverSock.recvfrom(530)
            print "Message from " + str(addr)# + ": ", str(data)
            roffle = []
            for j in range(0, 8):
                for i in range(0, 48):
                    r = ord(data[(i * 4) + 18])
                    g = ord(data[(i * 4) + 19])
                    b = ord(data[(i * 4) + 20])
                    w = ord(data[(i * 4) + 21])

                    roffle.append((int(r * .8), int(g * .8), int(b * .8), int(w * .8)))

                    # if r + g + b + w > 750:
                    #     roffle.append((int(r * .75), int(g * .75), int(b * .75), int(w * .75)))
                    # else:
                    #     roffle.append((r, g, b, w))
                    # print convertPixels((r, g, b, w))
            client.put_pixels(convertPixels(roffle))
        except socket.timeout:
            print "no data"
        time.sleep(0.01)
    holdPutPixels = False









def crowdBlinderManager():
    global setting_crowdblinder, setting_crowdblinderactive
    while True:
        if setting_crowdblinderactive:
            setting_crowdblinder += 30
            if setting_crowdblinder > 255:
                setting_crowdblinder = 255
        else:
            setting_crowdblinder -= 2
            if setting_crowdblinder < 0:
                setting_crowdblinder = 0
        time.sleep(0.01)


crowdBlinderManagerThread = Thread(target=crowdBlinderManager)
crowdBlinderManagerThread.daemon = True
crowdBlinderManagerThread.start()


def strobeManager():
    global strobe_active, strobe_duration
    while True:
        if strobe_active:
            print "strobe"
            client.put_pixels(convertPixels([ (0, 0, 128, 255) ] * 384))
            #client.put_pixels(convertPixels([ (0, 0, 255, 255) ] * 384))
            time.sleep(strobe_duration)
            client.put_pixels(convertPixels([ (0, 0, 0, 0) ] * 384))
            #client.put_pixels(convertPixels([ (0, 0, 0, 0) ] * 384))
            time.sleep(strobe_duration)
        else:
            time.sleep(0.02)

        # time.sleep(0.02)

strobeManagerThread = Thread(target=strobeManager)
strobeManagerThread.daemon = True
strobeManagerThread.start()







while True:
    # add new modes here and make sure the function only runs while the mode is the same as my function; it'll cycle between them and
    # stop on the active mode.  Don't block too much; otherwise it'll have to finish the cycle before it switches modes
    soundActivated()
    chase()
    solid()
    supachase()
    megapulse()
    colorscroll()
    megarainbow()
    flash()
    campfire()
    testChain()
    totd()
    christmaschase()
    print "b"
    artnet()
    print "c"











# for i in range(0, 400):
#   pixels = []
#   print i
#   for j in range(0, i):
#       pixels.append((255, 0, 0, 0))
#   for j in range(i, 120):
#       pixels.append((0, 0, 0, 255))
#   #print pixels
#   putConvertedPixels(pixels)
#   time.sleep(.005)

# for i in range(0, 400):
#   pixels = []
#   print i
#   for j in range(0, i):
#       pixels.append((0, 0, 0, 255))
#   for j in range(i, 120):
#       pixels.append((0, 255, 0, 0))
#   #print pixels
#   putConvertedPixels(pixels)
#   time.sleep(.1)


        



