import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel

import design

class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow) :
    def __init__(self):
     super().__init__()
     self.setupUi(self)
     db = QSqlDatabase.addDatabase('QSQLITE')
     db.setDatabaseName('data.db')
     db.open()
     self.model.setTable(db.tables()[0])
     self.tableView.setModel(self.model)
     self.model.select()
     self.select_table.addItems(db.tables())
     self.select_table.currentTextChange.connect(self.update_current_table)
     columns = []
     for i in range(self.model.record().count()):
         columns.append(self.model.headerData(i, QtCore.Qt.Horizontal))
     self.filter_col.addItems(columns)
     self.button_apply_filter.clicked.connect(self.apply_filter)
     self.button_cancel_filter.clicked.connect(self.cancel_filter)
     self.tableView.setSortingEnabled(True)

    def update_current_table(self) :
     self.model.setTable(self.select_table.currenText())
     self.filter_col.clear()
     columns = []
     for i in range(self.model.record().count()):
         columns.append(self.model.headerData(i, QtCore.Qt.Horizontal))
     self.filter_col.addItem(columns)
     self.model.select()

    def apply_filter(self):
         select_filter = self.filter_arg.displayText()
         try:
             select_filter = int(self.filter_arg.displayText())
             self.model.setFilter(f"{self.filter_col.currentText()}={select_filter}")
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
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
