#!/usr/bin/env python3
# -*- coding: utf8 -*-

# inspired by https://community.volumio.org/t/turn-on-a-led-when-volumio-ui-is-ready/5273

import RPi.GPIO as GPIO
import requests
import time

redLedPin   = 37
greenLedPin = 29
blueLedPin  = 31

url      = 'http://localhost:3000/index.html'


def setup():
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(redLedPin,GPIO.OUT)
  GPIO.setup(greenLedPin,GPIO.OUT)
  GPIO.setup(blueLedPin,GPIO.OUT)
  setLed(True, False, False) # initially RED

def setLed(red, green, blue):
  GPIO.output(redLedPin, GPIO.HIGH if red else GPIO.LOW)
  GPIO.output(greenLedPin, GPIO.HIGH if green else GPIO.LOW)
  GPIO.output(blueLedPin, GPIO.HIGH if blue else GPIO.LOW)

def getVolumioStatus():
  try:
     response = requests.get('http://localhost:3000/api/v1/getState', timeout=2)
     response.raise_for_status()
  except requests.exceptions.HTTPError as errHttp:
    print('HTTP error: %s', errHttp)
    return False
  except requests.ConnectionError as errCon:
    print('Connection error: %s', errCon)
    return False
  except requests.Timeout as errTimeout:
    print('Timeout: %s', errTimeout)
    return False
  except requests.exceptions.RequestException as errReq:
    print('Request Error: %s', errReq)
    return False

  json_data = response.json()
  if ('status' not in json_data):
      print ('No Status returned')
      return False

  status= json_data['status']
  print (status)
  return True
  

def LEDon():
  while True:
    volumioReady = getVolumioStatus()
    if volumioReady:
      break
    else:
      time.sleep(2)
  setLed(False, True, False) ## Green when ready

def destroy():
  setLed(False, False, False)    ## LED off
  GPIO.cleanup()                 ## Release resource

def main():
  setup()
  try:
    LEDon()
  except KeyboardInterrupt:      ## When 'CTRL+C' is pressed.
    destroy()

if __name__ == '__main__':       ## Program start from here
    main()