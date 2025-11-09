import os
import time
from TENSTAR_st7789v import ST7789V

# Set a valid font path
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
if not os.path.exists(font_path):
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"  # fallback

# Initialize display
lcd = ST7789V(rotation=0)

# Clear screen
lcd.clear()

# Scroll horizontally
lcd.draw_text(
    "Scrolling horizontally across the screen...",
    font_path=font_path,
    font_size=36,
    align="center",
    auto_fit=True,
    scroll=True,
    scroll_direction="horizontal",
    scroll_speed=0.01
)

time.sleep(1)

# Scroll vertically
lcd.draw_text(
    "Vertical scroll\nLine 2\nLine 3",
    font_path=font_path,
    font_size=36,
    align="center",
    auto_fit=True,
    scroll=True,
    scroll_direction="vertical",
    scroll_speed=0.01
)

time.sleep(1)

# Cleanup
lcd.clear()
lcd.close()
