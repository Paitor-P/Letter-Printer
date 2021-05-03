import os

from PIL import Image, ImageDraw, ImageFont

# Заполнение до конца строки полупрозрачными буквами
# Пользователю говорят о создании прописи, если он выбрал не открывать её после создания
# Отображение создания прописи
# Растояние меду "слогами" в строке должно быть больше ширины самого "слога", но таким,
# чтобы последняя буква была максимально близко к краю страницы (Не вплотную, чтобы было красиво)

SHEET_SIZE = (2480, 3508)
UP_MARGIN = 180
BOTTOM_MARGIN = 50
LINE_THICKNESS = 2
LETTER_MIN_SIZE = 75
LETTER_SETS = {
    "eng": "abcdefghijklmnopqrstuvwxyz",
    "rus": "абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
}


def make_prescription(font_name, lang, save_path):
    f_path = os.path.join("base fonts", font_name)
    letters = LETTER_SETS[lang]
    font_size = get_font_size(letters, f_path, LETTER_MIN_SIZE)
    font = ImageFont.truetype(f_path, font_size)
    lines_height = get_alphabet_heights(letters, font)
    y = 0
    sheets = []
    for ll, ul in zip(letters.lower(), letters.upper()):
        if (y + lines_height[ul] + LINE_THICKNESS + BOTTOM_MARGIN) >= SHEET_SIZE[1] or y == 0:
            im = Image.new('RGB', SHEET_SIZE, 'white')
            sheets.append(im)
            drawer = ImageDraw.Draw(im)
            y = UP_MARGIN - 1
        drawer.line(((0, y), (SHEET_SIZE[0] - 1, y)), 'black', LINE_THICKNESS)
        y += LINE_THICKNESS // 2
        y += lines_height[ul]
        drawer.text((10, y), ul + ' ' + ll, 'black', font, anchor='ls')
        drawer.line(((0, y), (SHEET_SIZE[0] - 1, y)), 'black', LINE_THICKNESS)
        y += LINE_THICKNESS // 2
        y += lines_height['space']

    sheets[0].save(save_path, save_all=True, append_images=sheets[1:])


def get_font_size(letters, font_path, min_size, start_size=20, index_=0):
    """Функция возвращает размер буквы в пунктах (для фнкции truetype),
     при которой буква фактически будет больше given_px_size"""
    while True:
        font = ImageFont.truetype(font_path, start_size)
        letter_size = abs(font.getbbox(letters[index_].upper(), anchor='ls')[1]) + 1
        if letter_size >= min_size:
            break
        else:
            start_size += 1
    index_ += 1
    if index_ > len(letters) - 1:
        return start_size
    else:
        return get_font_size(letters, font_path, min_size, start_size=start_size, index_=index_)


def get_alphabet_heights(letters, font: ImageFont.FreeTypeFont) -> dict:
    alphabet = {'space': 0}
    for i in letters.upper():
        box = font.getbbox(i, anchor='ls')
        alphabet[i] = abs(box[1]) + 1
        alphabet['space'] = max(box[3] - 1, alphabet['space'])
    alphabet['space'] += round(SHEET_SIZE[1] * 0.0171)
    return alphabet


if __name__ == "__main__":
    language = 'eng'
    font_ = 'Teacher_Sez_by_smartalecvt.ttf'
    path = 'prescription.pdf'
    make_prescription(font_name=font_, lang=language, save_path=path)
    os.startfile(path)
