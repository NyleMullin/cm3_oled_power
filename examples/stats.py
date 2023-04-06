# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-FileCopyrightText: 2017 James DeVito for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!

import time
import subprocess
import math

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306


# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
disp = adafruit_ssd1306.SSD1306_I2C(96, 16, i2c)

# rotate display
disp.rotation = 2

# Clear display.
disp.fill(0)
disp.write_cmd(0x2E)
disp.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = +3
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
#x = 0


# Load default font.
font = ImageFont.load_default()

text = (
    "172.16.136.87"
)
maxwidth, unused = draw.textsize(text, font=font)

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 9)

# Set animation
amplitude = height / 4
offset = height / 2 - 4
velocity = -2
startpos = width

pos = startpos

while True:

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Shell scripts for system monitoring from here:
    # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d' ' -f1"
    IP = subprocess.check_output(cmd, shell=True).decode("utf-8")

    # Write four lines of text.

    #draw.text((x, top + 0), "IP: " + IP, font=font, fill=255)

    # Display image.
    x = pos
    for i, c in enumerate(IP):
        # Stop drawing if off the right side of screen.
        if x > width:
            break
        # Calculate width but skip drawing if off the left side of screen.
        if x < -10:
            char_width, char_height = draw.textsize(c, font=font)
            x += char_width
            continue
        # Calculate offset from sine wave.
        y = offset + math.floor(amplitude * math.sin(x / float(width) * 2.0 * math.pi))
        # Draw text.
        draw.text((x, y), c, font=font, fill=255)
        # Increment x position based on chacacter width.
        char_width, char_height = draw.textsize(c, font=font)
        x += char_width

    # Draw the image buffer.
    disp.image(image)
    disp.show()

    # Move position for next frame.
    pos += velocity
    # Start over if text has scrolled completely off left side of screen.
    if pos < -maxwidth:
        pos = startpos

    # Pause briefly before drawing next frame.
    time.sleep(0.05)
