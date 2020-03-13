#!/usr/bin/env python
import requests
import colorsys
import time
import datetime
import json
from sys import exit

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    exit('This script requires the pillow module\nInstall with: sudo pip install pillow')

import unicornhathd as unicorn


print("""Unicorn HAT HD: Text

This example shows how to draw, display and scroll text in a regular TrueType font on Unicorn HAT HD.

It uses the Python Pillow/PIL image library, and all other drawing functions are available.

See: http://pillow.readthedocs.io/en/3.1.x/reference/

""")


def fullLine(start, row):
    for x in range(start, start+3):
        unicorn.set_pixel(x, row, 255, 255, 255)

def bothSides(start, row):
    unicorn.set_pixel(start, row, 255, 255, 255)
    unicorn.set_pixel(start+2, row, 255, 255, 255)

def leftSide(start, row):
    unicorn.set_pixel(start, row, 255, 255, 255)

def rightSide(start, row):
    unicorn.set_pixel(start+2, row, 255, 255, 255)
  
def bigbothSides(start, row):
    unicorn.set_pixel(start, row, 255, 255, 255)
    unicorn.set_pixel(start+3, row, 255, 255, 255)

# Numbers
def displayZero(x, y):
    #clearNumberPixels(x, y)
    fullLine(x, y)
    bothSides(x, y+1)
    bothSides(x, y+2)
    bothSides(x, y+3)
    fullLine(x, y+4)
    unicorn.show()

def displayOne(x, y):
    #clearNumberPixels(x, y)
    leftSide(x, y)
    leftSide(x, y+1)
    leftSide(x, y+2)
    leftSide(x, y+3)
    leftSide(x, y+4)
    unicorn.show()

def displayTwo(x, y):
    #clearNumberPixels(x, y)
    fullLine(x, y)
    leftSide(x, y+1)
    fullLine(x, y+2)
    rightSide(x, y+3)
    fullLine(x, y+4)
    unicorn.show()

def displayThree(x, y):
    #clearNumberPixels(x, y)
    fullLine(x, y)
    leftSide(x, y+1)
    fullLine(x, y+2)
    leftSide(x, y+3)
    fullLine(x, y+4)
    unicorn.show()

def displayFour(x, y):
    #clearNumberPixels(x, y)
    bothSides(x, y)
    bothSides(x, y+1)
    fullLine(x, y+2)
    leftSide(x, y+3)
    leftSide(x, y+4)
    unicorn.show()

def displayFive(x, y):
    #clearNumberPixels(x, y)
    fullLine(x, y)
    rightSide(x, y+1)
    fullLine(x, y+2)
    leftSide(x, y+3)
    fullLine(x, y+4)
    unicorn.show()

def displaySix(x, y):
    #clearNumberPixels(x, y)
    fullLine(x, y)
    rightSide(x, y+1)
    fullLine(x, y+2)
    bothSides(x, y+3)
    fullLine(x, y+4)
    unicorn.show()

def displaySeven(x, y):
    #clearNumberPixels(x, y)
    fullLine(x, y)
    leftSide(x, y+1)
    leftSide(x, y+2)
    leftSide(x, y+3)
    leftSide(x, y+4)
    unicorn.show()

def displayEight(x, y):
    #clearNumberPixels(x, y)
    fullLine(x, y)
    bothSides(x, y+1)
    fullLine(x, y+2)
    bothSides(x, y+3)
    fullLine(x, y+4)
    unicorn.show()

def displayNine(x, y):
    #clearNumberPixels(x, y)
    fullLine(x, y)
    bothSides(x, y+1)
    fullLine(x, y+2)
    leftSide(x, y+3)
    fullLine(x, y+4)
    unicorn.show()


def displayNumber(x,y, number):
    if number == 0:
        displayZero(x,y)
    elif number == 1:
        displayOne(x,y)
    elif number == 2:
        displayTwo(x,y)
    elif number == 3:
        displayThree(x,y)
    elif number == 4:
        displayFour(x,y)
    elif number == 5:
        displayFive(x,y)
    elif number == 6:
        displaySix(x,y)
    elif number == 7:
        displaySeven(x,y)
    elif number == 8:
        displayEight(x,y)
    elif number == 9:
        displayNine(x,y)

