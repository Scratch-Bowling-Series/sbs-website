import io
import json
import urllib
from io import BytesIO
from urllib.request import urlopen
from PIL import Image, ImageColor
from bs4 import BeautifulSoup

from oils.models import Oil_Pattern

oil_colors = ['transparent', 'rgb(153,204,255)', '#99ccff', '#0000CD', '#00008B', '#0033ff']

lib = {"Imajlar/imBos.gif": oil_colors[0],
       "Imajlar/imTurkuaz.gif": oil_colors[1],
       "Imajlar/imGradient.jpg": oil_colors[2],
       "Imajlar/imOrtaKoyuMavi.gif": oil_colors[3],
       "Imajlar/imKoyuMavi.gif": oil_colors[4],
       "Imajlar/imOrtaMavi.gif": oil_colors[5]

       }


def update_library(full_update):
    for index in range(510, 902):
        oil_pattern = Oil_Pattern.objects.filter(pattern_db_id=index).first()
        if oil_pattern is None:
            display_data = scrape_oil_display(index)
            if display_data is not None:
                display_data = json.dumps(display_data)
                oil_pattern = Oil_Pattern.create(index)
                oil_pattern.pattern_cache = display_data
                oil_pattern.save()
        print('Updating Library (' + str(index) + '/902)')


def get_oil_colors():
    return oil_colors


def get_gradient_location(color, height, max, count, total):
    scale = height / max
    scale = 100 * scale

    if total is 1: return scale


    if color is oil_colors[1] or color is oil_colors[0]:
        return scale
    elif color is oil_colors[5] and total is 2 and count is 1:
        return scale
    elif color is oil_colors[4] and total is 2 and count is 2:
        return scale
    elif color is oil_colors[4] and total is 3 and count is 3:
        print(100 - scale)
        return 100 - scale
    elif color is oil_colors[5] and total is 3 and count is 2:
        print(100 - scale)
        return 100 - scale


    return scale


def gradient_maker(pattern):
    gradient = []
    count = 0
    total = len(pattern)



    for image in pattern:
        count += 1
        color = image['src']
        height = image['height']
        straight = False
        above = False
        alt_color = None
        mult = 1

        if color in lib:
            color = lib[color]
            scale = get_gradient_location(color, int(height), 120, count, total)
            if color is oil_colors[2] and total is 2 and count is 1:
                straight = True
                alt_color = oil_colors[4]
                mult = 0.35
            if color is oil_colors[5] and total is 2 and count is 1:
                straight = True
                alt_color = oil_colors[4]
                mult = 1
            if color is oil_colors[5] and total is 3 and count is 2:
                straight = True
                alt_color = oil_colors[4]
                mult = 0.99

            if straight:
                if above:

                    grad = alt_color + ' ' + str(scale * mult) + '% ,'
                    gradient.append(grad)
                    grad = color + ' ' + str(scale) + '% ,'
                    gradient.append(grad)

                else:
                    grad = color + ' ' + str(scale * mult) + '% ,'
                    gradient.append(grad)
                    grad = alt_color + ' ' + str(scale) + '% ,'
                    gradient.append(grad)
            else:
                grad = color + ' ' + str(scale) + '% ,'
                gradient.append(grad)

    if len(gradient) < 2:
        gradient.append(gradient[0])
    if len(gradient) > 1:
        gradient[len(gradient) - 1] = gradient[len(gradient) - 1][:-1]
    data = ' '.join(gradient)
    return 'linear-gradient(' + data + ')'


def scrape_oil_display(pattern_id):
    with urlopen('http://patternlibrary.kegel.net/PatternLibraryPatternGraph.aspx?ID=' + str(pattern_id) + '&VIEW=COM') as response:
        soup = BeautifulSoup(response, 'lxml')
        urls = []
        patterns = soup.find_all(class_='clPatternHucre')
        if patterns is not None:
            for pattern in patterns:
                urls.append(gradient_maker_two(pattern.find_all('img')))
        oil_pattern = []
        for x in range(0, 39):
            am = []
            for i in range(0, 7):
                index = 39 * i + x
                am.append(index)
            try:
                color_1 = urls[am[0]]
                color_2 = urls[am[1]]
                color_3 = urls[am[2]]
                color_4 = urls[am[3]]
                color_5 = urls[am[4]]
                color_6 = urls[am[5]]
                color_7 = urls[am[6]]
                color_list = [color_1, color_2, color_3, color_4, color_5, color_6, color_7]
                oil_pattern.append(color_list)
            except IndexError:
                continue
        return oil_pattern


def gradient_maker_two(pattern):
    gradient = []
    count = 0
    cells = []
    for image in pattern:
        count += 1
        color = image['src']
        color = lib[color]
        height = image['height']
        height = int(height)
        cell = DCELL()
        cell.color = color
        cell.position = count
        cell.height = height
        cells.append(cell)

    if count == 1:
        if cells[0].color is oil_colors[2]:
            gradient.append(gradient_create(oil_colors[2], 20))
            gradient.append(gradient_create(oil_colors[4], 100))
        if cells[0].color is oil_colors[1]:
            gradient.append(gradient_create(oil_colors[1], 0))
            gradient.append(gradient_create(oil_colors[1], 100))
        else:
            gradient.append(gradient_create(cells[0].color, 0))
            gradient.append(gradient_create(cells[0].color, 100))
    elif count == 2:
        if cells[0].color is oil_colors[2]:
            if cells[1].color is oil_colors[5]:
                gradient.append(gradient_create(oil_colors[2], scale(0)))
                gradient.append(gradient_create(oil_colors[4], scale(cells[0].height)))
                gradient.append(gradient_create(oil_colors[5], scale(cells[0].height)))
        if cells[0].color is oil_colors[0]:
            if cells[1].color is oil_colors[1]:
                gradient.append(gradient_create(oil_colors[0], 0))
                gradient.append(gradient_create(oil_colors[0], scale(cells[0].height)))
                gradient.append(gradient_create(oil_colors[1], scale(cells[0].height)))
                gradient.append(gradient_create(oil_colors[1], 100))

        if cells[0].color is oil_colors[5]:
            if cells[1].color is oil_colors[4]:
                gradient.append(gradient_create(oil_colors[5], scale(0)))
                gradient.append(gradient_create(oil_colors[5], scale(cells[0].height)))
                gradient.append(gradient_create(oil_colors[4], scale(cells[0].height)))

    elif count == 3:
        if cells[0].color is oil_colors[2]:
            if cells[1].color is oil_colors[5]:
                gradient.append(gradient_create(oil_colors[2], scale(0)))
                gradient.append(gradient_create(oil_colors[4], scale(cells[0].height)))
                gradient.append(gradient_create(oil_colors[5], scale(cells[0].height)))
                gradient.append(gradient_create(oil_colors[5], scale(cells[0].height) + scale(cells[1].height)))
                gradient.append(gradient_create(oil_colors[4], scale(cells[0].height) + scale(cells[1].height)))
                gradient.append(gradient_create(oil_colors[4], 100))

    if len(gradient) > 0:
        gradient[len(gradient) - 1] = gradient[len(gradient) - 1][:-1]
    data = ' '.join(gradient)
    return 'linear-gradient(' + data + ')'


def gradient_create(color, percent):
    return color + ' ' + str(percent) + '% ,'


def scale(value):
    return 100 * (value / 120)


class DCELL:
    position = 0
    color = None
    height = None


def get_color(url):
    img = Image.open(url)
    img = img.convert('RGB')
    try:
        r, g, b = img.getpixel((1, 1))
        return '(' + str(r) + ',' + str(b) + ',' + str(g) + ')'
    except IndexError:
        return None