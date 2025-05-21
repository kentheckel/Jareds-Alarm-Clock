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

        # Use textbbox (not textsize) for compatibility with Pillow 10+
        bbox = draw.textbbox((0, 0), now, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (epd.width - text_width) // 2
        y = (epd.height - text_height) // 2

        draw.text((x, y), now, font=font, fill=0)

        print("Updating screen:", now)
        epd.display(epd.getbuffer(image))

        time.sleep(60)

if __name__ == "__main__":
    epd = epd4in2_V2.EPD()
    print("Initializing ePaper")
    epd.init()
    epd.Clear()

    try:
        draw_clock(epd)
    except KeyboardInterrupt:
        print("Sleeping screen...")
        epd.sleep()
