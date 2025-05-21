from waveshare_epd import epd4in2_V2
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import time

def draw_clock(epd):
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 80)

    while True:
        now = datetime.now().strftime("%H:%M")
        image = Image.new('1', (epd.width, epd.height), 255)
        draw = ImageDraw.Draw(image)

        text_width, _ = draw.textsize(now, font=font)
        x = (epd.width - text_width) // 2
        y = (epd.height - 80) // 2

        draw.text((x, y), now, font=font, fill=0)
        epd.display(epd.getbuffer(image))

        time.sleep(60)

if __name__ == "__main__":
    epd = epd4in2_V2.EPD()
    epd.init()
    epd.Clear()
    draw_clock(epd)
