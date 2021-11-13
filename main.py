import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel

import design  # Это наш конвертированный файл дизайна


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('data.db')
        db.open()
        self.model = QSqlTableModel(self)
        self.model.setTable(db.tables()[0])
        self.tableView.setModel(self.model)
        self.model.select()
        # Выбор таблицы для вывода:
        self.select_table.addItems(db.tables())
        self.select_table.currentTextChanged.connect(self.update_current_table)
        # Выбор таблицы для фильтра:
        columns = []
        for i in range(self.model.record().count()):
            columns.append(self.model.headerData(i, QtCore.Qt.Horizontal))
        self.filter_col.addItems(columns)
        # Обработка фильтров:
        self.button_apply_filter.clicked.connect(self.apply_filter)
        self.button_cancel_filter.clicked.connect(self.cancel_filter)
        # Сортировка
        self.tableView.setSortingEnabled(True)

    def update_current_table(self):
        self.model.setTable(self.select_table.currentText())
        self.filter_col.clear()
        columns = []
        for i in range(self.model.record().count()):
            columns.append(self.model.headerData(i, QtCore.Qt.Horizontal))
        self.filter_col.addItems(columns)
        self.model.select()

    def apply_filter(self):
        select_filter = self.filter_arg.displayText()
        try:
            select_filter = int(self.filter_arg.displayText())
            self.model.setFilter(f"{self.filter_col.currentText()}={select_filter}")  # работает как Where
        except ValueError:
            try:
                symbol = select_filter[0]
                select_filter = int(select_filter[1:])
                if symbol == '=' or symbol == '<' or symbol == '>':
                    self.model.setFilter(f"{self.filter_col.currentText()} {symbol} {select_filter}")
                else:
                    print('Возникла ошибка')
            except ValueError:
                self.model.setFilter(f"{self.filter_col.currentText()} LIKE '{self.filter_arg.displayText()}'")

    def cancel_filter(self):
        self.model.setFilter("")


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
