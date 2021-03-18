from PIL import Image, ImageDraw, ImageFont
import os


# Сделай выполнение алгоритма в отдельном потоке и добавь start файл
# Заполнение до конца строки полупрозрачными буквами
# Доавить предупреждение при создании без выбранного шрифта
# Не все шрифты грузятся (Сделай так, что если программа долго ничего не выдает, то пользователю об этом говорят)
# Пользователю говорят о создании прописи, если он выбрал не открывать её после создания

def make_prescription(font_name, lang, save_path, open_):
    print('hey')
    f_path = os.path.join("base fonts", font_name)

    sheet_size = (2480, 3508)
    up_margin = 190
    bottom_margin = 50
    line_width = 2
    letter_min_size = 75
    letters_sets = {
        "eng": "abcdefghijklmnopqrstuvwxyz",
        "rus": "абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
    }

    letters = letters_sets[lang]
    x = 20
    while True:
        font = ImageFont.truetype(f_path, x)
        lines_height = {}
        max_descender = 0
        for ur in letters.upper():
            box = font.getbbox(ur, anchor='ls')
            lines_height[ur] = abs(box[1]) + 1
            max_descender = max(box[3] - 1, max_descender)
        if all([i >= letter_min_size for i in lines_height.values()]):
            lines_height['space'] = max(max_descender, max(lines_height.values()))
            break
        else:
            x += 1

    font = ImageFont.truetype(f_path, x)
    y = 0
    sheets = []
    for ll, ul in zip(letters.lower(), letters.upper()):
        if (y + lines_height[ul] + line_width + bottom_margin) >= sheet_size[1] or y == 0:
            im = Image.new('RGB', sheet_size, 'white')
            sheets.append(im)
            drawer = ImageDraw.Draw(im)
            y = up_margin - 1
        drawer.line(((0, y), (sheet_size[0] - 1, y)), 'black', line_width)
        y += line_width // 2
        y += lines_height[ul]
        drawer.text((10, y), ul + ' ' + ll, 'black', font, anchor='ls')
        drawer.line(((0, y), (sheet_size[0] - 1, y)), 'black', line_width)
        y += line_width // 2
        y += lines_height['space']

    sheets[0].save(save_path, save_all=True, append_images=sheets[1:])
    if open_:
        os.startfile(save_path)


if __name__ == "__main__":
    language = 'eng'
    font_ = 'Teacher_Sez_by_smartalecvt.ttf'
    path = 'prescription.pdf'
    ope = True
    make_prescription(font_name=font_, lang=language, save_path=path, open_=True)
