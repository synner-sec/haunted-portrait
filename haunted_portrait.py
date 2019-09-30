#!/usr/bin/env python3
#Written by Jason Smith
#Nightmare on 17th Street Haunted House Kitchen Intro
#This setup allows for an intro mp3 to be played when button is presses, and for the portrait to trigger when PIR is activated

# Imports
import sys
from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep
import RPi.GPIO as GPIO
import time
import vlc
import os

#Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN)
audio1_path = 'path to 1st mp3 file'
audio2_path = 'path to 2nd mp3 file'
files = sys.argv[1]
slength = '1440'
swidth = '900'
print("Starting up....")
tgr = 0
audio_tgr = 0
mp3_1 = vlc.MediaPlayer(audio1_path)
mp3_2 = vlc.MediaPlayer(audio2_path)

# Remove OMX /tmp files to avoid system lockup
if os.path.exists('/tmp/omxplayerdbus.pi'):
    os.remove('/tmp/omxplayerdbus.pi')
if os.path.exists('/tmp/omxplayerdbus.pi.pid'):
   os.remove('/tmp/omxplayerdbus.pi.pid')
try:
    sleep(2)
    VIDEO_PATH = Path(files)
    player = OMXPlayer(VIDEO_PATH,  args=['--no-osd', '--loop', '--win', '784 588 640 480'.format(slength, swidth)])
    sleep(1)
    print("Ready to trigger")
    while True:
        player.pause()
        input_state2 = GPIO.input(24)
        input_state = GPIO.input(22)
        if input_state == True: # If PIR Triggered
            print("Triggering Painting")
            player.play()
            sleep(player.duration()) # not allow any other action until player has completed
            tgr = tgr + 1
            print("Playing exit audio")
            mp3_2.play()
            player.pause()
            print("sleeping for 5 Minutes")
            sleep(300)
            mp3_2.stop()
            print("Ready!")
        if input_state2 == False: # If button pressed
            sleep(10)
            print("Playing Intro")
            mp3_1.play()
            sleep(31) # Sleep to not allow PIR to trigger until intro has played through
            mp3_1.stop()
            print("Ready!")
        else:
            pass
        player.set_position(0.0)


except KeyboardInterrupt:
    player.quit()
    sys.exit()
