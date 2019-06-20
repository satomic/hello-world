# coding=utf-8

# while 循环：是为了满足某个条件
counter = 0
while counter < 10:
    print("counter is %s " % counter)
    counter += 1

# for 循环：是为了遍历某组数据
onjob_num = [8, 5, 7, 8, 9, 9]
day = 1
for i in onjob_num:
    print("周%s上班的人数 %s" % (day, i))
    day += 1

# while循环嵌套
i = 0
while i < 3:
    # 外层循环循环体开始
    j = 0
    while j < 4:
        # 内层循环循环体开始
        print("%s, %s" % (i, j))
        j += 1
    # 内层循环循环体结束
    i += 1
# 外层循环循环体结束

# for循环嵌套
for i in range(3):
    for j in range(4):
        print("%s, %s" % (i, j))


# continue
students = ["教主", "曾哥", "罗婷", "豆腐", "多多"]
for student in students:
    if student == "豆腐":
        break # break all loops, end here
    if student in ["曾哥"]:
        continue # continue to next loop directly
    print("%s是妹子" % student)

    if student == "教主":
        print("是群主")
    else:
        pass