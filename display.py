import os
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
        self.clock_font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
        self.clock_font = ImageFont.truetype(self.clock_font_path, 110)  # Large for clock face

        # Load all font files from Fonts directory
        self.fonts_dir = os.path.join(os.path.dirname(__file__), 'Fonts')
        self.font_files = [f for f in os.listdir(self.fonts_dir) if f.lower().endswith(('.ttf', '.otf'))]
        self.font_files.sort()
        self.font_preview_size = 38  # Smaller preview size
        self.selected_font_index = 0
        self.font_scroll_offset = 0  # For scrolling the preview list
        self.font_preview_count = 4  # Number of fonts to show at once
        self.font_preview_spacing = 50  # Tighter vertical spacing
        self.font_preview_x = 90  # Shift right to avoid 'fonts' label

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
        """Draw the main clock display with large time and alarm dots underneath, left-aligned with the clock digits"""
        now = datetime.now()
        if hour_format == "12":
            time_text = now.strftime("%I:%M %p").lower()
        else:
            time_text = now.strftime("%H:%M")

        # Get size and position of the clock text using the customizable clock font
        w, h = draw.textsize(time_text, font=self.clock_font)
        x = (self.epd.width - w) // 2
        y = (self.epd.height - h) // 2
        draw.text((x, y), time_text, font=self.clock_font, fill=0)

        # Draw 1-3 dots in the bottom left, left-aligned with the clock digits
        num_dots = min(3, len(alarms))
        if num_dots > 0:
            dot_radius = 4
            dot_spacing = 10
            dot_y = y + h + 18  # 18px below the clock digits
            dot_x_start = x
            for i in range(num_dots):
                dot_x = dot_x_start + i * (dot_radius * 2 + dot_spacing)
                draw.ellipse((dot_x, dot_y, dot_x + dot_radius * 2, dot_y + dot_radius * 2), fill=0)

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
        """Draw the fonts configuration screen with previews and selection (minimalist, no font names)"""
        now = datetime.now()
        time_text = now.strftime("%H:%M")
        # Calculate vertical start for centering previews
        total_height = self.font_preview_count * self.font_preview_spacing
        y_start = (self.epd.height - total_height) // 2
        for i in range(self.font_preview_count):
            font_idx = self.font_scroll_offset + i
            if font_idx >= len(self.font_files):
                break
            font_file = self.font_files[font_idx]
            font_path = os.path.join(self.fonts_dir, font_file)
            try:
                preview_font = ImageFont.truetype(font_path, self.font_preview_size)
            except Exception:
                preview_font = self.font_medium  # fallback if font fails to load
            y = y_start + i * self.font_preview_spacing
            # Highlight selected font
            if font_idx == self.selected_font_index:
                draw.rectangle((self.font_preview_x-10, y-5, self.epd.width-30, y+self.font_preview_size+10), outline=0, width=2)
            # Draw the time in the preview font
            draw.text((self.font_preview_x, y), time_text, font=preview_font, fill=0)
        # No font file names drawn

    # Add methods to handle font menu navigation and selection
    def font_menu_up(self):
        if self.selected_font_index > 0:
            self.selected_font_index -= 1
            if self.selected_font_index < self.font_scroll_offset:
                self.font_scroll_offset -= 1

    def font_menu_down(self):
        if self.selected_font_index < len(self.font_files) - 1:
            self.selected_font_index += 1
            if self.selected_font_index >= self.font_scroll_offset + self.font_preview_count:
                self.font_scroll_offset += 1

    def font_menu_select(self):
        # Set the selected font as the main clock font
        font_file = self.font_files[self.selected_font_index]
        font_path = os.path.join(self.fonts_dir, font_file)
        try:
            self.clock_font_path = font_path
            self.clock_font = ImageFont.truetype(font_path, 110)
        except Exception:
            pass  # fallback to previous font if loading fails
        # After selection, switch back to clock mode
        self.current_mode_index = 0
        self.current_mode = self.modes[self.current_mode_index]

    # ... rest of your menu drawing methods remain unchanged ...
