import pymysql
db = pymysql.connect("localhost","root","gx666666","new_schema")
cursor = db.cursor()

# hotel:str = input("酒店名称：")
# startdate:str = input("开始时间：")
# enddate:str = input("结束时间：")
# number:str = input("数量：")



# sql = "select hotel_name,room_id, room_name, date,remain \
#        from hotel natural join room_info natural join room_type \
#        where date >= '{start}' and date <= '{end}' \
#        and room_id in (select room_id \
#                 from hotel natural join room_type natural join room_info \
# 				where date >= '{start}' and date <= '{end}' and remain >= {num} and hotel_name = '{hotelname}' \
#                 group by room_id \
# 				having count(*) = cast('{end}' as date)-cast('{start}' as date)+1);".format(start = str(startdate), end = str(enddate), num = str(number), hotelname = str(hotel))

sql = """DROP TABLE IF EXISTS `room_info`;
CREATE TABLE `room_info`  (
  `info_id` int(11) NOT NULL,
  `date` date NULL DEFAULT NULL,
  `price` decimal(10, 2) NULL DEFAULT NULL,
  `remain` int(11) NULL DEFAULT NULL,
  `room_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`info_id`) USING BTREE,
  INDEX `room_info_key`(`room_id`) USING BTREE,
  CONSTRAINT `room_info_key` FOREIGN KEY (`room_id`) REFERENCES `room_type` (`room_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

INSERT INTO `room_info` VALUES (1, '2018-11-14', 500.00, 5, 1);
INSERT INTO `room_info` VALUES (2, '2018-11-15', 500.00, 4, 1);
INSERT INTO `room_info` VALUES (3, '2018-11-16', 600.00, 6, 1);
INSERT INTO `room_info` VALUES (4, '2018-11-14', 300.00, -6, 2);
INSERT INTO `room_info` VALUES (5, '2018-11-15', 300.00, -7, 2);
INSERT INTO `room_info` VALUES (6, '2018-11-16', 400.00, -7, 2);
INSERT INTO `room_info` VALUES (7, '2018-11-14', 200.00, 4, 3);
INSERT INTO `room_info` VALUES (8, '2018-11-15', 200.00, 3, 3);
INSERT INTO `room_info` VALUES (9, '2018-11-16', 300.00, 4, 3);
INSERT INTO `room_info` VALUES (10, '2018-11-14', 450.00, 5, 4);
INSERT INTO `room_info` VALUES (11, '2018-11-15', 300.00, 5, 4);
INSERT INTO `room_info` VALUES (12, '2018-11-16', 450.00, 5, 4);
INSERT INTO `room_info` VALUES (13, '2018-11-14', 400.00, 2, 5);
INSERT INTO `room_info` VALUES (14, '2018-11-15', 250.00, 2, 5);
INSERT INTO `room_info` VALUES (15, '2018-11-16', 400.00, 2, 5);
INSERT INTO `room_info` VALUES (16, '2018-11-14', 300.00, 1, 6);
INSERT INTO `room_info` VALUES (17, '2018-11-15', 200.00, 1, 6);
INSERT INTO `room_info` VALUES (18, '2018-11-16', 300.00, 5, 6);
INSERT INTO `room_info` VALUES (19, '2018-11-14', 300.00, 2, 7);
INSERT INTO `room_info` VALUES (20, '2018-11-15', 250.00, 3, 7);
INSERT INTO `room_info` VALUES (21, '2018-11-16', 300.00, 8, 7);
INSERT INTO `room_info` VALUES (22, '2018-11-14', 250.00, 1, 8);
INSERT INTO `room_info` VALUES (23, '2018-11-15', 200.00, 1, 8);
INSERT INTO `room_info` VALUES (24, '2018-11-16', 200.00, 5, 8);
INSERT INTO `room_info` VALUES (25, '2018-11-14', 200.00, 2, 9);
INSERT INTO `room_info` VALUES (26, '2018-11-15', 150.00, 4, 9);
INSERT INTO `room_info` VALUES (27, '2018-11-16', 150.00, 4, 9);"""

v = "select max(order_id) from `order`;"
s = "INSERT INTO new_schema.room_info VALUES (29, '2018-11-14', 500.00, 5, 1); INSERT INTO new_schema.room_info VALUES (30, '2018-11-14', 500.00, 5, 1);"

try:
    cursor.execute("DROP TABLE IF EXISTS `order`;")
    cursor.execute("""CREATE TABLE `order`  (
  `order_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自动递增的主键',
  `room_id` int(11) NULL DEFAULT NULL,
  `start_date` date NULL DEFAULT NULL,
  `leave_date` date NULL DEFAULT NULL,
  `amount` int(11) NULL DEFAULT NULL,
  `payment` decimal(10, 2) NULL DEFAULT NULL,
  `create_date` date NOT NULL,
  PRIMARY KEY (`order_id`) USING BTREE,
  INDEX `room_order_id`(`room_id`) USING BTREE,
  CONSTRAINT `room_order_id` FOREIGN KEY (`room_id`) REFERENCES `room_type` (`room_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;""")
    cursor.execute("""INSERT INTO `order` VALUES (1, 5, '2018-11-14', '2018-11-16', 2, 2100.00, '2018-11-01'),
        (2, 1, '2018-11-14', '2018-11-14', 5, 2500.00, '2018-11-01'),
        (3, 8, '2018-11-14', '2018-11-16', 2, 1296.00, '2018-11-01'),
        (4, 4, '2018-11-14', '2018-11-16', 2, 2400.00, '2018-11-01'),
        (5, 2, '2018-11-14', '2018-11-16', 4, 4000.00, '2018-11-01'),
        (6, 2, '2018-11-14', '2018-11-16', 4, 4000.00, '2018-11-01');""")
    db.commit()
    cursor.execute(v)
    result = cursor.fetchall()
    if len(result) != 0:
        for row in result:
            print(row[0])
            print(type(row[0]))
    else:print("该酒店已被预订完")
except: print("Error")

db.close()