from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd4in2_V2

class DisplayManager:
    def __init__(self):
        self.epd = epd4in2_V2.EPD()
        self.epd.init()
        self.epd.Clear()

        self.font_large = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 60)
        self.font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24)
        self.menu_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 20)

        self.menu_items = ["Alarm", "Sounds", "Wifi", "Brightness", "Hours", "Font"]
        self.selected_index = 0
        self.arrow_x = self.epd.width - 20
        self.menu_y_start = 10
        self.line_height = 25

        self.in_menu_mode = False  # <-- ADD THIS LINE


    def update_clock(self, hour_format="24", alarms=[]):
        self.epd.init()
        image = Image.new('1', (self.epd.width, self.epd.height), 255)
        draw = ImageDraw.Draw(image)

        now = datetime.now()
        if hour_format == "12":
            time_text = now.strftime("%I:%M %p")
        else:
            time_text = now.strftime("%H:%M")

        w, h = draw.textsize(time_text, font=self.font_large)
        x = (self.epd.width - w) // 2
        y = 20
        draw.text((x, y), time_text, font=self.font_large, fill=0)

        # Draw up to 3 alarms
        if len(alarms) >= 1:
            draw.text((10, 120), alarms[0], font=self.font_small, fill=0)
        if len(alarms) >= 2:
            w2, _ = draw.textsize(alarms[1], font=self.font_small)
            draw.text(((self.epd.width - w2)//2, 120), alarms[1], font=self.font_small, fill=0)
        if len(alarms) >= 3:
            w3, _ = draw.textsize(alarms[2], font=self.font_small)
            draw.text((self.epd.width - w3 - 10, 120), alarms[2], font=self.font_small, fill=0)

        self.epd.display(self.epd.getbuffer(image))

    def draw_static_menu(self):
        if not self.in_menu_mode:
            self.epd.init()
            self.epd.Clear()
            self.epd.init_fast()
            self.in_menu_mode = True

        image = Image.new('1', (self.epd.width, self.epd.height), 255)
        draw = ImageDraw.Draw(image)

        for i, item in enumerate(self.menu_items):
            y = self.menu_y_start + i * self.line_height
            draw.text((10, y), item, font=self.menu_font, fill=0)

        self.epd.display(self.epd.getbuffer(image))
        self.draw_arrow(self.selected_index)


    def draw_arrow(self, index):
        image = Image.new('1', (self.epd.width, self.epd.height), 255)
        draw = ImageDraw.Draw(image)
        y = self.menu_y_start + index * self.line_height
        draw.text((self.arrow_x, y), ">", font=self.menu_font, fill=0)
        self.epd.display_Partial(self.epd.getbuffer(image))

    def clear_arrow(self, index):
        image = Image.new('1', (self.epd.width, self.epd.height), 255)
        draw = ImageDraw.Draw(image)
        y = self.menu_y_start + index * self.line_height
        draw.rectangle((self.arrow_x, y, self.arrow_x + 10, y + self.line_height), fill=255)
        self.epd.display_Partial(self.epd.getbuffer(image))

    def update_menu_selection(self, direction):
        prev_index = self.selected_index
        if direction == "up":
            self.selected_index = (self.selected_index - 1) % len(self.menu_items)
        elif direction == "down":
            self.selected_index = (self.selected_index + 1) % len(self.menu_items)

        if self.selected_index != prev_index:
            self.clear_arrow(prev_index)
            self.draw_arrow(self.selected_index)

    def get_selected_menu_item(self):
        return self.menu_items[self.selected_index]
