from TENSTAR_st7789v import ST7789V
import time

lcd = ST7789V()
font = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
lcd.draw_text("Auto-fit\nCenter", font_path=font, font_size=100, align="center", auto_fit=True, rotation=0)
time.sleep(3)
lcd.clear()
lcd.close()
