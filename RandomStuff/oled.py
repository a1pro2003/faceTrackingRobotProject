from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, ws0010

# rev.1 users set port=0
# substitute spi(device=0, port=0) below if using that interface
# substitute bitbang_6800(RS=7, E=8, PINS=[25,24,23,27]) below if using that interface
serial = i2c(port=1, address=0x3C)

# substitute ssd1331(...) or sh1106(...) below if using that device
device = ssd1306(serial, rotate=0)

with canvas(device) as draw:
    # 128 x 54
    draw.rectangle(device.bounding_box, outline="red", fill="red")
    draw.text((30, 40), "Hello World", fill="black")
    draw.text((30, 30), "Hello World", fill="white")
    draw.text((30, 20), "Hello World", fill="white")