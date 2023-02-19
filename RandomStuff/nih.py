
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Display the Raspberry Pi logo (loads image as .png).
"""

from pathlib import Path
from demo_opts import get_device
from PIL import Image
import time
from luma.core.sprite_system import framerate_regulator
from PIL import Image, ImageSequence

try:
    import av
except ImportError:
    print("The pyav library could not be found. Install it using 'sudo -H pip install av'.")
    sys.exit()

vid = 1

def main():
    #For pictures
    global vid
    #regulator = framerate_regulator(fps=10)
    #img_path1 = str(Path(__file__).resolve().parent.joinpath('1.png'))
    #logo1 = Image.open(img_path1).transform(device.size, Image.Transform.AFFINE, (1, 0, 0, 0, 1, 0), Image.Resampling.BILINEAR).convert("RGB")
    while True:
 #       background = Image.new("RGB", device.size, "white")
  #      background.paste(logo1, (0,0))
   #     device.display(background.convert(device.mode))
    #    time.sleep(3)


    #For videos
        if vid == 1:  
            video_path = str(Path(__file__).resolve().parent.joinpath('a', '1.mp4'))
            vid = 2
        elif vid == 2:
            video_path = str(Path(__file__).resolve().parent.joinpath('a', '2.mp4'))
            vid = 3
        elif vid == 3:
            video_path = str(Path(__file__).resolve().parent.joinpath('a', '3.mp4'))
            vid = 4
        elif vid == 4:
            video_path = str(Path(__file__).resolve().parent.joinpath('a', '4.mp4'))
            vid = 5
        elif vid == 5:
            video_path = str(Path(__file__).resolve().parent.joinpath('a', '5.mp4'))
            vid = 1
        elif vid == 2:
            video_path = str(Path(__file__).resolve().parent.joinpath('a', '2.mp4'))
            vid = 3
            
            
        print('Loading {}...'.format(video_path))

        clip = av.open(video_path)

        for frame in clip.decode(video=0):
            print('{} ------'.format(frame.index))
            img = frame.to_image()
            if img.width != device.width or img.height != device.height:
            # resize video to fit device
                size = device.width, device.height 
                img = img.resize(size, Image.Resampling.LANCZOS)
    
            device.display(img.convert(device.mode))


 #   background = Image.new("RGB", device.size, "white")
  #  background.paste(logo1, (0,0))
   # device.display(background.convert(device.mode))
        time.sleep(2)



if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
