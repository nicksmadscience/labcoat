import opc, time, random, numpy
from timeit import default_timer as timer
client = opc.Client('localhost:7890')
from threading import Thread

mode = "campfire"
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
                        crowdblinder(_pixels[(pixelQuad * 3) + 0][0], -setting_crowdblinder) >> invbrightness,
                        crowdblinder(_pixels[(pixelQuad * 3) + 0][1], -setting_crowdblinder) >> invbrightness,
                        crowdblinder(_pixels[(pixelQuad * 3) + 0][2], setting_crowdblinder) >> invbrightness,
                    ))
                pixelsConverted.append((
                        crowdblinder(_pixels[(pixelQuad * 3) + 1][1], -setting_crowdblinder) >> invbrightness,
                        crowdblinder(_pixels[(pixelQuad * 3) + 0][3], setting_crowdblinder) >> invbrightness,
                        crowdblinder(_pixels[(pixelQuad * 3) + 1][0], -setting_crowdblinder) >> invbrightness,
                    ))
                pixelsConverted.append((
                        crowdblinder(_pixels[(pixelQuad * 3) + 1][3], setting_crowdblinder) >> invbrightness,
                        crowdblinder(_pixels[(pixelQuad * 3) + 1][2], setting_crowdblinder) >> invbrightness,
                        crowdblinder(_pixels[(pixelQuad * 3) + 2][1], -setting_crowdblinder) >> invbrightness,
                ))
                pixelsConverted.append((
                        crowdblinder(_pixels[(pixelQuad * 3) + 2][2], setting_crowdblinder) >> invbrightness,
                        crowdblinder(_pixels[(pixelQuad * 3) + 2][0], -setting_crowdblinder) >> invbrightness,
                        crowdblinder(_pixels[(pixelQuad * 3) + 2][3], setting_crowdblinder) >> invbrightness,
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
    global strobe_active, client
    if not strobe_active:
        client.put_pixels(_pixels)




def step(_sequence, _delay):
    pixels = _sequence * 96
    putPixels(convertPixels(pixels))
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
#   putPixels(convertPixels(pixels))
#   time.sleep(0.25)



def sweep(_color, _delay):
    putPixels(convertPixels([ (0, 0, 0, 0) ] * 384))

    for i in range(0, 186):
        pixels = []
        str = ""
        print i
        for j in range(0, i):
            str += " "
            pixels.append((0, 0, 0, 0))
        for k in range(0, 12):
            str += "x"
            pixels.append(_color)
        for j in range(i + 12, 192):
            pixels.append((0, 0, 0, 0))
            str += " "
        print str
        putPixels(convertPixels(pixels))
        time.sleep(_delay)

    for i in reversed(range(0, 186)):
        pixels = []
        str = ""
        print i
        for j in range(0, i):
            str += " "
            pixels.append((0, 0, 0, 0))
        for k in range(0, 12):
            str += "x"
            pixels.append(_color)
        for j in range(i + 12, 192):
            pixels.append((0, 0, 0, 0))
            str += " "
        print str
        putPixels(convertPixels(pixels))
        time.sleep(_delay)


def fullPulse(_color, _range):
    for i in range(0, _range):
        multiplier = float(i) / float(_range)
        # print int(float(_color[0]) * float(multiplier))
        pixels = [ (int(float(_color[0]) * float(multiplier)), int(float(_color[1]) * float(multiplier)), int(float(_color[2]) * float(multiplier)), int(float(_color[3]) * float(multiplier))) ] * 384
        putPixels(convertPixels(pixels))
    for i in reversed(range(0, _range)):
        multiplier = float(i) / float(_range)
        # print int(float(_color[0]) * float(multiplier))
        pixels = [ (int(float(_color[0]) * float(multiplier)), int(float(_color[1]) * float(multiplier)), int(float(_color[2]) * float(multiplier)), int(float(_color[3]) * float(multiplier))) ] * 384
        putPixels(convertPixels(pixels))



# numberOfPixels = 384
# pixels = [(0, 0, 0, 255)] * numberOfPixels
# putPixels(convertPixels(pixels))

# time.sleep(99999)

# import pyaudio
# p = pyaudio.PyAudio()
# info = p.get_host_api_info_by_index(0)
# numdevices = info.get('deviceCount')
# for i in range(0, numdevices):
#         if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
#             print "Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name')

# # time.sleep(1000000)
# import pyaudio
# import numpy as np
# np.set_printoptions(suppress=True) # don't use scientific notation

# CHUNK = 4096 # number of data points to read at a time
# RATE = 44100 # time resolution of the recording device (Hz)
# TARGET = 2100 # show only this one frequency

# p=pyaudio.PyAudio() # start the PyAudio class
# # devinfo = p.get_device_info_by_index(1)
# stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
#               frames_per_buffer=CHUNK, input_device_index=2)

# # create a numpy array holding a single read of audio data
# for i in range(10): #to it a few times just to see
#     data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
#     fft = abs(np.fft.fft(data).real)
#     fft = fft[:int(len(fft)/2)] # keep only first half
#     freq = np.fft.fftfreq(CHUNK,1/RATE)
#     freq = freq[:int(len(freq)/2)] # keep only first half
#     assert freq[-1]>TARGET, "ERROR: increase chunk size"
#     val = fft[np.where(freq>TARGET)[0][0]]
#     print(val)

# # close the stream gracefully
# stream.stop_stream()
# stream.close()
# p.terminate()




# # Read from Mic Input and find the freq's
# import pyaudio
# import numpy as np
# # import bge
# import wave

# chunk = 2048

# # use a Blackman window
# window = np.blackman(chunk)
# # open stream
# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 44100

# p = pyaudio.PyAudio()
# myStream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = chunk, input_device_index=2)

# def AnalyseStream(cont):
#     data = myStream.read(chunk)
#     # unpack the data and times by the hamming window
#     indata = np.array(wave.struct.unpack("%dh"%(chunk), data))*window
#     # Take the fft and square each value
#     fftData=abs(np.fft.rfft(indata))**2
#     # find the maximum
#     which = fftData[1:].argmax() + 1
#     # use quadratic interpolation around the max
#     if which != len(fftData)-1:
#         y0,y1,y2 = np.log(fftData[which-1:which+2:])
#         x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
#         # find the frequency and output it
#         thefreq = (which+x1)*RATE/chunk
#         print("The freq is %f Hz." % (thefreq))
#     else:
#         thefreq = which*RATE/chunk
#         print("The freq is %f Hz." % (thefreq))

# while True:
#     AnalyseStream(1)

# time.sleep(100000)

# stream.close()
# p.terminate()



# def design_filter(lowcut, highcut, fs, order=3):
#     nyq = 0.5*fs
#     low = lowcut/nyq
#     high = highcut/nyq
#     b,a = butter(order, [low,high], btype='band')
#     return b,a

# def normalize(block):
#     count = len(block) / 2
#     format = "%dh"%(count)
#     shorts = struct.unpack( format, block )
#     doubles = [x * SHORT_NORMALIZE from x in shorts]
#     return doubles


# def get_rms(samples):
#     sum_squares = 0.0
#     for sample in doubles:
#         sum_squares += n*n
#     return math.sqrt( sum_squares / count )


# pa = pyaudio.PyAudio()                                 
# stream = pa.open(format = FORMAT,                      
#          channels = CHANNELS,                          
#          rate = RATE,                                  
#          input = True,                                 
#          frames_per_buffer = INPUT_FRAMES_PER_BLOCK)   

# errorcount = 0                                                  

# # design the filter
# b,a = design_filter(19400, 19600, 48000, 3)
# # compute the initial conditions.
# zi = lfilter_zi(b, a)

# for i in range(1000):
#     try:                                                    
#         block = stream.read(INPUT_FRAMES_PER_BLOCK)         
#     except IOError, e:                                      
#         errorcount += 1                                     
#         print( "(%d) Error recording: %s"%(errorcount,e) )  
#         noisycount = 1          

#     samples = normalize(block)                            

#     bandpass_samples,zi = lfilter(b, a, samples, zi)

#     amplitude = get_rms(samples)
#     bandpass_ampl = get_rms(bandpass_samples)
#     print amplitude
#     print bandpass_ampl





# #Eng Eder de Souza 01/12/2011
# #ederwander
# from matplotlib.mlab import find
# import pyaudio
# import numpy as np
# import math


# chunk = 1024
# FORMAT = pyaudio.paInt16
# CHANNELS = 2
# RATE = 44100
# RECORD_SECONDS = 20


# def Pitch(signal):
#     signal = np.fromstring(signal, 'Int16');
#     crossing = [math.copysign(1.0, s) for s in signal]
#     index = find(np.diff(crossing));
#     f0=round(len(index) *RATE /(2*np.prod(len(signal))))
#     return f0;


# p = pyaudio.PyAudio()

# stream = p.open(format = FORMAT,
# channels = CHANNELS,
# rate = RATE,
# input = True,
# output = True,
# frames_per_buffer = chunk,
# input_device_index=2)

# for i in range(0, RATE / chunk * RECORD_SECONDS):
#     data = stream.read(chunk)
#     Frequency=Pitch(data)
#     print "%f Frequency" %Frequency

# time.sleep(100000)







# import pyaudio, struct, pprint, inspect, math
# from scipy import signal
# import numpy as np
# from timeit import default_timer as timer



# def design_filter(lowcut, highcut, fs, order=3):
#     nyq = 0.5*fs
#     low = lowcut/nyq
#     high = highcut/nyq
#     b,a = signal.butter(order, [low,high], btype='band')
#     return b,a

# def normalize(block):
#     count = len(block) / 2
#     format_ = "%dh"%(count)
#     shorts = struct.unpack( format_, block )

#     doubles = []
#     for x in shorts:
#         doubles.append(x * SHORT_NORMALIZE)

#     return doubles


# def get_rms(samples):
#     sum_squares = 0.0
#     for sample in samples:
#         sum_squares += sample * sample
#     return math.sqrt( sum_squares / len(samples) )

# SHORT_NORMALIZE = (1.0/32768.0)
# chunk = 1024
# FORMAT = pyaudio.paInt16
# CHANNELS = 2
# RATE = 44100

# pa = pyaudio.PyAudio()                                 
# stream = pa.open(format = FORMAT,                      
#          channels = CHANNELS,                          
#          rate = RATE,                                  
#          input = True,                                 
#          frames_per_buffer = chunk,
#          input_device_index=2)

# # design the filter
# b2,a2 = design_filter(19400, 19600, 48000, 3)
# # compute the initial conditions.
# zi2 = signal.lfilter_zi(b2, a2)


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
    global mode
    mode = "campfire"
    print "campfire!"
    return "text/plain", "campfire"

def requestHandler_reversedirection(_request):
    global setting_stepdirection
    if setting_stepdirection == 1:
        setting_stepdirection = -1
    else:
        setting_stepdirection = 1
    print "reverse direction!"
    return "text/plain", "reverse direction"

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

def requestHandler_color(_request):
    global setting_color, mode
    # mode = "color"
    print _request[2]
    color = _request[2]
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

httpRequests = {''      : requestHandler_index,
                'chase' : requestHandler_chase,
                'soundactivated' : requestHandler_soundactivated,
                'solid' : requestHandler_solid,
                'supachase' : requestHandler_supachase,
                'megapulse' : requestHandler_megapulse,
                'colorscroll' : requestHandler_colorscroll,
                'megarainbow' : requestHandler_megarainbow,
                'campfire' : requestHandler_campfire,
                'reversedirection' : requestHandler_reversedirection,
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

# httpThread = Thread(target=http)
# httpThread.daemon = True
# httpThread.start()


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
#         putPixels(convertPixels(drawFromTopToBottom(array)))
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

# putPixels(convertPixels(pixels))
# putPixels(convertPixels(pixels))
# time.sleep(9999)



import alsaaudio, audioop, math


inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK, cardindex=1)

inp.setchannels(2)
inp.setrate(11025)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

inp.setperiodsize(1024)

setting_decay = 4
numberOfPixels = 384
pixels = [(0, 0, 0, 0)] * numberOfPixels
colorIndex = 0
color = (255, 0, 0, 255)
timeSinceLastColorChange = time.time()
timeSinceLastFrame = time.time()
colorpulseValue = 0.0
def soundActivated():
    global pixels, setting_decay, colorIndex, color, timeSinceLastColorChange, timeSinceLastFrame, mode, sensitivity, setting_soundmode, colorpulseValue, setting_color

    # errorcount = 0
    while mode == "soundactivated":
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

                
                putPixels(convertPixels(pixels))
        except Exception as e:
            print e

        print timer() - start
                



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
        putPixels(convertPixels([ setting_color ] * 384))
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
            # print christmasSequence
        color = setting_color

        step += setting_stepdirection
        if setting_stepdirection == 1 and step == 40:
            step = 0
        elif setting_stepdirection == -1 and step == 0:
            step = 39

        if step == 1:
            putPixels(convertPixels([ black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black,  ] * 11))
        elif step == 2:
            putPixels(convertPixels([ black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black,  ] * 11))
        elif step == 3:
            putPixels(convertPixels([ black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black,  ] * 11))
        elif step == 4:
            putPixels(convertPixels([ black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black,  ] * 11))
        elif step == 5:
            putPixels(convertPixels([ black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black,  ] * 11))
        elif step == 6:
            putPixels(convertPixels([ black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black,  ] * 11))
        elif step == 7:
            putPixels(convertPixels([ black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black,  ] * 11))
        elif step == 8:
            putPixels(convertPixels([ black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black,  ] * 11))
        elif step == 9:
            putPixels(convertPixels([ black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black,  ] * 11))
        elif step == 10:
            putPixels(convertPixels([ black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black,  ] * 11))
        elif step == 11:
            putPixels(convertPixels([ black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black,  ] * 11))
        elif step == 12:
            putPixels(convertPixels([ black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black,  ] * 11))
        elif step == 13:
            putPixels(convertPixels([ black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black,  ] * 11))
        elif step == 14:
            putPixels(convertPixels([ black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black,  ] * 11))
        elif step == 15:
            putPixels(convertPixels([ black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black,  ] * 11))
        elif step == 16:
            putPixels(convertPixels([ black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black,  ] * 11))
        elif step == 17:
            putPixels(convertPixels([ black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black,  ] * 11))
        elif step == 18:
            putPixels(convertPixels([ black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color,  ] * 11))
        elif step == 19:
            putPixels(convertPixels([ color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color,  ] * 11))
        elif step == 20:
            putPixels(convertPixels([ color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color,  ] * 11))
        elif step == 21:
            putPixels(convertPixels([ color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color,  ] * 11))
        elif step == 22:
            putPixels(convertPixels([ color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color,  ] * 11))
        elif step == 23:
            putPixels(convertPixels([ color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color,  ] * 11))
        elif step == 24:
            putPixels(convertPixels([ color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color, color,  ] * 11))
        elif step == 25:
            putPixels(convertPixels([ color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color, color,  ] * 11))
        elif step == 26:
            putPixels(convertPixels([ color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color, color,  ] * 11))
        elif step == 27:
            putPixels(convertPixels([ color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color, color,  ] * 11))
        elif step == 28:
            putPixels(convertPixels([ color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color, color,  ] * 11))
        elif step == 29:
            putPixels(convertPixels([ color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color, color,  ] * 11))
        elif step == 30:
            putPixels(convertPixels([ color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color, color,  ] * 11))
        elif step == 31:
            putPixels(convertPixels([ color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color, color,  ] * 11))
        elif step == 32:
            putPixels(convertPixels([ color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color, color,  ] * 11))
        elif step == 33:
            putPixels(convertPixels([ color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color, color,  ] * 11))
        elif step == 34:
            putPixels(convertPixels([ color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color, color,  ] * 11))
        elif step == 35:
            putPixels(convertPixels([ color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color, color,  ] * 11))
        elif step == 36:
            putPixels(convertPixels([ color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color, color,  ] * 11))
        elif step == 37:
            putPixels(convertPixels([ color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, color,  ] * 11))
        elif step == 38:
            putPixels(convertPixels([ color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black,  ] * 11))
        elif step == 39:
            putPixels(convertPixels([ black, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, color, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black,  ] * 11))

        time.sleep(setting_chasedelay)

def megarainbow():
    global mode
    while mode == "megarainbow":
        global setting_chasedelay
        delay = setting_chasedelay

        putPixels(convertPixels([ (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0),  ] * 17))
        time.sleep(delay)
        putPixels(convertPixels([ (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0),  ] * 17))
        time.sleep(delay)
        putPixels(convertPixels([ (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0),  ] * 17))
        time.sleep(delay)
        putPixels(convertPixels([ (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0),  ] * 17))
        time.sleep(delay)
        putPixels(convertPixels([ (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0),  ] * 17))
        time.sleep(delay)
        putPixels(convertPixels([ (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0),  ] * 17))
        time.sleep(delay)
        putPixels(convertPixels([ (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0),  ] * 17))
        time.sleep(delay)
        putPixels(convertPixels([ (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0),  ] * 17))
        time.sleep(delay)
        putPixels(convertPixels([ (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0),  ] * 17))
        time.sleep(delay)
        putPixels(convertPixels([ (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0),  ] * 17))
        time.sleep(delay)
        putPixels(convertPixels([ (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0),  ] * 17))
        time.sleep(delay)
        putPixels(convertPixels([ (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0),  ] * 17))
        time.sleep(delay)
        putPixels(convertPixels([ (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0),  ] * 17))
        time.sleep(delay)
        putPixels(convertPixels([ (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0),  ] * 17))
        time.sleep(delay)
        putPixels(convertPixels([ (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0),  ] * 17))
        time.sleep(delay)
        putPixels(convertPixels([ (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0),  ] * 17))
        time.sleep(delay)
        putPixels(convertPixels([ (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0),  ] * 17))
        time.sleep(delay)
        putPixels(convertPixels([ (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0),  ] * 17))
        time.sleep(delay)
        putPixels(convertPixels([ (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0),  ] * 17))
        time.sleep(delay)
        putPixels(convertPixels([ (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0),  ] * 17))
        time.sleep(delay)
        putPixels(convertPixels([ (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0),  ] * 17))
        time.sleep(delay)
        putPixels(convertPixels([ (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0),  ] * 17))
        time.sleep(delay)
        putPixels(convertPixels([ (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 0, 0),  ] * 17))
        time.sleep(delay)
        putPixels(convertPixels([ (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0),  ] * 17))
        time.sleep(delay)
        putPixels(convertPixels([ (255, 0, 255, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 0, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (255, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 0, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 255, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (0, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0), (255, 0, 255, 0),  ] * 17))
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
        putPixels(convertPixels([ (255, 0, 0, 0) ] * 384))
        time.sleep(.5)
        putPixels(convertPixels([ (255, 255, 0, 0) ] * 384))
        time.sleep(.5)
        putPixels(convertPixels([ (0, 255, 0, 0) ] * 384))
        time.sleep(.5)
        putPixels(convertPixels([ (0, 255, 255, 0) ] * 384))
        time.sleep(.5)
        putPixels(convertPixels([ (0, 0, 255, 0) ] * 384))
        time.sleep(.5)
        putPixels(convertPixels([ (255, 0, 255, 0) ] * 384))
        time.sleep(.5)
        putPixels(convertPixels([ (0, 0, 0, 255) ] * 384))
        time.sleep(.5)


lastMode = mode
def flash():
    global mode, lastMode
    if mode == "flash":
        putPixels(convertPixels([ (64, 64, 64, 255) ] * 384))
        putPixels(convertPixels([ (64, 64, 64, 255) ] * 384))
        time.sleep(0.3)
        putPixels(convertPixels([ (0, 0, 0, 20) ] * 384))
        mode = lastMode


# noiseConstant = [154,136,124,101,99,98,99,101,108,119,134,139,131,114,99,108,105,96,103,114,109,98,129,149,167,173,165,149,133,124,125,131,138,148,157,151,141,135,127,117,112,106,101,99,110,110,100,103,114,114,112,117,120,114,110,114,120,122,117,110,110,109,109,107,101,122,143,166,185,192,180,157,128,111,102,99,115,126,140,152,151,141,126,114,112,112,114,106,97,98,100,99,96,104,115,132,154,165,176,176,162,143,132,134,138,137,122,97,108,116,129,128,124,121,123,130,139,143,144,136,132,129,126,115,107,100,97,102,97,102,106,115,114,110,101,97,97,100,108,120,131,138,129,105,103,118,130,130,123,110,111,125,128,127,129,134,137,129,116,107,104,103,96,106,108,114,111,105,107,114,115,109,106,99,99,103,106,104,97,98,105,103,103,104,99,103,108,107,96,114,123,141,163,175,179,165,142,120,101,101,109,124,135,142,142,139,127,118,119,120,115,107,96,103,107,115,117,119,113,101,104,112,111,104,98,102,109,115,113,111,106,97,103,105,106,112,122,122,113,101,97,97,96,97,100,99,101,96,103,114,122,122,115,102,106,123,131,129,115,103,99,103,98,108,121,140,156,161,160,151,133,102,114,125,127,121,111,98,109,112,109,107,101,99,103,105,105,108,112,117,119,112,100,99,99,100,100,119,132,134,]
noiseConstant = [12,11,10,8,6,4,2,1,0,0,0,2,3,4,5,5,6,6,6,6,7,6,6,6,5,5,4,3,2,2,1,0,0,1,1,0,0,0,1,2,2,3,4,4,5,4,4,2,1,0,2,4,6,7,8,8,8,9,10,11,11,12,12,12,12,11,11,11,11,9,7,5,3,1,0,1,2,3,3,4,3,2,1,1,1,2,2,2,2,2,2,1,0,1,2,2,2,2,2,0,0,1,2,3,4,5,5,5,5,4,2,1,0,0,1,1,1,1,0,0,3,5,8,9,11,11,11,11,9,8,6,4,1,0,2,4,5,6,6,6,4,3,1,0,2,3,4,5,7,8,7,7,6,4,3,2,0,0,0,0,0,0,1,2,3,4,5,5,5,4,4,4,4,4,4,3,2,1,0,0,1,1,2,2,1,1,0,0,1,1,0,0,1,1,2,3,4,5,6,7,8,9,9,9,8,8,8,8,9,10,11,12,13,13,13,11,9,6,3,0,1,3,4,4,4,4,3,3,1,0,3,6,8,9,11,11,10,9,9,7,6,5,3,2,1,0,0,0,1,1,1,1,1,0,0,1,1,1,1,1,1,2,4,6,8,10,10,10,10,8,6,4,3,2,1,0,0,0,0,1,3,5,7,9,11,12,12,12,10,9,6,4,2,0,1,2,2,2,2,3,]
noiseFrame = 0
def campfire():
    global mode, noiseFrame
    while mode == "campfire":
        pixelPreScale = [ (255, 255, 0, 64), (255, 200, 0, 32), (255, 192, 0, 0), (255, 128, 0, 0), (255, 96, 0, 0), (200, 60, 0, 0), (192, 48, 0, 0), (128, 32, 0, 0), (64, 16, 0, 0), (32, 8, 0, 0), (0, 0, 0, 0) ]
        for i in range(0, noiseConstant[noiseFrame]):
            pixelPreScale.append((0, 0, 0, 0))

        # print pixelPreScale
        putPixels(convertPixels(drawFromTopToBottom(pixelPreScale)))



        # thisNoise = noiseConstant[noiseFrame]
        # putPixels(convertPixels([(noiseConstant[noiseFrame], 0, 0, 0)] * 384))

        noiseFrame += 1
        if noiseFrame >= 300:
            noiseFrame = 0





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
            client.put_pixels(convertPixels([ (0, 0, 255, 255) ] * 384))
            client.put_pixels(convertPixels([ (0, 0, 255, 255) ] * 384))
            time.sleep(strobe_duration)
            client.put_pixels(convertPixels([ (0, 0, 0, 0) ] * 384))
            client.put_pixels(convertPixels([ (0, 0, 0, 0) ] * 384))
            time.sleep(strobe_duration)
        else:
            time.sleep(0.02)

        # time.sleep(0.02)

strobeManagerThread = Thread(target=strobeManager)
strobeManagerThread.daemon = True
strobeManagerThread.start()


while True:
    soundActivated()
    chase()
    solid()
    supachase()
    megapulse()
    colorscroll()
    megarainbow()
    flash()
    campfire()











# for i in range(0, 400):
#   pixels = []
#   print i
#   for j in range(0, i):
#       pixels.append((255, 0, 0, 0))
#   for j in range(i, 120):
#       pixels.append((0, 0, 0, 255))
#   #print pixels
#   putPixels(convertPixels(pixels))
#   time.sleep(.005)

# for i in range(0, 400):
#   pixels = []
#   print i
#   for j in range(0, i):
#       pixels.append((0, 0, 0, 255))
#   for j in range(i, 120):
#       pixels.append((0, 255, 0, 0))
#   #print pixels
#   putPixels(convertPixels(pixels))
#   time.sleep(.1)


        



