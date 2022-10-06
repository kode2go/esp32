# Led control

```
>>> led = Pin(4, Pin.OUT)
>>> from machine import Pin
>>> led.value(1)

>>> led.value(0)
```

https://how2electronics.com/esp32-micropython-web-server/

https://randomnerdtutorials.com/micropython-esp32-esp8266-access-point-ap/

# Webserver AP

```
# Complete project details at https://RandomNerdTutorials.com

try:
  import usocket as socket
except:
  import socket

import network

import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = 'MicroPython-AP'
password = '123456789'

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password)

while ap.active() == False:
  pass

print('Connection successful')
print(ap.ifconfig())
import random

def myrandnum():
    num1 = random.randint(0, 9)
    return num1
    
def web_page():
    temp = myrandnum()
    html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <meta http-equiv="refresh" content="1"></head>
      <body><h1>Hello, World!</h1>
      <span id="temperature">""" + str(temp) + """</span>
    </body></html>"""
    return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  print('Content = %s' % str(request))
  response = web_page()
  conn.send(response)
  conn.close()
```

# Web server 2 - boot setup

```
# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

try:
  import usocket as socket
except:
  import socket
  
from time import sleep
from machine import Pin

 
import network
 
import esp
esp.osdebug(None)
 
import gc
gc.collect()
 
 
ssid = 'xxx
password = 'xxx'
 
station = network.WLAN(network.STA_IF)
 
station.active(True)
station.connect(ssid, password)
 
while station.isconnected() == False:
  pass
 
print('Connection successful')
print(station.ifconfig())

```



# Web server 2 - main code with refresh

```
import random as rd

def read_ds_sensor():
  num1 = rd.randint(0, 999)
  return num1

  
def web_page():
  temp = read_ds_sensor()
  html = """<!DOCTYPE HTML><html><head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="refresh" content="5">
  <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
  <style> html { font-family: Arial; display: inline-block; margin: 0px auto; text-align: center; }
    h2 { font-size: 3.0rem; } p { font-size: 3.0rem; } .units { font-size: 1.2rem; } 
    .ds-labels{ font-size: 1.5rem; vertical-align:middle; padding-bottom: 15px; }
  </style></head><body><h2>ESP32 DS18B20 WebServer</h2>
  <p><i class="fas fa-thermometer-half" style="color:#059e8a;"></i> 
    <span class="ds-labels">Temperature</span>
    <span id="temperature">""" + str(temp) + """</span>
    <sup class="units">&deg;C</sup>
  </p>
    <p><i class="fas fa-thermometer-half" style="color:#059e8a;"></i> 
    <span class="ds-labels">Temperature</span>
    <span id="temperature">""" + str(round(temp * (9/5) + 32.0, 2)) + """</span>
    <sup class="units">&deg;F</sup>
  </p></body></html>"""
  return html
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
 
while True:
  try:
    if gc.mem_free() < 102000:
      gc.collect()
    conn, addr = s.accept()
    conn.settimeout(3.0)
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    conn.settimeout(None)
    request = str(request)
    print('Content = %s' % request)
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
  except OSError as e:
    conn.close()
    print('Connection closed')

```



# Cam usage shell

```
>>> import camera
>>> camera.init(0, format=camera.JPEG)
True
>>> buf = camera.capture()
>>> f = open('image.jpg','w')
>>> f.write(buf)
64664
>>> f.close()
>>> camera.speffect(camera.EFFECT_BW)
>>> 
>>> buf = camera.capture()
>>> f = open('image2.jpg','w')
>>> 
>>> f.write(buf)
59897
>>> f.close()

>>> buf = camera.capture()
>>> mylist = list(buf)
>>> mylist
```

