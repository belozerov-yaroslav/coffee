import sys, sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QTableWidgetItem, QApplication, QWidget, QLineEdit, QPushButton, QMainWindow, QDialog

BASE_NAME = 'coffee.sqlite'


class TablePainter:
    def __init__(self, table):
        self.table = table

    def draw_new(self, items):
        self.table.setRowCount(0)
        self.table.setRowCount(len(items))
        for i in range(len(items)):
            for j in range(len(items[i])):
                self.table.setItem(i, j, QTableWidgetItem(str(items[i][j])))


class MyWin(QWidget):
    def __init__(self):
        self.base_name = BASE_NAME
        super().__init__()
        uic.loadUi('main.ui', self)
        self.table_paint = TablePainter(self.tableWidget)
        self.con = sqlite3.connect(self.base_name)
        cur = self.con.cursor()
        headers = cur.execute('SELECT * FROM coffee').description
        self.tableWidget.setColumnCount(len(headers))
        self.column_count = len(headers)
        self.tableWidget.setHorizontalHeaderLabels([i[0] for i in headers])
        self.load_table()
        cur.close()

    def load_table(self):
        cur = self.con.cursor()
        data = cur.execute('SELECT * FROM coffee').fetchall()
        new_data = []
        for i in range(len(data)):
            new_data.append([q for q in data[i]])
            new_data[i][1] = cur.execute(f'''SELECT name FROM sort WHERE id = {data[i][1]}''').fetchone()[0]
            new_data[i][3] = 'молотый' if new_data[i][3] else 'растворимый'
        self.table_paint.draw_new(new_data)
        cur.close()

    def __del__(self):
        self.con.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWin()
    window.show()
    sys.exit(app.exec_())
