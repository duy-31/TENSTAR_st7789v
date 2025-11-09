import os
from TENSTAR_st7789v import ST7789V
import time

# Set a valid font path
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
if not os.path.exists(font_path):
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"  # fallback

lcd = ST7789V()
lcd.draw_text("Line 1\nLine 2\nLine 3", font_path=font_path, font_size=36, align="left", auto_fit=True)
time.sleep(3)
lcd.clear()
lcd.close()
