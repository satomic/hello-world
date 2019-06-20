# coding=utf-8

# 普通函数
def add(arg1, arg2): # def is short for define
    sum = arg1 + arg2
    return sum

def add_3_numbers(arg1, arg2, arg3): # def is short for define
    sum = arg1 + arg2 + arg3
    return sum

a = 1
b = 2
c = 3
d = add(a, b)
e = add_3_numbers(a,b,c)
print(d)
print(e)

# 默认值
def multi(arg1, arg2=4): # def is short for define
    return arg1 * arg2

'''
这是一个块注释
'''


print(multi(4))

name_sex_map = {
    "教主": "female",
    "曾哥": "male"
}
# 关键值函数
def judge_sex(name="教主"): # def is short for define
    '''
    :param name: 待判断性别的名字
    :return: 这个人的性别
    '''
    return name_sex_map.get(name, "unknow")

print(judge_sex())

tofu_sex = judge_sex(name="豆腐")
print(type(tofu_sex))
print(tofu_sex)


# # 不定长函数
# def printinfo(arg1, *vartuple):
#     "打印任何传入的参数"
#     print("固定参数: %s" % arg1)
#     counter = 1
#     for var in vartuple:
#         print("第%s个不固定参数：%s" % (counter, var))
#         counter += 1
#     return None
#
# # 调用printinfo 函数
# printinfo(10)
# printinfo(10, "哈哈")
# printinfo(70, 60, 50)