import spidev
from gpiozero import DigitalOutputDevice
from PIL import Image, ImageDraw, ImageFont
import time
import numpy as np
import random

class ST7789V:
    def __init__(self, width=240, height=320, spi_bus=0, spi_device=0, dc_pin=25, rst_pin=27, bl_pin=18, rotation=0, spi_speed_hz=62500000):
        self.width = width
        self.height = height
        self.rotation = rotation

        self.dc = DigitalOutputDevice(dc_pin)
        self.rst = DigitalOutputDevice(rst_pin)
        self.bl = DigitalOutputDevice(bl_pin)

        self.spi = spidev.SpiDev()
        self.spi.open(spi_bus, spi_device)
        self.spi.max_speed_hz = spi_speed_hz
        self.spi.mode = 0b11

        self._reset()
        self._init_display()
        self.bl.on()

    def _reset(self):
        self.rst.on()
        time.sleep(0.1)
        self.rst.off()
        time.sleep(0.1)
        self.rst.on()
        time.sleep(0.1)

    def _write_command(self, cmd):
        self.dc.off()
        self.spi.writebytes([cmd])

    def _write_data(self, data):
        self.dc.on()
        if isinstance(data, int):
            self.spi.writebytes([data])
        else:
            max_chunk = 2048
            for i in range(0, len(data), max_chunk):
                self.spi.writebytes(data[i:i + max_chunk])

    def _init_display(self):
        self._write_command(0x36)
        rotation_modes = [0x00, 0x60, 0xC0, 0xA0]
        self._write_data(rotation_modes[self.rotation % 4])

        self._write_command(0x3A)
        self._write_data(0x05)

        self._write_command(0xB2)
        self._write_data([0x0C, 0x0C, 0x00, 0x33, 0x33])

        self._write_command(0xB7)
        self._write_data(0x35)

        self._write_command(0xBB)
        self._write_data(0x19)

        self._write_command(0xC0)
        self._write_data(0x2C)

        self._write_command(0xC2)
        self._write_data(0x01)

        self._write_command(0xC3)
        self._write_data(0x12)

        self._write_command(0xC4)
        self._write_data(0x20)

        self._write_command(0xC6)
        self._write_data(0x0F)

        self._write_command(0xD0)
        self._write_data([0xA4, 0xA1])

        self._write_command(0xE0)
        self._write_data([0xD0, 0x08, 0x11, 0x08, 0x0C, 0x15, 0x39, 0x33,
                          0x50, 0x36, 0x13, 0x14, 0x29, 0x2D])

        self._write_command(0xE1)
        self._write_data([0xD0, 0x08, 0x10, 0x08, 0x06, 0x06, 0x39, 0x44,
                          0x51, 0x0B, 0x16, 0x14, 0x2F, 0x31])

        self._write_command(0x21)
        self._write_command(0x11)
        time.sleep(0.12)
        self._write_command(0x29)

    def _set_window(self, x0, y0, x1, y1):
        self._write_command(0x2A)
        self._write_data([x0 >> 8, x0 & 0xFF, x1 >> 8, x1 & 0xFF])
        self._write_command(0x2B)
        self._write_data([y0 >> 8, y0 & 0xFF, y1 >> 8, y1 & 0xFF])
        self._write_command(0x2C)

    def display(self, image: Image.Image):
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image = image.resize((self.width, self.height))

        pixel_data = np.asarray(image).astype(np.uint16)
        pixel565 = (((pixel_data[:, :, 0] & 0xF8) << 8) |
                    ((pixel_data[:, :, 1] & 0xFC) << 3) |
                    (pixel_data[:, :, 2] >> 3))

        pixel_bytes = np.dstack(((pixel565 >> 8) & 0xFF, pixel565 & 0xFF)).flatten().tolist()

        self._set_window(0, 0, self.width - 1, self.height - 1)
        self._write_data(pixel_bytes)

    def clear(self, color=(0, 0, 0)):
        image = Image.new("RGB", (self.width, self.height), color)
        self.display(image)

    def close(self):
        self.spi.close()
        self.dc.close()
        self.rst.close()
        self.bl.close()

    def draw_text(self, text, font_path=None, font_size=24, rotation=0,
              align="center", auto_fit=False, scroll=False,
              scroll_direction="horizontal", scroll_speed=0.05):
        from PIL import ImageFont, ImageDraw, Image
        import os
        import time

        # Load font
        if font_path and os.path.exists(font_path):
            font = ImageFont.truetype(font_path, font_size)
        else:
            font = ImageFont.load_default()

        lines = text.split("\n")
        line_spacing = 4

        # Auto-fit logic
        if auto_fit:
            while font_size > 8:
                font = ImageFont.truetype(font_path, font_size)
                ascent, descent = font.getmetrics()
                line_height = ascent + descent
                total_height = line_height * len(lines) + line_spacing * (len(lines) - 1)

                dummy_img = Image.new("RGB", (1, 1))
                dummy_draw = ImageDraw.Draw(dummy_img)
                widths = [dummy_draw.textbbox((0, 0), line, font=font)[2] for line in lines]
                max_line_width = max(widths)

                if scroll:
                    if scroll_direction == "horizontal":
                        fits = total_height <= self.height
                    else:
                        fits = max_line_width <= self.width
                else:
                    fits = max_line_width <= self.width and total_height <= self.height

                if fits:
                    break
                font_size -= 2

        # Final layout
        ascent, descent = font.getmetrics()
        line_height = ascent + descent
        total_height = line_height * len(lines) + line_spacing * (len(lines) - 1)

        dummy_img = Image.new("RGB", (1, 1))
        dummy_draw = ImageDraw.Draw(dummy_img)
        widths = [dummy_draw.textbbox((0, 0), line, font=font)[2] for line in lines]
        max_line_width = max(widths)

        text_img = Image.new("RGBA", (max_line_width, total_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_img)

        y = 0
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            line_width = bbox[2] - bbox[0]
            if align == "left":
                x = 0
            elif align == "right":
                x = max_line_width - line_width
            else:
                x = (max_line_width - line_width) // 2
            draw.text((x, y), line, font=font, fill=(255, 255, 255))
            y += line_height + line_spacing

        # Rotate text image if needed
        if rotation != 0:
            text_img = text_img.rotate(rotation, expand=True)

        # Scrolling logic
        if scroll:
           scroll_axis = 0 if scroll_direction == "horizontal" else 1
           scroll_size = text_img.size[scroll_axis]
           frame_size = self.width if scroll_axis == 0 else self.height
           start_offset = 0  # Start from center visually

           for offset in range(start_offset, scroll_size - frame_size + 1):
               frame = Image.new("RGB", (self.width, self.height), (0, 0, 0))
               if scroll_axis == 0:
                   x = (self.width - frame_size) // 2
                   y = (self.height - text_img.height) // 2
                   frame.paste(text_img, (-offset + x, y), text_img)
               else:
                   x = (self.width - text_img.width) // 2
                   y = (self.height - frame_size) // 2
                   frame.paste(text_img, (x, -offset + y), text_img)

               if self.rotation == 1:
                   frame = frame.rotate(270, expand=True)
               elif self.rotation == 2:
                   frame = frame.rotate(180, expand=True)
               elif self.rotation == 3:
                   frame = frame.rotate(90, expand=True)
               self.display(frame)
               time.sleep(scroll_speed)
           return
    
        # Static display
        frame = Image.new("RGB", (self.width, self.height), (0, 0, 0))
        x = (self.width - text_img.width) // 2
        y = (self.height - text_img.height) // 2
        frame.paste(text_img, (x, y), text_img)

        if self.rotation == 1:
            frame = frame.rotate(270, expand=True)
        elif self.rotation == 2:
            frame = frame.rotate(180, expand=True)
        elif self.rotation == 3:
            frame = frame.rotate(90, expand=True)

        self.display(frame)

# End of ST7789V class
