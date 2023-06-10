import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, \
    QMessageBox

situation = {
    'лодка': 'L',
    'волк': 'L',
    'коза': 'L',
    'качан': 'L'
}

game = True
selected_object = None
step = 1

B, W, G, C, N = 'лодка', 'волк', 'коза', 'качан', 'ничего'


class QMessage:
    @classmethod
    def question(cls):
        pass


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.click = None
        self.game_layout = None

        # Область игрового поля
        self.game_field = QWidget()
        self.game_field_layout = QHBoxLayout()
        self.situation = QWidget()
        self.situation.setLayout(self.create_game_field())
        self.game_field_layout.addWidget(self.situation)
        self.game_field.setLayout(self.game_field_layout)

        # Область управления
        self.control_area = QWidget()
        self.control_area_layout = QHBoxLayout()
        self.transition = QPushButton('Сделать ход')
        self.transition.clicked.connect(self.update_game_field)
        self.control_area_layout.addWidget(self.transition, alignment=Qt.AlignCenter)
        self.control_area.setLayout(self.control_area_layout)

        # Область окна программы
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.game_field)
        self.main_layout.addWidget(self.control_area)
        self.main_layout.addStretch(1)

        self.setLayout(self.main_layout)
        self.setWindowTitle('Волк Коза Капуста')
        self.setGeometry(800, 100, 450, 600)

    # Создание игрового поля
    def create_game_field(self):
        if game:
            return self.show_situation()

    # Обновление игрового поля
    def update_game_field(self):
        if game:
            new_situation = QWidget()
            new_situation.setLayout(self.create_game_field())
            item = self.game_field_layout.itemAt(0)
            self.game_field_layout.removeItem(item)
            self.game_field_layout.addWidget(new_situation)

    # Ситуация на поле
    def show_situation(self):
        global step
        global game
        global situation
        global selected_object

        print(f'\nЭпизод №{step}')
        print('Перед переправой ситуация следующая:')
        for y in range(4):
            print(f'{list(situation.keys())[y]} : {list(situation.values())[y]}')

        if selected_object:
            print(f'был сделан выбор (индекс строки): {selected_object}')
            print(f'название объекта: {list(situation.keys())[selected_object]}')
            print(f'положение объекта: {situation[list(situation.keys())[selected_object]]}')
            if situation[list(situation.keys())[selected_object]] == 'L':
                situation[list(situation.keys())[selected_object]] = 'R'
            else:
                situation[list(situation.keys())[selected_object]] = 'L'

            if step > 1:
                if situation[G] == situation[C] != situation[B] or situation[G] == situation[C] != 'R':
                    game = False
                    QMessageBox.information(self, 'Поражение', "Коза съела капусту.", QMessageBox.Ok)
                    result = QMessageBox.information(self, 'Поражение', 'Вы проиграли!')
                    if result == QMessageBox.Ok:
                        sys.exit(app.exec())
                if situation[G] == situation[W] != situation[B] or situation[G] == situation[W] != 'R':
                    game = False
                    QMessageBox.information(self, 'Поражение', "Волк съел козу.", QMessageBox.Ok)
                    result = QMessageBox.information(self, 'Поражение', 'Вы проиграли!')
                    if result == QMessageBox.Ok:
                        sys.exit(app.exec())
                if (situation[B] == situation[W] == situation[G] == situation[C] == 'R') or (
                        situation[B] == situation[W] == situation[G] == situation[C] == 'L'):
                    game = False
                    QMessageBox.information(self, 'Победа!!!', "Вы успешно переправили всех на другой берег.",
                                            QMessageBox.Ok)
                    result = QMessageBox.information(self, 'Победа!', 'Вы выиграли!')
                    if result == QMessageBox.Ok:
                        sys.exit(app.exec())
            if step > 1:
                while situation[G] == situation[C] != situation[B] or situation[G] == situation[C] != 'L':
                    game = False
                    QMessageBox.information(self, 'Поражение', "Коза съела капусту.", QMessageBox.Ok)
                    result = QMessageBox.information(self, 'Поражение', 'Вы проиграли!')
                    if result == QMessageBox.Ok:
                        sys.exit(app.exec())
                while situation[G] == situation[W] != situation[B] or situation[G] == situation[W] != 'L':
                    game = False
                    QMessageBox.information(self, 'Поражение', "Волк съел козу.", QMessageBox.Ok)
                    result = QMessageBox.information(self, 'Поражение', 'Вы проиграли!')
                    if result == QMessageBox.Ok:
                        sys.exit(app.exec())
                while (situation[B] == situation[W] == situation[G] == situation[C] == 'R') or (
                        situation[B] == situation[W] == situation[G] == situation[C] == 'L'):
                    game = False
                    QMessageBox.information(self, 'Победа!!!', "Вы успешно переправили всех на другой берег.",
                                            QMessageBox.Ok)
                    result = QMessageBox.information(self, 'Победа!', 'Вы выиграли!')
                    if result == QMessageBox.Ok:
                        sys.exit(app.exec())
        self.game_layout = QGridLayout()
        index = 0
        for i in range(4):
            key = list(situation)[i]
            position = situation[f'{key}']
            for j in range(3):
                label = QLabel()
                if j == 1:
                    color = 'blue'
                    label.setStyleSheet(f'background: {color}')
                else:
                    if position == 'L' and j == 0 or position == 'R' and j == 2:
                        label.setStyleSheet(
                            f'min-height: 150px; min-width: 150px; '
                            f'background-image: url("images/{i}.jpg")')
                    else:
                        label.setText('')
                        label.setStyleSheet(
                            f'min-height: 150px; min-width: 150px; '
                            f'background-image: url("images/4.jpg")')
                label.setObjectName(f'{index}')
                label.installEventFilter(self)
                self.game_layout.addWidget(label, i, j)
                index += 1

        if situation[B] == 'L':
            situation[B] = 'R'
        else:
            situation[B] = 'L'

        selected_object = None

        step += 1

        return self.game_layout

    def eventFilter(self, obj, event):
        if event.type() == 2:
            print('-' * 7)
            print('Ваш выбор:')
            print(f'индекс выбранного объекта: {obj.objectName()}')

            position = self.game_layout.getItemPosition(int(obj.objectName()))
            print(f'строка выбранного объекта: {position[0]}')
            print(f'столбец выбранного объекта: {position[1]}')

            global selected_object
            if position[1] == 2 and situation[list(situation.keys())[position[0]]] == 'R' and situation[B] == 'L'\
                    or position[1] == 0 and situation[list(situation.keys())[position[0]]] == 'L' and situation[B] == 'R':
                selected_object = position[0]
                print('объект выбран')
            else:
                print('Этот объект нельзя выбрать')

            for i in range(4):
                for j in range(3):
                    if i == position[0] and j == position[1]:
                        label = QLabel()
                        label.setStyleSheet('border: 2px solid yellow')
                        self.game_layout.addWidget(label, i, j)

        return super(QWidget, self).eventFilter(obj, event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())