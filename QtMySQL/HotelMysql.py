import sys
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget, QFrame, QCheckBox, QLineEdit, QLabel, QPushButton, QTextBrowser, QTableWidget, \
    QAbstractItemView, QTableWidgetItem, QMenuBar, QStatusBar, QApplication, QMainWindow
from decimal import Decimal

import pymysql
import datetime


class Mainwindow(object):

    def initUI(self,MainWindow):
        # 连接数据库
        self.db = pymysql.connect("localhost","root","gx666666","new_schema")
        self.cursor = self.db.cursor()
        self.startdate:str = None #开始时间
        self.enddate:str = None #结束时间
        self.number:str = None #订房数量
        self.hotel:str = None #酒店名称
        self.booking:list = {} #可预订房型
        self.temp_sqlstring = "MySQL here"
        self.outYes = "结果如上"
        self.outNo = "没有满足要求的结果"
        self.description = "说明：1、酒店名可以不选，不选则返回所有满足要求的酒店  2、订房数量为整数输入  3、时间格式为(例：2018-12-10)"
        
        # 主窗口
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(760, 560)
        MainWindow.setFixedSize(MainWindow.width(), MainWindow.height())
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # 检索框
        self.frame = QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(10, 10, 491, 121))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName("frame")

        # 酒店名check键
        self.check_hotel_name = QCheckBox(self.frame)
        self.check_hotel_name.setGeometry(QtCore.QRect(20, 10, 71, 16))
        self.check_hotel_name.setObjectName("check_hotel_name")
        # 酒店名编辑框
        self.hotelnameEidt = QLineEdit(self.frame)
        self.hotelnameEidt.setGeometry(QtCore.QRect(90, 10, 113, 16))
        self.hotelnameEidt.setObjectName("hotelnameEidt")

        # 开始时间check键
        self.check_start_date = QCheckBox(self.frame)
        self.check_start_date.setGeometry(QtCore.QRect(20, 40, 71, 16))
        self.check_start_date.setObjectName("check_start_date")
        # 开始时间编辑框
        self.start_date_Edit = QLineEdit(self.frame)
        self.start_date_Edit.setGeometry(QtCore.QRect(90, 40, 113, 16))
        self.start_date_Edit.setObjectName("start_date_Edit")

        # 订房数量check键
        self.check_number = QCheckBox(self.frame)
        self.check_number.setGeometry(QtCore.QRect(270, 10, 71, 16))
        self.check_number.setObjectName("check_number")
        # 订房数量编辑框
        self.number_Edit = QLineEdit(self.frame)
        self.number_Edit.setGeometry(QtCore.QRect(340, 10, 113, 16))
        self.number_Edit.setObjectName("number_Edit")

        # 结束时间check键
        self.check_end_date = QCheckBox(self.frame)
        self.check_end_date.setGeometry(QtCore.QRect(270, 40, 71, 16))
        self.check_end_date.setObjectName("check_end_date")
        # 结束时间编辑框
        self.end_date_Edit = QLineEdit(self.frame)
        self.end_date_Edit.setGeometry(QtCore.QRect(340, 40, 113, 16))
        self.end_date_Edit.setObjectName("end_date_Edit")

        # 查询按钮
        self.find = QPushButton(self.frame)
        self.find.setGeometry(QtCore.QRect(380, 100, 75, 21))
        self.find.setObjectName("find")
        self.find.clicked.connect(self.find_btn)

        # 复原按钮
        self.update = QPushButton(self.frame)
        self.update.setGeometry(QtCore.QRect(180,100, 75, 21))
        self.update.setObjectName("update")
        self.update.clicked.connect(self.p1_clicked)

        # MySQL输出框
        self.sql_out = QTextBrowser(self.centralwidget)
        self.sql_out.setGeometry(QtCore.QRect(10, 140, 740, 61))
        self.sql_out.setObjectName("sql_out")

        # 结果框
        self.out = QTextBrowser(self.centralwidget)
        self.out.setGeometry(QtCore.QRect(10, 460, 740, 30))
        self.out.setObjectName("out")

        # 使用说明框
        self.description_out = QTextBrowser(self.centralwidget)
        self.description_out.setGeometry(QtCore.QRect(10, 500, 740, 30))
        self.description_out.setObjectName("description_out")

        # 查询结果表格
        self.result_out = QTableWidget(self.centralwidget)
        self.result_out.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 不可编辑表格
        self.result_out.setGeometry(QtCore.QRect(10, 210, 740, 241))
        self.result_out.setObjectName("result_out")
        self.result_out.setColumnCount(7)
        self.result_out.setRowCount(20)
        self.result_out.resizeColumnsToContents()
        self.result_out.resizeRowsToContents()

        item = QTableWidgetItem()
        self.result_out.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.result_out.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.result_out.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.result_out.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.result_out.setHorizontalHeaderItem(4, item)
        item = QTableWidgetItem()
        self.result_out.setHorizontalHeaderItem(5, item)
        item = QTableWidgetItem()
        self.result_out.setHorizontalHeaderItem(6, item)

        self.result_out.horizontalHeader().setDefaultSectionSize(100)
        self.result_out.horizontalHeader().setMinimumSectionSize(25)
        self.result_out.verticalHeader().setDefaultSectionSize(30)

        # 退出按钮
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(675, 110, 75, 21))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.p2_clicked)

        # 窗口置中
        MainWindow.setCentralWidget(self.centralwidget)

        # Bar （为了美观）
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 509, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def p1_clicked(self):
        self.pyqt_clicked.emit()
    def p2_clicked(self):
        self.pyqt_clicked1.emit()
    def find_btn(self):
        self.pyqt_clicked2.emit()


    # 各个组件显示命名
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "酒店查询系统", None))
        self.check_hotel_name.setText(_translate("MainWindow", "酒店名", None))
        self.check_start_date.setText(_translate("MainWindow", "开始时间", None))
        self.check_end_date.setText(_translate("MainWindow", "结束时间", None))
        self.check_number.setText(_translate("MainWindow", "订房数量", None))
        self.find.setText(_translate("MainWindow", "查询", None))
        self.update.setText(_translate("MainWindow", "复原", None))
        self.sql_out.setText(self.temp_sqlstring)
        self.description_out.setText(self.description)
        item = self.result_out.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "hotel_name", None))
        item = self.result_out.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "room_id", None))
        item = self.result_out.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "room_name", None))
        item = self.result_out.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "date", None))
        item = self.result_out.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "price", None))
        item = self.result_out.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "remain", None))
        item = self.result_out.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "预订", None))
        self.pushButton_2.setText(_translate("MainWindow", "退出", None))

    # 测试鼠标点击事件是否发生
    def mousePressEvent(self, event):
        time = datetime.datetime.now()
        print(datetime.datetime.strftime(time, '%Y-%m-%d %H:%M:%S')+"\t点击了鼠标")
        print("\n\n")

    # 检测各按钮的状态并实行关联事件
    def buttonTest(self):
        _translate = QtCore.QCoreApplication.translate
        is_first = True

        # 检测各check框是否被勾选
        if self.check_hotel_name.isChecked():
            if is_first:
                is_first = False
                self.hotel = self.hotelnameEidt.text()
            else:
                self.hotel = self.hotelnameEidt.text()

        if self.check_start_date.isChecked():
            if is_first:
                is_first = False
                self.startdate = self.start_date_Edit.text()
            else:
                self.startdate = self.start_date_Edit.text()

        if self.check_number.isChecked():
            if is_first:
                is_first = False
                self.number = self.number_Edit.text()
            else:
                self.number = self.number_Edit.text()

        if self.check_end_date.isChecked():
            if is_first:
                is_first = False
                self.enddate = self.end_date_Edit.text()
            else:
                self.enddate = self.end_date_Edit.text()

        self.sqlstring1 = "select hotel_name, room_id,room_name, date, price, remain \
                                  from hotel natural join room_info natural join room_type \
                                  where date >= '{start}' and date <= '{end}' \
                                  and room_id in (select room_id \
                                  from hotel natural join room_type natural join room_info \
        				          where date >= '{start}' and date <= '{end}' and remain >= {num} and hotel_name = '{hotelname}' \
                                  group by room_id \
        				          having count(*) = cast('{end}' as date)-cast('{start}' as date)+1);".format(
            start=str(self.startdate), end=str(self.enddate), num=str(self.number), hotelname=str(self.hotel))

        self.sqlstring2 = "select hotel_name, room_id,room_name, date, price, remain \
                                          from hotel natural join room_info natural join room_type \
                                          where date >= '{start}' and date <= '{end}' \
                                          and room_id in (select room_id \
                                          from hotel natural join room_type natural join room_info \
                				          where date >= '{start}' and date <= '{end}' and remain >= {num} \
                                          group by room_id \
                				          having count(*) = cast('{end}' as date)-cast('{start}' as date)+1);".format(
            start=str(self.startdate), end=str(self.enddate), num=str(self.number))

        # 检测是否check了酒店名
        if self.check_hotel_name.isChecked():
            self.temp_sqlstring = self.sqlstring1
        else: self.temp_sqlstring = self.sqlstring2

        # 输出结果
        self.result_out.clearContents()  # 每一次查询时清除表格中信息
        if not (is_first):
            print(self.temp_sqlstring)
            self.cursor.execute(self.temp_sqlstring)
            self.result = self.cursor.fetchall()
            print(len(self.result))
            if len(self.result) == 0:
                self.out.setText(self.outNo)
            else:self.out.setText(self.outYes)
            k = 0
            for i in self.result:
                print("-----",i)
                w = 0
                for j in i:
                    if type(j) == int:
                        newItem = QTableWidgetItem(str(j))
                    elif type(j) == datetime.date:
                        newItem = QTableWidgetItem(j.strftime('%Y-%m-%d'))
                    elif type(j) == Decimal:
                        newItem = QTableWidgetItem(str(Decimal(j).quantize(Decimal('0.00'))))
                    else:
                        newItem = QTableWidgetItem(j)
                    # 根据循环标签一次对table中的格子进行设置
                    self.result_out.setItem(k, w, newItem)
                    w += 1
                # 设置预订按钮
                self.booking[k] = QPushButton()
                self.booking[k].setCheckable(True)
                self.booking[k].setText(_translate("MainWindow", "预订"+str(k+1), None))
                self.result_out.setCellWidget(k, w, self.booking[k])
                self.booking[k].clicked[bool].connect(self.RtnBook)
                k += 1

        self.sql_out.setText("MySQL here")
        self.sql_out.append(self.temp_sqlstring)
        time = datetime.datetime.now()
        print(datetime.datetime.strftime(time, '%Y-%m-%d %H:%M:%S')+"\t查询按钮按下")
        print("\n\n")

    # 预订按钮关联函数
    def RtnBook(self,pressed):
        source = self.sender()
        for i in range(20):
            if source.text() == "预订"+str(i+1):
                # 更新room_info表
                sql1 = "update room_info set remain = remain-{num} where date = '{theDate}' and room_id = {id};".format(num=self.number,id=self.result[i][1],theDate=self.result[i][3].strftime('%Y-%m-%d'))
                print(sql1)
                self.cursor.execute(sql1)

                # 插入order表
                self.cursor.execute("select max(order_id) from `order`;")
                maxid = self.cursor.fetchall()
                # print(maxid[0][0]+1)
                # print(self.result[i][1])
                # print(self.result[i][3].strftime('%Y-%m-%d'))
                # print(self.number)
                # print(float(self.number)*float(self.result[i][4]))
                # print(datetime.datetime.now().strftime('%Y-%m-%d'))
                sql2 = "insert into `order` value({max_id},{room_id},'{start_date}','{end_date}',{num},{price},'{create_date}');".format(max_id=maxid[0][0]+1,room_id = self.result[i][1],start_date = self.result[i][3].strftime('%Y-%m-%d'),end_date = self.result[i][3].strftime('%Y-%m-%d'),num = self.number, price = float(self.number)*float(self.result[i][4]),create_date=datetime.datetime.now().strftime('%Y-%m-%d'))
                print(sql2)
                self.cursor.execute(sql2)
                self.db.commit()
                source.setText("已预订")
                print(self.result[i])
                time = datetime.datetime.now()
                print(datetime.datetime.strftime(time, '%Y-%m-%d %H:%M:%S')+"\t预订按钮按下")
                print("\n\n")

    def buttonupdate(self):
        self.cursor.execute("DROP TABLE IF EXISTS `room_info`;")
        self.cursor.execute("""CREATE TABLE `room_info`  (
                               `info_id` int(11) NOT NULL,
                               `date` date NULL DEFAULT NULL,
                               `price` decimal(10, 2) NULL DEFAULT NULL,
                               `remain` int(11) NULL DEFAULT NULL,
                               `room_id` int(11) NULL DEFAULT NULL,
                                PRIMARY KEY (`info_id`) USING BTREE,
                                INDEX `room_info_key`(`room_id`) USING BTREE,
                                CONSTRAINT `room_info_key` FOREIGN KEY (`room_id`) REFERENCES `room_type` (`room_id`) ON DELETE RESTRICT ON UPDATE RESTRICT) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;""")

        self.cursor.execute("""INSERT INTO `room_info` VALUES (1, '2018-11-14', 500.00, 5, 1),
                                                              (2, '2018-11-15', 500.00, 4, 1),
                                                              (3, '2018-11-16', 600.00, 6, 1),
                                                              (4, '2018-11-14', 300.00, -6, 2),
                                                              (5, '2018-11-15', 300.00, -7, 2),
                                                              (6, '2018-11-16', 400.00, -7, 2),
                                                              (7, '2018-11-14', 200.00, 4, 3),
                                                              (8, '2018-11-15', 200.00, 3, 3),
                                                              (9, '2018-11-16', 300.00, 4, 3),
                                                              (10, '2018-11-14', 450.00, 5, 4),
                                                              (11, '2018-11-15', 300.00, 5, 4),
                                                              (12, '2018-11-16', 450.00, 5, 4),
                                                              (13, '2018-11-14', 400.00, 2, 5),
                                                              (14, '2018-11-15', 250.00, 2, 5),
                                                              (15, '2018-11-16', 400.00, 2, 5),
                                                              (16, '2018-11-14', 300.00, 1, 6),
                                                              (17, '2018-11-15', 200.00, 1, 6),
                                                              (18, '2018-11-16', 300.00, 5, 6),
                                                              (19, '2018-11-14', 300.00, 2, 7),
                                                              (20, '2018-11-15', 250.00, 3, 7),
                                                              (21, '2018-11-16', 300.00, 8, 7),
                                                              (22, '2018-11-14', 250.00, 1, 8),
                                                              (23, '2018-11-15', 200.00, 1, 8),
                                                              (24, '2018-11-16', 200.00, 5, 8),
                                                              (25, '2018-11-14', 200.00, 2, 9),
                                                              (26, '2018-11-15', 150.00, 4, 9),
                                                              (27, '2018-11-16', 150.00, 4, 9)""")

        self.cursor.execute("DROP TABLE IF EXISTS `order`;")
        self.cursor.execute("""CREATE TABLE `order`  (
                               `order_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自动递增的主键',
                               `room_id` int(11) NULL DEFAULT NULL,
                               `start_date` date NULL DEFAULT NULL,
                               `leave_date` date NULL DEFAULT NULL,
                               `amount` int(11) NULL DEFAULT NULL,
                               `payment` decimal(10, 2) NULL DEFAULT NULL,
                               `create_date` date NOT NULL,
                                PRIMARY KEY (`order_id`) USING BTREE,
                                INDEX `room_order_id`(`room_id`) USING BTREE,
                                CONSTRAINT `room_order_id` FOREIGN KEY (`room_id`) REFERENCES `room_type` (`room_id`) ON DELETE RESTRICT ON UPDATE RESTRICT) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;""")
        self.cursor.execute("""INSERT INTO `order` VALUES (1, 5, '2018-11-14', '2018-11-16', 2, 2100.00, '2018-11-01'),
                                                          (2, 1, '2018-11-14', '2018-11-14', 5, 2500.00, '2018-11-01'),
                                                          (3, 8, '2018-11-14', '2018-11-16', 2, 1296.00, '2018-11-01'),
                                                          (4, 4, '2018-11-14', '2018-11-16', 2, 2400.00, '2018-11-01'),
                                                          (5, 2, '2018-11-14', '2018-11-16', 4, 4000.00, '2018-11-01'),
                                                          (6, 2, '2018-11-14', '2018-11-16', 4, 4000.00, '2018-11-01');""")
        self.db.commit()
        time = datetime.datetime.now()
        print(datetime.datetime.strftime(time, '%Y-%m-%d %H:%M:%S')+"\t复原按钮按下")
        print("\n\n")


    def buttonExit(self):
        time = datetime.datetime.now()
        print(datetime.datetime.strftime(time, '%Y-%m-%d %H:%M:%S')+"\t退出按钮按下")
        self.db.commit()
        self.cursor.close()
        self.db.close()
        self.close()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.buttonExit()

class MyWindow(QMainWindow, Mainwindow):
    pyqt_clicked = pyqtSignal()
    pyqt_clicked1 = pyqtSignal()
    pyqt_clicked2 = pyqtSignal()
    def __init__(self):
        super(MyWindow, self).__init__()
        self.initUI(self)
        self.pyqt_clicked.connect(self.buttonupdate)
        self.pyqt_clicked1.connect(self.buttonExit)
        self.pyqt_clicked2.connect(self.buttonTest)



if __name__ == "__main__":
    app =  QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    myshow = MyWindow()
    myshow.show()
    sys.exit(app.exec_())