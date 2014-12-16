__author__ = 'Edilio'

import os


def get_font_path():
    windows_font = "C:/Windows/Fonts/"
    linux_font = "/usr/share/fonts/truetype/"
    mac = "/Library/Fonts"

    path = windows_font if os.name == 'nt' else linux_font
    if os.path.isdir(path):
        return path
    else:
        return mac

font_path = get_font_path()
print font_path

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import StringIO

filter_dict = {
    'BLUR': ImageFilter.BLUR,
    'CONTOUR': ImageFilter.CONTOUR,
    'DETAIL': ImageFilter.DETAIL,
    'EDGE_ENHANCE': ImageFilter.EDGE_ENHANCE,
    'EDGE_ENHANCE_MORE': ImageFilter.EDGE_ENHANCE_MORE,
    'EMBOSS': ImageFilter.EMBOSS,
    'FIND_EDGES': ImageFilter.FIND_EDGES,
    'SMOOTH': ImageFilter.SMOOTH,
    'SMOOTH_MORE': ImageFilter.SMOOTH_MORE,
    'SHARPEN': ImageFilter.SHARPEN
}


def get_font_full_path(font_dir, font_name):
    ext = '.TTF' if font_name.upper() == font_name else ".ttf"
    return font_dir + font_name + ext


def create_image(font_name, font_size, font_color, width, height, back_ground_color, text,
                 img_type="JPEG", image_filter=None):

    font_full_path = get_font_full_path(font_path, font_name)
    font = ImageFont.truetype(font_full_path, font_size)

    im = Image.new("RGB", (width, height), back_ground_color)
    draw = ImageDraw.Draw(im)
    text_x, text_y = font.getsize(text)
    x = (width - text_x)/2
    y = (height - text_y)/2
    draw.text((x, y), text, font=font, fill=font_color)

    if image_filter:
        real_filter = filter_dict[image_filter]
        im = im.filter(real_filter)
#    im.save ( "runaway_emboss.jpg" )

    output = StringIO.StringIO()
    im.save(output, format=img_type)
    contents = output.getvalue()
    output.close()
    return contents


if __file__ == 'main':
    #print create_image('BOOKOSBI', 26, "#949494", 200, 200, "#f1f1f1","JED Utils", 'DETAIL')
    create_image('BOOKOSBI', 26, "#949494", 200, 200, "#ebebeb","JED Utils", 'DETAIL')