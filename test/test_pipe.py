
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from time import sleep

from sys import path
path += ['../papertty']
from pipe_driver import AutoPipeDisplay
from IT8951 import constants

def clear_display(display):
    print('Clearing display...')
    display.clear()

def display_gradient(display):
    print('Displaying gradient...')

    # set frame buffer to gradient
    for i in range(16):
        display.frame_buf.paste(i*0x10, box=(i*display.width//16, 0, (i+1)*display.width//16, display.height))

    # update display
    display.draw_full(constants.DisplayModes.GC16)

def display_image_8bpp(display):
    img_path = '../pics/sleeping_penguin.png'
    print('Displaying "{}"...'.format(img_path))

    # clearing image to white
    display.frame_buf.paste(0xFF, box=(0, 0, display.width, display.height))

    img = Image.open(img_path)

    # TODO: this should be built-in
    dims = (display.width, display.height)

    img.thumbnail(dims)
    paste_coords = [dims[i] - img.size[i] for i in (0,1)]  # align image with bottom of display
    display.frame_buf.paste(img, paste_coords)

    display.draw_full(constants.DisplayModes.GC16)

def place_text(img, text, x_offset=0, y_offset=0):
    '''
    Put some centered text at a location on the image.
    '''
    fontsize = 80

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', fontsize)

    img_width, img_height = img.size
    text_width, _ = font.getsize(text)
    text_height = fontsize

    draw_x = (img_width - text_width)//2 + x_offset
    draw_y = (img_height - text_height)//2 + y_offset

    draw.text((draw_x, draw_y), text, font=font)

def partial_update(display):
    print('Starting partial update...')

    # clear image to white
    display.frame_buf.paste(0xFF, box=(0, 0, display.width, display.height))

    print('  writing full...')
    place_text(display.frame_buf, 'partial', x_offset=-200)
    display.draw_full(constants.DisplayModes.GC16)

    # TODO: should use 1bpp for partial text update
    print('  writing partial...')
    place_text(display.frame_buf, 'update', x_offset=+200)
    display.draw_partial(constants.DisplayModes.DU)

def main():
    print('Initializing...')
    display = AutoPipeDisplay()

    tests = [
        clear_display,
        display_gradient,
        partial_update,
        display_image_8bpp,
    ]

    for t in tests:
        t(display)
        sleep(1)

    print('Done!')

if __name__ == '__main__':
    main()
