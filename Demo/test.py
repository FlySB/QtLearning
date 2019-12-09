import sys
from PyQt5.QtWidgets import QApplication, QWidget


if __name__ == '__main__':

    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(1000, 500)
    w.move(300, 300)
    w.setWindowTitle('一个简单的测试')
    w.show()

    sys.exit(app.exec_())