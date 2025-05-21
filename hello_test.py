from waveshare_epd import epd4in2_V2
from PIL import Image, ImageDraw, ImageFont

epd = epd4in2_V2.EPD()
epd.init()
epd.Clear()

image = Image.new('1', (epd.width, epd.height), 255)
draw = ImageDraw.Draw(image)
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 60)

draw.text((50, 100), "HELLO", font=font, fill=0)

print("Displaying HELLO...")
epd.display(epd.getbuffer(image))
epd.sleep()
