from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os


def make_prescription(font_path: str, lang, save_path, open_) -> int:
    sheet_size = (2480, 3508)
    up_margin = 190
    bottom_margin = 50
    line_width = 2
    letter_min_size = 75
    all_letters_sets = {
        "eng": "abcdefghijklmnopqrstuvwxyz",
        "rus": "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    }
    small_letters_sets = {  # they have minimum size in the most fonts
        "eng": "acemnv",
        "rus": "агеилс",
    }
    small_letters = small_letters_sets[lang]
    alleged_size = 20
    while alleged_size < sheet_size[1]:
        font = ImageFont.truetype(font_path, alleged_size)
        row_width = sheet_size[1]
        for ltr in small_letters:
            box = font.getbbox(ltr, anchor='ls')
            row_width = min(abs(box[1]) + 1, row_width)
        if row_width >= letter_min_size:
            break
        else:
            alleged_size += 1
    else:
        return -1
    row_gap = 0
    for ltr in all_letters_sets[lang].upper():
        m = font.getbbox(ltr, anchor='ls')
        row_gap = max(abs(m[1]), m[3], row_gap)
    font = ImageFont.truetype(font_path, alleged_size)
    y = 0
    sheets = []
    for ll, ul in zip(all_letters_sets[lang].lower(), all_letters_sets[lang].upper()):
        if (y + row_width + line_width + bottom_margin) >= sheet_size[1] or y == 0:
            im = Image.new('RGB', sheet_size, 'white')
            sheets.append(im)
            drawer = ImageDraw.Draw(im)
            y = up_margin - 1
        # noinspection PyUnboundLocalVariable
        drawer.line(((0, y), (sheet_size[0] - 1, y)), 'black', line_width)
        y += line_width // 2
        y += row_width
        drawer.text((10, y), ul + ' ' + ll, 'black', font, anchor='ls')
        drawer.line(((0, y), (sheet_size[0] - 1, y)), 'black', line_width)
        y += line_width // 2
        y += row_gap

    sheets[0].save(save_path, save_all=True, append_images=sheets[1:])
    if open_:
        os.startfile(save_path)
    return 0


if __name__ == "__main__":
    for ffff in Path('base fonts').iterdir():
        for llll in "eng", "rus":
            make_prescription(font_path=str(ffff), lang=llll,
                              save_path=Path("test_base_propisi") / Path(str(ffff.stem) + " " + llll + ".pdf"), open_=False)

    # language = 'rus'
    # # font_ = str(Path('base fonts/Coronet.ttf'))
    # font_ = str(Path('base fonts/Cursive_standard.ttf'))
    # path = 'prescription.pdf'
    # ope = True
    # make_prescription(font_path=font_, lang=language, save_path=path, open_=ope)
    # os.startfile(path)
