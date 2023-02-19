
"""
Display the Raspberry Pi logo (loads image as .png).
"""

from pathlib import Path
from imports.demo_opts import get_device
from PIL import Image
import time
from luma.core.sprite_system import framerate_regulator
from PIL import Image, ImageSequence
from pubsub import pub
from math import sqrt
import paho.mqtt.client as mqtt
import json


try:
    import av
except ImportError:
    print("The pyav library could not be found. Install it using 'sudo -H pip install av'.")
    sys.exit()

class oledController:
    device = get_device()

    def __init__(self):
        pub.subscribe(self.showEmotion, "emotion")
                
            
    def motor(self):
        print("HEYEYEYEYEY")



    def showEmotion(self, client, userdata, message):
        global device
        
        #For pictures
        #img_path1 = str(Path(__file__).resolve().parent.joinpath('1.png')) # Get picture frame
        #logo1 = Image.open(img_path1).transform(device.size, Image.Transform.AFFINE, (1, 0, 0, 0, 1, 0), Image.Resampling.BILINEAR).convert("RGB") # Convert frame to correct color format
     #       background = Image.new("RGB", device.size, "white")
      #      background.paste(logo1, (0,0))
       #     device.display(background.convert(device.mode))
        #    time.sleep(3)
        
        #emotion = arg['emotion']
        string = str(message.payload.decode("utf-8"))
        print(string)
        jsonstring = json.loads(string)
        emotion = int(jsonstring["emotion"])

        # Selects correct animation depending on the arrg
        if emotion == 1:  
            video_path = str(Path(__file__).resolve().parent.joinpath('videos', 'vids', '1.mp4'))

        elif emotion == 2: # Sad animation
            video_path = str(Path(__file__).resolve().parent.joinpath('videos', 'vids', '2.mp4'))

        elif emotion == 3: # Straioght face animation
            video_path = str(Path(__file__).resolve().parent.joinpath('videos', 'vids', '3.mp4'))

        elif emotion == 4: # In love animation
            video_path = str(Path(__file__).resolve().parent.joinpath('videos', 'vids', '4.mp4'))

        elif emotion == 5: # Angry animation
            video_path = str(Path(__file__).resolve().parent.joinpath('videos', 'vids', '5.mp4'))

        elif emotion == 6: # Glorify animation
            video_path = str(Path(__file__).resolve().parent.joinpath('videos', 'vids', '6.mp4'))
                
                
        print('Loading {}...'.format(video_path))

        clip = av.open(video_path) # Opens Video file

        for frame in clip.decode(video=0):
            print('{} ------'.format(frame.index))
            img = frame.to_image()
            if img.width != self.device.width or img.height != self.device.height:
                # resize video to fit device
                size = self.device.width, self.device.height 
                img = img.resize(size, Image.Resampling.LANCZOS)
            self.device.display(img.convert(self.device.mode)) # Display video
            

     #   background = Image.new("RGB", device.size, "white")
      #  background.paste(logo1, (0,0))
       # device.display(background.convert(device.mode))


oled = oledController()
client = mqtt.Client('client_3')
client.connect('0.0.0.0', port=1883, keepalive=60, bind_address="")
client.subscribe('emotion')
client.on_message = oled.showEmotion
client.loop_start()

while True:
    pass