def displayTimeDots(x, y):
    unicorn.set_pixel(x, y-1, 255, 0, 0)
    unicorn.set_pixel(x, y-3, 255, 0, 0)
    unicorn.show()
def clearNumberPixels():
    for y1 in range(8, 15):
        for x1 in range(0,16):
            unicorn.set_pixel(x1, y1, 0, 0, 0)
    unicorn.show()
# ========== Change the text you want to display, and font, here ================

TEXT = 'Hello World!'

FONT = ('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 8)
TIME_FONT = ('/usr/share/fonts/truetype/freefont/FreeMono.ttf', 7)

# Use `fc-list` to show a list of installed fonts on your system,
# or `ls /usr/share/fonts/` and explore.

# sudo apt install fonts-droid
# FONT = ('/usr/share/fonts/truetype/droid/DroidSans.ttf', 12)

# sudo apt install fonts-roboto
# FONT = ('/usr/share/fonts/truetype/roboto/Roboto-Bold.ttf', 10)

# ================ Now, let's draw some amazing rainbowy text! ===================

# Get the width/height of Unicorn HAT HD.
# These will normally be 16x16 but it's good practise not to hard-code such numbers,
# just in case you want to try and hack together a bigger display later.
width, height = unicorn.get_shape()

height = height//2

unicorn.rotation(0)
unicorn.brightness(1)

# We want to draw our text 1 pixel in, and 2 pixels down from the top left corner
text_x = 0
text_y = -2
r = 255
g = 255
b = 255
# Grab our font file and size as defined at the top of the script
font_file, font_size = FONT
time_font_file, time_font_size = TIME_FONT
# Load the font using PIL's ImageFont
font = ImageFont.truetype(font_file, font_size)
time_font = ImageFont.truetype(time_font_file, time_font_size) 
# Ask the loaded font how big our text will be
text_width, text_height = font.getsize(TEXT)

# Make sure we accommodate enough width to account for our text_x left offset
text_width += width + text_x
# text_width = width
# Now let's create a blank canvas wide enough to accomodate our text
image = Image.new('RGB', (text_width, max(height, text_height)), (0, 0, 0))

# To draw on our image, we must use PIL's ImageDraw
draw = ImageDraw.Draw(image)

# And now we can draw text at our desited (text_x, text_y) offset, using our loaded font
draw.text((text_x, text_y), TEXT, fill=(255, 255, 255), font=font)

# To give an appearance of scrolling text, we move a 16x16 "window" across the image we generated above
# The value "scroll" denotes how far this window is from the left of the image.
# Since the window is "width" pixels wide (16 for UHHD) and we don't want it to run off the end of the,
# image, we subtract "width".
last_time = int(0)
r = None
new_text = ''
old_time = ''
try:
    while True:
        try:
            # timer rest call
            cur_time = int(round(time.time() * 1000))
            if cur_time >= last_time + 1000:
                #print(requests.get('http://localhost/api/trip/state'))
                response = requests.get('http://localhost/api/trip/state')
                #print(response.json()[0])
                #print(type(response.json()[0]))
                r = json.loads(response.json()[0])            
                last_time = cur_time
            # redefine text, text_width 
            #print(r['status'])
            if r['status'] == 'FINISHED':
                new_text = 'FINISHED'
            else:
                dnow = datetime.datetime.now() - datetime.timedelta(hours=2)
                s = r['stops'][0]
                if s['Status'] == 'ARRIVED':
                    route = r['route'].split(',')
                    next_port = route[route.index(s['Stop']) + 1]
                    new_text = 'Departing to ' + next_port + ' in... '
                    dstop = datetime.datetime.strptime(s['DepartureTime'],'%Y-%m-%d %H:%M:%S')
                    ddiff = dstop - dnow
                    #new_time = dstop - dnow
                if s['Status'] == 'ON-THE-WAY':
                    next_port = s['Stop']
                    new_text = 'Arriving to ' + next_port + ' in...'
                    darr = datetime.datetime.strptime(s['ArrivalTime'],'%Y-%m-%d %H:%M:%S')
                    ddiff = darr - dnow
                new_time = '{:02d}:{:02d}'.format((ddiff.seconds // 3600) % 3600, (ddiff.seconds // 60) % 60)
                #print(new_time)
        except Exception:
            new_text = 'Connection error...'
            new_time = '00:00'
        # Ask the loaded font how big our text will be
        text_width, text_height = font.getsize(new_text)
        # Make sure we accommodate enough width to account for our text_x left offset
        text_width += width + text_x
        # text_width = width
        # Now let's create a blank canvas wide enough to accomodate our text
        image = Image.new('RGB', (text_width, max(height, text_height)), (0, 0, 0))

        # To draw on our image, we must use PIL's ImageDraw
        draw = ImageDraw.Draw(image)

        # And now we can draw text at our desited (text_x, text_y) offset, using our loaded font
        draw.text((text_x, text_y), new_text, fill=(255, 255, 255), font=font)
    
#         time_width, time_height = font.getsize(new_time)
#         #time_width += width + 0 #TODO check
#         time_img = Image.new('RGB', (time_width, time_height), (0,0,0))
#         draw = ImageDraw.Draw(time_img)
#         draw.text((text_x, 1), new_time, fill=(255, 255, 255), font=time_font)
#         #time_img.save('test.jpg')
        if new_time != old_time:
            clearNumberPixels()
            xoff = 0
            for c in new_time[5::-1]:
                if c == ':':
                    displayTimeDots(8,13)
                    xoff +=1
                else:
                    displayNumber(xoff,9,int(c))
                    xoff +=4
        old_time = new_time
           
        for scroll in range(text_width - width):
            for x in range(width):

                # Figure out what hue value we want at this point.
                # "x" is the position of the pixel on Unicorn HAT HD from 0 to 15
                # "scroll" is how far offset from the left of our text image we are
                # We want the text to be a complete cycle around the hue in the HSV colour space
                # so we divide the pixel's position (x + scroll) by the total width of the text
                # If this pixel were half way through the text, it would result in the number 0.5 (180 degrees)
                #hue = (x + scroll) / float(text_width)
                hue = 1
                # Now we need to convert our "hue" value into r,g,b since that's what colour space our
                # image is in, and also what Unicorn HAT HD understands.
                # This list comprehension is just a tidy way of converting the range 0.0 to 1.0
                # that hsv_to_rgb returns into integers in the range 0-255.
                # hsv_to_rgb returns a tuple of (r, g, b)
                br, bg, bb = [int(n * 255) for n in colorsys.hsv_to_rgb(hue, 1.0, 1.0)]

                # Since our rainbow runs from left to right along the x axis, we can calculate it once
                # for every vertical line on the display, and then re-use that value 16 times below:
#                 for y in range(height,2*height):
#                     pix = time_img.getpixel((x,y - height))
#                     print(pix)
#                     
#                     #sleep(5)
#                     r, g, b = pix #[float(n / 255.0) for n in pix]
#                     
#                     unicorn.set_pixel(width - 1 - x, y, r,g,b)
#                     
#                     #unicorn.set_pixel(0,15,255,255,255)
#                     #unicorn.set_pixel(15,15,0,255,0)
#                      
                    
                for y in range(height):
                    # Get the r, g, b colour triplet from pixel x,y of our text image
                    # Our text is white on a black background, so these will all be shades of black/grey/white
                    # ie 255,255,255 or 0,0,0 or 128,128,128
                    pixel = image.getpixel((x + scroll, y))
                    #print(pixel)
                    # Now we want to turn the colour of our text - shades of grey remember - into a mask for our rainbow.
                    # We do this by dividing it by 255, which converts it to the range 0.0 to 1.0
                    r, g, b = [float(n / 255.0) for n in pixel]

                    # We can now use our 0.0 to 1.0 range to scale our three colour values, controlling the amount
                    # of rainbow that gets blended in.
                    # 0.0 would blend no rainbow
                    # 1.0 would blend 100% rainbow
                    # and anything in between would copy the anti-aliased edges from our text
                    r = int(br * r)
                    g = int(bg * g)
                    b = int(bb * b)

                    # Finally we colour in our finished pixel on Unicorn HAT HD
                    unicorn.set_pixel(width - 1 - x, y, r, g, b)
            # clock setup
            
            
            # Finally, for each step in our scroll, we show the result on Unicorn HAT HD
            unicorn.show()

            # And sleep for a little bit, so it doesn't scroll too quickly!
            time.sleep(0.03)

except KeyboardInterrupt:
    unicorn.off()
