import os
from PyQt5 import QtWidgets, QtCore, QtGui
import shutil
from pathlib import Path


class MainWindow(QtWidgets.QWidget):
    saving_sgl = QtCore.pyqtSignal(str, str, str, bool)

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
        self.saving_sgl.emit(f, t, p, o)


class MainTab(QtWidgets.QWidget):
    texts = {
        'Английский': ('abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
        'Русский': ('абвгдеёжзийклмнопрстуфхцчшщъыьэюя', 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')
    }

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        label1 = QtWidgets.QLabel('Выберите стиль (шрифт) прописи')

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

    def on_review(self):
        self.fonts_w.clear()
        self.fonts_w.addItems(
            map(lambda x: os.path.splitext(x)[0], os.listdir(os.path.join(os.path.dirname(__file__), 'base fonts'))))

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        super().showEvent(a0)


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
        d_dir, d_file = os.path.split(str(self.get_dsave_path()))

        input_dir_w.setText(d_dir.replace('\\\\', '\\'))
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
        path = os.path.join(self.input_dir_w.text(), self.input_file_w.text())
        with open(r'last_path.txt', 'w') as file:
            file.write(path)
        self.clicked_save_btn.emit(path)
        self.close()

    @staticmethod
    def get_dsave_path():
        with open(r'last_path.txt', 'r') as file:
            p = Path(file.read())
        if p == Path(''):
            p = Path(os.getenv('USERPROFILE'), 'Documenttt', 'propis.pdf')
            if not p.exists():
                p = Path('propis.pdf')
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
        text = """<h4>О программе </h4>
        <p>Генератор Прописей 1.6.4</p>
        <p>Разработка этой программы является проектной деятельностью ученика 9-го класса,
а сама программа — ее продуктом. Основной функцией является создание PDF документов прописи. Поддерживается
русский и английский язык прописи. Использовать полученные файлы можно при обучении детей дошкольного возраста
грамоте, коррекции письма детей школьного возраста или взрослых, выработке каллиграфического или художественного
почерка. Программа имеет открытый исходный код.</p>
        """
        about_w = QtWidgets.QLabel(text)
        about_w.setWordWrap(True)
        box = QtWidgets.QVBoxLayout()
        box.addWidget(about_w)
        self.setLayout(box)
