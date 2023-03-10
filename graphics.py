from PyQt6 import QtWidgets, QtCore, QtGui
import os
import sys
from pathlib import Path
import shutil


import algoritm

test_value = 0


def test(test_val=None):
    with open(r'test output.txt', 'w') as f:
        f.write(f'Раб{str(test_val)} ')
    os.startfile(r'test output.txt')


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Генератор прописей')
        menu = QtWidgets.QTabWidget()
        self.tab1 = MainTab()
        self.tab2 = SettingsTab()
        self.tab3 = AboutTab()
        menu.addTab(self.tab1, 'Главная')
        menu.addTab(self.tab2, 'Настройки')
        menu.addTab(self.tab3, 'О программе')
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(menu)
        self.setLayout(vbox)

        self.tab1.message.signal.connect(self.creating_file)
        self.tab2.review_list_signal.connect(self.tab1.on_review_fonts_w)

    def creating_file(self, save_path: Path):
        font_name = self.tab1.fonts_w.currentItem().text()
        if not (fin := tuple(Path("base fonts").glob(f"{font_name}.*"))):
            fin = tuple(Path("user fonts").glob(f"{font_name}.*"))
        font_path = str(fin[0])
        for i in self.tab1.langs:
            if i.isChecked():
                t = i.text()
        # noinspection PyUnboundLocalVariable
        t = 'eng' if t == 'Английский' else 'rus'
        save_path = save_path.with_suffix('.pdf')
        if not save_path.parent.exists():
            save_path.parent.mkdir(parents=True)
        o = self.tab1.open_finished_w.isChecked()
        try:
            res_code = algoritm.make_prescription(font_path, lang=t, save_path=save_path, open_=o)
        except Exception as e:
            print(e, type(e))
            raise e
        if res_code == 0 and not o:
            QtWidgets.QMessageBox.information(self, "Успех!", "Пропись успешно создана")
        elif res_code == -1:
            QtWidgets.QMessageBox.information(self, "Провал(", "Не удалось создать пропись. Возможно шрифт не поддерживает "
                                                               "выбранный язык")


