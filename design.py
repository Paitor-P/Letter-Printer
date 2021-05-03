import os
from PyQt5 import QtWidgets, QtCore, QtGui
import shutil
from pathlib import Path
import json
import algorithm


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

        self.tab1.message.clicked_save_btn.connect(self.creating_emit)
        self.tab2.review_list.connect(self.tab1.on_review)

    def creating_emit(self, path):
        f = self.tab1.fonts_w.currentItem().text() + '.ttf'
        t = 'Английский'
        for i in self.tab1.langs:
            if i.isChecked():
                t = i.text()
        t = 'eng' if t == 'Английский' else 'rus'

        p = path
        if '.' in os.path.split(p)[1]:
            p = p[:p.index('.')] + '.pdf'
        else:
            p = p + '.pdf'
        o = self.tab1.open_finished_w.isChecked()
        progress_bar = QtWidgets.QProgressBar(self)
        progress_bar.setRange(0, 0)
        progress_bar.show()
        algorithm.make_prescription(f, t, p)
        progress_bar.close()
        if o:
            os.startfile(p)
        else:
            pass  # вывод окна загрузки


class MainTab(QtWidgets.QWidget):
    texts = {
        'Английский': ('abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
        'Русский': ('абвгдеёжзийклмнопрстуфхцчшщъыьэюя', 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')
    }

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        with open(r'fonts_date.json', 'r') as file:
            self.data = json.load(file)

        label1 = QtWidgets.QLabel('Выберите шрифт для прописи')

        self.open_finished_w = QtWidgets.QCheckBox('Открыть после создания')
        self.open_finished_w.setChecked(True)

        self.save_btn = QtWidgets.QPushButton('Создать')
        self.fonts_w = QtWidgets.QListWidget()
        self.fonts_w.addItems(
            map(lambda x: os.path.splitext(x)[0], os.listdir(os.path.join(os.path.dirname(__file__), 'base fonts'))))

        languages = list(self.texts.keys())
        self.langs = [QtWidgets.QRadioButton(i) for i in languages]
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
        h_box2 = QtWidgets.QHBoxLayout()
        h_box2.addStretch(5)
        h_box2.addWidget(self.save_btn)
        v_box3 = QtWidgets.QVBoxLayout()
        v_box3.addLayout(v_box1)
        v_box3.addStretch(5)
        v_box3.addLayout(h_box2)
        self.setLayout(v_box3)
        self.message = SaveMessage()
        self.save_btn.clicked.connect(self.on_save)
        self.fonts_w.currentItemChanged.connect(self.on_choose_lang)

    def on_save(self):
        if self.fonts_w.currentItem() is None:
            QtWidgets.QMessageBox.critical(self, 'Ошибка', 'Выберите шрифт', QtWidgets.QMessageBox.Ok)
            return
        elif not any(map(lambda x: x.isChecked(), self.langs)):
            QtWidgets.QMessageBox.critical(self, 'Ошибка', 'Выберите язык', QtWidgets.QMessageBox.Ok)
            return
        self.message.show()

    def on_choose_lang(self, current: QtWidgets.QListWidgetItem):
        self.langs[0].setEnabled(True)
        self.langs[1].setEnabled(True)
        if 'eng' not in self.data[current.text()]:
            self.langs[0].setEnabled(False)
            self.langs[1].setChecked(True)
        elif 'rus' not in self.data[current.text()]:
            self.langs[1].setEnabled(False)
            self.langs[0].setChecked(True)

    def on_review(self):
        self.fonts_w.clear()
        self.fonts_w.addItems(
            map(lambda x: os.path.splitext(x)[0], os.listdir(os.path.join(os.path.dirname(__file__), 'base fonts'))))


class SaveMessage(QtWidgets.QDialog):
    clicked_save_btn = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setModal(True)
        self.resize(299, 127)

        input_dir_w = QtWidgets.QLineEdit()
        input_file_w = QtWidgets.QLineEdit()
        open_dir_btn = QtWidgets.QPushButton()
        ok_btn = QtWidgets.QPushButton("Ок")

        icon = QtGui.QIcon(r"img\folder_icon.png")
        open_dir_btn.setIcon(icon)
        default_save_path = self.get_dsave_path()

        input_dir_w.setText(str(default_save_path.parent))
        input_file_w.setText(str(default_save_path.name))

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
        f_box1.setRowWrapPolicy(QtWidgets.QFormLayout.WrapAllRows)

        f_box2 = QtWidgets.QFormLayout()
        f_box2.addRow('Введите название файла', input_file_w)
        f_box2.setRowWrapPolicy(QtWidgets.QFormLayout.WrapAllRows)

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
        self.resize(self.width(), 185)
        super().showEvent(a0)

    @QtCore.pyqtSlot()
    def on_open_dir(self):
        old_path = self.input_dir_w.text()
        dir_ = self.file_dialog.getExistingDirectory(directory=os.path.split(old_path)[0])
        self.input_dir_w.setText(dir_)
        if self.input_dir_w.text() == "":
            self.input_dir_w.setText(old_path)

    @QtCore.pyqtSlot()
    def on_ok(self):
        path = Path(self.input_dir_w.text(), self.input_file_w.text())
        with open(r'last_path.txt', 'w') as file:
            file.write(str(path))
        self.clicked_save_btn.emit(str(path))
        self.close()

    @staticmethod
    def get_dsave_path() -> Path:
        with open(r'last_path.txt', 'r') as file:
            p = Path(file.read())
        if p == Path(''):
            p = Path(os.getenv('USERPROFILE'), 'Documents')
            if not p.exists():
                p = Path('propis.pdf')
            else:
                p.joinpath('propis.pdf')
        return p


class SettingsTab(QtWidgets.QWidget):
    review_list = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        label1 = QtWidgets.QLabel("<h4>Управнение шрифтами</h4>")
        label3 = QtWidgets.QLabel("Введите путь к шрифту")
        message_l = QtWidgets.QLabel('')

        font_path_w = QtWidgets.QLineEdit()
        add_font_btn = QtWidgets.QPushButton("Добавить")
        remove_font_btn = QtWidgets.QPushButton("Удалить")

        add_font_btn.setEnabled(False)
        remove_font_btn.setEnabled(False)

        add_font_btn.clicked.connect(self.add_font)
        remove_font_btn.clicked.connect(self.remove_font)
        font_path_w.textEdited.connect(self.name0path_edited)

        f_box1 = QtWidgets.QFormLayout()
        f_box1.addRow(label3, font_path_w)

        h_box1 = QtWidgets.QHBoxLayout()
        h_box1.addLayout(f_box1)

        h_box2 = QtWidgets.QHBoxLayout()
        h_box2.addStretch(20)
        h_box2.addWidget(add_font_btn)
        h_box2.addStretch(5)
        h_box2.addWidget(remove_font_btn)
        h_box2.addStretch(20)

        h_box3 = QtWidgets.QHBoxLayout()
        h_box3.addStretch()
        h_box3.addWidget(message_l)
        h_box3.addStretch()

        v_box1 = QtWidgets.QVBoxLayout()
        v_box1.addLayout(h_box1)
        v_box1.addSpacing(10)
        v_box1.addLayout(h_box2)
        v_box1.addLayout(h_box3)

        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(label1)
        v_box.addStretch(5)
        v_box.addLayout(v_box1)
        v_box.addStretch(100)
        self.setLayout(v_box)

        self.font_path_w = font_path_w
        self.add_font_btn = add_font_btn
        self.remove_font_btn = remove_font_btn
        self.message_l = message_l

    @QtCore.pyqtSlot()
    def add_font(self):
        path = self.font_path_w.text()
        try:
            shutil.copy(path, os.path.join(os.path.dirname(__file__), 'base fonts', os.path.split(path)[1]))
            flag = True
        except:
            flag = False

        if flag:
            self.message_l.setText('Шрифт успешно установлен')
            self.review_list.emit()
        else:
            self.message_l.setText(f'Ошибка установки!')

    @QtCore.pyqtSlot()
    def remove_font(self):
        path = self.font_path_w.text()
        try:
            os.remove(os.path.join(os.path.dirname(__file__), 'base fonts', os.path.split(path)[1]))
            flag = True
        except:
            flag = False
        if flag:
            self.message_l.setText(f'Шрифт успешно удален')
            self.review_list.emit()
        else:
            self.message_l.setText(f'Ошибка удаления!')

    @QtCore.pyqtSlot()
    def name0path_edited(self):
        if self.font_path_w.text().strip():
            self.remove_font_btn.setEnabled(True)
            self.add_font_btn.setEnabled(True)
        else:
            self.remove_font_btn.setEnabled(False)
            self.add_font_btn.setEnabled(False)


class AboutTab(QtWidgets.QWidget):
    def __init__(self):
        super(AboutTab, self).__init__()
        with open(r'about_tab_text.txt', 'r', encoding='utf-8') as f:
            text = f.read()
        about_w = QtWidgets.QLabel(text)
        about_w.setWordWrap(True)
        box = QtWidgets.QVBoxLayout()
        box.addStretch(1)
        box.addWidget(about_w)
        box.addStretch(4)
        self.setLayout(box)
