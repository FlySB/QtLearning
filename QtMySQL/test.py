"""
    QPushButton:切换按钮就是QPsuhButton的一种特殊模式，他有两种状态：按下和未按下。我们在点击的时候切换两种状态，有很多场景会用到这个功能
    Author：dengyexun
    DateTime：2018.11.20
"""
from PyQt5.QtWidgets import QWidget, QPushButton, QFrame, QApplication
from PyQt5.QtGui import QColor
import sys

class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initGUI()

    def initGUI(self):
        # 功能区
        self.col = QColor(0, 0, 0)    # 颜色句柄
        # 初始化pushButton
        redb = QPushButton('Red', self)
        redb.setCheckable(True)
        redb.move(60, 60)
        # 槽与信号连接.当redb被点击时，传入一个bool值给setColor的pressed参数
        redb.clicked[bool].connect(self.setColor)

        greenb = QPushButton('Green', self)
        greenb.setCheckable(True)
        greenb.move(60, 80)
        greenb.clicked[bool].connect(self.setColor)

        blueb = QPushButton('Blue', self)
        blueb.setCheckable(True)
        blueb.move(60, 100)
        blueb.clicked[bool].connect(self.setColor)

        # QFrame对象
        self.square = QFrame(self)
        self.square.setGeometry(110,110,200,200)
        # 更改QWidget的样式风格
        self.square.setStyleSheet("QWidget {backgroud-color:%s}" % self.col.name())


        # Frame
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle("toggle button")
        self.show()

    def setColor(self, pressed):
        """
        自定义槽函数
        :param pressed: 鼠标被按下的状态
        :return:
        """
        # 得到切换按钮的信息，哪一个信号被触发了
        source = self.sender()
        # 当按下按钮
        if pressed:
            val = 255
        else:
            val = 0
        # 判断这个信号的文本内容
        if source.text() == 'Red':
            self.col.setRed(val)
        elif source.text() == 'Green':
            self.col.setGreen(val)
        else:
            self.col.setBlue(val)
        # 更改QFrame的样式风格，设置背景为特定的颜色
        color = self.col.name()     # 样式的背景色编码
        self.square.setStyleSheet("QFrame {background-color:%s}" % self.col.name())


        print('ok')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())