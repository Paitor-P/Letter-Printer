from PIL import Image, ImageDraw, ImageFont
from string import ascii_lowercase, ascii_uppercase
import timeit

"""input"""
lang = 'eng'
f_name = r'D:\Документы\Программы на Python\Letter Printer 2.1\base fonts\ofont.ru_Nexa Script.ttf'

PDF_SIZE = (2480, 3508)
UP_MARGIN = 120
BOTTOM_MARGIN = 70
LINE_WIDTH = 2

x = 20
while True:
    font = ImageFont.truetype(f_name, x)
    sum_size = 0
    max_size = 0
    for lr, ur in zip(ascii_lowercase[:23], ascii_uppercase[:23]):
        ur_s = abs(font.getbbox(ur, anchor='ls')[1]) + 1
        max_size = max(max_size, ur_s)
        sum_size += ur_s
    if sum_size + max_size * 22 + UP_MARGIN + BOTTOM_MARGIN + LINE_WIDTH * 23 + 2 * 23 >= PDF_SIZE[1]:
        x -= 1
        font = ImageFont.truetype(f_name, x)
        letters = {i: abs(font.getbbox(ur, anchor='ls')[1]) + 1 for i in ascii_uppercase}
        letters['space'] = max_size
        break
    else:
        x += 1

im = Image.new('RGB', PDF_SIZE, 'pink')
drawer = ImageDraw.Draw(im)
font = ImageFont.truetype(f_name, x)

y = UP_MARGIN - 1
for ll, ul in zip(ascii_lowercase[:23], ascii_uppercase[:23]):
    drawer.line(((0, y), (PDF_SIZE[0] - 1, y)), 'black', LINE_WIDTH)
    y += LINE_WIDTH // 2
    y += letters[ul]
    drawer.text((10, y), ul + ' ' + ll, 'black', font, anchor='ls')
    drawer.line(((0, y), (PDF_SIZE[0] - 1, y)), 'black', LINE_WIDTH)
    y += LINE_WIDTH // 2
    y += letters['space']
drawer.line(((20, im.height - BOTTOM_MARGIN - 1), (20, im.height - 1)), 'blue', 1)
im.show()
