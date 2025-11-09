from TENSTAR_st7789v import ST7789V
import time
import os

# Font path
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
if not os.path.exists(font_path):
    font_path = None  # fallback to default

# Initialize display (rotation=0 means 90° clockwise)
lcd = ST7789V(rotation=0)

# Clear screen
lcd.clear()

# Display centered text
lcd.draw_text(
    "Hello, World!",
    font_path=font_path,
    font_size=28,
    align="center",
    auto_fit=True,
    rotation=0  # no extra rotation inside the image
)

# Hold for 5 seconds
time.sleep(5)
lcd.clear()
lcd.close()
