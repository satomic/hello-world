# coding=utf-8

dict = {}

name_sex_map = {
    "教主": "female",
    "曾哥": "male"
}

print(name_sex_map)
print(name_sex_map.get("教主"))
print(name_sex_map.get("豆腐", "unknow"))