class MainTab(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.texts = {
            'Английский': ('abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
            'Русский': ('абвгдеёжзийклмнопрстуфхцчшщъыьэюя', 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')
        }
        label1 = QtWidgets.QLabel('Выберите стиль (шрифт) прописи')

        self.open_finished_w = QtWidgets.QCheckBox('Открыть после создания')
        self.open_finished_w.setChecked(True)

        self.save_btn = QtWidgets.QPushButton('Создать')
        
        Path("user fonts").mkdir(exist_ok=True)
        self.fonts_w = QtWidgets.QListWidget()
        self.fonts_w.addItems(
            map(lambda x: x.stem, Path('base fonts').iterdir()))
        self.fonts_w.addItems(
            map(lambda x: x.stem, Path('user fonts').iterdir()))
        self.fonts_w.setCurrentRow(0)
        languages = list(self.texts.keys())
        self.langs = [QtWidgets.QRadioButton(i) for i in languages]
        self.langs[0].setChecked(True)
        t_layout = QtWidgets.QVBoxLayout()
        for i in self.langs:
            t_layout.addWidget(i)

        texts_w = QtWidgets.QGroupBox()
        texts_w.setLayout(t_layout)
        texts_w.setTitle('Выберите язык прописи')

        v_box1 = QtWidgets.QVBoxLayout()
        v_box1.addWidget(label1)
        v_box1.addWidget(self.fonts_w)
        v_box1.addWidget(texts_w)
        v_box1.addWidget(self.open_finished_w)
        v_box1.addStretch(1)
        h_box2 = QtWidgets.QHBoxLayout()
        h_box2.addStretch(1)
        h_box2.addWidget(self.save_btn)
        v_box3 = QtWidgets.QVBoxLayout()
        v_box3.addLayout(v_box1)
        v_box3.addStretch(1)
        v_box3.addLayout(h_box2)
        self.setLayout(v_box3)
        self.message = SaveMessage()
        self.save_btn.clicked.connect(self.on_save)

    def on_save(self):
        self.message.show()

    def on_review_fonts_w(self):
        self.fonts_w.clear()
        self.fonts_w.addItems(
            map(lambda x: x.stem, Path('base fonts').iterdir()))
        self.fonts_w.addItems(
            map(lambda x: x.stem, Path('user fonts').iterdir()))

    def showEvent(self, a0: QtGui.QShowEvent):
        super().showEvent(a0)


class SaveMessage(QtWidgets.QDialog):
    signal = QtCore.pyqtSignal(Path)

    def __init__(self):
        super().__init__()
        self.setModal(True)
        self.resize(299, 127)

        input_dir_w = QtWidgets.QLineEdit()
        input_file_w = QtWidgets.QLineEdit()
        open_dir_btn = QtWidgets.QPushButton()
        ok_btn = QtWidgets.QPushButton("Ок")

        dir_icon = QtGui.QIcon(str(Path(r"img\folder_icon.png")))
        open_dir_btn.setIcon(dir_icon)
        d_dir, d_file = self.get_dsave_name_and_dir()

        input_dir_w.setText(d_dir)
        input_file_w.setText(d_file)

        file_dialog = QtWidgets.QFileDialog()

        open_dir_btn.clicked.connect(self.on_open_dir)
        ok_btn.clicked.connect(self.on_ok)

        h_box1 = QtWidgets.QHBoxLayout()
        h_box1.addWidget(input_dir_w)
        h_box1.addWidget(open_dir_btn)

        h_box2 = QtWidgets.QHBoxLayout()
        h_box2.addStretch()
        h_box2.addWidget(ok_btn)

        f_box1 = QtWidgets.QFormLayout()
        f_box1.addRow('Выберите папку сохранения файла', h_box1)
        f_box1.setRowWrapPolicy(QtWidgets.QFormLayout.RowWrapPolicy.WrapAllRows)

        f_box2 = QtWidgets.QFormLayout()
        f_box2.addRow('Введите название файла', input_file_w)
        f_box2.setRowWrapPolicy(QtWidgets.QFormLayout.RowWrapPolicy.WrapAllRows)

        v_box = QtWidgets.QVBoxLayout()
        v_box.addStretch(2)
        v_box.addLayout(f_box1)
        v_box.addStretch(5)
        v_box.addLayout(f_box2)
        v_box.addStretch(10)
        v_box.addLayout(h_box2)

        self.setLayout(v_box)

        self.input_dir_w = input_dir_w
        self.input_file_w = input_file_w
        self.ok_btn = ok_btn
        self.file_dialog = file_dialog

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.resize(self.width(), self.height() + 40)
        super().showEvent(a0)

    @QtCore.pyqtSlot()
    def on_open_dir(self):
        old_path = str(Path(self.input_dir_w.text()))
        dir_ = self.file_dialog.getExistingDirectory(directory=old_path)
        self.input_dir_w.setText(dir_)

    @QtCore.pyqtSlot()
    def on_ok(self):
        path = Path(self.input_dir_w.text()) / Path(self.input_file_w.text())
        Path(r'last_path.txt').write_text(str(path))
        self.signal.emit(path)
        self.close()

    @staticmethod
    def get_dsave_name_and_dir() -> tuple[str, str]:
        asset_path = Path(r'last_path.txt')
        asset_path.touch()
        p = asset_path.read_text()
        try:
            if p == "":
                raise FileNotFoundError
            (p := Path(p)).touch()
        except FileNotFoundError:
            i = 1
            while True:
                p = Path(os.getenv("ALLUSERSPROFILE")) / Path(rf"Propisi\propis{i}.pdf")
                if not p.exists() or i > 30:
                    break
                i += 1
        return str(p.parent), p.name


class SettingsTab(QtWidgets.QWidget):
    review_list_signal = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        label1 = QtWidgets.QLabel("<h4>Управнение шрифтами</h4>")
        label3 = QtWidgets.QLabel("Введите название шрифта")
        message_l = QtWidgets.QLabel('')

        open_dir_btn = QtWidgets.QPushButton()
        dir_icon = QtGui.QIcon(str(Path(r"img\folder_icon.png")))
        open_dir_btn.setIcon(dir_icon)
        font_path_w = QtWidgets.QLineEdit()
        add_font_btn = QtWidgets.QPushButton("Добавить")
        remove_font_btn = QtWidgets.QPushButton("Удалить")

        add_font_btn.setEnabled(False)
        remove_font_btn.setEnabled(False)

        open_dir_btn.clicked.connect(self.on_open_dir)
        add_font_btn.clicked.connect(self.add_font)
        remove_font_btn.clicked.connect(self.remove_font)
        font_path_w.textChanged.connect(self.name0path_edited)

        h_box1 = QtWidgets.QHBoxLayout()
        h_box1.addWidget(open_dir_btn)
        h_box1.addWidget(font_path_w)

        f_box1 = QtWidgets.QFormLayout()
        f_box1.addRow(label3, h_box1)

        h_box2 = QtWidgets.QHBoxLayout()
        h_box2.addLayout(f_box1)

        h_box3 = QtWidgets.QHBoxLayout()
        h_box3.addStretch(20)
        h_box3.addWidget(add_font_btn)
        h_box3.addStretch(5)
        h_box3.addWidget(remove_font_btn)
        h_box3.addStretch(20)

        h_box4 = QtWidgets.QHBoxLayout()
        h_box4.addStretch()
        h_box4.addWidget(message_l)
        h_box4.addStretch()

        v_box1 = QtWidgets.QVBoxLayout()
        v_box1.addLayout(h_box2)
        v_box1.addSpacing(10)
        v_box1.addLayout(h_box3)
        v_box1.addLayout(h_box4)

        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(label1)
        v_box.addStretch(5)
        v_box.addLayout(v_box1)
        v_box.addStretch(100)
        self.setLayout(v_box)

        self.file_dialog = QtWidgets.QFileDialog()
        self.font_path_w = font_path_w
        self.add_font_btn = add_font_btn
        self.remove_font_btn = remove_font_btn
        self.message_l = message_l

    @QtCore.pyqtSlot()
    def on_open_dir(self):
        dir_ = self.file_dialog.getOpenFileName(filter="Fonts (*.ttf *.TTF *.ttc)")[0]
        self.font_path_w.setText(dir_)

    @QtCore.pyqtSlot()
    def add_font(self):
        path = Path(self.font_path_w.text())
        try:
            shutil.copy(path, Path("user fonts"))
            QtCore.QTimer.singleShot(100, lambda: self.message_l.setText('Шрифт успешно установлен'))
            self.review_list_signal.emit()
        except FileNotFoundError:
            QtCore.QTimer.singleShot(100, lambda: self.message_l.setText('Ошибка: Шрифт не найден!'))

    @QtCore.pyqtSlot()
    def remove_font(self):
        path = Path("user fonts") / Path(self.font_path_w.text()).name
        self.message_l.setText("")
        try:
            if not path.suffix:
                for i in (".ttf", ".TTF",):
                    if (path := path.with_suffix(i)).exists():
                        break
                else:
                    path = path.with_suffix(".ttc")
            path.unlink()
            QtCore.QTimer.singleShot(100, lambda: self.message_l.setText(f'Шрифт успешно удален'))
            self.review_list_signal.emit()
        except FileNotFoundError:
            QtCore.QTimer.singleShot(100, lambda: self.message_l.setText(f'Ошибка: Шрифт не найден!'))

    @QtCore.pyqtSlot()
    def name0path_edited(self):
        if self.font_path_w.text():
            self.remove_font_btn.setEnabled(True)
            self.add_font_btn.setEnabled(True)
        else:
            self.remove_font_btn.setEnabled(False)
            self.add_font_btn.setEnabled(False)


class AboutTab(QtWidgets.QWidget):
    def __init__(self):
        super(AboutTab, self).__init__()
        text = """<h4>О программе </h4>
        <p>Генератор Прописей 3.0.1</p>
        <p>Разработка этой программы является проектной деятельностью ученика 9-го класса,
а сама программа — ее продуктом. Основной функцией программы является создание прописей в формате PDF документов.
Поддерживается русский и английский язык прописи. Использовать полученные файлы можно при обучении детей дошкольного возраста
грамоте, коррекции письма детей школьного возраста или взрослых, выработке каллиграфического или художественного
почерка. Программа имеет открытый исходный код.</p>
        <p>Проект на GitHub (+ инструкция по добавлению шрифтов): ссылка</p>
        <p>Связь с разработкчиком: e-mail</p>
        """
        about_w = QtWidgets.QLabel(text)
        about_w.setWordWrap(True)
        box = QtWidgets.QVBoxLayout()
        box.addWidget(about_w)
        self.setLayout(box)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
