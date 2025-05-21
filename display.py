from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd4in2_V2

class DisplayManager:
    def __init__(self):
        # Initialize display
        self.epd = epd4in2_V2.EPD()
        self.epd.init()
        self.epd.Clear()

        # Font setup - all lowercase
        self.font_large = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 60)
        self.font_medium = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 36)
        self.font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24)

        # Prepare for clock font customization
        self.clock_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 110)  # Large for clock face

        # Mode management
        self.modes = ["clock", "alarm", "sounds", "wifi", "brightness", "hours", "fonts"]
        self.current_mode_index = 0
        self.current_mode = self.modes[self.current_mode_index]

    def cycle_mode(self):
        """Cycle to the next mode"""
        self.current_mode_index = (self.current_mode_index + 1) % len(self.modes)
        self.current_mode = self.modes[self.current_mode_index]
        self.epd.init()  # Reinitialize display for clean refresh
        self.epd.Clear()

    def update_display(self, hour_format="24", alarms=[]):
        """Update the display based on current mode"""
        self.epd.init()
        image = Image.new('1', (self.epd.width, self.epd.height), 255)
        draw = ImageDraw.Draw(image)

        # Only draw mode indicator if not in clock mode
        if self.current_mode != "clock":
            draw.text((10, 10), self.current_mode, font=self.font_small, fill=0)

        if self.current_mode == "clock":
            self._draw_clock(draw, hour_format, alarms)
        elif self.current_mode == "alarm":
            self._draw_alarm_menu(draw, alarms)
        elif self.current_mode == "sounds":
            self._draw_sounds_menu(draw)
        elif self.current_mode == "wifi":
            self._draw_wifi_menu(draw)
        elif self.current_mode == "brightness":
            self._draw_brightness_menu(draw)
        elif self.current_mode == "hours":
            self._draw_hours_menu(draw, hour_format)
        elif self.current_mode == "fonts":
            self._draw_fonts_menu(draw)

        self.epd.display(self.epd.getbuffer(image))

    def _draw_clock(self, draw, hour_format, alarms):
        """Draw the main clock display with large time and alarms to the left"""
        now = datetime.now()
        if hour_format == "12":
            time_text = now.strftime("%I:%M %p").lower()
        else:
            time_text = now.strftime("%H:%M")

        # Get size of the clock text using the customizable clock font
        w, h = draw.textsize(time_text, font=self.clock_font)
        x = (self.epd.width - w) // 2
        y = (self.epd.height - h) // 2
        draw.text((x, y), time_text, font=self.clock_font, fill=0)

        # Draw up to 3 alarms, vertically aligned to the left of the clock digits
        alarm_x = x - 10  # 10px padding to the left of the clock
        alarm_y_start = y
        alarm_spacing = self.font_small.getsize("0")[1] + 5  # vertical space between alarms
        for i in range(min(3, len(alarms))):
            alarm_y = alarm_y_start + i * alarm_spacing
            # Only draw if it doesn't extend past the clock text
            if alarm_y + self.font_small.getsize("0")[1] <= y + h:
                draw.text((alarm_x - self.font_small.getsize(alarms[i])[0], alarm_y), alarms[i], font=self.font_small, fill=0)

    def _draw_alarm_menu(self, draw, alarms):
        """Draw the alarm configuration screen"""
        draw.text((10, 60), "alarm 1:", font=self.font_medium, fill=0)
        draw.text((10, 100), "alarm 2:", font=self.font_medium, fill=0)
        draw.text((10, 140), "alarm 3:", font=self.font_medium, fill=0)

        # Draw alarm times if they exist
        for i, alarm in enumerate(alarms[:3]):
            draw.text((120, 60 + i*40), alarm, font=self.font_medium, fill=0)

    def _draw_sounds_menu(self, draw):
        """Draw the sounds configuration screen"""
        draw.text((10, 60), "sound options:", font=self.font_medium, fill=0)
        draw.text((10, 100), "coming soon...", font=self.font_small, fill=0)

    def _draw_wifi_menu(self, draw):
        """Draw the wifi configuration screen"""
        draw.text((10, 60), "wifi settings:", font=self.font_medium, fill=0)
        draw.text((10, 100), "coming soon...", font=self.font_small, fill=0)

    def _draw_brightness_menu(self, draw):
        """Draw the brightness configuration screen"""
        draw.text((10, 60), "brightness:", font=self.font_medium, fill=0)
        draw.text((10, 100), "coming soon...", font=self.font_small, fill=0)

    def _draw_hours_menu(self, draw, hour_format):
        """Draw the hours format configuration screen"""
        draw.text((10, 60), "time format:", font=self.font_medium, fill=0)
        current_format = "12 hour" if hour_format == "12" else "24 hour"
        draw.text((10, 100), current_format, font=self.font_medium, fill=0)

    def _draw_fonts_menu(self, draw):
        """Draw the fonts configuration screen"""
        draw.text((10, 60), "font options:", font=self.font_medium, fill=0)
        draw.text((10, 100), "coming soon...", font=self.font_small, fill=0)
