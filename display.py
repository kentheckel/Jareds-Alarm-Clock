from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd4in2_V2


class DisplayManager:
    def __init__(self):
        self.epd = epd4in2_V2.EPD()
        self.epd.init()
        self.font_large = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 60)
        self.font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24)

    def update_time(self, current_time):
        image = Image.new('1', (self.epd.width, self.epd.height), 255)
        draw = ImageDraw.Draw(image)
        draw.text((10, 10), current_time.strftime("%H:%M"), font=self.font_large, fill=0)
        self.epd.display(image)

    def update_alarms(self, alarms):
        image = Image.new('1', (self.epd.width, self.epd.height), 255)
        draw = ImageDraw.Draw(image)
        draw.text((10, 10), datetime.now().strftime("%H:%M"), font=self.font_large, fill=0)
        y_offset = 80
        for alarm in alarms:
            draw.text((10, y_offset), alarm, font=self.font_small, fill=0)
            y_offset += 30
        self.epd.display(image)

    def show_menu(self):
        pass  # To be implemented

    def handle_menu_selection(self, selection, dial, alarms):
        pass  # To be implemented
